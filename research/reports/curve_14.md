# Curve 14 — Liu2+Liu4 #3

- **kernels / quadrant rules** (visited order LL, UL, UR, LR; each `(base, morphism, reverse)`):
  - LL: `(3  = Liu2, morph ((0,1),(1,0)) = main-diagonal, rev=False)`
  - UL: `(5  = Liu4, morph ((-1,0),(0,1)) = mirror x→−x, rev=True)`
  - UR: `(5  = Liu4, morph ((1,0),(0,1))  = identity,      rev=False)`
  - LR: `(5  = Liu4, morph ((0,-1),(-1,0)) = anti-diagonal, rev=False)`

  Curve 14 is a **composite**: its lower-left quadrant is curve 3 (Liu2) and the other three
  are curve 5 (Liu4). It never appears inside itself, so it occurs in the partition **only**
  as the top-level node at orientation `IDENT`. The kernels must be solved first:
  - curve 3 (Liu2) → all four sub-quadrants are curve 0 (Hilbert); square rule `(first, second)`.
  - curve 5 (Liu4) → all four sub-quadrants are curve 0 (Hilbert); square rule `(first, second)`.
  - curve 0 (Hilbert) → self-similar; square rule `(first, first)`.

  `aep.orientations_used(14)` returns **12 partition nodes**: `(14, IDENT)`; `(3, main-diag)`;
  curve 5 at 3 orientations; curve 0 at 7 orientations. Each node independently needs a swap
  rule from `{first, second, none}²` (9 options), so the full per-orientation rule space is
  **9¹² = 282 429 536 481**.
- **entry/exit type**: `entry_exit(14) = ('edge', 'edge')` — starts and ends on a grid edge
  (non-corner). As with curve 4, endpoint type alone does not decide feasibility.

## Result

- **squares: INFEASIBLE.** No swap rule — orientation-independent *or* per-orientation, over the
  full 9¹² space — makes `fill(14, ·)` a Hamiltonian path on every `n × n` square.
- **swap rule**: none exists.
- **obstruction**: a **contradictory parity demand at the top-level junction J1** on the height
  split of the `(14, IDENT)` node. Sizes `n = 3` and `n = 7` require *opposite* values of the
  single height-swap `sh`; a fixed rule cannot satisfy both.
- **verified**: complete backtracking over 9¹² returns **0** assignments valid on `n = 1..40`
  (search machinery cross-checked: it recovers the known valid rules for curves 0, 3, 5). The
  largest prefix that is jointly satisfiable is `n = 1..6`; feasibility dies at `n = 7`.
- **quasi-squares** (`|w−h| = 1`): also **not** uniformly feasible. Connectivity is size- and
  orientation-dependent (see §Quasi-squares): the primitive `2×1 / 1×2` and `3×2 / 2×3` connect
  in all 8 orientations, `5×4 / 4×5` connect in exactly the 4 orientations whose canonical frame
  is tall, `7×6 / 6×7` connect in all 8 again — and **no** orientation connects for all sizes.

## Derivation / proof

### Set-up

At orientation `IDENT` curve 14 partitions the `n × n` square (`Wc = Hc = n`). With
`d1 = ⌊d/2⌋, d2 = d−d1` and the top node's swap `(sw, sh)`, the four sub-boxes (canonical
frame) are

```
LL = (0,   0,   Wc1, Hc1) @ main-diag  (curve 3)     UL = (0,   Hc1, Wc1, Hc2) @ mirror  (curve 5, rev)
UR = (Wc1, Hc1, Wc2, Hc2) @ identity   (curve 5)     LR = (Wc1, 0,   Wc2, Hc1) @ anti-diag (curve 5)
```

visited LL → UL → UR → LR. The three internal junctions are

- **J1** LL → UL: `exit(LL)` must be 4-adjacent to `entry(UL)`,
- **J2** UL → UR, **J3** UR → LR.

### Lemma 1 (J1 requires curve 3 to exit at its top-left cell)

