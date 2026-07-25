# Curve 15 — Liu2+Liu4 #4

- **kernels / quadrant rules** (visited order LL, UL, UR, LR):
  | quadrant | base | morphism `M` | reverse |
  |----------|------|--------------|---------|
  | LL | 3 (Liu2) | `((0,-1),(1,0))` = **rot90** | False |
  | UL | 5 (Liu4) | `((0,-1),(1,0))` = **rot90** | False |
  | UR | 5 (Liu4) | `((0,1),(1,0))`  = **transpose** | **True** |
  | LR | 5 (Liu4) | `((-1,0),(0,-1))` = **rot180** | **True** |

  Curve 15 is a **composite** kernel. It recurses into **curve 3 (Liu2)** once (LL) and
  **curve 5 (Liu4)** three times (UL, UR, LR); each of 3 and 5 in turn recurses only into
  **curve 0 (Hilbert)**. The dependency DAG is `15 → {3, 5} → 0`, so the problem is
  approached **bottom-up**. Curve 15 itself appears in the recursion **only at the identity
  orientation** — it is never re-oriented by its own rules (its four bases are 3,5,5,5,
  never 15), so the node `(15, IDENT)` is the unique top node and is shared by **every**
  square size `n`. This single fact is what the impossibility proof turns on.

  (Sibling contrast: curve 15 differs from curve 13 only in the **LR** quadrant — 15 uses
  `Liu4 @ rot180,rev` where 13 uses `Liu2 @ rot270`. That one change makes the `5×5`
  square *feasible* for curve 15, so curve 15's obstruction is **not** the within-`n=5`
  `2×3` colour-lock that kills curve 13; it is a genuinely different, cross-size conflict.)

- **entry/exit type:** `entry_exit(15) = ('edge','edge')`. Like its parents 3 and 5 it is
  an edge→edge curve. On odd AEP squares the concrete fill enters and exits in the **lower
  row** (e.g. `n=5`: start `(2,0)`, end `(4,2)`), consistent with the `∩`-shaped top-level
  traversal LL → UL → UR → LR (up the left column, across the top, down the right column).

- **partition nodes** (`orientations_used(15)`, the `(curve, orientation)` pairs a swap rule
  must cover): **12** nodes total —
  **curve 15** (1: identity), **curve 3** (1), **curve 5** (3), **curve 0** (7).
  Because the swap choice itself changes which sub-boxes are odd (and hence which nodes get
  recursed into), the node set relevant to a given `n` is computed by branching over *both*
  split parities. Key fact used below: for `n ∈ {5, 7}` the reachable node set is exactly
  the **same 5 nodes** — `{(3,rot90), (5,rot90), (5,transpose), (5,rot180), (15,IDENT)}` —
  and curve 0 is **never reached** (all Hilbert instances bottom out as `≤2`-cell leaves).
  This was confirmed two ways: by the parity-branching reachability walk, and by
  instrumenting 500 random real fills (the visited-node set is always a subset of these 5).

## Result

- **squares: INFEASIBLE.** No swap rule — orientation-independent **or** fully
  per-orientation over the complete node space — makes `fill(15,·)` a valid Hamiltonian
  path on every `n × n` square. The obstruction is a **cross-size conflict**: the `5×5`
  and `7×7` squares impose **contradictory** demands on the single shared node `(15,IDENT)`.

- **swap rule:** none exists. (The `5×5` *forces* the root to `(second,second)`; the `7×7`
  *forces* the root height-split to `first`. These are incompatible at one fixed node.)

