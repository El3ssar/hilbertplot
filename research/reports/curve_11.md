# Curve 11 — Improper6

- **kernels / quadrant rules** (visited order LL, UL, UR, LR; each `(base, morphism, reverse)`):
  | quadrant | base | morphism `M` | reverse |
  |----------|------|--------------|---------|
  | LL | 5 (Liu4) | `((1,0),(0,-1))` = **vflip** (`m`) | False |
  | UL | 5 (Liu4) | `((0,-1),(1,0))` = **rot90** (`g`) | False |
  | UR | 5 (Liu4) | `((0,1),(1,0))` = **maindiag / transpose** (`o`) | **True** |
  | LR | 5 (Liu4) | `((0,1),(-1,0))` = **rot270** (`x`) | False |

  Every quadrant base is **curve 5 (Liu4)**, whose four quadrant bases are all **curve 0
  (Hilbert)**. The kernel chain is therefore **11 → 5 → 0**. Curve 11 never appears inside
  itself, so in the partition it occurs **only as the top-level node at orientation `id`**;
  all deeper nodes are curve 5 (4 orientations) and curve 0 (7 orientations). The kernels
  must be given correct swap rules too, and the problem is naturally solved bottom-up
  (curve 0 first, then curve 5, then curve 11) — although, as shown below, the obstruction
  lives entirely at the **top node** and is independent of the kernel rules.

- **entry/exit type**: `entry_exit(11) = ('edge','interior')`. Curve 11 enters on an edge and
  **exits in the interior** — the only "improper" endpoint in this kernel family (curve 5 is
  `('edge','edge')`, curve 0 is `('corner','corner')`). The interior exit is produced by the
  UR quadrant carrying `reverse=True`, which folds the last two quadrants inward.

- **partition nodes** (`orientations_used(11)`) — the `(curve, orientation)` pairs that need a
  swap rule — **12 nodes**, a closed set:
  - `(11, id)` — curve 11 at identity (it never appears at any other orientation);
  - `(5, ·) × 4` — curve 5 at `{rot90, vflip, maindiag, rot270}`;
  - `(0, ·) × 7` — curve 0 at seven orientations, closed under the recursion.

## Result

- **squares: INFEASIBLE.** No swap rule — **orientation-independent or per-orientation, over
  the full `9^12` rule space** — makes `fill(11,·)` a connected space-filling path on every
  `n × n` square. The obstruction is a **contradiction between the height-split parity
  demanded at `n = 5` and at `n = 7`**, both imposed on the *same* size-independent height
  rule `sh` of the single top node `(11, id)`.
- **swap rule**: **none exists.**
- **verified**: exhaustive search returns **empty** — see §Evidence. The certificate is small
  and complete: the viable top-node sets `S(5)` and `S(7)` (each computed by an exhaustive
  `9^5 = 59049`-rule search) are **disjoint**. Powers of two are unconditionally valid and
  the curve reproduces hilbertplot at `n = 2^k` for `k = 1,2,3,4`: **yes**. (Note: not every even
  `n` is automatically fine — e.g. `n = 6 = 3+3` already needs a swap; only `n = 2^k` splits
  evenly at every level. The confined failure is the odd sizes, and no single rule repairs
  them all.)
- **individually** each odd size *is* feasible (explicit valid rules found for
  `n = 5,7,9,11,13,15`); the impossibility is **global** — no rule serves `n = 5` and `n = 7`
  simultaneously.
- **quasi-squares** (`|w−h| = 1`): connected only under an aspect-selected, **size-periodic**
  orientation class, and **no** orientation connects *all* wide (or all tall) quasi-squares.
  See §Quasi-squares.

## Derivation / proof

### Setup — the top-level split

Curve 11 on an `n × n` square at orientation `id` (no transpose) splits into four
**curve-5 blocks**, visited `LL → UL → UR → LR`:

```
UL = (0,   Hc1, Wc1, Hc2) @ rot90               UR = (Wc1, Hc1, Wc2, Hc2) @ maindiag, rev
LL = (0,   0,   Wc1, Hc1) @ vflip               LR = (Wc1, 0,   Wc2, Hc1) @ rot270
```

with width split `(Wc1, Wc2)` and height split `(Hc1, Hc2)` governed by
`swap(11, id) = (sw, sh)`. The two **lower** blocks `LL, LR` have height `Hc1`; the two
**upper** blocks `UL, UR` have height `Hc2`. The horizontal junctions `LL→UL` and `UR→LR`
straddle the internal line `y = Hc1`; the vertical junction `UL→UR` straddles `x = Wc1`
along the top tier.

### Lemma 1 (`sh` fixes the parity of `Hc1` uniformly across odd `n`)

