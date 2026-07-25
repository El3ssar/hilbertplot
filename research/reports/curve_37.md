# Curve 37 — Moore+Liu4 #6

- **kernels / quadrant rules** (order LL, UL, UR, LR):
  - LL: base **5** (Liu4), morphism `((1,0),(0,-1))` (x, −y), rev `False`
  - UL: base **5**, morphism `((0,-1),(1,0))`, rev `False`
  - UR: base **5**, morphism `((0,1),(1,0))`, rev **`True`**
  - LR: base **1** (Moore), morphism `((1,0),(0,-1))`, rev `False`
- **entry/exit type**: `('edge', 'interior')` (global start on an edge, end in the interior).
- **kernel curves involved** (transitive closure, all orientations): `{0 (Hilbert), 1 (Moore), 5 (Liu4), 37}`.

## Result

- **squares: INFEASIBLE.** No swap rule — orientation-independent **or** per-orientation — makes
  `fill(37, …)` a Hamiltonian path on every `n×n`. Proven by exhaustive search of the full
  per-orientation rule space (`9^12 = 282 429 536 481` assignments) plus a closed-form parity
  obstruction.
- **swap rule: none exists.** The single top node `(37, IDENT)` cannot be given a height-split
  mode that works for all odd `n`.
- **verified**: no valid rule for `n = 1..40` (exhaustive); the minimal obstruction is already
  present in the size set `{3,7}` (and `{5,7}`), proven by full `9^5 = 59049` enumeration of the
  only nodes those sizes can reach. Matches hilbertplot at `2^k`: N/A (the curve does not admit a valid
  arbitrary-square family; at the pure powers `2^k` the standard equal split is used and coincides
  with hilbertplot, but that is not an arbitrary-square generalization).
- **quasi-squares**: orientation-dependent (see §Quasi-squares). Under the identity orientation the
  *wide* quasi-squares `w=h+1` connect whenever `h` is odd (`w` even) throughout `n≤12`; *tall*
  quasi-squares `h=w+1` connect for a proper subset (`w≤4` and sporadically beyond).

## Derivation / proof

### Setup: the partition nodes

`aep.orientations_used(37)` returns the complete set of `(curve, orientation)` nodes that ever need
a swap rule when drawing curve 37 on odd squares. There are **12**:

| curve | # orientations | role |
|-------|----------------|------|
| 0 (Hilbert) | 7 | leaves of the kernel recursion |
| 5 (Liu4)    | 3 | LL, UL, UR sub-quadrants |
| 1 (Moore)   | 1 | LR sub-quadrant, at `((1,0),(0,-1))` |
| 37          | 1 | the top node, at `IDENT` |

The set of `(curve, orientation)` pairs is **independent of the swap choice**: swaps change only the
*sizes* `d1,d2` of the two halves, never the morphisms `RULES[idx][i]` that propagate orientation.
Hence 12 nodes is the exact and complete rule space; the per-orientation search space is `9^12`.

Kernel status (each verified with `aep.square_valid` / const search over `n=1..19`):
* curve 5 is arbitrary-square-feasible with the orientation-independent rule `(first, second)`.
* curve 0 is feasible with its known orientation-dependent Hilbert rule.
* **curve 1 (Moore) admits no square rule at all** (`const` search returns `[]`). This is contextual:
  inside curve 37, curve 1 is only ever drawn on *rectangles*, so its square-infeasibility is not the
  operative obstruction. The obstruction below is intrinsic to curve 37's own top node.

### The top-junction parity condition (Lemma)

Curve 37 splits an `n×n` square (canonical frame) into
`LL=(0,0,Wc1,Hc1)`, `UL=(0,Hc1,Wc1,Hc2)`, `UR=(Wc1,Hc1,Wc2,Hc2)`, `LR=(Wc1,0,Wc2,Hc1)`,
visited LL→UL→UR→LR, where `(Hc1,Hc2)` is the height split and `(Wc1,Wc2)` the width split. The three
internal junctions are LL→UL (vertical, low), UL→UR (horizontal, high), UR→LR (vertical, high→low).

