# Production-Readiness Audit — Performance & Scalability

**Library:** `hilbertplot` (src/hilbertplot/)
**Reviewer dimension:** Performance & scalability
**Date:** 2026-07-25
**Method:** direct benchmarking with the installed editable package via `.venv/bin/python`; every number below is measured, every claim is anchored to `file:line`. Benchmark scripts archived in the session scratchpad (`bench.py`, `prof.py`, `prof2.py`, `prof3.py`).

---

## Verdict

**Readiness: 7 / 10 — solid, with one scaling cliff to fix before 1.0.**

The power-of-two core is genuinely well engineered: curve generation is fully numpy-vectorized and `lru_cache`d, `word()` uses a C-speed `bytes.translate`, and every data-mapping primitive (`scatter`, `gather`, `label_map`, `difference_map`, `fourier_spectrum`) is vectorized with no per-cell Python. At the paper's stated data-viz scale (~1M cells) the power-of-two path renders end-to-end in ~250 ms.

There is one real problem: the **arbitrary-square (`grid`) path is a pure-Python recursion** (`_core/arbitrary.py::_fill`) that runs at ~1.5 µs/cell with 10× memory overhead, and it is the **default** layout for the eight generalizing curves — including curve 0 (Hilbert), the library's flagship. As a result `hilbert_plot(0, data_of_1M).image()` takes **1.6 s** (vs **47 ms** for the same data on the power-of-two path), and it is recomputed on every render because nothing caches it. This is the headline finding. Everything else is minor polish or already fast enough.

---

## Strengths (measured)

| Path | Result | Note |
|---|---|---|
| `word(8/10/12)` | 0.20 / 2.62 / 41.8 ms | `curve_codes(...).tobytes().translate()` — `generation.py:99`. Excellent. |
| `curve_codes(0, 12)` (generation only) | ~40 ms for 16.7M strokes | Vectorized morphism/reversion/concatenate + `lru_cache` — `generation.py:62-79`. |
| `scatter` 1M cells | 7.6 ms | Vectorized fancy-index write — `mapping.py:113`. |
| `fourier_spectrum` 1024² / 2048² | 33 / 164 ms | Pure `np.fft` — `mapping.py:150`. Fine. |
| `difference_map` order 10 (1024²) | 91 ms | 8-neighbour loop is 9 vectorized full-array ops, no per-cell Python — `mapping.py:212`. |
| Render `save()` 1M (pad path) | 242 ms; +difference 465 ms; fourier 302 ms | Matplotlib-bound; `render.py` auto-switches to O(cells) `imshow` fill mode at order ≥ 8 (`render.py:27,45`). Appropriate. |

The `line`→`fill` auto-switch at order 8 (`_AUTO_FILL_ORDER`, `render.py:27`) is exactly the right call: it avoids one-`LineCollection`-segment-per-stroke blowup at high order and is the only legible view there anyway.

---

## Findings

### 1. [MAJOR] Default `fit="auto"` routes generalizing curves through the pure-Python `grid()` recursion — 34× slower than the power-of-two path at 1M cells, and the documented default
**Location:** `_viz/hilbert_plot.py:186-195` (`_layout`: `effective = "square" if self._curve.generalizes else "pad"`), backed by `_core/arbitrary.py:65-100` (`_fill`/`square_points`).

**Evidence** (`prof3.py`):
```
image() 1M default(fit=auto=square->grid): 1624 ms   shape (1000,1000)
image() 1M fit=pad (points path):            47 ms   shape (1024,1024)
image() 1M Moore(pad, non-generalizing):     49 ms
```
For a generalizing curve (Hilbert, Liu2/3/4, and four composites — `arbitrary.py:23`), `fit="auto"` picks the tight `ceil(sqrt(N))` square, which can only be built by `grid()` → `_fill`. For 1M values that is a 1000×1000 grid built by Python recursion in 1.6 s. The identical data on the power-of-two `pad` path is 47 ms. So the *default* rendering of the *default* curve at the paper's stated scale is the **slowest** path in the library, and 34× slower than an available alternative.

The tight-square default is a deliberate, documented UX choice (no power-of-two padding waste — `hilbert_plot.py:120-126`), so this is not a bug; it is a performance/UX tension. But at data-viz scale the cost is severe and surprising.

