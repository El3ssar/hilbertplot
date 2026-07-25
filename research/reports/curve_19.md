# Curve 19 — Hilbert+Liu3 #2

- **kernels / quadrant rules** (visited order LL, UL, UR, LR):
  | quadrant | base | morphism (matrix) | reverse | transposes? |
  |----------|------|-------------------|---------|-------------|
  | LL | **4** (Liu3)    | `((1,0),(0,-1))` reflect-y     | True  | no |
  | UL | **0** (Hilbert) | `((1,0),(0,1))`  identity      | False | no |
  | UR | **0** (Hilbert) | `((1,0),(0,1))`  identity      | False | no |
  | LR | **4** (Liu3)    | `((-1,0),(0,-1))` rot180       | False | no |

  Kernel dependency chain: `19 → {0, 4}`, `4 → {0}`, `0 → {0}` (Hilbert self-referential). Solved bottom-up. **Every one of curve 19's four quadrant morphisms is non-transposing** (`M[0][0] ≠ 0`) — curve 19 never places a kernel on its side. This single fact drives the impossibility.

- **entry/exit type:** `('interior','interior')` (from `aep.entry_exit(19)`). Curve 19 is an interior→interior curve, like curve 16; unlike the corner→corner Hilbert it has no globally protected endpoint pair.

## Result

- **squares: INFEASIBLE.** No swap rule — orientation-independent *or* per-orientation, over the **entire** `{first,second,none}²` space at **every** partition node — makes `fill(19,·)` a Hamiltonian path on the `7×7` square. Since a globally valid rule must in particular be valid at `n=7`, curve 19 does **not** admit a connected arbitrary-square generalization.
- **swap rule:** none exists (see proof). Curve 19 is valid on `n ∈ {1,2,3,4,5,6,8}` (each verified exhaustively) but no single rule survives the first obstruction at `n=7`.
- **verified:** valid on `n×n` for `n ∈ {1..6, 8}`; **infeasible** (exhaustively, over the complete swap space) for `n ∈ {7, 9, 15, 17}`; status of `n ∈ {10,11,12,13,14,16}` undetermined (no forced-dead child, junctions unresolved — irrelevant to the verdict). `matches hilbertplot at 2^k`: **yes** — at `n = 2^k` every split is even, the swap is inert, and `fill(19,·)` reproduces `hilbertplot.curve(19)` (checked at `n=4,8`); the obstruction is purely a non-power-of-two phenomenon.
- **quasi-squares:** curve 19 connects on a **parity-checkerboard** of quasi-squares that is symmetric under transpose-of-orientation (see §Quasi-squares). Non-transposing top orientations and transposing top orientations realize *complementary* sets of `(w,h)`; no orientation realizes all.

## Derivation / proof

### Lemma 1 (kernel fillability of quasi-squares)

In their canonical (non-transposing) frame, the kernels Hilbert (0) and Liu3 (4) can be filled as a Hamiltonian path on a `W×H` box, *for some swap rule*, only on a narrow band around the diagonal — with specific quasi-squares **excluded**. Verified exhaustively over all `9` swaps per node (`Y` = a valid path exists for some rule, `.` = none exists for any rule):

```
curve0 (Hilbert) canonical fillability      curve4 (Liu3) canonical fillability
      H: 1  2  3  4  5  6  7                      H: 1  2  3  4  5  6  7
 W1 :   Y  Y  .  .  .  .  .                  W1 :   Y  Y  .  .  .  .  .
 W2 :   Y  Y  Y  .  .  .  .                  W2 :   Y  Y  Y  .  .  .  .
 W3 :   .  Y  Y  .  .  .  .                  W3 :   .  Y  Y  .  .  .  .
 W4 :   .  .  Y  Y  Y  .  .                  W4 :   .  .  Y  Y  Y  .  .
 W5 :   .  .  .  .  Y  Y  .                  W5 :   .  .  .  .  Y  Y  .
 W6 :   .  .  .  .  Y  Y  Y                  W6 :   .  .  .  .  Y  Y  .
 W7 :   .  .  .  .  .  .  Y                  W7 :   .  .  .  .  .  Y  Y
```

The two kernels agree on every cell relevant below. In particular the **quasi-squares `(W,H) = (3,4)` and `(5,4)` are dead for both kernels** (`.`), as are `(7,8)` and `(9,8)` (verified separately, exhaustively). This is the interior-curve shadow of the `1×2`/`2×1` primitive dichotomy: an interior→interior kernel drawn under a non-transposing morphism can absorb a one-cell surplus only on the axis its entry/exit chord runs along, and only for particular size parities; the "wrong" quasi-square has no admissible path at all — not for lack of a swap, but intrinsically.

