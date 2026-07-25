# Curve 2 — Liu1

- **kernels / quadrant rules** (visited order LL, UL, UR, LR; each `(base, morphism, reverse)`):
  - LL: `(0, C = 180° ((-1,0),(0,-1)), rev=False)`
  - UL: `(0, A = identity ((1,0),(0,1)), rev=False)`
  - UR: `(0, A = identity ((1,0),(0,1)), rev=False)`
  - LR: `(0, C = 180° ((-1,0),(0,-1)), rev=False)`

  Every quadrant base is **curve 0 (Hilbert)**. Curve 2 never appears inside itself, so in the
  partition it occurs only as the top-level node at orientation `A = identity`; all deeper nodes
  are curve 0. The kernel to solve first is therefore curve 0 (its established square rule is used
  below). The morphism string is **`(C, A, A, C)`** — crucially, *all four* morphisms are
  **non-transpose** (each fixes the coordinate axes; `M[0][0] ≠ 0`). This is the single fact that
  makes curve 2 infeasible (contrast curve 4, whose string `(B, A, A, C)` contains the transpose
  `B`).
- **entry/exit type**: `('interior', 'interior')` — curve 2 starts and ends in the interior.
  (Endpoint type does *not* by itself predict feasibility, but here both endpoints being interior
  is consistent with the failure being internal rather than at a junction.)

## Result

- **squares: INFEASIBLE.** No swap rule — not the 9 orientation-independent options, and not any
  of the `9^5 = 59049` per-orientation assignments over the full partition-node set — makes
  `fill(2, ·)` a Hamiltonian path on every `n × n` square. The obstruction already appears at
  **n = 7**: *every* one of the 59049 assignments fails there (reason: `disconnected`).
- **swap rule**: none exists.
- **verified**: exhaustively searched the full rule space (see §Evidence). Per-size winner counts
  over the full `9^5` space: `n=3: 6561`, `n=5: 5832`, `n=7: 0`, `n=9: 0`, `n=11: 18`, `n=13: 0`,
  `n=15: 0`. Because a universal square rule must work at **every** n simultaneously, and n = 7 has
  **zero** valid assignments, no such rule can exist. Curve 2 **does** reproduce hilbertplot's `2^k` curve
  for k = 1,2,3,4 (powers of two use only even splits, so the swap is irrelevant there) — but that
  is the only regime in which it is reliably connected.
- **quasi-squares** (`|w−h| = 1`): also not uniformly feasible; only the smallest ones connect, and
  only under an aspect-matched orientation class (see §Quasi-squares).

## Derivation / proof (impossibility)

Write the top-level partition of curve 2 on an `n × n` square at orientation `A`. With
`d1 = ⌊d/2⌋, d2 = d − d1` and a swap choice per axis, the four sub-boxes (canonical frame) are

```
LL = (0,   0,   Wc1, Hc1) @ C       UL = (0,   Hc1, Wc1, Hc2) @ A
UR = (Wc1, Hc1, Wc2, Hc2) @ A       LR = (Wc1, 0,   Wc2, Hc1) @ C
```