- **verified:**
  - Orientation-independent `(sw,sh)` for curve 15 (kernels at their established
    `0:(first,first), 3:(first,second), 5:(first,second)` rules): all **9** options fail on
    `n = 1..40` (fail-sets listed in Evidence; every option fails by `n ≤ 7`).
  - Per-**index** rule for all four curves `{0,3,5,15}` jointly: exhaustive **9⁴ = 6561**
    combinations, **0 valid** on `n = 1..20`.
  - Full **per-orientation** rule over the complete `n ∈ {5,7}` node universe (5 nodes):
    exhaustive **9⁵ = 59049** assignments. `5×5` has **1944** valid assignments and `7×7`
    has **2430**, but their **intersection is empty**. Since `swap(index,M)` assigns a fixed
    `(sw,sh)` to each node independent of region size, and these 5 nodes are *all* the nodes
    either size can reach, this enumerates **every** restriction any global swap function can
    have at `n = 5` and at `n = 7`. Disjoint valid sets ⇒ no global rule validates both.
  - Heuristic corroboration over the full 12-node space (`9¹² ≈ 2.8×10¹¹`): coordinate
    descent (400 restarts) and simulated annealing both **plateau at ≥ 13 failing sizes**
    out of `n = 3..27`; neither finds a zero-failure rule.
  - `2^k` sanity: for `n = 2,4,8,16` the fill is valid and **matches hilbertplot** exactly
    (`canonical_form` equality); at powers of two every split is even so the swap rule is
    irrelevant (verified: `n=8` valid for 50/50 random rules).

- **quasi-squares (`|w−h| = 1`):** curve 15 connects on many quasi-squares (the obstruction
  is specific to odd *squares*), with a clean **transpose vs non-transpose** duality that is
  itself **size-dependent** — see below.

## Derivation / proof of impossibility

### The rigorous core (exhaustive, unconditional)

**Node-sharing.** Curve 15 is never a base of any curve (its own bases are `3,5,5,5`), so
the recursion places curve 15 only at the top, at the identity orientation. Hence there is a
**unique** node `r := (15, IDENT)`, and the swap function assigns it **one** value
`swap(15,IDENT) = (sw*, sh*)` that is used for **every** square size.

**Complete search at `n = 5` and `n = 7`.** For both sizes the set of `(curve,orientation)`
nodes reachable under *any* swap assignment is the same 5-element set `U` above (verified by
parity-branching and by instrumented fills). Enumerating all `9⁵ = 59049` assignments of `U`:

| size | # valid assignments (of 59049) | forced root value `swap(15,IDENT)` |
|------|-------------------------------|-------------------------------------|
| `5×5` | **1944** | **every** valid assignment has root `= (second, second)` |
| `7×7` | **2430** | **every** valid assignment has root height-split `sh = first` |

The minimal conflicting projection is onto the **single** coordinate `sh*` of the root node:
`5×5` admits **only** `sh* = second`; `7×7` admits **only** `sh* = first`. A single fixed
node cannot carry both.

> **Theorem (curve 15 is square-infeasible).** There is no swap function
> `swap : (index, M) ↦ (sw, sh) ∈ {first,second,none}²` for which `fill(15,·)` is a valid
> Hamiltonian path on both the `5×5` and the `7×7` square. A fortiori none is valid on all
> `n×n`. ∎

This is unconditional: the `9⁵` enumeration is exhaustive over the entire node universe that
`n=5` and `n=7` can touch, so it covers every possible global rule's behaviour there.

### Why the two sizes disagree (mechanism)

The top split of an odd `n×n` produces a lower row (LL, LR) of height `Hc1` and an upper row
(UL, UR) of height `Hc2`, with `{Hc1,Hc2} = {⌊n/2⌋, ⌈n/2⌉}`; `sh` chooses which is even.
The `∩`-traversal routes **two vertical junction transfers** through the outer columns
(LL→UL climbs the left column; UR→LR descends the right column) while both global endpoints
sit in the **lower** row. Reading off the forced valid configurations:

| `n` | halves `{⌊n/2⌋,⌈n/2⌉}` | forced `(Hc1, Hc2)` | lower row | `n mod 4` |
|-----|------------------------|---------------------|-----------|-----------|
| 5 | `{2,3}` | `(3, 2)` (sh=second) | the **larger** half (3) | 1 |
| 7 | `{3,4}` | `(4, 3)` (sh=first)  | the **larger** half (4) | 3 |