*(Reflections preserve `(W,H)` and path validity, so the table for every non-transposing orientation is identical to the canonical one; a transposing orientation swaps the roles of `W` and `H`.)*

### The odd-square partition

Approximately-even splitting of an odd side `n` gives halves `{f, c}` with `f = (n−1)/2`, `c = f+1`. The four quadrants receive the four sizes
`(Wc1,Hc1), (Wc1,Hc2), (Wc2,Hc2), (Wc2,Hc1)` with `{Wc1,Wc2}={f,c}`, `{Hc1,Hc2}={f,c}` — i.e. **exactly one square `(f,f)`, one square `(c,c)`, one "tall-by-one" `(f,c)`, and one "wide-by-one" `(c,f)`**, in some arrangement. The swap rule `(sw,sh)` of node `(19,IDENT)` only chooses *which quadrant* receives the mixed boxes; it cannot avoid producing them.

### Theorem (impossibility at `n=7`)

For the `7×7` square the complete set of partition nodes is
`{(19,IDENT), (0,IDENT), (4,((1,0),(0,-1))), (4,((-1,0),(0,-1)))}` — four nodes (Hilbert and the two Liu3 orientations bottom out into `≤2`-sized primitives without spawning further nodes). The full rule space is therefore `9⁴ = 6561` assignments. Exhaustive test:

```
n=7 nodes: (19,IDENT),(0,IDENT),(4,reflect-y),(4,rot180)
n=7 exhaustive: tested 6561 (9^4), valid 0
```

Zero valid. The mechanism is transparent in the per-split decomposition — with `f=3, c=4`, the tall-by-one box is `(3,4)`, dead for both kernels by Lemma 1, and it lands on **each** quadrant as `(sw,sh)` ranges over its four settings:

```
TOP split Wc=(3,4) Hc=(3,4):  UL curve0 3x4 -> 0 internally-valid swaps (dead)
TOP split Wc=(3,4) Hc=(4,3):  LL curve4 3x4 -> 0 internally-valid swaps (dead)
TOP split Wc=(4,3) Hc=(3,4):  UR curve0 3x4 -> 0 internally-valid swaps (dead)
TOP split Wc=(4,3) Hc=(4,3):  LR curve4 3x4 -> 0 internally-valid swaps (dead)
```

Because all four quadrant morphisms are non-transposing, the `(3,4)` box is always a *canonical* tall-by-one box for whichever kernel receives it, hence always dead. No swap rule can rescue a quadrant whose sub-region admits no path at all. Since any square-universal rule must validate `n=7`, and `n=7` is unwinnable, **curve 19 admits no connected arbitrary-square generalization.** ∎

### Corollary (the obstruction recurs; `2^m ± 1` pattern)

The same argument kills every odd `n` whose *mixed child* `(f,c)` or `(c,f)` lies in the kernels' shared dead-set. Verified exhaustively by decomposition:

| `n` | `f,c` | forced-dead child (both kernels) | rigor |
|-----|-------|----------------------------------|-------|
| 7   | 3,4   | `(3,4)` tall-by-one              | exhaustive `9⁴` full-square **and** per-split |
| 9   | 4,5   | `(5,4)` wide-by-one              | per-split, each child exhaustively dead (`9³`–`9⁴`) |
| 15  | 7,8   | `(7,8)` tall-by-one              | per-split, child exhaustively dead |
| 17  | 8,9   | `(9,8)` wide-by-one              | per-split, child exhaustively dead |

The verified infeasible squares in `1..40` are `{7, 9, 15, 17}`, which are exactly `{2³−1, 2³+1, 2⁴−1, 2⁴+1}`. Because the kernel dead-set doubles self-similarly (dead mixed boxes cluster at sizes near `2^k`, so the forced child of size `≈ n/2` is dead when `n ≈ 2^{m}±1`), the natural conjecture is that the infeasible squares are exactly `{2^m ± 1 : m ≥ 3}` — i.e. `{7, 9, 15, 17, 31, 33, …}`. This is stated as a conjecture; `n=31,33` were not verified (their block searches exceed the exhaustive budget). **The verdict does not rest on the conjecture** — the single exhaustive `n=7` result is sufficient.