For odd `n = 2m+1`, `_split(n, ·)` gives `d1 = m, d2 = m+1` and then corrects by the rule.
Exactly one of `m, m+1` is even, and the correction is *the same for every odd `n`*:

- `sh = "first"` ⟹ `Hc1` is the **even** half — `(Hc1,Hc2) = (even, odd)` — for all odd `n`;
- `sh = "second"` ⟹ `Hc1` is the **odd** half — `(Hc1,Hc2) = (odd, even)` — for all odd `n`;
- `sh = "none"` ⟹ `Hc1 = n//2 = m`, parity `= m mod 2` (i.e. `n≡1 (mod4) → even`,
  `n≡3 (mod4) → odd`).

Thus a single fixed `sh` symbol determines the parity of the lower tier `Hc1` by a
*fixed function of `n`*. (`sw` behaves analogously for `Wc1`; it plays no role below.)

Concretely (`aep._split`):

```
n=5: first→Hc1=2 (even)   second→Hc1=3 (odd)   none→Hc1=2 (even)
n=7: first→Hc1=4 (even)   second→Hc1=3 (odd)   none→Hc1=3 (odd)
```

### Lemma 2 (Curve 5 is edge-to-edge, so its junction cells drift with block size)

Curve 5 (`entry_exit(5) = ('edge','edge')`) meets a shared *horizontal* edge at a cell that
is **not pinned to a corner** — it moves with the block size. For the LL orientation
(`vflip`) the exit cell of an `s × s` curve-5 block is (local coords, verified `s = 2..7`):
`s=2:(1,1), s=3:(2,2), s=4:(2,3), s=5:(2,4), s=6:(3,5), s=7:(4,6)`; the exit **column**
(`1,2,2,2,3,4`) grows with `s` rather than staying pinned to a corner. The mirror orientation
`rot90` (UL) has the entry column drift the same way. Consequently the `LL→UL` and `UR→LR` horizontal junctions across `y = Hc1` can be
made 4-adjacent **only for a specific parity of `Hc1`** relative to `n` — the drifting exit
of the lower block and drifting entry of the upper block line up on one parity of the tier
height and miss by a Manhattan distance `≥ 2` on the other.

This is the size-dependent adjacency that the *fixed* `sh` symbol of Lemma 1 must satisfy
**simultaneously at every odd `n`** — which is impossible when two odd sizes demand opposite
parities of `Hc1`.

### Lemma 3 (Two odd sizes demand opposite `Hc1` parity — exhaustive certificate)

The top node `(11, id)` is the **unique** curve-11 node and appears in the decomposition of
*every* square, so its `(sw, sh)` value is shared across all `n`. Define
`S(n) = { top ∈ {first,second,none}² : some completion of the other active nodes makes
fill(11, n, n) valid }`, computed exhaustively over the (over-approximated) active node set
of size `n`:

- `S(5) = {(first,second), (none,second)}` — **requires `sh = "second"`**, i.e. `Hc1` **odd**;
- `S(7) = {(first,first), (none,first), (second,first)}` — **requires `sh = "first"`**, i.e.
  `Hc1` **even**.

Each is a complete `9^5 = 59049`-rule search. They are **disjoint**: `S(5) ∩ S(7) = ∅`.

### Theorem (impossibility)

There is no swap rule making `fill(11,·)` valid on all `n × n` squares.

*Proof.* Any rule fixes a single value `sh` at the unique top node `(11, id)` (Lemma). By
Lemma 3, validity at `n = 5` requires `Hc1` odd (`sh = "second"`) while validity at `n = 7`
requires `Hc1` even (`sh = "first"`). No symbol yields both: `"first"`→(even,even),
`"second"`→(odd,odd), `"none"`→(even at `n=5`, odd at `n=7`) — every symbol fails at least one
of `{5,7}`. Since these are *necessary* conditions established by exhaustive search over all
completions of the remaining nodes, no assignment of the full `9^12` per-orientation rule
space (indeed no per-orientation freedom exists at the top, there being one curve-11 node)
can satisfy both sizes. ∎

The mechanism (Lemmas 1–2): curve 5's **edge** endpoints make the horizontal-junction
adjacency at `y = Hc1` depend on the parity of the lower tier `Hc1`; the required parity is
set by `n` and *flips* between `n = 5` and `n = 7`, but the swap rule can only encode one
fixed parity relationship. This is the same edge-endpoint obstruction that afflicts the other
Improper members of the `·→5→0` family; curve 11's interior global exit does not rescue it.

## Quasi-squares (`|w − h| = 1`)

For each top orientation `M`, exhaustive per-size feasibility (any swap; `9^{k}` over the
size-`k` active set, small quasi-squares) gives (`Y` = some rule connects, `N` = none):

