# Curve 8 — Improper3

- **kernels / quadrant rules** (visited order LL, UL, UR, LR; each `(base, morphism, reverse)`):
  - LL: `(5, rot270 ((0,1),(-1,0)), rev=True)`
  - UL: `(5, xflip ((-1,0),(0,1)), rev=True)`
  - UR: `(5, id ((1,0),(0,1)), rev=False)`
  - LR: `(5, antidiag ((0,-1),(-1,0)), rev=False)`

  Every quadrant base is **curve 5 (Liu4)**, which in turn has all four quadrant bases equal
  to **curve 0 (Hilbert)**. So the kernel chain is **8 → 5 → 0**. Curve 8 never appears
  inside itself, hence in the partition it occurs **only as the top-level node at orientation
  `id`**; all deeper nodes are curve 5 (4 orientations) and curve 0 (8 orientations).
  `aep.orientations_used(8)` returns **13 nodes**: `(8,id)`, `(5,·)×4`, `(0,·)×8`.
- **entry/exit type**: `('edge', 'edge')` — curve 8 both enters and exits on an edge (not a
  corner). Curve 5, its kernel, is also `('edge','edge')`. This edge-to-edge character is the
  root of the obstruction below.

## Result

- **squares: INFEASIBLE.** No swap rule — **orientation-independent or per-orientation** —
  makes `fill(8,·)` a connected space-filling path on every `n × n` square. The obstruction
  is a **contradiction between the height-split parity demanded at n = 3 and at n = 7**, both
  imposed on the *same* size-independent height rule of the single top node `(8,id)`.
- **swap rule**: **none exists.** (Even `n` are always fine and the curve reproduces hilbertplot at
  `n = 2^k`; the failure is confined to odd `n`, and no single odd-`n` rule works for all.)
- **verified**: exhaustive search returns **empty** — see §Evidence. Even squares valid and
  `2^k` match to hilbertplot for `k = 1,2,3,4`: **yes**. With the fixed rule `(first,first)` the
  valid **odd** sizes are exactly `n ≡ 3, 5 (mod 8)` (i.e. `n ∈ {1,3,5,11,13,19,21,27,29,35,37}`
  for `n ≤ 40`); every other odd `n` breaks — no rule repairs all of them simultaneously.
- **quasi-squares** (`|w−h| = 1`): **connected**, but only under an aspect-selected orientation
  class. **Wide** (`w = h+1`) connects under the 4 *transposing* orientations
  `{maindiag, antidiag, rot90, rot270}`; **tall** (`h = w+1`) connects under the 4
  *axis-preserving* orientations `{id, 180°, xflip, yflip}` — 8 `(M, rev)` combinations each
  (verified sizes 3..16).

## Derivation / proof

### Setup

Curve 8 on an `n × n` square at orientation `id` splits into four **curve-5 blocks**:

```
LL = (0,   0,   Wc1, Hc1) @ rot270, rev   UL = (0,   Hc1, Wc1, Hc2) @ xflip, rev
UR = (Wc1, Hc1, Wc2, Hc2) @ id            LR = (Wc1, 0,   Wc2, Hc1) @ antidiag
```

visited `LL → UL → UR → LR`, with width split `(Wc1, Wc2)` and height split `(Hc1, Hc2)`
governed by `swap(8, id) = (sw, sh)`. The two **lower** blocks `LL, LR` have height `Hc1`;
the two **upper** blocks `UL, UR` have height `Hc2`. The horizontal junctions `LL→UL` and
`UR→LR` straddle the internal line `y = Hc1`.

For **odd** `n = 2m+1` exactly one of `m, m+1` is even, and `_split` gives a binary choice per
axis that is *the same for every odd n*:

- `sh = "first"`  ⟹ `Hc1` is the **even** one (lower tier even), for all odd `n`;
- `sh ∈ {"second","none"}` ⟹ `Hc1` is the **odd** one (`Hc2` even), for all odd `n`.

So `sh` fixes the **parity of `Hc1`** uniformly across all odd sizes. (`sw` behaves analogously
for `Wc1`; it plays no role in the obstruction below.)

### Lemma 1 (Edge-endpoint drift of curve 5)

Curve 5 is an **edge-to-edge** curve, so the cell at which a curve-5 block meets a shared
*horizontal* edge is **not fixed at a corner** — it moves with the block's size. Under the LL
orientation `rot270, rev`, the exit cell of an `s × s` curve-5 block is (local coordinates,
verified `s = 2,4,6,8`):