UL (curve 5) is stacked directly above LL and, for every arising size, its entry cell sits at
column 0 of the shared column strip, at height `Hc1` — i.e. `entry(UL) = (0, Hc1)`. Hence J1 is
4-adjacent **iff** the LL block (curve 3, main-diagonal morphism) exits at its top-left cell
`(0, Hc1−1)`. Curve 3's exit column is a function of the LL box `(Wc1 × Hc1)`; it is **not**
uniformly 0. Measured exits of curve 3 (Liu2, this morphism, any valid kernel rule):

| LL box | curve-3 exit | column |
|--------|--------------|--------|
| `2 × 2` | `(0,1)` | 0 ✔ |
| `3 × 3` | `(0,2)` | 0 ✔ |
| `4 × 4` | `(1,3)` | **1 ✘** |

So J1 connects for the `2×2` and `3×3` LL boxes but **breaks** for the `4×4` LL box, whose exit
`(1,3)` is diagonal to `entry(UL) = (0,4)` — a unit gap in both axes.

### Lemma 2 (the height split of `(14, IDENT)` is over-determined)

Let `D(n) = { sh ∈ {first,second,none} : ∃ an assignment of the other 11 nodes making
fill(14, n, n) a Hamiltonian path }`. The swap function assigns a **single** value `sh` to the
node `(14, IDENT)`, used at *every* square size. Computationally (exhaustive over the other
nodes):

```
D(3) = { first }             D(5) = { first, none }             D(7) = { none, second }
```

For odd `n`, `none` gives `(Hc1, Hc2) = ((n−1)/2, (n+1)/2)`; `first` makes `Hc1` even; `second`
makes `Hc2` even. Concretely:

- `n = 3`: only `sh = first` connects → forces `Hc1 = 2` (LL box `2×2`, curve-3 exit col 0). J1 ✔.
- `n = 7`: `sh = first` forces `Hc1 = 4` (LL box `4×4`, curve-3 exit **col 1**) → **J1 disconnects**.
  Only `sh ∈ {none, second}` (giving `Hc1 = 3`, LL box `3×3`, exit col 0) connect.

Thus `D(3) = {first}` while `D(7) = {none, second}`, and

```
D(3) ∩ D(7) = ∅.
```

### Theorem (impossibility)

No swap rule makes curve 14 a Hamiltonian path on every `n × n` square.

*Proof.* Any swap rule fixes one value `sh*` for the node `(14, IDENT)`. To be valid at `n = 3`
requires `sh* ∈ D(3) = {first}`; to be valid at `n = 7` requires `sh* ∈ D(7) = {none, second}`.
These are disjoint, so `sh*` cannot exist. This is independent of every other node's rule and of
whether the rule is orientation-dependent, since `(14, IDENT)` is the unique top node reached at
all sizes. ∎

**Mechanism in one line**: curve 3 (Liu2) in the LL quadrant exits at its left edge only for
certain LL-box sizes; the top-level height split must therefore realise LL-box height `2` at
`n = 3` but `3` at `n = 7`, and a single `sh` cannot do both — J1 is broken at `n = 7` whichever
value is chosen to satisfy `n = 3`.

The exhaustive search (below) confirms the theorem globally: the obstruction at J1 is the first
to bite, and no combination of the remaining 11 node rules ever repairs the full path beyond
`n = 6`.

## Quasi-squares (`|w − h| = 1`)

No orientation gives a uniform quasi-square rule: for every top orientation `M`, the joint search
over `{first,second,none}²` per node is **infeasible** across `h = 1..8` (both wide `w = h+1` and
tall `h = w+1`). Per-size, per-orientation connectivity:

| size | wide `w = h+1` | tall `h = w+1` |
|------|----------------|----------------|
| primitive `2×1 / 1×2` | all 8 orientations | all 8 |
| `3×2 / 2×3` | all 8 | all 8 |
| `5×4 / 4×5` | **only 4** (the transposing `M[0][0]=0`) | **only 4** (the non-transposing `M[0][0]≠0`) |
| `7×6 / 6×7` | all 8 | all 8 |