**Wide** `(w,h) = (h+1,h)`:
```
orientation           2x1  3x2  4x3  5x4  6x5
id, xflip, 180, yflip  Y    N    Y    Y    Y     (axis-preserving)
maindiag,rot90,        Y    Y    Y    N    N     (transposing)
antidiag,rot270
```
**Tall** `(w,h) = (w,w+1)`:
```
orientation           1x2  2x3  3x4  4x5  5x6
id, xflip, 180, yflip  Y    Y    Y    N    N     (axis-preserving)
maindiag,rot90,        Y    N    Y    Y    Y     (transposing)
antidiag,rot270
```

Observations:
- The 8 orientations split into the two D4 cosets by **transpose parity** (`M[0][0]=0`?), and
  the wide/tall patterns are **exact complements** of each other between the cosets — a
  transposing top orientation turns a wide region into a *tall* canonical frame and vice
  versa, so it inherits the opposite coset's pattern.
- **No orientation connects all wide (or all tall) quasi-squares**: the axis-preserving coset
  fails wide `3×2`, the transposing coset fails wide `5×4, 6×5` (and mirror for tall). The
  Y/N pattern is size-periodic, the quasi-square analogue of the odd-square obstruction.
- **Primitive link.** At the bottom the recursion terminates on `1×2` (a *tall* domino,
  reachable canonically under orientations A, C) and `2×1` (a *wide* domino, orientations
  B, D). A wide quasi-square handled by an axis-preserving orientation bottoms out through
  wide `2×1` dominoes; a transposing orientation re-expresses it through tall `1×2` dominoes.
  The complementary Y/N tables are exactly this primitive-orientation alignment propagated up
  the recursion — the same 1×2 / 2×1 dichotomy that governs the parity of the lower tier in
  Lemma 1.

## Evidence

Environment: `cd /home/elessar/Projects/HilbertPlots && .venv/bin/python`, with
`import sys; sys.path.insert(0,"research"); import aep`.

**Structure.**
```
aep.NAME[11] = 'Improper6'
aep.RULES[11] = [(5, vflip, False), (5, rot90, False), (5, maindiag, True), (5, rot270, False)]
aep.entry_exit(11) = ('edge', 'interior')
orientations_used(11): 12 nodes = (11,id)×1, (5,·)×4, (0,·)×7
unique curve-11 node: (11, ((1,0),(0,1)))            # only orientation id ever occurs
```

**No global constant rule.** A single `(sw,sh)` applied to all indices fails every one of the
9 options on `n = 1..40` (`valid_all = False` for all 9).

**No per-curve constant rule.** Searching an independent const `(sw,sh)` for each of
`{0,5,11}` (`9^3 = 729` combinations), tested on `n = 1..40`: **0 solutions**.

**Exhaustive impossibility certificate** (`scratchpad/final.py`):
```
Hc1 parity per symbol:
  n=5: first:Hc1=2(even)  second:Hc1=3(odd)  none:Hc1=2(even)
  n=7: first:Hc1=4(even)  second:Hc1=3(odd)  none:Hc1=3(odd)

S(3) [1 node,  9^1]  viable top: {(first,none),(first,second),(none,none),
                                  (none,second),(second,none),(second,second)}  → sh∈{none,second}
S(5) [5 nodes, 9^5]  viable top: {(first,second),(none,second)}                 → sh∈{second}  (Hc1 odd)
S(7) [5 nodes, 9^5]  viable top: {(first,first),(none,first),(second,first)}    → sh∈{first}   (Hc1 even)
S(5) ∩ S(7) = ∅
full per-orientation rule space = 9^12 = 282,429,536,481
```
The empty intersection `S(5) ∩ S(7)` is a complete proof: the two exhaustive `9^5` searches
certify that `n = 5` needs `sh = "second"` and `n = 7` needs `sh = "first"`, contradictory at
the single shared top node.

**Even sizes / `2^k` match** (`scratchpad/even.py`, trivial swap `(first,first)`):
```
n=2 OK, n=4 OK, n=6 disconnected, n=8 OK, n=16 OK, n=32 OK
2^k match to hilbertplot (canonical_form): k=1,2,3,4 → all True
```
(`n=6` needs a swap because `6=3+3`; it is not a counterexample to the theorem, which is about
the impossibility of a *single* rule for all sizes.)

**Individual-size feasibility** (`scratchpad/single.py`, simulated annealing per size): valid
rules found for `n = 5,7,9,11,13,15` individually — confirming the obstruction is the *shared*
top node, not per-size impossibility.

**Search space explored.** Global const: 9. Per-curve const: `9^3 = 729`. Impossibility
certificate: `S(5)` and `S(7)` each exhaustive over `9^5 = 59049`; `S(3)` over `9`. The full
per-orientation space `9^12 ≈ 2.82×10^11` is *ruled out in bulk* by the two-size argument (the
top node has only 9 values, of which `n=5` eliminates all but `sh=second` and `n=7` all but
`sh=first`).