**Recommendation (ranked):**
1. **Cache `grid()` output** (see finding 3) so at least repeated renders of the same plot are free — cheapest partial fix.
2. **Vectorize `_fill`** (see finding 2) — the real fix; brings the square path toward the pad path's speed.
3. Failing both, consider a size threshold above which `fit="auto"` falls back to `"pad"` (documented), or emit a one-time note that `fit="pad"` is far faster for large N. Least preferred (changes semantics).

---

### 2. [MAJOR] `grid()` / `square_points()` is a pure-Python recursion: ~1.5 µs/cell, 10× memory overhead, does not vectorize
**Location:** `_core/arbitrary.py:65-100` (`_fill`, `square_points`).

**Evidence** (`bench.py`, `prof2.py`):
```
grid(100)  =    20.7 ms   (10k cells)
grid(300)  =   214.9 ms   (90k cells)
grid(1000) =  1522.3 ms   (1M cells)          -> ~1.52 µs/cell, O(cells) linear
  _fill list build: 1392 ms (91%)  |  np.array(list): 172 ms (9%)
  _fill recursive call count for n=1000: 349,525
  result tuples: list of 1,000,000 Python tuples
grid(1000) tracemalloc peak: 167.4 MB  vs  result array 16.0 MB  (10.5× overhead)
```
By contrast the power-of-two `points(10)` produces the same 1M cells in 66 ms — `grid` is **~23× slower per cell**. The cost is intrinsic to the design: each cell is emitted as a Python tuple via a per-quadrant closure `f(cx, cy)` (`arbitrary.py:62,70,85`), accumulated with `out += [...]` across 349k recursive calls, then converted with `np.array(list_of_tuples)`. None of it touches numpy until the final conversion. Scaling is linear in output (10k→1M cells is ~100× cells, 20.7→1522 ms is ~74×), so it is O(cells) — but with a Python constant ~23× the vectorized path and 10× the memory. It will not scale past a few million cells.

**Recommendation:** Rewrite `_fill` to emit into preallocated numpy arrays instead of a list of tuples. Two viable approaches:
- **Iterative with an explicit box stack**, writing base-case cells directly into a preallocated `(n*n, 2)` int array via a running write cursor — eliminates 1M tuple objects and the final `np.array` copy (saves the 172 ms conversion and the 150 MB of intermediate tuples outright).
- Or keep recursion but have each call return `(start, end)` index ranges and fill a shared output buffer, so only the base cases write. Given the base cases are the 1×/2×/2×2 blocks, they can be written as small vectorized slices rather than tuple lists.
Either removes the dominant Python-object churn; realistic target is single-digit-×`points()` speed (i.e. well under 200 ms for 1M).

---

### 3. [MINOR] No memoization of `points()` or `grid()` — repeated renders recompute the full coordinate array
**Location:** `_core/curve.py:156-180` (`points` — recomputes `codes_to_points` each call); `_core/curve.py:182-222` / `arbitrary.py:93` (`grid`/`square_points` — no cache at all).

**Evidence** (`prof3.py`):
```
points(10) #1: 40.1 ms
points(10) #2: 40.9 ms      <- codes are lru_cached, but codes_to_points is redone every call
image() 1M (grid) #1: 1624 ms
image() 1M (grid) #2: 1589 ms   <- grid fully recomputed every render
```
`curve_codes` is `lru_cache`d (`generation.py:62`), so the *stroke codes* are shared, but the coordinate array is regenerated on every `points()` call, and `grid()` has no cache whatsoever. A normal interactive workflow renders the same curve+order repeatedly (a colormap sweep, then `difference=True`, then `fourier=True`); each render pays the full layout again. For the grid path that is 1.6 s **per render**.

**Recommendation:** Add an `lru_cache` (or a small keyed cache with `.flags.writeable = False`, mirroring `generation.py:78`) on the coordinate producers: memoize `codes_to_points`-of-cached-codes for `points(index, order)`, and memoize `square_points(index, n)`. Keep the returned arrays read-only and let call sites copy when they must mutate. Expose it through the existing `clear_cache()` (`generation.py:102`). This turns every render after the first into a near-free lookup and is the cheapest mitigation for finding 1.