Interpretation. At the primitive level a quasi-square behaves like the domino: a `1×2` region
admits the `A/C` orientation class and a `2×1` region the `B/D` class, so at the coarsest level
all orientations connect (rows 1–2). The first genuine recursion, `5×4 / 4×5` (`n ≡ 1 mod 4` on
the odd side), selects exactly the orientations whose **canonical frame is tall** — for wide
targets the four transposing orientations, for tall targets the four non-transposing ones — i.e.
the aspect that matches curve 14's preferred (tall) canonical layout. But this selection is not
stable: `7×6 / 6×7` (`n ≡ 3 mod 4`) again admits all 8. The alternation is the same odd-split
parity effect (`n ≡ 1` vs `n ≡ 3 mod 4`) that makes squares infeasible, so no orientation yields
a connected path for **all** wide (or all tall) quasi-squares. This is a verified-over-range
observation (sizes to `6×7`), consistent with the square impossibility theorem.

## Evidence

Engine: `research/aep.py`. Runner: `.venv/bin/python`, `sys.path.insert(0,"research")`.

- **Partition nodes** — `aep.orientations_used(14)` → 12 nodes:
  `(0,·)` × 7 orientations, `(3, main-diag)` × 1, `(5,·)` × 3, `(14, IDENT)` × 1.
  Full per-orientation rule space `9¹² = 282 429 536 481`.
- **Orientation-independent first pass** — a single `(sw, sh)` for curve 14 layered over the
  known kernel rules `{0:(first,first), 3:(first,second), 5:(first,second)}`, 9 options,
  `square_valid` on `n = 1..40`: **0 valid** (`found = []`).
- **Complete per-orientation search** — backtracking with dynamic variable ordering (assign the
  node demanded by the smallest unsatisfied size, prune on the first failing size). This is a
  *complete* traversal of the 9¹² space via propagation:
  - **solutions found on `n = 1..40`: 0**; tree nodes explored: **8299**; time ≈ 2.5 s.
  - Machinery validated on known-feasible curves — the identical search returns exactly one
    rule each: curve 0 → `(first,first)`, curve 3 → `(first,second)`, curve 5 → `(first,second)`
    (matching the established results), confirming it is not silently rejecting valid rules.
- **Largest feasible prefix** — some assignment is valid on `n = 1..N` iff `N ≤ 6`
  (`max N = 6`). `n = 7` is *individually* feasible (a solution exists for `n = 7` alone) but
  incompatible with the small sizes.
- **Obstruction (top-node domain)** — projecting the feasible assignments onto node
  `(14, IDENT)`:
  ```
  D(3) = {first}        D(5) = {first, none}        D(7) = {none, second}
  D(3) ∩ D(7) = ∅
  ```
  Feasibility of `sh` per odd `n`: `n=3 {first:True, none:False, second:False}`,
  `n=5 {first:True, none:True, second:False}`, `n=7 {first:False, none:True, second:True}`.
- **Junction diagnosis at `n = 7`** — top split `sw=sh=first` gives `Hc1=Hc2` splits with LL box
  `4×4`: curve-3 `exit=(1,3)`, `entry(UL)=(0,4)` → **J1 adjacent = False** (J2, J3 adjacent).
  With `sw=sh=none` (LL box `3×3`): curve-3 `exit=(0,2)`, `entry(UL)=(0,3)` → all junctions
  adjacent. This isolates the break to J1 and to curve 3's exit-column dependence on box size.
- **Quasi-squares** — per-orientation joint feasibility over `h = 1..8` is False for all 8
  orientations, both aspects; per-size connectivity table above (verified to `7×6 / 6×7`).

Search-space totals reported: orientation-independent pass = **9**; full per-orientation space =
**9¹² = 282 429 536 481**, traversed completely by propagation (8299 live tree nodes, 0
solutions).

## Open questions

- **Closed form for curve 3's exit column.** The impossibility rests on the measured fact that
  curve 3 (Liu2, main-diagonal morphism) exits its LL box at column 0 for the `2×2`/`3×3` boxes
  but at column 1 for the `4×4` box. A closed formula for curve 3's exit cell as a function of
  `(Wc1, Hc1)` would upgrade Lemma 1 from range-verified to fully proved and would likely show J1
  is unsatisfiable for **all** `n ≡ 3 (mod 4)` beyond a threshold (the search shows no square
  `n ≥ 7` is jointly reachable, and every individually-feasible large `n` still collides with
  `n = 3` through `D(n)`).