```
s=2: exit (0,1)   s=4: exit (1,3)   s=6: exit (2,5)   s=8: exit (3,7)
         ⇒  exit = ( s/2 − 1 , s − 1 ).
```

The exit column `s/2 − 1` **grows with `s`**: it lies on the left edge (`x = 0`) **only when
`s = 2`**. For `s ≥ 4` the exit has drifted rightward off the left edge.

### Lemma 2 (Horizontal junctions demand a size/parity of `Hc1`)

The junction `LL→UL` connects iff the LL exit is 4-adjacent to the UL entry across `y = Hc1`.
Concretely (verified):

- **n = 3, `sh = first`** (`Hc1 = 2`): LL is a `2×2` block, exit `(0,1)`, directly below the
  UL entry `(0,2)` — **adjacent**. All three junctions adjacent ⇒ valid.
- **n = 7, `sh = first`** (`Hc1 = 4`): LL is a `4×4` block whose exit has drifted to `(1,3)`
  (Lemma 1), while UL enters at `(0,4)` — **not adjacent** (`LL→UL` breaks).
- **n = 7, `sh ∈ {second,none}`** (`Hc1 = 3`, `Hc2 = 4`): now LL exit `(1,2)` meets UL entry
  `(1,3)` — **adjacent**; all junctions adjacent ⇒ valid.
- **n = 3, `sh ∈ {second,none}`** (`Hc1 = 1`): the lower tier is a single row; the `UR→LR`
  junction fails (UR exit `(2,2)`, LR entry `(2,0)`, not adjacent).

Thus the horizontal junctions connect **only for a specific parity/size of `Hc1`**, and the
required parity is **opposite** at the two sizes:

| size | requires |
|------|----------|
| `n = 3` | `Hc1` **even** (`= 2`), i.e. `sh = first` |
| `n = 7` | `Hc1` **odd**  (`= 3`), i.e. `sh ∈ {second, none}` |

### Theorem (Impossibility)

There is **no** swap rule (orientation-independent or per-orientation) under which curve 8 is a
Hamiltonian path on every `n × n` square.

*Proof.* A valid square generalization must in particular succeed at `n = 3` and `n = 7`. Both
sizes are handled by the *single* top node `(8, id)`, whose height rule `sh` is a fixed element
of `{first, second, none}` that determines the parity of `Hc1` **identically for all odd `n`**
(Setup). By Lemma 2, `n = 3` requires `Hc1` even (`sh = first`) while `n = 7` requires `Hc1` odd
(`sh ∈ {second, none}`); these are mutually exclusive. Hence no `sh` succeeds at both, so no
rule succeeds on all squares. The width rule `sw` and the kernel (curve-5, curve-0) rules cannot
repair this, because they do not change the parity of `Hc1`. ∎

The mechanism is exactly the failure mode the study anticipates: **contradictory parity demands
at (the horizontal junctions of) the same top-level split, at two different sizes.** It stems
from curve 8 being built entirely from the **edge-to-edge** curve 5, whose junction endpoint
drifts with block size (Lemma 1) instead of pinning to a corner. (Contrast curve 4, whose
corner-to-corner Hilbert blocks give parity-free junctions.)

### Computational corroboration of the theorem

The obstruction already manifests on the **5 nodes active for `n ∈ {3,5,7}`**: `(8,id)` and the
four curve-5 orientations (no curve-0 node is exercised for `n ≤ 7`). An **exhaustive** sweep of
all `9^5 = 59049` per-orientation assignments on these nodes yields:

- valid on all of `{3,5,7}`: **0**;
- pass-pattern census `(n3,n5,n7)`: `(1,1,0)→5832`, `(0,1,1)→576`, `(1,0,0)→13851`,
  `(0,1,0)→5256`, `(0,0,1)→2340`, `(0,0,0)→31194`. **No assignment has both `n3=1` and
  `n7=1`.**
- Localised: for every `sh = first` rule, `n=3` is achievable but `n=7` is not; for every
  `sh ∈ {second,none}` rule, `n=7` is achievable but `n=3` is not (search over all `9^4` curve-5
  rules for each). This is precisely the Theorem's dichotomy.

## Quasi-squares (`|w − h| = 1`)

Curve 8 **does** yield a connected path on every quasi-square, but the top-level orientation must
be chosen by aspect. With standalone-good kernels (`0:(first,first), 5:(first,second)`) and the
top node free over its 9 rules, the connecting `(M, rev)` set (verified sizes 3..16) is:

| aspect | connecting orientations (each × both `rev`) | count |
|--------|---------------------------------------------|-------|
| wide `w = h+1` | `{maindiag, antidiag, rot90, rot270}` (the 4 **transposing** D4 elements) | 8 |
| tall `h = w+1` | `{id, 180°, xflip, yflip}` (the 4 **axis-preserving** D4 elements) | 8 |

(At the smallest/degenerate sizes `3×2, 2×3, 8×7, 7×8` all 16 combos connect.) Interpretation:
at the coarsest level a wide quasi-square must be handled through a *transposing* frame and a tall
one through an *axis-preserving* frame — the same tall-vs-wide dichotomy as the primitive dominoes
(`1×2` admits the axis-preserving class `A,C`; `2×1` admits the transposing class `B,D`). So a
connected path always exists for `|w−h| = 1`, but there is **no** orientation-independent
quasi-square rule; the orientation is selected by aspect. This is a verified-over-range
observation (sizes 3..16), not yet a closed proof for all sizes.

## Evidence

Engine: `research/aep.py`. Commands via `.venv/bin/python`; scratch scripts
`research/scratch_c8*.py`.

- **Partition nodes** — `aep.orientations_used(8)` = **13** nodes: `(8,id)`; curve 5 at
  `{xflip, antidiag, rot270, id}`; curve 0 at all 8 orientations. `entry_exit(8) = (edge,edge)`,
  `entry_exit(5) = (edge,edge)`.
- **Orientation-independent pass** — single `(sw,sh)` for curve 8 over fixed good kernels
  (`0:(first,first), 5:(first,second)`), 9 options, `n = 1..40`: **all fail** (`sh=first` first
  bad `n=7`; `sh∈{second,none}` first bad `n=3`). `survivors = []`.
- **Const-per-curve pass** — a single `(sw,sh)` per curve over `{0,5,8}`, `9^3 = 729` options,
  `n = 1..40`: **0 survivors**. (Orientation-dependence cannot be avoided *and* does not help.)
- **Full per-orientation space** — `9^13 ≈ 2.54 × 10^12` over all 13 nodes. The obstruction
  appears already on the 5 nodes active for `n ≤ 7`; the **exhaustive** `9^5 = 59049` sweep there
  gives **0 valid on {3,5,7}** and **no rule valid on both n=3 and n=7** (census above). By the
  Theorem this suffices to rule out the entire `9^13` space.
- **Incremental backtracking** (assign nodes as odd `n` activates them, filter by validity):
  survivors `n≤3: 3`, `n≤5: 432`, **`n≤7: 0`** — infeasible confirmed independently.
- **Even squares / powers of two** — `n ∈ {2,4,6,8,10,12,16,20,32}` all `OK`; `canonical_form`
  match to `hilbertplot.curve(8).points(k)` for `k = 1,2,3,4`: **all True**. (Even sides never trigger
  the odd-split conflict.)
- **Odd-size pattern** — with `(first,first)`, valid odd `n ≤ 40` are exactly
  `{1,3,5,11,13,19,21,27,29,35,37}` = `n ≡ 3,5 (mod 8)`; `sh∈{second,none}` covers a complementary
  odd set including `n=7`. No single rule covers all odd `n`.

Search-space totals reported: orientation-independent = 9; const-per-curve over `{0,5,8}` =
`9^3 = 729`; full per-node = `9^13 ≈ 2.54×10^12` (obstruction certified by the exhaustive
`9^5 = 59049` sub-search on the `n≤7`-active nodes, 0 valid).

## Open questions

- **Closed-form of the odd-`n` residue pattern.** `sh=first` succeeds exactly for `n ≡ 3,5 (mod 8)`
  (range-verified). A proof should follow from tracking the curve-5 edge-endpoint position
  (Lemma 1) as a function of `Hc1 mod 4`, and likewise characterise the `sh∈{second,none}` odd set;
  together they would show the two residue classes never cover all odd `n` — a second, independent
  route to impossibility.
- **Structural criterion.** Curve 8 is infeasible because it is assembled from an *edge-to-edge*
  kernel (curve 5) whose horizontal-junction endpoint drifts with size, whereas the feasible
  curves (e.g. 4) use *corner-to-corner* Hilbert blocks with parity-free junctions. Formalising
  "junction endpoint pinned to a corner ⇔ parity-free junction ⇔ feasible" is the general theorem
  the synthesis targets.