### Why curve 19 fails where curve 0 (Hilbert) succeeds

Hilbert (curve 0) generalizes to all squares because it is corner→corner and *self*-similar: at odd `n` its own recursion places its four sub-Hilberts under morphisms **two of which transpose** (its `LL`/`LR` rules are `((0,1),(1,0))` and `((0,-1),(-1,0))`), so a mixed box can always be routed onto a transposing quadrant where it becomes the *good* aspect. Curve 19's four morphisms are **all non-transposing**, so it can never re-aspect a mixed child: a tall-by-one box stays tall-by-one for the kernel, and lands on a cell of the dead-set. Feasibility is therefore *not* predicted by endpoint type (curve 4 is corner→interior yet generalizes as a standalone square curve) but by whether the curve's morphisms can transpose forced mixed children onto a live kernel aspect.

## Quasi-squares

`fill(19,·)` on quasi-squares `|w−h|=1`, best over the full local swap space, depends only on whether the **top orientation transposes** (all four non-transposing orientations behave identically; all four transposing ones behave identically — as forced by the symmetry of Lemma 1):

```
non-transposing top orientation {e, reflect-x, reflect-y, rot180}:
   WIDE  w=h+1:  3x2:Y  4x3:Y  5x4:N  6x5:Y  7x6:Y
   TALL  h=w+1:  2x3:Y  3x4:N  4x5:Y  5x6:Y  6x7:N
transposing top orientation {main-diag, rot90, anti-diag, rot270}:
   WIDE  w=h+1:  3x2:Y  4x3:N  5x4:Y  6x5:Y  7x6:N
   TALL  h=w+1:  2x3:Y  3x4:Y  4x5:N  5x6:Y  6x7:Y
```

The two orientation classes realize **complementary** quasi-square sets (transposing = the transpose of non-transposing), and neither realizes all sizes. The dead cells here (`3×4`, `5×4` at non-transposing orientations) are precisely the kernel dead quasi-squares of Lemma 1 propagated to the top level, and they are the same cells that kill the odd squares `n=7` (`3×4`) and `n=9` (`5×4`). Relation to the primitive constraint: the base dominoes are `1×2` (orientations A,C) and `2×1` (orientations B,D); Lemma 1 is the recursive lift of this dichotomy to the interior kernels 0 and 4 — each kernel behaves as a "macro-domino" that can only be entered/exited along one aspect, so odd-side splitting, which always manufactures one box of each aspect, cannot satisfy a non-transposing parent.

## Evidence

Commands run (engine `research/aep.py`, `.venv/bin/python`):