**Lemma.** For odd `n`, validity of the top partition is governed *entirely by the parity of the
bottom height `Hc1`*; the width mode is unconstrained. Concretely, exhaustive `9^5` enumeration over
the five nodes reachable at `n∈{3,4,5,6,7}` (curve 0 is provably never queried there) gives the
admissible top-node modes:

| n | admissible width-mode | admissible height-mode | `Hc1` by height-mode `{first,second,none}` | required `Hc1` parity |
|---|----|----|----|----|
| 3 | `{first,second,none}` | `{none, second}` | `{first:2, second:1, none:1}` | **odd** |
| 4 | all | all | `{2,2,2}` | — (even n) |
| 5 | `{first,second,none}` | `{second}`       | `{first:2, second:3, none:2}` | **odd** |
| 6 | all | all | `{3,3,3}` | — (even n) |
| 7 | `{first,second,none}` | `{first}`        | `{first:4, second:3, none:3}` | **even** |

Read the "required parity" column off the admissible modes: a mode is admissible **iff** the `Hc1` it
produces has the required parity (odd for `n=3,5`; even for `n=7`), and within a parity the actual
value is irrelevant (`n=3`: both odd-producing modes `second,none` work). The width mode is admissible
in all three values for every `n`, so the whole obstruction lives on the height axis. ∎

### Impossibility (Theorem)

**Theorem.** There is no swap rule `swap(37, IDENT) → (sw, sh)` (equivalently, no per-orientation rule
over the 12 nodes) making `fill(37,·)` valid on all squares.

**Proof.** A swap rule assigns to the top node a *single, n-independent* height mode
`sh ∈ {first, second, none}`. For odd `n` the produced bottom height is

```
Hc1(first)  = n//2  made even   → Hc1 ≡ 0 (mod 2) for every odd n
Hc1(second) = n//2  (n//2 even) or n-n//2 → Hc1 ≡ 1 (mod 2) for every odd n
Hc1(none)   = n//2                        → parity = parity of n//2 (alternates)
```

By the Lemma the top junction needs `Hc1` **odd** at `n=3` and **even** at `n=7`. No fixed mode meets
both:
* `sh=first` → `Hc1` even at both ⇒ fails `n=3` (needs odd);
* `sh=second` → `Hc1` odd at both ⇒ fails `n=7` (needs even);
* `sh=none` → `Hc1(3)=1` odd (ok), `Hc1(5)=2` even (`n=5` needs odd ⇒ fails), `Hc1(7)=3` odd (`n=7`
  needs even ⇒ fails).

Thus the size pair `{3,7}` is already unsatisfiable, and so is `{5,7}`. Because the height mode is
fixed once and for all, no choice covers both parity demands. ∎

### Why it recurs (periodicity)

The required `Hc1` parity is not a one-off: it is periodic with period 8 in `n`. Fixing the top height
mode and reading off which odd `n` survive (kernels set to their feasible rules):

* `sh=second` (⇒ `Hc1` odd): valid odd `n ≡ 3 (mod 8)`; every odd `n ≡ 1,5,7 (mod 8)` fails.
* `sh=first`  (⇒ `Hc1` even): valid odd `n ≡ 7 (mod 8)`; every odd `n ≡ 1,3,5 (mod 8)` fails.

With the best available kernel rules the surviving/failing residues broaden to: valid `n mod 8 ∈
{0,3,4,5}`, **failing `n mod 8 ∈ {1,2,6,7}`** for `n ≥ 7`. Either way the two height modes cover
*disjoint* residue families, so infinitely many `n` fail under any fixed rule. This is the arbitrary-
square analogue of curve 1 (Moore) being square-infeasible: curve 37 inherits an unavoidable
vertical-parity conflict from stacking three Liu4 blocks over a Liu4/Moore row.

## Quasi-squares (|w−h| = 1)

Witness search (per size, random assignments of the 12 nodes; a hit certifies "connects", so the
lists are lower bounds) under each top orientation:

* **Identity `((1,0),(0,1))` — the most permissive.** Wide `w=h+1` connects for
  `2×1, 4×3, 6×5, 8×7, 10×9, 12×11` — i.e. exactly when `h` is **odd** (`w` even). Tall `h=w+1`
  connects for `1×2, 2×3, 3×4, 4×5, 6×7, 8×9` (`w≤4` reliably, sporadically beyond). The wide-even
  pattern is the direct descendant of the **2×1 wide-domino primitive** (`base_cells(2,1)=[(0,0),
  (1,0)]`), which is only realizable at orientations `{B,D}`; the tall series descends from the
  **1×2 primitive** (`base_cells(1,2)=[(0,0),(0,1)]`, orientations `{A,C}`).
* **Other orientations** connect only sporadically in the search (single sizes such as `4×3` or
  `7×8`), consistent with their global entry/exit being rotated away from the aspect that the curve's
  LL/UL/UR/LR stack prefers. Quasi-square connectivity is therefore strongly **orientation-dependent**,
  in contrast to the square case where *no* orientation succeeds for all `n`.

## Evidence

Commands (run from `/home/elessar/Projects/HilbertPlots`, engine `research/aep.py`):

```
# Partition nodes and kernels
aep.orientations_used(37)  -> 12 nodes over curves {0,1,5,37}
aep.RULES[37] = [(5,(x,-y),F),(5,(-y,x),F),(5,(y,x),T),(1,(x,-y),F)]
aep.entry_exit(37) = ('edge','interior')

# Kernel square-feasibility
curve 5 const square-valid: [('first','second')]
curve 1 const square-valid: []           # Moore infeasible on squares
```

Orientation-independent rule: none.
```
global const (all indices, 9 options): 0 valid
37-const layered on kernel-const:      0 valid
```

Full per-orientation search (sound pruned DFS; a size is judged only when its fill queries no
unassigned node, so pruning is exact and the space is traversed completely):
```
EXHAUSTIVE search of 9^12 = 282,429,536,481 assignments, n=1..40
  -> solution exists? False        (natural termination, ~15 s, 31k branch-checks)
```

Minimal obstruction, exhaustive `9^5 = 59049` over the curve-0-free nodes reached at n≤7:
```
size 3: 39366 valid assignments        size 7: 1944 valid assignments
pair {3,7}: 0 joint solutions   <-- INFEASIBLE
pair {5,7}: 0 joint solutions   <-- INFEASIBLE
minimal infeasible size-subsets: {3,7}, {5,7}
admissible top height-mode:  n=3 -> {none,second};  n=5 -> {second};  n=7 -> {first}   (disjoint)
```

Periodicity:
```
top height-mode='second': valid odd n = 3,11,19,27,35   (n ≡ 3 mod 8)
top height-mode='first' : valid odd n = 7,15,23,31,39   (n ≡ 7 mod 8)
best-effort fixed rule  : fails n mod 8 ∈ {1,2,6,7} for n≥7
```

Scratch scripts: `dfs2.py` (exhaustive `9^12`), `conflict.py`/`proj.py`/`final.py` (the `{3,7}`
obstruction and admissible-mode table), `verify.py` (periodicity + re-confirmation), `quasi2.py`
(quasi-squares) in the session scratchpad.

## Open questions

- **Closed form for the required `Hc1` parity** as a function of `n mod 8`, derived analytically from
  the Liu4 (curve 5) entry/exit boundary vectors rather than read off computationally. The data give
  "odd for `n ≡ 3,5`, even for `n ≡ 1,7` (mod 8)"; a boundary-vector proof would make the period-8
  law a theorem rather than verified-over-range.
- **Could a richer partition primitive rescue curve 37?** The infeasibility is relative to the
  approximately-even partition with a per-axis `{first,second,none}` swap. A construction allowing the
  top node to choose its split parity as a function of `n mod 8` (outside the current swap-rule
  formalism) would connect all squares; whether that stays within the paper's rule family is open.
- **Rectangles** `w×h` generally: the width axis is unconstrained at the top node, so the obstruction
  is purely vertical; this suggests curve 37 may connect on many non-square rectangles whose height
  avoids the bad parity. Not yet mapped.

## Verification

**Verdict: CONFIRMED.** An independent, skeptical re-derivation reproduces the report's `INFEASIBLE`
result exactly and upgrades confidence: the impossibility is a genuine *proof* (two finite witnesses
over a provably-complete node space), not merely verified-over-range.