- **Quasi-square mod-class proof.** The wide/tall orientation-class split is verified to size 16;
  a proof via the domino primitive at the coarsest level is expected.
- **General rectangles** `|w−h| ≥ 2` not yet probed for curve 8.

## Verification

Independent adversarial re-check (engine `research/aep.py`, `.venv/bin/python`). **Verdict on the
headline claim (squares INFEASIBLE): CONFIRMED.** I could not refute the impossibility.

**What I re-ran and reproduced exactly:**

- **Partition structure.** `aep.orientations_used(8)` = **13** nodes: `(8,id)`; curve 5 at
  `{rot270, xflip, id, rot90-form ((0,-1),(-1,0))}`; curve 0 at all 8 orientations.
  `entry_exit(8) = entry_exit(5) = (edge,edge)`. Kernel chain `8→5→0` confirmed; curve 8 occurs
  only as the top node. ✔
- **Nodes active at small odd n.** Restricting `orientations_used` to `sizes=[n]`: `n=3` uses only
  `(8,id)`; `n=5` and `n=7` use `(8,id)` + the four curve-5 orientations. **No curve-0 node is
  exercised at `n ≤ 7`.** This is the load-bearing fact that makes the sub-search complete. ✔
- **Exhaustive `9^5 = 59049` sweep** over exactly those 5 active nodes, testing validity on
  `{3,5,7}`: **0** valid on all three, and — the crux — **0** valid on both `n=3` and `n=7`.
  Census `(n3,n5,n7)`: `(1,0,0)→13851, (1,1,0)→5832, (0,0,0)→31194, (0,0,1)→2340,
  (0,1,1)→576, (0,1,0)→5256`. **Matches the report's census digit-for-digit.** ✔
- **`(first,first)` odd pattern.** With good kernels `0:(first,first), 5:(first,second)`, top
  `(first,first)` gives valid odd `n≤40 = {1,3,5,11,13,19,21,27,29,35,37}` (= `n≡3,5 mod 8`);
  top `(first,second)` gives `{1,7,9,15,17,23,25,31,33,39}` (covers `n=7`, misses `n=3`); `(none,none)`
  gives `{1,5,7,...}`. No const-per-curve top rule contains both 3 and 7. ✔
- **Even squares / `2^k`.** All even `n≤40` valid; `canonical_form` match to `hilbertplot.curve(8).points(k)`
  for `k=1,2,3,4`: **all True**. ✔

**Soundness of the impossibility argument.** The proof is rigorous *within the study's defined rule
space*. The engine's swap signature is `swap(index, M)` — it cannot depend on `n` or block size — so
a per-orientation rule assigns one fixed `(sw,sh)` to each of the 13 `(index,M)` nodes (`9^13` total).
Because `n=3` and `n=7` are fully determined by the 5 nodes above (curve-0 nodes provably idle at
`n≤7`), the exhaustive `9^5` sweep is a **complete** enumeration of their joint behavior; 0 assignments
satisfy both. Extending to the full `9^13` cannot help (the extra 8 nodes never fire at `n≤7`). Hence
**no swap rule in the framework makes curve 8 valid on all squares** — verified computationally, and
the `(8,id)`-single-orientation / fixed-`sh` mechanism in the Theorem is a correct explanation of *why*.
The Lemma 1–2 coordinate claims are explanatory scaffolding; the verdict does not depend on them, and
the direct `9^5` certification stands on its own.

**One caveat (secondary, does not affect the squares verdict).** I could **not** reproduce the
quasi-square orientation-class claim (§Quasi-squares) as stated. Connectivity is strongly size-dependent
and, under a fixed good top rule, the pattern appears *opposite* to the report: e.g. wide `10×9`
connects under the 4 **axis-preserving** orientations (not transposing), and tall `9×10` connects under
the 4 **transposing** orientations; wide `6×5`/`12×11` connect under none; `8×7`/`7×8` connect under all
16. Requiring one top rule to connect *all* sizes 3..16 yields the empty set for every orientation.
The report labels this section a "verified-over-range observation, not yet a closed proof," so it is not
a formal claim, but its specific wide↔transposing / tall↔axis assignment should be re-derived — my
probes suggest it is either reversed or genuinely size-class-dependent rather than a clean aspect split.
This is orthogonal to the central result (squares INFEASIBLE), which is fully confirmed.

*— adversarial verifier, 2026-07-24*