- **Structure.** `aep.RULES[19]` → the four rules above; `aep.orientations_used(19)` → 9 nodes at `sizes=range(3,12,2)` `{(19,IDENT), (0,·)×6, (4,·)×2}`; `aep.entry_exit(19)` → `('interior','interior')`. Bases are curves 0 and 4.
- **Full per-orientation rule space over `n=1..40`:** the reachable partition-node set (over both split choices) is **11 nodes** — `(19,IDENT)`, curve 0 at all **8** orientations, curve 4 at 2 orientations — so the complete per-orientation space is `9¹¹ = 31 381 059 609`. Orientation-*independent* search (kernels fixed at `0:(first,first)`, `4:(second,first)`): `0/9` valid on `n=1..40`. Reduced joint search (curve 0 pinned to `(first,first)`, curve 4 ×2 and curve 19 free): `0/729` (`9³`). First/second-only per-orientation over the 9 `orientations_used` nodes: `0/262144` (`4⁹`). Randomized full-space (`9⁹` restricted to those nodes): `0/400000` samples. All empty.
- **Headline exhaustive proof.** `n=7` full node set is 4 nodes → space `9⁴ = 6561`; **exhaustive test returns 0 valid.** Per-split decomposition shows a dead `(3,4)` kernel child in every one of the 4 top-splits.
- **Kernel Lemma 1.** Canonical fillability tables for curves 0 and 4 (above), each cell decided exhaustively over all 9 swaps (or over the block's full sub-node space).
- **Corroborating infeasibility.** `n=9` (`(5,4)` dead child, each child block exhaustively dead over `9³`–`9⁴`), `n=15` (`(7,8)`), `n=17` (`(9,8)`).
- **Feasible sizes / hilbertplot match.** `n∈{1..6,8}` valid (exhaustive over their node sets); `n=4,8` reproduce `hilbertplot.curve(19)` up to symmetry (`canonical_form` equality) with the inert swap.
- **Quasi-square probe.** Table above, per top orientation, over local swap search.

## Open questions

- **Prove the `2^m ± 1` classification.** Establish rigorously that the kernel dead-set contains exactly the mixed boxes forcing infeasibility at `n = 2^m ± 1` (verify `n=31,33` and give a self-similarity induction on the kernel fillability tables). Current status: `{7,9,15,17}` proven, pattern conjectured.
- **Determine `n ∈ {10,11,12,13,14,16}`.** These odd/even sizes have no forced-dead child; feasibility then hinges on the LL→UL→UR→LR junction chain, not tested here. (Immaterial to the impossibility verdict.)
- **Rectangles.** The kernel fillability tables (Lemma 1) already characterize which `w×h` rectangles each kernel admits; a full rectangle theory for curve 19 would compose these through the non-transposing morphisms.
- **Structural theorem.** These results support the synthesis conjecture: *a curve generalizes to all squares iff its quadrant morphisms can transpose every forced mixed child onto a live kernel aspect.* Curve 19 fails this (all morphisms non-transposing, kernels dead on the forced aspect); Hilbert passes it.

## Verification

**Verdict: CONFIRMED.** Independent, skeptical re-run of the engine reproduces every load-bearing claim; the impossibility verdict is airtight.

### What was re-run (engine `research/aep.py`, `.venv/bin/python`)

1. **Node enumeration is complete (not trusted from the report).** Instrumented `fill(19,·)` with a probe swap that *records* every `(index,M)` pair actually consulted. At `n=7` exactly **4** nodes are queried — `(19,IDENT), (0,IDENT), (4,reflect-y), (4,rot180)` — matching the report. Since a swap function's signature is `swap(index,M)` and `fill` consults it only at these 4 nodes, the space of *distinct behaviors* at `n=7` is exactly `9⁴=6561`. This closes the only real loophole (a hidden node would have made `9⁴` non-exhaustive); it does not exist.

2. **Headline exhaustive search.** Full `9⁴=6561` sweep over the 4 nodes: **valid = 0**. Confirmed. Because any square-universal rule restricts to one of these 6561 behaviors at `n=7`, and all fail, **no swap function (orientation-independent or per-orientation) is valid at `n=7`** — hence none is square-universal. The logic is sound with no gap.

3. **Attempted refutation — did NOT find any working rule.** Beyond the exhaustive `n=7` sweep (the strongest possible refutation attempt), I also fully exhausted `n=9`: its complete node set is **6** nodes (`9⁶=531441` behaviors), **valid = 0**. This is *stronger* than the report, which only argued `n=9` via per-split decomposition — I confirm it by full-square exhaustion. No rule works for either. Refutation failed on the merits.

4. **Feasible sizes confirmed.** Exhaustive per-`n` search shows a valid rule *exists* for each `n∈{1,2,3,4,5,6,8}` (valid counts 1,1,3,9,72,243,6561 respectively), consistent with the report — these are per-`n` existence, not a common rule, as the verdict requires.

5. **Lemma 1 kernel-fillability tables** reproduced cell-for-cell by exhaustive box search, *including* the asymmetry between curve 0 and curve 4 at `W6/W7`. The four forced-dead mixed boxes `(3,4),(5,4),(7,8),(9,8)` are confirmed dead (no swap valid) for **both** kernels.

6. **2^k match** confirmed via `canonical_form` equality at `k=1,2,3` (`n=2,4,8`): `fill(19,·)` with the inert swap equals `hilbertplot.curve(19)`.

7. **Quasi-square table** reproduced exactly for both a non-transposing top orientation (IDENT) and a transposing one (main-diagonal), including all four `N` cells.

### Assessment of the impossibility argument

The verdict rests on a single exhaustive fact (`n=7`, `9⁴`, zero valid) plus a trivial, correct restriction argument — it does **not** depend on Lemma 1, the `2^m±1` conjecture, or the per-split narrative, all of which are nonetheless independently verified here. The `2^m±1` classification remains an explicitly-labeled conjecture (the report is careful about this) and the verdict does not lean on it. No logical gap found. The impossibility is **confirmed for squares** (rigorously at `n=7` and `n=9` by full exhaustion of the complete swap space; the general claim that curve 19 admits *no* connected arbitrary-square generalization follows from `n=7` alone).
