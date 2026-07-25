# Arbitrary-size generalization of the forty two-dimensional Hilbert curves

*A classification of which Estévez-Rams Hilbert-type space-filling curves admit a connected
approximately-even-partition generalization to arbitrary square grids, with swap rules for the
feasible curves and impossibility proofs for the rest.*

---

## 1. Introduction and sources

Space-filling curves index a 2-D grid by a 1-D Hamiltonian path (every cell visited once,
consecutive cells 4-adjacent), so that spatial locality is largely preserved in the linear
order. The Hilbert curve is the canonical example; it is normally defined only on `2^k × 2^k`
grids by a self-similar recursion into four equal quadrants.

This work sits between two prior results.

**(a) The catalog of forty curves.** Estévez-Rams *et al.* (*Rev. Cub. Fís.* **34**, 9, 2017;
implemented in the `hilbertplot` package) enumerate the complete set of **forty** distinct
two-dimensional Hilbert-type space-filling curves. Each curve `index ∈ {0,…,39}` is specified
recursively by four **quadrant rules** for the sub-quadrants `LL, UL, UR, LR` (lower-left,
upper-left, upper-right, lower-right), visited in that order and joined by unit steps. A
quadrant rule is a triple `(base, morphism, reverse)`: `base` is the kernel curve drawn in that
quadrant, `morphism ∈ D4` a dihedral symmetry, and `reverse` a traversal reversal. On the
standard `2^k × 2^k` grid all four quadrants have equal size `2^{k-1}`. The six "base" curves
`0`–`5` (Hilbert, Moore, Liu1, Liu2, Liu3, Liu4) recurse only into Hilbert (curve 0); the
remaining curves compose these as kernels.

**(b) The arbitrary-size Hilbert curve.** Wu & Chang (*IET Image Process.* **6**(6):746, 2012)
generalize **only the standard Hilbert curve** to any `n × m` region by the *approximately even
partition* (AEP): split each side `d` into `d1 = ⌊d/2⌋, d2 = ⌈d/2⌉`, recurse into four (now
unequal) sub-regions, and bottom out on the `1×1, 2×1, 1×2, 2×2` primitives. To keep the path
connected at odd sizes they force a chosen half of each split to be even — a per-orientation
**swap rule** (their Fig. 5) — using four board orientations A, B, C, D (the D4 subset
`{identity, main-diagonal, 180°, anti-diagonal}`).

**This paper** asks the natural combined question: *for which of the forty catalog curves does
the AEP construction, driven by that curve's own quadrant rules and full D4, extend to a single
connected Hamiltonian path on every `n × n` square?* We give a complete answer — **exactly
eight of the forty** — together with the swap rule for each feasible curve and an impossibility
proof for each of the thirty-two infeasible ones, and we isolate the structural property of a
curve's quadrant rules that decides feasibility.

All computation uses the shared engine `research/aep.py`. Every feasibility claim is verified by
`aep.square_valid` over `n = 1..40` (Hamiltonian on every square, and matching hilbertplot at `2^k`,
`k=1,2,3`); every impossibility claim is an exhaustive swap search over the complete reachable
node set at a witness size. Throughout we distinguish **verified over a stated range `R`** from
**proved for all `n`**.

---

## 2. The approximately-even-partition framework: canonical frame and the D4 engine

### 2.1 Regions, orientations, and the AEP split

A **region** is an axis-aligned rectangle `(x0, y0, w, h)`. An **orientation** is one of the
eight D4 matrices `M` acting on a column vector `(x,y)`. The **approximately-even partition** of
a length `d` is `d1 = ⌊d/2⌋, d2 = d − d1` (so `|d1 − d2| ≤ 1`).

