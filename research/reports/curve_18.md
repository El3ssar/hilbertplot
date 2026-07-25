# Curve 18 — Hilbert+Liu3 #1

- **kernels / quadrant rules** (visited order LL, UL, UR, LR; each `(base, morphism, reverse)`):
  - LL: `(4, ((0,1),(-1,0)),  rev=True)`   — curve 4 (Liu3), rotated, reversed
  - UL: `(0, ((1,0),(0,1)),   rev=False)`  — curve 0 (Hilbert), identity
  - UR: `(0, ((1,0),(0,1)),   rev=False)`  — curve 0 (Hilbert), identity
  - LR: `(4, ((0,-1),(-1,0)), rev=False)`  — curve 4 (Liu3), rotated

  The quadrant bases are `{4, 0, 0, 4}`: curve 18 is built from **curve 4 (Liu3)** on the
  LL/LR quadrants and **curve 0 (Hilbert)** on the UL/UR quadrants. Curve 18 never appears
  inside itself, so in the partition it occurs only as the top-level node at `id`; every
  deeper node is curve 0 or curve 4, and curve 4's own bases are all curve 0. The kernels to
  solve first are therefore **curve 0**, then **curve 4** (both established feasible on
  *squares*: curve 0 with `(first,first)`, curve 4 with `(second,first)`).
- **partition nodes** — `aep.orientations_used(18)` together with the full closure over both
  approximately-even split parities gives **11 nodes**:
  `(18, id)`; `(4, ·)` at the 2 orientations `{((0,-1),(-1,0)), ((0,1),(-1,0))}`;
  `(0, ·)` at **all 8** D4 orientations. (Below the top two levels the tree is pure curve 0.)
- **entry/exit type**: `('interior', 'interior')` — both endpoints interior. (For a *square*
  this imposes no corner constraint, so endpoint type again does not settle feasibility.)

## Result

- **squares: INFEASIBLE.** No swap rule — orientation-independent **or** per-orientation over
  the 11 partition nodes — makes `fill(18, ·)` a Hamiltonian path on every `n × n` square.
- **swap rule**: **none exists.** The obstruction is unconditional (independent of any rule).
- **obstruction**: the **7 × 6 rectangle**. Curve 18's approximately-even partition forces a
  `7 × 6` sub-box at `n = 13`, and neither kernel (curve 0 at UL/UR, curve 4 at LL/LR) can
  fill a `7 × 6` rectangle under any swap rule. Hence the `13 × 13` square has no valid rule.
- **verified**:
  - **`n = 13` is unfillable by *any* rule** — proved below (four-way split certificate) and
    confirmed by direct search: random sampling over `9^10` for the 13×13 node set found no
    valid assignment; the four-case certificate is exhaustive.
  - **Exhaustive corroboration**: the full per-orientation rule space, `9^11`, is soundly
    reduced to `3^4 · 6^6 = 3 779 136` candidate assignments that *provably contain every
    solution* (see §Evidence); an exhaustive pass over all of them found **0** assignments
    valid on `n = 1..40`. The best assignment reaches only `n = 1..12` (max first-fail = 13).
  - Individually, `n = 3, 5, 7, 9, 11` are feasible and so are `n = 15, 17`, but **`n = 13`
    is individually infeasible** — the obstruction is a specific bad size, not a monotone
    cutoff. Because a generalization must hold on *every* square, `n = 13` alone refutes it.
  - matches hilbertplot at `2^k`: N/A (no valid rule exists).
- **quasi-squares** (`|w−h| = 1`): also **not** uniformly feasible; see §Quasi-squares.

## Derivation / proof

Write the top-level partition of curve 18 on `n × n` at orientation `id` with width split
`(w1, w2)` and height split `(h1, h2)` (`{w1,w2}` and `{h1,h2}` the two approximately-even
halves, chosen by the swap rule). The four sub-boxes and their kernels are

```
LL = (0,  0,  w1, h1) : curve 4 @ ((0,1),(-1,0))  rev      UL = (0,  h1, w1, h2) : curve 0 @ id
UR = (w1, h1, w2, h2) : curve 0 @ id                        LR = (w1, 0,  w2, h1) : curve 4 @ ((0,-1),(-1,0))
```