**What was re-run (from `/home/elessar/Projects/HilbertPlots`, engine `research/aep.py`):**

1. **Partition structure reproduced.** `aep.RULES[37] = [(5,(x,−y),F),(5,(−y,x),F),(5,(y,x),T),
   (1,(x,−y),F)]`; `entry_exit(37)=('edge','interior')`; `orientations_used(37)` returns **12** nodes
   over curves `{0:7, 5:3, 1:1, 37:1}`. Curve 37's quadrant bases are `{5,5,5,1}` and the transitive
   closure of bases is `{0,1,5,37}` — curve 37 is **never** a kernel of a sub-curve, so `(37, IDENT)`
   is the *unique* top node, appearing once, with a single fixed height mode. No hidden orientation
   degree of freedom exists. All confirmed.

2. **Reachable-node instrumentation (independent).** Instrumenting `fill` to record every queried
   `(index, M)` shows that at `n ∈ {3,5,7}` only the five nodes
   `{(37,IDENT), (1,(x,−y)), (5,(−y,x)), (5,(y,x)), (5,(x,−y))}` are ever touched; **curve 0 is never
   queried** at `n ≤ 7`, as claimed.

3. **Decisive exhaustive re-search — `9^5 = 59049` over those five nodes**, checking `aep.validate ==
   "OK"`. A completeness guard raised on any query to an unassigned node and **never fired**
   (`reached-unassigned = 0` at each of n=3,5,7), so the five-node space is provably complete for these
   sizes. Independent counts: **n=3 → 39366 valid, n=5 → 5508, n=7 → 1944** (n=3 and n=7 match the
   report's numbers exactly). Crucially:
   - **pair {3,7}: 0 joint solutions**  ⟶ INFEASIBLE
   - **pair {5,7}: 0 joint solutions**  ⟶ INFEASIBLE
   - pair {3,5}: 5508 (feasible — so the conflict is genuinely {3,7}/{5,7}, not spurious).
   Because those five nodes are the complete reachable set at n=3,5,7 under *every* mode choice, any
   full 12-node per-orientation rule restricts to them at these sizes; since none satisfies both n=3
   and n=7, **no 12-node rule (and a fortiori no orientation-independent rule) can validate all
   squares.** This is a two-witness contradiction proof valid for all n — not a range check.

4. **Lemma (admissible modes) independently reproduced.** Projecting the valid assignments onto the
   top node: admissible top height-modes are `n=3 → {none, second}`, `n=5 → {second}`, `n=7 →
   {first}` — matching the report's table. Width-mode is admissible in all three values at every n
   (obstruction is purely on the height axis). Via `aep._split`: `sh=first` gives `Hc1` even for every
   odd n, `sh=second` gives `Hc1` odd for every odd n, `sh=none` alternates (odd at n=3, even at n=5,
   odd at n=7). Required parity: odd at n=3 and n=5, even at n=7 — no fixed mode meets both, exactly
   as the Theorem states.

5. **Supporting kernel claims checked.** Curve 5 with `(first,second)` is square-valid over
   **n=1..40** (`True`); curve 1 (Moore) admits **no** orientation-independent square rule (const
   search returns `[]`). The report correctly flags curve 1's infeasibility as *contextual* (Moore is
   only drawn on rectangles inside curve 37) and not the operative obstruction.

**Scrutiny of the argument.** The proof does **not** depend on trusting the report's `9^12` pruned-DFS
implementation: the entire impossibility follows from the exhaustive, provably-complete `9^5`
enumeration on `{3,7}`, which I reproduced from scratch. The parity Lemma is a faithful *description*
of that enumeration. The one genuinely unproven item is correctly parked in Open Questions: the
period-8 closed form for the required `Hc1` parity is stated as *verified-over-range*, not proved —
appropriate labeling. The quasi-square section is explicitly hedged as witness-search lower bounds and
is not load-bearing for the squares verdict.

**Gaps found:** none affecting the verdict. The squares result `INFEASIBLE` is sound and, in fact,
proven for all n by the finite {3,7} obstruction over a complete node space.