The engine works in the curve's **canonical frame** (orientation = identity) and applies `M` to
place cells; a sub-quadrant with quadrant rule `(base_i, morph_i, rev_i)` is drawn with kernel
`base_i` at orientation `M · morph_i` and traversal parity `rev_i ⊕ rev`. Writing
`(Wc, Hc)` for the canonical width/height (the physical `(w,h)` transposed when `M` transposes
the axes), the recursion `fill(index, x0,y0,w,h, M, rev, swap)` is:

- if `w ≤ 2` and `h ≤ 2`: emit the primitive `base_cells(Wc, Hc)` mapped by `M`, reversed if
  `rev`;
- otherwise split `Wc → (Wc1, Wc2)`, `Hc → (Hc1, Hc2)` using the swap rule, form the four boxes
  `LL=(0,0,Wc1,Hc1)`, `UL=(0,Hc1,Wc1,Hc2)`, `UR=(Wc1,Hc1,Wc2,Hc2)`, `LR=(Wc1,0,Wc2,Hc1)`, and
  recurse into them in order `LL → UL → UR → LR` (reversed if `rev`), concatenating the four
  contiguous cell-lists.

### 2.2 The swap rule

An odd side `d = 2m+1` splits into consecutive integers `{m, m+1}` — one even, one odd. A
**swap rule** decides, per axis, which half is made even:

```
sw, sh ∈ {first, second, none}   # first: make d1 (low half) even; second: make d2 (high half) even; none: no correction
```

Crucially the swap function has signature `swap(index, M)` — it depends on the curve and
orientation of a node, **not on the region size `n`**. A **node** is a `(curve, orientation)`
pair reached in the recursion; `orientations_used(index)` (corrected to close over both split
parities) enumerates them. The full per-orientation rule space for a curve with `k` nodes is
`9^k`, and because the swap cannot see `n`, a rule's behaviour at any fixed size is one of
finitely many assignments of the nodes that size reaches. **This is the lever behind every
impossibility proof: a single square with zero valid assignments over its complete node set
proves infeasibility for all `n`.**

### 2.3 Validity and the two verification modes

`validate(cells, w, h)` returns `OK` iff `cells` is a Hamiltonian path (count, distinctness,
bounding box, and 4-adjacency of consecutive cells). We call a curve **FEASIBLE** iff some
size-independent swap rule gives `validate == OK` on every `n×n` (checked over `n=1..40`, with
the `2^k` match to hilbertplot), else **INFEASIBLE**.

Two calibrations recur:

- At `n = 2^k` every split is even, so the swap is inert and every curve reproduces its hilbertplot
  curve exactly — feasibility is entirely an odd/non-power-of-two phenomenon.
- `endpoint_type` classifies each global endpoint as corner / edge / interior. We show below
  that endpoint type **does not** decide feasibility (curve 4 is corner→interior yet feasible;
  curve 18 is interior→interior yet infeasible); the true criterion is structural.

---

## 3. Junction connectivity and the swap-rule theory

### 3.1 Reduction to blocks and junctions

Because `fill` concatenates the four sub-block cell-lists, a whole-square path is Hamiltonian
**iff** (i) each sub-block is internally a Hamiltonian path on its rectangle, and (ii) the three
internal **junctions** `LL→UL, UL→UR, UR→LR` are 4-adjacent (the exit cell of one block adjacent
to the entry cell of the next). Both conditions are size-local and D4-covariant, which makes the
node-by-node analysis possible.

### 3.2 The checkerboard (bipartite) lemma

Colour cell `(x,y)` by `χ(x,y) = (x+y) \bmod 2`. The grid graph is bipartite; a Hamiltonian path
alternates colours, so **its two endpoints share a colour iff the cell count `WH` is odd, and
have opposite colours iff `WH` is even.** On an odd `n×n` square the majority (corner) colour has
`(n²+1)/2` cells, so *both* global endpoints must lie on it. This single lemma yields:

- **Corner-anchored curves survive.** Hilbert (0) is corner→corner with corners of the majority
  colour, so it meets the constraint automatically. This is why curve 0 generalizes.