visited LL → UL → UR → LR. A necessary condition for the whole path to be Hamiltonian is
that **each sub-box is itself internally fillable** by its kernel (a broken sub-box breaks
the whole path regardless of the junctions). The proof shows a sub-box is forced onto an
unfillable shape.

### Lemma 1 (Curve 0 cannot fill an odd × even rectangle corner-to-corner)

In the AEP construction curve 0 (Hilbert) enters at the corner `(0,0)` and exits at the
opposite bottom corner `(w−1, 0)` (verified: exit `= (w−1,0)` on every fillable box). Colour
the grid as a checkerboard `χ(x,y) = (x+y) mod 2`. A Hamiltonian path on a `w × h` board has
its two endpoints on **opposite** colours iff the area `wh` is **even** (and on the same
colour iff `wh` is odd). The two bottom corners satisfy
`χ(0,0) = 0`, `χ(w−1,0) = (w−1) mod 2`, i.e. they are the **same** colour exactly when `w` is
**odd**. Combining:

> curve 0 fills `w × h` corner-to-corner ⟹ `(w odd) ⟺ (wh odd)`.
> This fails precisely when **`w` is odd and `h` is even**.

So curve 0 (identity) cannot fill any odd-width, even-height rectangle. In particular it
cannot fill **`7 × 6`** (`χ(0,0)=χ(6,0)=0`, but area `42` is even → endpoints must differ):
`fillable(0, id, 7, 6)` = **False** over `9^3 = 729`, while `fillable(0, id, 6, 7)` = **True**
(exit `(5,0)`, colour 1, opposite — consistent). The asymmetry `7×6` ✗ vs `6×7` ✓ is exactly
this parity relation.

### Lemma 2 (Curve 4 cannot fill 7 × 6 at either orientation used)