visited LL → UL → UR → LR, each a curve-0 (Hilbert) block. `fill` assigns to each sub-box a
*contiguous segment* of the output list containing exactly that box's `w·h` cells. The impossibility
below needs only this one structural fact — **no junction analysis is required**: if some sub-box
admits no Hamiltonian sub-path, then the segment of the output covering that box's cells cannot be
internally 4-connected, so the whole output is not a Hamiltonian path (it fails `disconnected`),
*for every swap*. (Empirically the three internal junctions are moreover adjacent for all swaps at
the relevant sizes n = 5,7,9 — LL@C exits its top edge into UL@A's bottom-left, etc. — so the break
is always the internal one, matching the failure reason `disconnected` at n = 7 across all 59049
assignments. This mirrors curve 4's junction structure but is not load-bearing here.)

### Lemma A (Hilbert corner-coloring obstruction)

Curve 0 (Hilbert), filled with `rev = False`, has a **fixed entry** at the image of local `(0,0)`
and — on the rectangles that arise here — a **forced exit at the opposite corner of the same
horizontal edge**. Concretely (verified exhaustively over all sub-orientation swaps, `9^4 = 6561`
assignments):

- under `A = id` on a `w × h` box the only reachable `(entry, exit)` on `3×4` is `((0,0),(2,0))`
  and on `5×4` is `((0,0),(4,0))` — both endpoints on the bottom edge `y = 0`, at `x = 0` and
  `x = w−1`;
- under `C = 180°` the mirror holds: both endpoints on the top edge, at `x = 0` and `x = w−1`.

Give the grid the checkerboard coloring `χ(x,y) = (x+y) mod 2`. The two horizontal-edge corners
`(0, y₀)` and `(w−1, y₀)` satisfy `χ = y₀` and `χ = (w−1+y₀)`, which are **equal iff `w` is odd**.
A Hamiltonian path on a `w × h` grid (a bipartite graph) has endpoints of **equal** color iff the
number of cells `w·h` is **odd**. Therefore a Hilbert block whose forced endpoints are the two
corners of a horizontal edge admits a valid path **only when [`w` odd ⇔ `w·h` odd]**, i.e. it
**fails exactly when `w` is odd and `h` is even** (with `w ≥ 3`, `h ≥ 4` — the regime where the
exit is pinned to the far corner rather than a mid-edge cell).

Instances (E5): `3×4` and `5×4` are **not** curve-0-fillable under `A` or `C`; whereas `4×3`, `4×4`
(even width), `3×3` (odd cells), `3×2` and `5×6` (exit reaches a mid-edge cell, escaping the pin)
all are. The reachable-exit colors for the killed boxes are `colE = colX = 0` on an even grid — a
direct contradiction (E6).

### Lemma B (an odd×even non-transpose box is forced)

For **odd n**, the AEP halves `{Wc1, Wc2} = {a, a+1}` and `{Hc1, Hc2} = {a, a+1}` (`a = ⌊n/2⌋`)
have one odd and one even member each, regardless of swap. The four quadrants realize **all four**
combinations of `{Wc1,Wc2} × {Hc1,Hc2}`, so **one quadrant is always `(odd width) × (even height)`**.
Because curve 2's morphism string `(C, A, A, C)` is entirely **non-transpose**, *every* quadrant —
including this odd×even one — is a horizontal-running Hilbert block subject to Lemma A. (Curve 4
escapes precisely here: its `B` on LL is a transpose, and its rule steers the odd×even box onto
that transposed block, where curve 0 *can* fill it.)

### Theorem (infeasibility)

At **n = 7** the halves are `{3, 4}`, so Lemma B forces a **`3 × 4`** quadrant onto a non-transpose
Hilbert block, which by Lemma A has **no** Hamiltonian path. Hence no swap rule makes `fill(2, ·)`
valid on the 7×7 square. Exhaustive search confirms: all `9^5 = 59049` per-orientation assignments
fail at n = 7 (reason `disconnected`). Since any universal square rule must in particular succeed at
n = 7, **curve 2 admits no connected arbitrary-square generalization.** ∎

**Remark (which odd n fail).** The forced box is `(odd half) × (even half)`. Feasibility of size n
coincides exactly with curve-0-fillability of that box:
`n=3→1×2 ✓`, `n=5→3×2 ✓`, `n=7→3×4 ✗`, `n=9→5×4 ✗`, `n=11→5×6 ✓`, `n=13→7×6 ✗`, `n=15→7×8 ✗`
— matching the observed winner counts (feasible n = 3, 5, 11; infeasible n = 7, 9, 13, 15). So curve 2
is connected on *some* odd squares but not others; the impossibility of a *universal* rule needs only
one failing size, and n = 7 is the smallest.

## Quasi-squares (`|w − h| = 1`)

Searching, per top-level orientation, whether *some* swap yields a valid path (bases 2..4):

| orientation class | wide `w = h+1` (3×2, 4×3, 5×4) | tall `h = w+1` (2×3, 3×4, 4×5) |
|-------------------|------------------------------|-------------------------------|
| non-transpose `{A, C, σx, σy}` | `Y, Y, .` | `., ., Y` |
| transpose `{B, D, r90, r270}`  | `., ., Y` | `Y, Y, .` |

The transpose orientations swap the wide/tall behaviour of the non-transpose ones, as expected (a
transpose of the board exchanges the two aspects). Reading the non-transpose row: the small wide
quasi-squares `3×2, 4×3` connect but `5×4` breaks — and `5×4` is exactly the odd-width×even-height
box killed by Lemma A. So quasi-squares inherit the same obstruction: connectivity holds only while
the arising `(odd × even)` sub-rectangle stays curve-0-fillable, and there is **no** orientation that
connects all wide (or all tall) quasi-squares. At the coarsest level this mirrors the domino
primitive: a tall `1×2` region admits the `{A, C}` class, a wide `2×1` region the `{B, D}` class
(`fill(2)` on `1×2` = `[(0,0),(0,1)]` under `A,B`; on `2×1` = `[(0,0),(1,0)]`), so the connecting
orientation must be chosen by aspect. This is a verified-over-small-range observation, not a closed
proof.

## Evidence

Engine: `research/aep.py`. All commands via `.venv/bin/python`; scripts in the session scratchpad.

- **Partition nodes** — `aep.orientations_used(2, sizes=range(3,41,2))` returns **5** nodes (stable
  over n = 3..39): `(2, A=id)` and `(0, ·)` at all four axis-orientations `{A=id, B=maindiag,
  C=180, D=antidiag}`. `RULES[2] = [(0,R2,False),(0,id,False),(0,id,False),(0,R2,False)]`;
  `entry_exit(2) = ('interior','interior')`.
- **Orientation-independent search** (9 options, verified n = 1..40): **all fail** — `(first,first)`
  fails first at n = 5, every other option at n = 3.
- **Full per-orientation search** — 5 nodes × `{first,second,none}²` = **`9^5 = 59049`** assignments.
  Per-size valid counts: `n=3: 6561`, `n=5: 5832`, **`n=7: 0`**, **`n=9: 0`**, `n=11: 18`,
  **`n=13: 0`**, **`n=15: 0`**. Total search space explored across the two passes: `9 + 59049`.
- **Failure mode at n = 7** — all 59049 assignments return `disconnected` (never `not distinct`/
  `count`/`bbox`): the break is internal to a sub-block, never at a junction.
- **Forced-box unfillability (Lemma A)** — curve-0 Hamiltonian-path existence, tuning all four
  curve-0 sub-orientation swaps (`9^4 = 6561` each):
  `3×4: id ✗, R2 ✗` · `5×4: id ✗, R2 ✗` · `3×2 ✓` · `3×3 ✓` · `4×3 ✓` · `4×4 ✓` · `5×6 ✓` · `4×5 ✓`.
  Reachable endpoints on the killed boxes: `id 3×4 → ((0,0),(2,0))`, `id 5×4 → ((0,0),(4,0))`, both
  with `colE = colX = 0` on an even-cell grid (impossible).
- **2^k match** — `canonical_form(fill(2, 2^k))` equals `hilbertplot.curve(2).points(k)` and `validate`
  = `OK` for k = 1,2,3,4.

## Open questions

- Lemma A is stated for the box regime `w` odd, `h` even with the exit pinned to the far corner
  (`w ≥ 3, h ≥ 4`); a closed characterization of *when* Hilbert's exit is corner-pinned vs
  mid-edge (explaining `3×2, 5×6` fillable but `3×4, 5×4, 7×6` not) would turn the "Remark" pattern
  of infeasible n into a proved statement `n infeasible ⇔ (odd-half × even-half) box is Hilbert-
  unfillable`. This rests on curve 0's rectangle-fillability theorem.
- Structural characterization for the synthesis: the evidence supports **"a curve whose four
  Hilbert-kernel morphisms are all non-transpose cannot absorb the forced odd×even box and is
  square-infeasible, whereas one transpose morphism (placed on the quadrant receiving that box)
  restores feasibility"** — curve 2 `(C,A,A,C)` vs curve 4 `(B,A,A,C)` is the minimal contrast.
  Confirming this against the other 38 curves is the next step.
- General rectangles `|w−h| ≥ 2` not probed.

## Verification

**Verdict: CONFIRMED.** Independent adversarial re-run of the engine reproduces every load-bearing
number and the impossibility conclusion holds within the study's swap-rule model.

**What I ran** (all via `.venv/bin/python`, `sys.path.insert(0,"research"); import aep`):

1. **Partition-node set.** `orientations_used(2, range(3,41,2))` → exactly **5** nodes: `(2, id)` plus
   curve 0 at all four axis orientations `{id, 180, maindiag, antidiag}`. `RULES[2] =
   [(0,180,F),(0,id,F),(0,id,F),(0,180,F)]`, `entry_exit(2) = ('interior','interior')`. Since curve 0
   is orientation-closed and curve 2 occurs only at the top, these 5 nodes are the **complete** rule
   space; the engine's `swap(index, M)` signature cannot depend on size or position, so `{first,
   second,none}²` per node is exhaustive.
2. **Full `9^5 = 59049` per-orientation search.** Reproduced the per-size valid counts **exactly**:
   `n=3: 6561, n=5: 5832, n=7: 0, n=9: 0, n=11: 18, n=13: 0, n=15: 0`. Because **n = 7 has zero valid
   assignments over the entire rule space**, no universal square rule can exist — this alone is a
   rigorous impossibility proof *within the engine's swap model*, independent of the Lemma A/B
   argument. (n=7's nodes are a subset of the 5, so completeness holds.)
3. **Orientation-independent search (9 options, n = 1..40).** Reproduced: `(first,first)` first fails
   at **n = 5**; all eight other options first fail at **n = 3**.
4. **Lemma A boxes** (curve-0 fillability, searching all `9^4` sub-orientation swaps under
   orientations A and C): reproduced exactly — `3×4: ✗/✗`, `5×4: ✗/✗`, and `3×2, 3×3, 4×3, 4×4, 5×6,
   4×5` all `✓/✓`.
5. **2^k match.** `canonical_form(fill(2, 2^k))` equals `hilbertplot.curve(2).points(k)` with
   `validate = OK` for **k = 1,2,3,4**.

**Attempt to refute (failed).** I searched the full rule space myself rather than trusting the report;
no rule is valid on all sizes (n = 7 forces zero). No swap function expressible in the engine escapes
the obstruction. Refutation attempt unsuccessful.

**Scrutiny of the argument.** Lemma B is sound: for odd n the halves are `{a, a+1}` (one odd, one
even), the four quadrants realize all four `{Wc1,Wc2}×{Hc1,Hc2}` combinations regardless of swap, so a
`(odd width)×(even height)` quadrant always exists; curve 2's all-non-transpose string `(C,A,A,C)`
places it on an A/C Hilbert block. At n = 7 this is the `3×4` box, unfillable by Lemma A — matching the
`disconnected` failure and confirmed by the exhaustive count. The Lemma A checkerboard-coloring
argument is valid *given* its premise (Hilbert's exit is corner-pinned to the far corner of the same
horizontal edge on these boxes), which the report verifies computationally rather than proving in
closed form; the report honestly flags this in Open Questions. This is a caveat on the *general
odd-n characterization*, **not** on the top-line impossibility, which rests only on the exhaustively
verified n = 7 result. No logical gap affects the conclusion.

**Caveat on scope (unchanged from report).** "Impossible" means: no swap rule in the engine's
`swap(index, M)` model. Verified computationally over n up to 15 in the full search and n = 1..40 in
the const search; the impossibility is *proved* (not merely verified over a range) because a single
size (n = 7) with zero valid assignments over the complete rule space suffices.