---

### 4. [MINOR] `codes_to_points` uses int64 and strided 2-column axis-0 reductions — ~3× slower and 2× the memory it needs at high order
**Location:** `_core/geometry.py:42,52-66` (`_STEP_LOOKUP` int64; `points` int64; `.min(axis=0)`).

**Evidence** (`prof.py`, order 12 / 16.7M strokes):
```
_STEP_LOOKUP[codes]  (int64 lookup -> (16.7M,2) int64): 237 ms, 268 MB
cumsum:                                                  114 ms
min(axis=0) + subtract:                                  328 ms   <- strided 2-col reduction
--------------------------------------------------------------------
full int64 codes_to_points:                             ~680 ms
split 1-D int16-step cumsum variant:                    ~198 ms   (~3.4× faster)
```
Coordinates never exceed `2**order - 1` (4095 at order 12), so int64 is 4× wider than needed; the `(N,2)` layout also forces the `min(axis=0)` reduction to run strided over the long axis, which is the single most expensive line (328 ms). Doing the walk as two contiguous 1-D `cumsum`s with a narrow step dtype is ~3.4× faster and halves peak memory. Note this only bites at order ≥ 11–12 (16M+ cells) — `points(10)` is already 66 ms, comfortably inside the 1M-cell target — so it is polish, not a blocker.

**Recommendation:** In `codes_to_points`, index into a narrow (`int16`) step lookup, run per-axis 1-D `cumsum` into `int32` buffers, normalize with 1-D `.min()`, and `column_stack` once. Keeps identical output, ~3× faster and half the memory at high order. Pairs naturally with finding 3's caching.

---

### 5. [MINOR] `difference_map` at high order is heavy due to full-size float64 temporaries
**Location:** `_data/mapping.py:212-247`.

**Evidence** (`bench.py`):
```
difference_map order 8  (256²):   4.1 ms
difference_map order 10 (1024²):  91 ms
difference_map order 12 (4096²): 3109 ms
```
The algorithm is already vectorized (9 iterations, each a full-array op — no per-cell Python), so it is O(cells)×8 and fine at every realistic viz order (≤10 → 91 ms). At order 12 it allocates several 16M-element float64 temporaries per neighbour (`padded`, `neighbour`, `valid`, `diff`, plus `total`/`count`), which is what drives 3.1 s. Since the difference map is an overlay normally drawn at the same order as the plot (≤10), this is polish only.

**Recommendation:** If order-12 difference maps become a use case, accumulate in float32 and reuse a single scratch buffer across the 8 neighbour offsets instead of allocating `diff`/`valid` fresh each pass. Otherwise leave as-is.

---

### 6. [NIT] `order_for` / `order_floor` / `square_side` use Python `while` loops
**Location:** `_data/mapping.py:37-39, 51-53, 106-110`.

These loop in Python to compute `ceil(log4(n))` etc. Operands are tiny (a handful of iterations even for n=10^9), so the cost is unmeasurable. Mentioned only for completeness — could be closed-form via `int.bit_length()`, but there is no reason to.

---

## Scale summary (what happens at ~1M cells, the paper's target)

| Operation | 1M-cell cost | Verdict |
|---|---|---|
| `word(10)` | 2.6 ms | fast |
| `points(10)` (power-of-two) | 66 ms | fast |
| `grid(1000)` (arbitrary square) | **1522 ms** | **slow — findings 1,2** |
| `scatter` | 7.6 ms | fast |
| `difference_map` (1024²) | 91 ms | fast |
| `fourier` (1024²) | 33 ms | fast |
| `image()` default Hilbert (→grid) | **1624 ms** | **slow — finding 1** |
| `image()` fit='pad' (→points) | 47 ms | fast |
| `save()` end-to-end (pad) | 242 ms | fast (matplotlib-bound) |

**Bottom line:** everything on the power-of-two path is production-ready at 1M cells. The single scalability liability is the arbitrary-square `grid` recursion (findings 1–3), which is both the slowest path and the silent default for the flagship curve. Vectorizing `_fill` plus caching `grid`/`points` closes the gap and is the work to prioritize before 1.0.