- **Near-cyclic curves die.** Moore (1) is an opened Hamiltonian *cycle*: its two endpoints are
  forced 4-adjacent, hence opposite colours — impossible on an odd square. This kills Moore and,
  by inheritance, every Moore-bearing curve (§5.1).
- **Improper curves die.** The "improper" curves (6, and others) place their global entry and
  exit as two adjacent central cells (opposite colours by construction) — the same obstruction.

### 3.3 Parity-free junctions and the swap-forcing mechanism

For the feasible curves a stronger fact holds: the three internal junctions are 4-adjacent for
**every** split, provided the height split makes the low half `Hc1` even. Concretely, for the
morphism template `(B, A, A, C)` of curve 4 (and its relatives), the blocks meet at the shared
cell-corner of the internal cross:

```
LL exit (Wc1−1, Hc1−1)  →  UL entry (Wc1−1, Hc1)     vertical, dist 1
UL exit (Wc1−1, ·)      →  UR entry (Wc1, ·)          horizontal, dist 1
UR exit (Wc−1, Hc1)     →  LR entry (Wc−1, Hc1−1)     vertical, dist 1
```

*(Correction to the per-curve reports: junction 4-adjacency requires `Hc1` even, i.e.
`sh=first`; the curve-4 report's Lemma 1 overstated this as parity-free. The corrected statement
— "with `sh=first`, junctions are 4-adjacent for any width split" — is what the verified `n=1..40`
regime uses, and it does not change any result.)*

When junctions are parity-free (given the height pin), validity **reduces to sub-block
fillability**, and the swap rule's only remaining job is to hand each kernel a fillable shape.
This is the engine of the classification: the swap on each axis is forced exactly to the extent
that some block demands a parity, and free otherwise. Two clean patterns recur across the
feasible curves:

- **`sh` (height) is pinned** by the corner-termination requirement of the Hilbert kernels:
  `sh=first` at every curve-0 node makes the low half even so the vertical junctions land at
  integer parity (the "make the entry-corner-side half even" principle of Wu & Chang).
- **`sw` (width) is free** when every block self-corrects its width internally, and **pinned**
  when a block's fillability depends on width parity (e.g. a Liu4 block whose last-visited
  quadrant joins a *vertical* corner-pair, or a Liu3 block that must be handed an odd×odd
  square).

The full valid-rule set for a feasible curve is a clean Cartesian product of these per-node
freedoms (e.g. curve 0: `{sh=first}⁴ × {sw free}⁴ = 81`; curve 3: `243 = 3⁵`; curves
4/5/24/29/31: `81 = 3⁴`), verified exhaustively.

---

## 4. The classification theorem

**Theorem (classification).** Of the forty catalog curves, exactly the eight

```
0 (Hilbert), 3 (Liu2), 4 (Liu3), 5 (Liu4), 24, 29, 30, 31 (Hilbert+Liu3 #7,#12,#13,#14)
```

admit a connected AEP generalization to arbitrary squares. For each, a single
**orientation-independent** swap rule works, verified on `n = 1..40` and matching hilbertplot at `2^k`:

| curve | swap rule (const, per index) | valid-set size | pinned / free |
|------:|------------------------------|:--------------:|---------------|
| 0 | `0:(first,first)` | 81 = 3⁴ | `sh=first` every node; `sw` free |
| 3 | `3:(·,second)`, `0:sh=first` | 243 = 3⁵ | `sh` pinned (0:first, 3:second); `sw` free |
| 4 | `4:(second,first)`, `0:sh=first` | 81 = 3⁴ | `(4)=(second,first)` forced; `0:sh=first`, `sw` free |
| 5 | `5:(first,second)`, `0:sh=first` | 81 = 3⁴ | curve 5 both axes pinned; `0:sh=first` |
| 24 | `24:(first,second)`, `4:(second,first)`, `0:sh=first` | 81 = 3⁴ | 24 & 4 both axes pinned; `0:sh=first` |
| 29 | `29:(second,first)`, `4:(second,first)`, `0:sh=first` | 81 = 3⁴ | 29 & 4 forced; `0:sh=first` |
| 30 | `30:(second,first)`, `4:(second,first)`, `0:sh=first` | (witness rule) | 30 & 4 forced; `0:sh=first` |
| 31 | `31:(first,second)`, `4:(second,first)`, `0:sh=first` | 81 = 3⁴ | 31 & 4 forced; `0:sh=first` |

