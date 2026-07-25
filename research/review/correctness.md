# Production-readiness review — Correctness, edge cases & test coverage

**Dimension:** Correctness, edge cases & test coverage (adversarial)
**Reviewer:** senior audit, adversarial pass
**Date:** 2026-07-25
**Suite status:** `uv run pytest -q` → **217 passed in ~2.2s**. Module doctests → **25 passed** (`uv run python -m pytest --doctest-modules src/hilbertplot -q`). Line coverage **96%** (`coverage run -m pytest` / `coverage report`).

## Verdict

**Correctness core is excellent — no blockers, no correctness-breaking majors.** The mathematical
guarantees the library rests on all hold under adversarial probing: every one of the 40 curves is
space-filling, all 40 are distinct up to symmetry/reversion, the arbitrary-square (AEP) construction
is a valid Hamiltonian path for all 8 feasible curves across every size I tried (n=1..40, plus
150/256/257/300/500/1000), the documented `grid(2**k) == points(k)` invariant is exact, and the
`unroll` round-trip is bit-exact. Input validation on the public surface (negative order, out-of-range
index, `n<1`, infeasible-curve `grid`, non-square / wrong-power-of-two `unroll`, bad `fit`,
`granularity<1`) is present and returns clear, actionable errors.

Findings are all **minor/nit**: a numpy `RuntimeWarning` leaking from a degenerate `difference_map(0)`,
a docstring that overstates immutability, doctests not wired into CI, un-handled `inf` data, and a
handful of untested-but-working branches. None block a release; the first two are worth fixing before 1.0.

## Strengths (verified, not assumed)

- **Space-filling, all 40 curves, orders 0–6:** `is_space_filling(points(k), k)` true for every
  (curve, order). 0 failures.
- **Distinctness:** 40 distinct `canonical_form` keys at order 3 — no two curves collide under D4+reversion.
- **Arbitrary squares, all 8 feasible curves:** for n=1..40 and large n (150/256/257/300), `grid(n)`
  has exact `(n·n,2)` shape, full coverage (`unique==n·n`), correct `[0,n-1]²` bbox, **and** a
  connected unit-step path (`|Δ|₁==1` between every consecutive pair). 0 failures.
- **Invariant `grid(2**k)==points(k)`:** exact for all 8 curves, k=0..5.
- **Round-trips:** `unroll(image(...))` bit-exact for feasible curves at arbitrary sizes
  (n∈{1,3,7,10,16,25,50}) and for non-feasible curves at powers of two. 0 failures.
- **Validation & messages:** infeasible `grid` names the witness size and points to
  `generalizing()`; `unroll` distinguishes non-square vs wrong-power-of-two; `fit='square'` on a
  non-generalizing curve explains the fix.
- **Coverage 96%** with the misses concentrated in window-opening `show()` paths and a few
  defensive branches (below), not in core logic.

## Findings

### 1. `difference_map(0)` emits a numpy RuntimeWarning and returns `nan` — minor
- **Location:** `src/hilbertplot/_data/mapping.py:247` (`return total / count`), reached via
  `src/hilbertplot/_core/curve.py:313` (`Curve.difference_map`).
- **Evidence:**
  ```
  >>> import warnings, hilbertplot as hp
  >>> warnings.simplefilter("always")
  >>> hp.curve(0).difference_map(0)
  .../mapping.py:247: RuntimeWarning: invalid value encountered in divide
  array([[nan]])
  ```
  At order 0 the grid is a single cell with no neighbours, so `count==0` and `total/count` is `0/0`.
  `difference_map` is a public, documented method (`Curve.difference_map(order)`), and the same
  warning also leaks through the renderer: `hp.hilbert_plot(0,[1]).draw(difference=True)` warns
  (`_overlay_difference` computes the map on a 1×1 plot).
- **Recommendation:** guard the degenerate case — either require `order >= 1` in
  `Curve.difference_map` with a clear error, or compute the ratio under
  `np.errstate(invalid="ignore")` / `np.divide(total, count, out=..., where=count>0)` so no warning
  escapes and the empty-neighbour cell is a defined value.

### 2. `HilbertPlot.data` docstring claims a "copy-safe view" but returns the mutable internal array — minor
- **Location:** `src/hilbertplot/_viz/hilbert_plot.py:101-104`.
- **Evidence:**
  ```
  >>> p = hp.hilbert_plot(0, np.arange(16.0)); d = p.data; d[0] = 999.0
  >>> p.data[0]
  999.0
  ```
  The property returns `self._data` directly; the docstring (line 103) says
  "The 1-D data vector (a copy-safe view of the held values)". Mutating the returned array silently
  corrupts every subsequent render of the plot.
- **Recommendation:** either return `self._data.copy()` (or a read-only view via
  `v = self._data.view(); v.flags.writeable = False`) to match the docstring, or change the docstring
  to state the array is the live internal buffer and must not be mutated.

### 3. Doctests pass but are not part of the test suite — minor
- **Location:** `pyproject.toml` `[tool.pytest.ini_options]` — `testpaths=["tests"]`, no `addopts`,
  no `--doctest-modules`.
- **Evidence:** the 25 docstring examples (specific claimed outputs like `word(2)=='ruluurdrurddldr'`,
  `image().shape==(100,100)`) are green when run explicitly
  (`uv run python -m pytest --doctest-modules src/hilbertplot -q` → 25 passed) but a plain
  `uv run pytest -q` never runs them, so a documented example can drift out of sync undetected.
- **Recommendation:** add `addopts = "--doctest-modules"` (or a dedicated CI step / a
  `tests/test_doctests.py` that collects them) so the README-facing examples are enforced.