At the LL and LR positions curve 4 is placed at `((0,1),(-1,0))` (reversed) and
`((0,-1),(-1,0))`. Exhaustive search over each `7×6` curve-4 subtree (`4` nodes, `9^4 = 6561`
rule assignments) gives **0** valid fillings at both orientations:
`fillable(4, ((0,1),(-1,0)), 7, 6, rev)` = `fillable(4, ((0,-1),(-1,0)), 7, 6)` = **False**.
(Unlike Lemma 1, the two-colouring of curve 4's fixed corner→interior endpoints *can* be made
opposite, so this is not the simple parity clash; it is a boundary-vector incompatibility of
curve 4's recursive endpoint structure with the `7×6` shape — certified exhaustively.) By
contrast `7 × 7` and `6 × 7` are curve-4-fillable, so the obstruction is specific to the
odd-wide `7 × 6` shape.

### Theorem (Curve 18 does not generalize to arbitrary squares)

Consider `n = 13`. Its two approximately-even halves are `{6, 7}` (`13 = 6 + 7`). Whatever the
swap rule, `(w1,w2) ∈ {(6,7),(7,6)}` and `(h1,h2) ∈ {(6,7),(7,6)}`, so the four sub-boxes
`(w1,h1),(w1,h2),(w2,h2),(w2,h1)` are exactly the four combinations `{6,7} × {6,7} =
{6×6, 6×7, 7×6, 7×7}` — a `7 × 6` box is **always present**, only its position among
(LL,UL,UR,LR) changes with the split parity:

| split `w=(w1,w2)`, `h=(h1,h2)` | box that is `7×6` | its kernel | fillable? |
|---|---|---|---|
| `w=(6,7), h=(6,7)` | LR `(w2,h1)=(7,6)` | curve 4 `@((0,-1),(-1,0))` | **No** (Lemma 2) |
| `w=(6,7), h=(7,6)` | UR `(w2,h2)=(7,6)` | curve 0 `@id`               | **No** (Lemma 1) |
| `w=(7,6), h=(6,7)` | LL `(w1,h1)=(7,6)` | curve 4 `@((0,1),(-1,0))`  | **No** (Lemma 2) |
| `w=(7,6), h=(7,6)` | UL `(w1,h2)=(7,6)` | curve 0 `@id`               | **No** (Lemma 1) |

In every case a sub-box is a `7 × 6` block handed to curve 0 or curve 4, which cannot fill it
(Lemmas 1–2). Therefore `fill(18, 13, 13, ·)` contains an internally broken sub-box for **every**
swap rule, so no rule yields a Hamiltonian path on the `13 × 13` square. Since a valid
arbitrary-square generalization must succeed on *every* `n × n`, **curve 18 admits none.** ∎

**Mechanism in one line**: curve 18 mixes two corner-anchored kernels whose recursive endpoints
force parity/boundary constraints; the approximately-even split of `13 = 6+7` unavoidably
produces a `7 × 6` (odd-wide, even-tall) sub-box, and that shape is unfillable by both kernels
— by a checkerboard parity contradiction for curve 0 and by a boundary-vector obstruction for
curve 4.

### Why the feasible curves escape and 18 does not

Curve 0 and curve 4 generalize to *squares* because their swap rule can keep every sub-box a
**square or 6×7-type (even-wide) rectangle**, avoiding odd×even boxes at their corner-to-corner
kernels. Curve 18's fixed morphism assignment `(4@rot, 0, 0, 4@rot)` gives it no split that
avoids the odd-wide box at `n = 13`: the two kernels demand *opposite* aspect parities at the
same junctions, so no single split satisfies both. This is the "contradictory parity demands at
two junctions on the same split" obstruction anticipated in the study brief.

## Quasi-squares (`|w − h| = 1`)

Curve 18 is **not** uniformly feasible on quasi-squares either. Testing all 8 top-level D4
orientations for existence of *some* swap rule (small sizes):

- **Non-transposing orientations** (`M[0][0] ≠ 0`, e.g. `id`): wide `w=h+1` connects for
  `h = 2,3,5` but **fails at `h = 4`** (the `5×4` box — odd-wide even-tall again); tall
  `h=w+1` connects for `w = 2,4,5` but **fails at `w = 3`**.
- **Transposing orientations** (`M[0][0] = 0`): the wide/tall pattern is exactly transposed —
  wide fails at `h = 3`, tall fails at `w = 4`.

So for each orientation there are quasi-square sizes with no valid rule; the failures are the
same odd×even-rectangle obstruction seen at the smallest scale. This ties to the primitive
domino constraint: a tall `1×2` region admits only orientations `{A, C}` and a wide `2×1`
region only `{B, D}`, and curve 18's kernels inherit that aspect-parity split — wide and tall
quasi-squares connect under *complementary* orientation classes, never simultaneously under
one, and never for all sizes. (Verified for the sizes probed; the smallest failing box is the
same `odd × even` shape of Lemma 1.)

## Evidence

Engine: `research/aep.py`, run via `.venv/bin/python`. All validity via `aep.validate`.

- **Partition nodes** — closure over both split parities for `n = 1..40`, top curve 18:
  `18@id`; `4@{((0,-1),(-1,0)),((0,1),(-1,0))}`; `0@` all 8 D4 orientations = **11 nodes**.
  `RULES[18] = [(4,((0,1),(-1,0)),True),(0,id,False),(0,id,False),(4,((0,-1),(-1,0)),False)]`.
- **Unfillability certificates** (exhaustive over each box's own subtree):
  - `curve0 @id  7×6` : nodes 3, space `9^3=729`, valid = **0** → UNFILLABLE.
  - `curve0 @id  6×7` : space `729`, valid = **27** → FILLABLE (asymmetry, Lemma 1).
  - `curve0 @id  7×7` : valid = **81** → FILLABLE.
  - `curve4 @((0,1),(-1,0)) 7×6 (rev)`  : nodes 4, space `9^4=6561`, valid = **0** → UNFILLABLE.
  - `curve4 @((0,-1),(-1,0)) 7×6`        : space `6561`, valid = **0** → UNFILLABLE.
  - `curve4 @((0,1),(-1,0)) 7×7` : valid = **162** → FILLABLE.
- **Curve-0 parity check** (Lemma 1) — entry `(0,0)`, exit `(w−1,0)`:
  `7×6`: colours `(0,0)` area even → need opposite, have same → **CONTRADICTION**;
  `6×7`: colours `(0,1)` → opposite → OK; `3×4`: same → CONTRADICTION; `4×3`: opposite → OK.
- **`n = 13` four-way split certificate** (`scratchpad/obstruction.py`): for each of the 4
  approximately-even splits, an unfillable sub-box is exhibited (table above);
  "Every split leaves an unfillable sub-box: **True**".
- **Individual-size feasibility** (random search over the size's node set, `9^{10..11}`):
  `n = 3,5,7,9,11` feasible; **`n = 13` infeasible** (no hit in 8·10^5 samples, and proved
  above); `n = 15` feasible (hit at try 304), `n = 17` feasible (try 12).
- **Exhaustive search of the full rule space (corroboration)** — sound reduction of `9^11`:
  1. The 4 "early" nodes `{18@id, 0@id, 4@((0,-1),(-1,0)), 4@((0,1),(-1,0))}` are forced to
     `sh = first`: brute over the full `9^4` for `n ≤ 8` leaves **exactly 81** assignments,
     all with `sh = first` (3 choices of `sw` each ⇒ `3^4 = 81`). Node `18@id` fills a `3×3`
     at `n = 3`, forcing `sh18 = first`; this cascades.
  2. The 6 "late" curve-0 nodes (the rotated orientations, first appearing at `n = 9`) each
     provably receive a single-node `3×2` or `2×3` box under **every** one of the 81 early
     survivors, on which only `sw ∈ {second, none}` is valid (`sw = first` excluded). Hence
     `6` options each. This reduces the search to `3^4 · 6^6 = 3 779 136` assignments that
     contain *all* solutions.
  3. Exhaustive pass over all `3 779 136`: **0** valid on `n = 1..40`; the maximum first-fail
     reached is **13** (some rule is valid on `n = 1..12`).
- **Search-space totals reported**: orientation-independent first pass `= 9` (0 valid, first
  fail `n = 3` or `11`); full per-orientation space `= 9^11 ≈ 3.1·10^10`, soundly reduced to
  and exhausted at `3 779 136` (0 valid); the `n = 13` impossibility is settled independently
  by the 4-split × exhaustive-subbox certificate (`4 × (729 or 6561)` sub-fills).

## Verification (adversarial, independent)

Re-ran the engine from a scratch script (`sys.path.insert(0,"research"); import aep`), mirroring
`fill()`'s decomposition exactly. **Verdict: NEEDS-WORK** — the *conclusion* (curve 18 is
INFEASIBLE on squares, obstruction at `n = 13`) is **confirmed and rigorously certified**, but
**Lemma 1 as stated is false** and its parity argument does not prove what it claims.

### Confirmed
- `RULES[18] = [(4,((0,1),(-1,0)),True),(0,id,False),(0,id,False),(4,((0,-1),(-1,0)),False)]`,
  `entry_exit(18) = ('interior','interior')`. ✓
- **7×6 unfillability certificates** (exhaustive over each kernel's own subtree, free endpoints):
  `curve0@id 7×6` = **0**/729; `curve0@id 6×7` = **27**; `curve0@id 7×7` = **81**;
  `curve4@((0,1),(-1,0)) 7×6 rev` = **0**/6561; `curve4@((0,-1),(-1,0)) 7×6` = **0**/6561;
  `curve4@((0,1),(-1,0)) 7×7 rev` = **162**. All match the report exactly. ✓
- **`n = 13` four-way certificate (corrected, complete).** For **all 9** top-node `(sw,sh)` options
  at `18@id` (not just the 4 in the report's table), exactly one sub-box is a physical **7×6**
  handed to curve 0@id or curve 4@rot, which is internally unfillable. Since `fill()` emits each
  sub-box as a contiguous block, an internally-unfillable sub-box makes the whole path invalid
  regardless of junctions. Hence **no** rule fills `13×13`. ✓ (One caveat: an early version of my
  own checker mis-computed absolute sub-box dims using the *child* orientation instead of the
  *parent*; corrected to match `fill()` — parent-`M` transpose — every top-split leaves a 7×6.)
- **Direct refutation attempt.** Randomized search for *any* per-orientation rule valid on `n×n`:
  `n = 3,5,7,9,11` each found a valid rule within ~9k tries; **`n = 13` found none in 40 000 tries.**
  Consistent with the impossibility. I could not refute the conclusion.
- Because a square generalization must hold on *every* `n`, `n = 13` alone settles it: **INFEASIBLE**. ✓

### Error found in the derivation (Lemma 1)
Lemma 1 asserts: *"curve 0 (Hilbert) enters `(0,0)` and exits `(w−1,0)` on every fillable box"* and
concludes *"curve 0 cannot fill **any** odd-width even-height rectangle."* **Both are false.**
- Counterexample: **`curve0@id 5×6` is fillable** (5 odd, 6 even), with entry `(0,0)` and exit
  **`(4,1)`** — colour 1, *opposite* to `(0,0)`, area 30 even → a perfectly valid Hamiltonian path,
  no parity contradiction. So the exit is **not** pinned to `(w−1,0)`, and the checkerboard argument
  does not apply to it. Verified valid via `aep.validate`.
- Over odd×even boxes the pattern is **irregular**, not uniformly "unfillable": `3×4` ✗, **`5×6` ✓**,
  `7×6` ✗, `9×6` ✗, `5×4` ✗, `3×8` ✗. Lemma 1 predicts all ✗; `5×6` refutes it.

Consequence: Lemma 1's parity "proof" that `7×6` is unfillable is **invalid** (it rules out only
fills that exit at `(w−1,0)`; curve 0 can exit elsewhere). The *fact* that `7×6` is unfillable is
nonetheless **true** — but it is established solely by the **exhaustive certificate** (0/729), which
the report also reports, not by the parity argument. The theorem does not depend on Lemma 1's false
generality (it uses the free-endpoint "internally fillable at all" necessary condition, correctly
certified exhaustively), so **the impossibility conclusion stands**. But the report must:
1. **Retract** the general claim "curve 0 cannot fill any odd×even rectangle" (5×6 is a counterexample);
2. **Remove or repair** the pinned-exit premise `(w−1,0)`; the parity argument, as written, proves
   nothing about `7×6` because the exit is free. Rely on the exhaustive 7×6 certificate instead
   (as already done in §Evidence), and treat the curve-0 case as an exhaustive certificate on the
   same footing the report already grants curve 4's Lemma 2.

Lemma 2 (curve 4, `7×6` unfillable) is an honest exhaustive certificate and reproduced fine. The
"mechanism in one line" and the "contradictory parity demands" narrative rest on Lemma 1 and should
be re-derived once Lemma 1 is fixed.

### Bottom line
Computational check **passes** (all certificates reproduced; `n=13` impossible by a sound, complete
four-way argument). The stated **Lemma 1 is mathematically wrong** (false general claim + invalid
parity proof), even though its needed instance (`7×6` unfillable) is true by exhaustion. Result =
**confirmed**; derivation = **needs correction**. Overall: **needs-work**.

## Open questions

- **Closed form for curve 4's `7×6` obstruction (Lemma 2).** Curve 0's part is a clean
  two-colouring argument; curve 4's is currently an exhaustive certificate. A boundary-vector
  lemma (curve 4's corner→interior endpoint-displacement parity vs. an odd-wide even-tall box)
  should close it analytically, mirroring Lemma 1.
- **General classification.** Lemma 1 gives a candidate structural criterion: a curve fails to
  generalize to squares if its fixed morphism assignment forces some corner-anchored kernel
  onto an `odd × even` rectangle at some `n`. Curve 18 is the first studied curve where the
  two kernels' aspect-parity demands are irreconcilable. Whether this criterion is also
  *sufficient* (i.e. characterizes exactly the infeasible curves) is open.
- **All-`n` statement.** Impossibility is proved outright via the single square `n = 13`
  (sufficient to refute the generalization). The stronger claim that curve 18 fails on
  infinitely many / a positive density of sizes is supported by the exhaustive `n = 1..40`
  search (max reachable `n = 12`) but not separately proved.
- **General rectangles `w × h` (`|w−h| ≥ 2`)** not probed here; Lemma 1 already forbids all
  `odd × even` boxes for the curve-0 blocks.