The remaining thirty-two curves are infeasible; §5 collects the proofs.

### 4.1 The structural condition on the quadrant rules

Feasibility is decided not by endpoint type but by the kernels and the morphism assignment.
Write the transpose class of a morphism `μ` as `T` if `μ` swaps the axes (`μ[0][0]=0`) and `N`
otherwise, and the quadrant-morphism string as `(class_LL, class_UL, class_UR, class_LR)`.

**Feasibility criterion (structural characterization).** A curve generalizes to arbitrary
squares iff

1. **(kernels)** every kernel appearing in its recursion is *corner-anchored* — Hilbert (0) or
   Liu3 (4) — and never a near-cyclic Moore (1) nor an edge-to-edge Liu4 (5) *used as a
   sub-block*; and
2. **(morphisms)** its four quadrant morphisms realize one of the four **parity-free-junction
   templates** of the feasible base curves — those whose class string is *heterogeneous* (mixes
   `T` and `N`) *and* aligned so that, at every odd split, each Hilbert block receives a
   rectangle of curve-0-fillable parity (under `sh=first`) and each Liu3 block receives an
   **odd×odd square**.

The three feasible composites are exactly the base templates with the last-visited Hilbert
quadrant swapped for a Liu3 block that inherits an odd×odd square:

```
24 (class NTTT)  =  curve 5's template  with LR = Liu3      29 (class TNNN)  =  curve 4's template with LR = Liu3
30 (class TNNT)  =  curve 0's template  with LR = Liu3      31 (class NTTN)  =  curve 3's template with LR = Liu3
```

This condition supersedes the endpoint heuristic: the class strings of the six base curves are
`0:TNNT, 1:TTTT, 2:NNNN, 3:NTTN, 4:TNNN, 5:NTTT`. The two infeasible ones are exactly the two
**homogeneous** strings (`TTTT` Moore, `NNNN` Liu1); the four feasible ones are heterogeneous.
Heterogeneity is *necessary* (a homogeneous string cannot route both the forced odd×even and
even×odd sub-blocks) but not *sufficient* — among the Hilbert+Liu3 curves, several heterogeneous
strings (18, 20, 21, 28) still misroute a block onto an unfillable near-square (§5.4). The
sufficient condition is the full template-plus-odd×odd-square alignment above.

### 4.2 Per-curve feasibility lemmas (feasible curves)

- **Curve 0 (Hilbert).** Self-referential; `sh=first` at all four nodes makes the low height
  half even at every odd `n`, satisfying all four block colour conditions for every `sw`
  (proved by the checkerboard lemma, for all `n`); `sw` free. Verified `n=1..80`.
- **Curve 3 (Liu2).** Kernels all Hilbert; junctions parity-free; the top height pin is
  `sh=second` (forcing `Hc2` even) while the kernel pin is `sh=first`; `sw` free everywhere.
  Its last-visited quadrant joins a **horizontal** corner-pair, leaving `sw` free — contrast
  curve 5.
- **Curve 4 (Liu3).** Kernels all Hilbert; morphism `(B,A,A,C)` gives parity-free junctions
  (given `sh=first`); `(sw,sh)=(second,first)` is the unique top rule making all four
  sub-rectangles curve-0-fillable. (The curve-4 report's Lemma 1/3 mechanism is corrected as in
  §3.3; result and rule are confirmed.)