## Verification

**Verdict: CONFIRMED.** An independent, skeptical re-derivation reproduces the impossibility
result and its exhaustive certificate. The report's central claim — curve 11 is INFEASIBLE on
squares, with the obstruction a contradiction between the height-split parity demanded at
`n=5` (needs `sh="second"`) and `n=7` (needs `sh="first"`) at the shared top node — is sound.

**What was re-run** (`cd HilbertPlots && .venv/bin/python`, `sys.path.insert(0,"research")`):

1. **Structure.** `RULES[11]` bases `= [5,5,5,5]`, `RULES[5] = [0,0,0,0]`, `RULES[0] = [0,0,0,0]`.
   Kernel chain `11→5→0` confirmed; curve 11 never recurses into itself, so the only curve-11
   partition node is `(11, id)` — its `(sw,sh)` is genuinely shared across every `n`. Confirmed.
   `orientations_used(11)` (default range) = 12 nodes `= (11,id)×1 + (5,·)×4 + (0,·)×7`, exactly
   as reported.

2. **Node-set completeness (a subtlety the report got right, worth flagging).** A naive
   `orientations_used(11, sizes=[5])` returns only **4** nodes, because it partitions with the
   no-swap even split and misses the curve-5 `maindiag` node that appears under other swaps. My
   first exhaustive pass over those 4 nodes gave a spurious `S(5)=∅`. Recomputing the **true
   reachable node set** — and proving it complete by a **fixpoint closure** (exhaustively
   enumerate all `9^k` assignments over the current node set; expand if any new node appears;
   iterate to fixpoint) — yields exactly **5 nodes** at both `n=5` and `n=7`, matching the
   report's "over-approximated active node set of size n = 5 nodes". No swap assignment can
   reach any node outside this set, so the `9^5` searches below are **complete**, not
   heuristic.

3. **Necessary conditions (exhaustive `9^5` over the complete 5-node set):**
   - `S(5) = {(first,second),(none,second)}` → every valid rule at `n=5` has **`sh="second"`** (`Hc1` odd).
   - `S(7) = {(first,first),(none,first),(second,first)}` → every valid rule at `n=7` has **`sh="first"`** (`Hc1` even).
   - `S(5) ∩ S(7) = ∅`. Reproduces the report's Lemma 3 exactly.

4. **Direct refutation attempt (strongest test).** Exhaustive `9^5` search over the union node
   set of `{5,7}` for **any** per-orientation rule valid on `n=5` **and** `n=7` simultaneously:
   returns **`None`**. No rule exists. Since `n=1..40` contains both 5 and 7, no rule is valid
   on all squares. Feasibility is refuted directly, not only via the parity narrative.

5. **Ancillary claims.** `2^k` canonical match to hilbertplot for `k=1,2,3,4`: all **True**.
   `n∈{2,4,8,16,32}` valid with trivial swap; `n=6` disconnected (expected — `6=3+3` needs a
   swap; not a counterexample). All confirmed.

**Scrutiny of the argument.** The impossibility proof rests entirely on the exhaustive
`S(5)/S(7)` disjointness at the provably-unique, provably-complete top node — this is rigorous
and I reproduced it from scratch. Lemma 2 (the "drifting exit cell" mechanism for curve 5) is
the report's *intuition* for *why* the parity flips; it is **not load-bearing** for the proof
(the report itself flags its closed form as open), so its heuristic status does not weaken the
conclusion. I found **no gap**: the necessary conditions are established by complete search, the
node sets are proven complete by closure, and the top node is proven unique by the kernel chain.

## Open questions

- **Exact junction lemma.** Lemma 2 is stated structurally and verified computationally.
  A closed-form expression for curve 5's horizontal-junction cell as a function of block
  `(w,h)` under the `vflip`/`rot90`/`maindiag`/`rot270` orientations would upgrade the
  mechanism from "verified" to "derived", pinning the exact `n mod k` at which the required
  `Hc1` parity flips (the data show `n=5` and `n=7` on opposite parities but the individual
  feasible rules at `n=9,11,13,15` use *both* `sh` values, so the required-parity function is
  not a simple `n mod 4` — its exact form is open).
- **General rectangles.** Whether any `w × h` family (beyond squares/quasi-squares) admits a
  connected generalization, and whether the interior global exit interacts with rectangle
  aspect ratio, is untested here.
- **Classification hook.** Curve 11 joins the Improper `·→5→0` curves (e.g. curve 8) whose
  infeasibility stems from curve 5's *edge* endpoints forcing a size-dependent tier parity.
  This supports a conjecture: *a curve whose kernel is edge-to-edge and whose top split places
  that kernel across a straddling horizontal (or vertical) junction is infeasible on squares.*