The **geometric** requirement is size-uniform: *the lower row must receive the larger half*
(so the two Liu4 vertical junctions and the lower-row endpoints reconcile). But the swap rule
is phrased in terms of **parity** (“which half is even”), and *larger half* ↔ *even half*
coincide **only for `n ≡ 3 (mod 4)`**: the larger half `⌈n/2⌉` is even iff `n ≡ 3 (mod 4)`.

- `n = 5 ≡ 1`: larger half `3` is **odd** ⇒ to put it on the bottom, make the **top** even
  ⇒ `sh = second`.
- `n = 7 ≡ 3`: larger half `4` is **even** ⇒ to put it on the bottom, make the **bottom**
  even ⇒ `sh = first`.

The same geometric target therefore demands **opposite** `sh` at `n=5` and `n=7`. No
size-independent `sh*` can track a parity that flips with `n mod 4`; that is the obstruction.

(The width split is only weakly constrained: `7×7` leaves `sw` free, while `5×5` additionally
pins `sw = second`. The **binding, contradictory** constraint is the height split `sh`.)

### Honest scope of the mechanism

The `n=5`/`n=7` conflict is *proved* (exhaustive). The broader `n`-pattern is **not** a clean
`mod 4` law: sampling the forced root height-split over larger `n` gives an **irregular**
sequence (`n=5→second, 7→first, 9→first, 13→second, 15→first, 17→first, …`) because from
`n ≥ 9` the recursion also reaches curve-0 nodes and deeper Liu4 junctions, adding
constraints. We therefore do **not** claim “`sh` must equal `f(n mod 4)`”. The proof rests
solely on the two exhaustively-searched sizes `n=5, n=7`, which already suffice.

## Quasi-squares (`|w − h| = 1`)

The odd-*square* obstruction does not apply to quasi-squares (they split with a different
shape multiset). Testing **existence** of a valid swap assignment (exhaustive over the
reachable nodes when `≤ 6`, else 8k random samples) for curve 15 placed at each top
orientation, on wide `(s+1)×s` and tall `s×(s+1)` regions:

```
                       wide (w=s+1,h=s)      tall (w=s,h=s+1)     (s = 2,3,4)
 non-transpose class   F F T                 T T F
 {e, rot180, vflip, hflip}
 transpose class       T T F                 F F T
 {transpose, rot90, antidiag, rot270}
```

- **Duality.** The two D4 cosets are mirror images: whatever a non-transpose orientation
  achieves on *tall* quasi-squares, a transpose orientation achieves on *wide* ones, and
  vice-versa. This is the boundary-vector face of the `1×2` (orientations A, C) / `2×1`
  (orientations B, D) primitive constraint — the top orientation decides whether curve 15's
  edge-endpoint “grain” lies along the long or the short axis.
- **Size-dependence.** Connectivity is **not** monotone/uniform in `s` (e.g. non-transpose
  *wide* fails at `s=2,3` i.e. `3×2, 4×3`, then succeeds at `s=4`; the pattern reflects the
  same parity flip as the square case). So **no single orientation connects all sizes of one
  aspect** — quasi-squares echo, rather than escape, the square obstruction. A per-size or
  per-`(s mod ·)` orientation choice is required; a uniform quasi-square rule is not claimed.

## Evidence

Commands run from `/home/elessar/Projects/HilbertPlots` against engine `research/aep.py`
(`swap` = `per_orientation_swap` / `const_swap`; validity = `aep.validate == "OK"`).