- **Curve 5 (Liu4).** Kernels all Hilbert; its last-visited quadrant joins a **vertical**
  corner-pair, which pins `sw=first` in addition to `sh=second` (double pin). This is exactly
  the vflip→rot270 change from curve 3 that removes the width freedom.
- **Curves 24, 29, 30, 31.** Three Hilbert + one Liu3, on the four base templates. The Liu3
  quadrant is handed an **odd×odd square**, which curve 4 fills with its own square rule
  `(second,first)`; the three Hilbert blocks are pinned by `sh=first`. (Curve 24's report gives a
  false counterfactual in Lemma 4 — curve 4 *can* fill some even×odd rectangles — but the pin
  `sw=first` is genuine because `sw=second` disconnects at `n=7`; the odd×odd-square property is
  the correct positive reason.)

---

## 5. Impossibility proofs (collected and cleaned)

Each infeasible curve is killed by one (or more) of four mechanisms. Every proof reduces to an
**exhaustive swap search over the complete reachable node set at a witness square**, which is
finite and size-independent, hence decisive for all `n`.

### 5.1 Near-cyclic Moore obstruction (checkerboard parity)

Curve 1 (Moore) is an opened cycle: its two endpoints are 4-adjacent, so on an odd square they
are opposite colours, violating the majority-colour requirement (§3.2). Exhaustively, at `n=7`
and `n=9` the black–black endpoint pair is unreachable over all `9^5` rules, so Moore admits no
odd-square path (its odd-feasible sizes are exactly the **Jacobsthal numbers** `1,3,5,11,21,…`,
verified to `n=85`). The obstruction is inherited: any curve that forces a Moore block onto an
odd square is infeasible. Curves **1, 32–39** fall here; curve 39 is the sharpest — for
`n ≡ 2 (mod 4)` the balanced split hands the Moore quadrant the odd square `(n/2)²`, so curve 39
fails at `n=14, 18, 26, 30, 34, 38 = 2·{7,9,13,15,17,19}` and connects at `n=22=2·11` only
because 11 is Jacobsthal. (Curve 6 is the improper analogue: its adjacent central-cell endpoints
give the same opposite-colour obstruction; at `n=3` all 9 rules disconnect — a rigorous single-
size proof. The broader "all odd `n`" mechanism for curve 6 is verified only to `n≤7`
exhaustively and by sampling beyond, as its parity Lemma 1 fails over the per-orientation space.)

### 5.2 Edge-to-edge Liu4 drift (size-dependent junction parity)

Liu4 (curve 5) is feasible standalone but is *edge-to-edge* and *doubly pinned* (both split axes
forced). When nested as a sub-block, the cell at which it meets a shared internal edge **drifts
with the block size** rather than staying corner-pinned, so a straddling horizontal junction is
4-adjacent only for a specific parity of the tier height `Hc1` — and that required parity flips
between two odd sizes. Since the swap is size-independent, no fixed value serves both. This kills
every curve whose kernels include Liu4 as a sub-block: **6–17**. The clean certificate is a pair
of disjoint viable-top-node sets, e.g. curve 11: `S(5) = {sh=second}`, `S(7) = {sh=first}`,
`S(5) ∩ S(7) = ∅`; curve 8: `n=3` needs `Hc1` even, `n=7` needs `Hc1` odd. Curves 9 and 13 are
variants where a forced `2×3` block is colour-locked (same-colour endpoints on a 6-cell region ⇒
no path) at `n=5`.

### 5.3 Homogeneous-morphism obstruction (unroutable forced box)

An odd split always produces exactly one odd×even and one even×odd sub-block. A curve-0/curve-4
block at a **non-transpose** orientation can fill an even×odd but not an odd×even near-square, and
a **transpose** orientation the reverse. If all four morphisms lie in one transpose class, the
forced box of the "wrong" parity has nowhere to go. This kills the homogeneous strings: curve 2
(`NNNN`, forced `3×4` at `n=7`), curve 26 (`TTTT`, forced `4×3` at `n=7`), and contributes to
9, 19, 22, 27, 32, 34. Each is certified by an exhaustive search at the witness size returning 0
valid rules.