### 4. Non-finite (`inf`) data is silently mishandled downstream — minor
- **Location:** `src/hilbertplot/_data/mapping.py:150-186` (`fourier_spectrum`) and
  `src/hilbertplot/_viz/hilbert_plot.py:268-271` (vmin/vmax defaults).
- **Evidence:**
  ```
  >>> hp.hilbert_plot(0, [np.inf,1,2,3]).fourier()      # -> all-NaN spectrum + warnings
  array([[nan, nan],[nan, nan]])                        # invalid value in subtract / fft
  >>> ax = hp.hilbert_plot(0, [np.inf,1,2,3]).draw(); ax.images[0].get_clim()
  (1.0, inf)                                            # degenerate scale, no warning
  ```
  `NaN` is a first-class, documented input (padding → transparent, replaced by finite mean before
  FFT), but `inf` is not: `img - img.mean()` becomes `nan`, the whole spectrum collapses to `nan`,
  and `draw` sets `vmax=inf` so every finite value maps to one end of the colormap — silently.
- **Recommendation:** decide the contract for non-finite data. Either sanitize `±inf` the way `NaN`
  is handled (treat as padding / clip) in `fourier_spectrum` and in the vmin/vmax computation, or
  validate against `inf` in `HilbertPlot.__init__` / `image` with an explicit error. At minimum note
  the restriction in the docstrings.

### 5. Coverage gaps — real behaviour untested (nit)
All verified working by hand; these are gaps, not defects.
- **Arbitrary-square `unroll` is tested only for curve 0.** `tests/test_data.py:168-177` exercises the
  non-power-of-two `unroll` path for Hilbert only; the parametrized inverse test
  (`test_data.py:148-153`, indices 0/5/12/39) forces power-of-two via `image(order=order)`, so the
  arbitrary-grid `unroll` branch for the other 7 feasible curves (3,4,5,24,29,30,31) is never hit. I
  confirmed all 8 round-trip exactly at n∈{3,7,10,25,50}; add a parametrized test over `FEASIBLE`.
- **`fourier` NaN-padding branch untested** (`mapping.py:180`): every fourier test feeds full,
  power-of-4 data (`arange(1024)`, `zeros(1024)`), so the `np.where(isnan, nanmean, ...)` line is
  never exercised. Verified working (`fourier()` on `arange(50)` → 8×8, all finite).
- **`Curve.show` / `HilbertPlot.show` untested** (`curve.py:372-375`, `hilbert_plot.py:304-308`) —
  they open a window; expected, but a smoke test with a non-interactive backend would cover them.
- **`gallery` empty-list error and the `plt.show()` path** (`render.py:151,171`) untested; only the
  `save=` path is (`test_plotting.py:32`).

### 6. Loose index typing and a slightly misleading error message — nit
- **Location:** `src/hilbertplot/_core/curve.py:472-505`, `src/hilbertplot/_core/catalog.py:307-314`.
- **Evidence:**
  ```
  >>> hp.curve(True).name          # bool is an int subclass -> index 1
  'Moore'
  >>> hp.curve(1.5)
  KeyError: "curve index 1.5 out of range; expected an integer in 0..39"
  ```
  `True`/`False` are accepted as curve indices, and a non-integer like `1.5` is reported as "out of
  range" though its problem is that it is not an integer.
- **Recommendation:** cosmetic — optionally reject `bool` and word the message as
  "expected an integer in 0..39" without "out of range" when the value is non-integral.

### 7. `grid()` is pure-Python O(n²) — scalability note (nit)
- **Location:** `src/hilbertplot/_core/arbitrary.py:65-100` (`_fill` builds Python lists recursively).
- **Evidence:** `grid(1000)` (1e6 cells) ≈ **1.56s**; `grid(500)` ≈ 0.40s; `grid(200)` ≈ 0.085s.
  By contrast `points(k)` builds millions of cells in tens of ms via numpy. Fine for typical use,
  but ~100× slower per cell and the `grid` docstring makes no scalability caveat while `points`
  advertises "a few tens of milliseconds" for order-10.
- **Recommendation:** none required for release; consider a one-line note in `Curve.grid` that very
  large `n` is materially slower than power-of-two `points`, or vectorize `_fill` later.

## What I ran (paper trail)

- `uv run pytest -q` → 217 passed.
- `uv run python -m pytest --doctest-modules src/hilbertplot -q` → 25 passed.
- `coverage run -m pytest` + `coverage report --show-missing` → 96%, misses at
  curve.py:267,372-375; geometry.py:92; symmetry.py:129,185-188; mapping.py:49,104,109,180;
  hilbert_plot.py:35,43,92,104,304-308,344; render.py:151,162,164,171.
- Adversarial probes (all from a clean cwd — note: the project `scratchpad/` contains a stray
  `timeit.py` that shadows stdlib and breaks matplotlib import if scripts are run from there):
  - order 0 / negative order for `word`/`points`/`difference_map`; index 40/-1/-41/1.5/True/'zzz';
    `grid(0)`/`grid(-3)`/`grid(1)`/`grid` on non-generalizing.
  - empty / single-value / NaN / inf data through `image`/`draw`/`fourier`; `granularity` 0/-2/>N;
    `fit` truncate/square/bogus; data-longer-than-grid via explicit `order`.
  - all-40 space-filling (orders 0–6); 40 distinct canonical forms; `grid` coverage+connectivity for
    all 8 feasible curves n=1..40 and large n; `grid(2**k)==points(k)`; `unroll` round-trips
    (feasible arbitrary sizes + non-feasible pow2); `unroll` error paths (non-square/1D/3D/0×0/
    wrong-power).