```
# structure
aep.NAME[15] = 'Liu2+Liu4 #4'
aep.RULES[15] = [(3, rot90, F), (5, rot90, F), (5, transpose, T), (5, rot180, T)]
aep.entry_exit(15) = ('edge','edge')
len(aep.orientations_used(15)) = 12   # curve 15×1, 3×1, 5×3, 0×7 ; curve 15 only at IDENT

# orientation-independent (kernels 0:(f,f) 3:(f,s) 5:(f,s)); fail-sets over n=1..20:
(first,first)  fails {3,5,11,13,19}      (second,second) fails {7,9,15,17}
(first,second) fails {3,5,7,9,11,13,15,17,19}   (second,none)  fails {5,7,13,15}
(first,none)   fails {3,5,7,11,13,15,19} (none,first)   fails {3,5,11,13,19}
(second,first) fails {3,5,11,13,19}      (none,second)  fails {5,7,9,13,15,17}
                                          (none,none)   fails {5,7,13,15}
-> no orientation-independent (sw,sh) valid on n=1..40   (0 of 9)

# joint per-index rule over {0,3,5,15}: 9^4 = 6561 combos, n=1..20  ->  0 valid

# reachable-node set (branch both split parities) — the COMPLETE node universe per size:
reachable(15, 5,5) = reachable(15, 7,7) = the SAME 5 nodes ; curve 0 not reached
                       {(3,rot90),(5,rot90),(5,transpose),(5,rot180),(15,IDENT)}
(cross-check: 500 random real fills at n=5,7 visit only these 5 nodes -> True)

# EXHAUSTIVE 9^5 = 59049 over those 5 nodes:
n=5 : 1944 valid,  ALL with root (15,IDENT) = (second, second)
n=6 : 11664 valid
n=7 : 2430 valid,  ALL with root height-split sh = first  (sw free)
intersect(valid_5, valid_7) = 0            <-- the decisive contradiction
intersect(valid_3, valid_7) = 0 ;  intersect(valid_3,valid_5,valid_6,valid_7) = 0
minimal conflicting projection = the single coord sh* of node (15,IDENT):
   n=5 allows only sh*=second ;  n=7 allows only sh*=first     (disjoint)

# 2^k check (swap-irrelevant at powers of two):
2^1..2^4 : valid=OK and canonical_form == hilbertplot.curve(15).points(k)   (all True)
n=8 valid for 50/50 random rules  (confirms swap-independence at even sizes)

# heuristic full-space (9^12) searches, objective = #failing n in 3..27:
coordinate descent (400 restarts): best = 13 failing sizes
simulated annealing (40 runs):     best = 14 failing sizes           (no rule reaches 0)
```

**Total search space explored for the impossibility:** `9` (orientation-independent)
`+ 6561` (`9⁴` per-index) `+ 59049` (`9⁵` full per-orientation over the complete `n∈{5,7}`
node universe) `= 65619` assignments enumerated exhaustively, plus the 12-node `9¹²`
space explored heuristically (CD + annealing, never reaching 0 failures). The decisive proof
is the `9⁵` enumeration showing `valid(5×5) ∩ valid(7×7) = ∅` at the shared root node.

## Open questions

- **General theorem / classification.** Curve 15 fails by a *cross-size* mechanism (a
  size-uniform geometric target — “lower row = larger half” — that maps to a `mod 4`-flipping
  parity demand at the single shared root node), which is **distinct** from curve 13's
  *within-`n=5`* `2×3` colour-lock. Both are edge→edge Liu2+Liu4 composites, yet fail for
  different reasons. A clean section-7 classification should separate (i) composites
  infeasible at a single size via a same-colour `2×(odd)` block, from (ii) composites like 15
  that are feasible at each *individual* small size but whose forced root split is
  size-incompatible. The discriminant appears to be whether the `∩`-traversal's two vertical
  junctions demand the larger or the even half in the lower row.
- **Exact `n`-law.** The forced root height-split is irregular for `n ≥ 9` (curve-0 nodes and
  deeper junctions enter). Characterising it fully (and whether it is eventually periodic in
  `n mod 2^k`) is open, though not needed for the impossibility.