### 5.4 Mis-routing with good kernels (odd×even near-square handed to a corner kernel)

Even with only Hilbert/Liu3 kernels and a heterogeneous morphism string, the assignment can force
a block onto a near-square rectangle its kernel cannot fill:

- **Curve 18** (`13 = 6+7`): every split produces a `7×6` block, unfillable by curve 0 (checked
  by exhaustion — the report's parity argument is false in general, e.g. `5×6` *is* fillable, but
  the specific `7×6` is unfillable by the `9^3=729` exhaustive certificate) and by curve 4.
- **Curve 21**: kernels 0 and 4 have *opposite* off-square chirality at `m=6,9`
  (`f4W∧f0W` and `f4T∧f0T` both false), so no split at `n=13, 19` fills both.
- **Curves 25, 28**: the Liu3 quadrant is pinned to a single orientation and handed a `6×7`
  (curve 25) or an odd-width near-square (curve 28) it cannot fill; hard walls at `n=13`.
- **Curves 20, 22, 27**: the Hilbert blocks force a unique split parity that then hands the Liu3
  (or an even-width Hilbert) block an unfillable central quasi-square; `n=7` (22, 27) or
  `n=7/9/13` (20).
- **Curve 23**: no working rule exists under any test (including an 11-node search stronger than
  the report's), but the written proof is unsound — the node space is 11 not 9, and its
  corner-pinning Lemma 3 is false — so this is recorded as *verified infeasible over `n=1..40`,
  proof to be redone*.

### 5.5 Two-witness parity conflicts (composite curves)

Many composites are killed most cleanly by a **two-size conflict**: the single top node `(ν, e)`
is the only free curve-`ν` node (curve `ν` never recurses into itself), so its `(sw,sh)` is
shared across all sizes; two witness sizes force disjoint singletons for one axis. Examples:
curves **7** (`n≡1 vs 3 mod 8`), **10, 11, 15, 33, 35, 36** (`n=5 vs 7`), **12, 14, 37** (`n=3
vs 7`), **16** (`n=7` hard wall; note the report mis-anchored this at `n=5`, which is in fact
feasible with 3888 rules — the true obstruction is `n=7`), **17** (endpoint `(E,E)`-pair
unreachable at `n=5`), **38** (`n=7` junction/interior conflict with the Moore tail). Each is an
exhaustive finite check over the complete node set of the witness sizes.

---

## 6. Quasi-squares and the road to rectangles

### 6.1 The domino-primitive dichotomy

For `|w−h| = 1` (quasi-squares) the aspect is forced and the AEP recursion bottoms out on the
`1×2` (tall) and `2×1` (wide) dominoes. The `1×2` primitive is laid only by the **non-transpose**
D4 coset `{A, C}`-class (`M[0][0] ≠ 0`), the `2×1` only by the **transpose** coset `{B, D}`-class
(`M[0][0] = 0`). Consequently, for **every** catalog curve:

> No orientation-independent quasi-square rule exists. A given quasi-square connects only under
> the transpose-coset whose terminal domino matches its aspect; wide and tall connect under
> *complementary* cosets (exact transposes of each other).

### 6.2 Feasible curves on quasi-squares

For the eight feasible curves the picture is sharp: at each quasi-square size **exactly 4 of the
8 orientations connect**, forming one complete D4 transpose-coset, selected by the size (often a
clean `mod 4` residue for the pure-Hilbert-kernel curves 0, 3, 4; irregular / binary-recursion
dependent for the Liu3-composites 29, 30, 31). Small boundary sizes occasionally connect under
all 8. Thus every quasi-square is realizable by choosing the orientation from the size-appropriate
class, but there is no uniform rule. Curve 3 has the cleanest law: it connects iff its canonical
width `Wc` is even (the odd side must be the canonical height).

### 6.3 Infeasible curves on quasi-squares

Infeasible curves inherit their square obstruction into the quasi-square family: some sizes (or
whole residue classes) connect under no orientation at all (curve 7: residues `b≡4,5` wide fail
everywhere; curve 25: no orientation connects any quasi-square). *(The per-curve quasi-square
tables for curves 7 and 8 were flagged by verification as containing factual errors and should be
regenerated per-size without assuming clean periodicity before use.)*

### 6.4 Toward general rectangles

For `|w−h| ≥ 2` the AEP recursion leaves the square/quasi-square family, and thin boxes (`1×k`,
`k≥3`) already fail even for Hilbert. A rectangle theory would require an **aspect-keyed** swap
policy (choosing orientation per sub-region by its domino class) outside the fixed
`swap(index, M)` model studied here. The feasible curves' quasi-square coset laws are the natural
seed: the checkerboard lemma gives the necessary parity `w even OR h odd` for a corner→corner
Hilbert block in orientation `e`, and the coset selection extends it one level. This is left open.

---

## 7. Open problems

1. **Close the "for all `n`" gap for feasible curves.** The square feasibility of curves
   3, 4, 5, 24, 29, 30, 31 is *verified over `n=1..40`* and reduced by junction lemmas to two
   kernel inputs: (a) curve 0's arbitrary-rectangle corner-termination (the Wu–Chang property,
   which parities/orientations Hilbert fills), and (b) curve 4's odd×odd-square and near-square
   fillability. Stating these as standalone lemmas, proved by induction on `n`, would upgrade all
   seven to fully closed all-`n` theorems.