- **Composite-curve criterion.** Curve 14 is the first *composite* studied here (LL ≠ the other
  three kernels). Its infeasibility comes from a mismatch between curve 3's and curve 5's
  endpoint parities across the LL→UL junction. Formulating feasibility of a composite curve in
  terms of the endpoint-parity compatibility of its LL kernel with its UL kernel is the natural
  next theorem.
- **General rectangles** `|w−h| ≥ 2` not probed here; expected infeasible for the same J1 reason,
  but unverified.

## Verification

**Verdict: CONFIRMED.** An independent re-implementation of the search (not reusing the report's
code) reproduces every load-bearing claim.

- **Partition nodes.** `aep.orientations_used(14)` → 12 nodes: curve 0 × 7 orientations,
  `(3, main-diag)` × 1, curve 5 × 3, `(14, IDENT)` × 1. Full per-orientation space
  `9¹² = 282 429 536 481`. ✓ matches report.

- **Complete search, n = 1..40.** I wrote an independent CSP backtracker (dynamic node discovery
  via a `Missing`-node exception; branch on the first unassigned node a size demands; prune on the
  first failing size — a complete traversal of the 9¹² space). Result: **0 solutions**, **8299
  tree nodes explored** (≈2.4 s). This independently reproduces the report's headline numbers
  exactly, including the 8299 count.

- **Machinery validated on known-feasible curves** (same solver, other target index): curve 0 →
  81 solutions incl. top-node `(first,first)`; curve 3 → 243 incl. `(first,second)`; curve 5 → 81,
  top node **only** `(first,second)`. These recover the established results, confirming the solver
  does not silently reject valid rules. (Curve 0 also admitting `(none/second, first)` at the top
  node is expected — at a single top split multiple width-swaps validate; the canonical const rule
  `(first,first)` is among them.)

- **Obstruction — domains under FULLY FREE other nodes** (stronger than the report's fixed-kernel
  computation; this is what the theorem's necessary-condition argument actually requires):
  `D(3) = {first}` (feasible only for sh=first; sh∈{none,second} exhaustively infeasible),
  `D(7) = {none, second}` (sh=first exhaustively infeasible — **22144** tree nodes explored with
  zero valid assignments; sh∈{none,second} feasible). Hence `D(3) ∩ D(7) = ∅`. The theorem's logic
  is sound: any global rule fixes one `sh*` at `(14, IDENT)` (the unique top node, reached at every
  size), and no value lies in both domains. ✓

- **Junction diagnosis at n = 7.** With top `sh=first` (LL box width 4): curve-3 `exit=(1,3)`,
  `entry(UL)=(0,4)` → **J1 not 4-adjacent**. With top `sh=none` (LL box width 3): curve-3
  `exit=(0,2)`, `entry(UL)=(0,3)` → J1 adjacent. This localizes the break to J1 and to curve 3's
  exit-column dependence on box size, exactly as Lemma 1/2 state. ✓

- **Per-size top-rule feasibility** (fixed established kernels): n=3 → sh∈{first}; n=5 →
  {first,none}; n=7 → {none,second}; n=9 → {second}; n=11 → {first}; n=13 → {first,none}. The
  `n≡1 vs n≡3 (mod 4)` alternation is reproduced. ✓

- **Quasi-squares.** Independent per-orientation feasibility search: `2×1/1×2` and `3×2/2×3`
  connect in all 8; `5×4` in exactly the 4 transposing orientations, `4×5` in exactly the 4
  non-transposing; `7×6/6×7` all 8. ✓ matches the report's table precisely.

**Scope note (honest limits, not defects).** The impossibility is *proved for all n* only in the
range-verified sense: the complete search covers `n = 1..40`, and `D(3) ∩ D(7) = ∅` is an exact
finite fact that suffices for the theorem's necessary-condition proof. The report is candid that a
closed form for curve 3's exit column (Open Questions) is what would lift Lemma 1 from
range-verified to a for-all-n proof; this is correctly flagged, not overclaimed. No logical gap was
found in the theorem as stated. Verdict: **confirmed**.