- **Rectangles.** A full `w×h` characterisation beyond the quasi-square duality table is left
  open; the non-monotone quasi-square pattern points to a size-parity condition.
- **Size-dependent rules.** Unlike curve 13 (whose `2×3` block has *no* Hamiltonian path),
  curve 15's every individual size *is* fillable; a swap rule permitted to depend on `n`
  (outside the paper's size-independent model) *would* rescue it. The infeasibility is
  strictly a property of the **size-independent** rule model.
```

## Verification

**Verdict: CONFIRMED (square-infeasible).** Independent, skeptical re-run of the engine
reproduces every load-bearing number and the impossibility argument is logically sound.

**What I re-ran** (`.venv/bin/python`, engine `research/aep.py`, validity = `aep.validate == "OK"`):

- **Structure.** `aep.RULES[15] = [(3,rot90,F),(5,rot90,F),(5,transpose,T),(5,rot180,T)]`;
  `entry_exit(15)=('edge','edge')`; `len(orientations_used(15))=12` with per-curve counts
  `{15:1, 3:1, 5:3, 0:7}`. Bases are `3,5,5,5` (never 15) ⇒ node `(15,IDENT)` is unique and
  shared across all sizes. Matches the report.
- **Orientation-independent (kernels `0:(f,f), 3:(f,s), 5:(f,s)`).** All 9 `(sw,sh)` options
  fail on `n=1..40`; the per-option fail-sets match the report exactly (e.g. `(second,second)`
  fails `{7,9,15,17}`, `(second,none)` fails `{5,7,13,15}`). Every option fails by `n≤7`.
- **The decisive `9⁵` enumeration (5-node universe, per-axis pairs per node).** Reproduced
  independently:
  - `n=5`: **1944** valid, **all** with root `(15,IDENT) = (second,second)`.
  - `n=7`: **2430** valid, **all** with root height-split `sh = first` (`sw` free).
  - `valid(5×5) ∩ valid(7×7) = 0`.
- **Completeness check (the linchpin), verified independently.** I instrumented every one of
  the `9⁵` assignments to record which nodes the fill actually queries. At **both** `n=5` and
  `n=7` the set of nodes touched outside the 5-node universe is **empty** across all 59049
  assignments. Since node-reachability depends only on swap values at already-touched nodes,
  the values at the other 7 nodes are irrelevant at `n=5,7`; hence validity there is *fully*
  determined by the 5-node restriction, and the enumeration is genuinely exhaustive over every
  possible global rule's behaviour at these two sizes. This closes the one gap that could have
  undermined the argument.
- **`2^k` sanity.** For `n=2,4,8,16` the fill (root `(second,second)`) is `validate==OK` and
  `canonical_form` equals `hilbertplot.curve(15).points(k)` (all True).

**Soundness of the impossibility argument.** The proof rests on three facts, each independently
confirmed: (i) `swap` has signature `(index,M)↦(sw,sh)` and therefore cannot depend on the
square size, so `(15,IDENT)` carries a *single* fixed value for all `n`; (ii) `n=5` validity
forces that value's `sh = second`; (iii) `n=7` validity forces `sh = first`. These are
contradictory, and by the completeness check each size's validity depends only on nodes that
include the shared root. Therefore no size-independent swap function is valid on both `5×5` and
`7×7`, a fortiori none on all `n×n`. The theorem is unconditional and correct. I found no
logical gap. The "mechanism" section (lower-row-must-be-larger-half ↔ parity flip at
`n≡3 mod 4`) is a heuristic explanation and is honestly scoped as such (the report explicitly
disclaims a clean `mod 4` law for `n≥9`); the impossibility does not depend on it.

*Independent checker's note:* the report's claim that curve 0 is "never reached" at `n=5,7` is
corroborated by the empty outside-touched set, but note the proof does **not** actually require
it — all that is needed is that both sizes' validity is determined by their touched sets and
that both share the root node with conflicting forced `sh`. That holds regardless. The proof is
robust.