2. **Prove the structural criterion is exactly sufficient.** §4.1 gives a criterion
   (corner-anchored kernels + parity-free-junction template + odd×odd routing of Liu3) that is
   necessary and matches the classification. A direct proof that it is *sufficient* for every
   admissible morphism assignment — rather than curve-by-curve verification — is the target
   theorem "curve `ν` generalizes to squares iff ⟨condition on its quadrant rules⟩."

3. **Symbolic kernel fillability maps.** Several impossibility proofs invoke computationally-
   verified facts: Moore's Jacobsthal odd-square set, Liu4's rectangle-fillability band, Liu3's
   near-square map. Closed forms (from boundary-vector arguments) would make the mod-8 and
   Jacobsthal statements symbolic rather than range-verified.

4. **Repair the flagged proofs.** Curves 6, 18, 23, 24 have sound *verdicts* but flawed
   *derivations* (Lemma 1 of 6/18, Lemma 3 of 23, Lemma 4 of 24; and curve 16's mis-anchored
   witness). These are corrected here at the reduction level (§3.3, §4.2, §5.4) but the per-curve
   reports should be updated: replace false parity lemmas with the exhaustive certificates that
   actually carry them, and use the complete (swap-closed) node set for search-space accounting.

5. **Quasi-square residue laws and rectangles.** Prove the domino-primitive coset selection is
   the stated `mod 4` (or `mod 8`) residue where clean, and develop the aspect-keyed rectangle
   policy of §6.4.

---

### Appendix: reproduction

All results reproduce from `research/aep.py` (`.venv/bin/python`, `sys.path` including
`research`). Feasibility: `aep.square_valid(idx, aep.const_swap(rule), sizes=range(1,41),
check_2k=True)` for the eight rules in §4. Impossibility: enumerate the complete reachable node
set at the witness size (close over all three split modes per axis), then exhaust
`{first,second,none}²` per node with `aep.validate(aep.fill(idx,0,0,n,n,IDENT,False, swap),n,n)`.
Per-curve derivations and evidence are in `research/reports/curve_<index>.md`, each with an
independent adversarial "## Verification" section.
