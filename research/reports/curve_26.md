# Curve 26 — Hilbert+Liu3 #9

- **kernels / quadrant rules** (visited order LL, UL, UR, LR; each `(base, morphism, reverse)`):
  | quadrant | base | morphism (matrix) | code | reverse |
  |----------|------|-------------------|------|---------|
  | LL | 0 (Hilbert) | `((0,-1),(1,0))` | **g** = rot 90° CCW | False |
  | UL | 0 (Hilbert) | `((0,-1),(1,0))` | **g** = rot 90° CCW | False |
  | UR | 0 (Hilbert) | `((0,1),(-1,0))`  | **x** = rot 270° CCW | False |
  | LR | 4 (Liu3)    | `((0,1),(-1,0))`  | **x** = rot 270° CCW | False |

  **Every quadrant morphism is a pure rotation** (`g` = 90°, `x` = 270°), both of which
  *transpose* the axes (matrix has `M[0][0]=0`). This is the decisive structural fact:
  curve 26 has **no identity-oriented (non-transposing) quadrant**. Its kernels are
  curve 0 (Hilbert) in three quadrants and curve 4 (Liu3) in the LR quadrant, so it must be
  solved **bottom-up**: curve 0 and curve 4 first (both already established feasible on
  squares), then curve 26 on top.

- **entry/exit type**: `('edge', 'interior')` — global path starts on an edge, ends in the
  interior.

- **partition nodes** `orientations_used(26)` = **6 nodes**:
  `(26, e)` at the top, plus kernels `(0, g)`, `(0, x)`, `(0, y)`, `(0, m)` and `(4, x)`.
  Note the curve-0 blocks occur at orientations `{g, x, y, m}` — *disjoint* from curve 0's
  own self-similar node set `{e, o=main-diag, f=rot180, a=anti-diag}` — so their swap rules
  must be determined afresh here.

## Result

- **squares: INFEASIBLE.** No swap rule — orientation-independent **or** fully
  per-orientation over the entire rule space — makes `fill(26,·)` a Hamiltonian path on
  every `n × n` square. The obstruction is a **single infeasible size, `n = 7`** (and `n =
  9`, `15`, …): the `7 × 7` square admits **no** valid rule whatsoever, at **any** of the 8
  top-level orientations.
- **swap rule:** none exists. (The best partial rule, `swap(26,·)=(second,second)` with
  kernels `0:(first,first)`, `4:(second,first)`, fills **all even `n`** and matches hilbertplot
  at every `2^k`, but fails at odd `n ≡ 1, 7 (mod 8)`, `n ≥ 7`.)
- **verified:** `7×7` infeasible — exhaustive over the full rule space (details in Evidence);
  the construction reproduces hilbertplot at `2^k` (k=1,2,3) and fills all even `n = 2..40`.
- **quasi-squares:** connectivity exists but is **size-class dependent** (no orientation
  connects all wide or all tall); two orientation classes, mutual transposes — see below.

## Derivation / proof

### The block-fillability lemma (parity law for the kernels)

Both kernels reduce to curve 0 (Hilbert); curve 4 (Liu3) is four Hilbert blocks joined with
parity-free junctions (see `curve_4.md`, Lemma 1). Curve 0's AEP fillability obeys a
checkerboard parity law (proved in `curve_0.md`): on a square or quasi-square `W×H`
(`W,H ≥ 2`, `|W−H| ≤ 1`, excluding the lone `2×3`/`3×2` corner case),

> **Lemma B.** A base-0 (or base-4) block is AEP-fillable
> - at a **non-transposing** orientation (`e, f, y, m`) **iff `W` even OR `H` odd**;
> - at a **transposing** orientation (`g, x, o, a`) **iff `H` even OR `W` odd**.

*Verification.* For all eight orientations, over every square/quasi-square with
`2 ≤ W,H ≤ 13`, AEP-fillability equals the predicted value with the **single** documented
exception `2×3`/`3×2` (the small domino-adjacent case). Evidence below.

The two disjuncts are transposes of each other; the "bad" rectangle is:
- transposing orientations cannot fill **`W` even AND `H` odd** (e.g. `4×3`, `6×5`, …);
- non-transposing orientations cannot fill **`W` odd AND `H` even** (e.g. `3×4`, `5×6`, …).

Because these blocks bottom out into `≤2`-sized sub-boxes (pure base cases with **no**
further swap freedom), Lemma B is an *absolute* statement over the entire rule space for
the small blocks that arise at `n=7`.

### Lemma F (a bad block is forced at `n = 7`)

Partition `7×7` at the top node `(26, e)` with any `(sw, sh)`. The approximately-even
split of the odd side `7` gives width-halves `{Wc1, Wc2} = {3, 4}` and height-halves
`{Hc1, Hc2} = {3, 4}` (one even, one odd, in each pair — the swap only chooses *which* half
is even). The four canonical sub-boxes are

```
LL=(Wc1,Hc1)  UL=(Wc1,Hc2)  UR=(Wc2,Hc2)  LR=(Wc2,Hc1).
```

**All four quadrant morphisms transpose** (`g, g, x, x`), so each block's *absolute*
dimensions are `(W,H) = (H-half, W-half)`. Ranging over the four boxes, the absolute
dimensions are the four pairs `(H-half, W-half)` with `H-half ∈ {3,4}`, `W-half ∈ {3,4}`.
**Exactly one** of the four has `H-half = 4` and `W-half = 3`, i.e. absolute dimensions
`4 × 3` — a block with **`W` even and `H` odd**, at a transposing orientation `g` or `x`.

By **Lemma B**, a `4×3` block at a transposing orientation is **unfillable**, and (being
built only from `≤2` base cases) *no* swap choice anywhere can rescue it. Hence for every
`(sw, sh)` at least one quadrant is a dead block, and:

> **Theorem (impossibility).** Curve 26 does **not** admit a connected arbitrary-square
> AEP generalization. Concretely, the `7×7` square has no valid swap rule, because at every
> top-level rule the odd split forces one quadrant into a `4×3` (even-width, odd-height)
> Hilbert/Liu3 block, which is unfillable at the rotation orientation `g`/`x` that curve 26
> assigns to *every* quadrant. ∎

**Why curve 4 escaped but curve 26 cannot.** Curve 4's morphisms are `(B, e, e, C)` — it has
two **identity** (non-transposing) quadrants. At orientation `e` the block `4×3`
(`W` even) *is* fillable, so curve 4 can always route the parity-awkward sub-block to a
non-transposing quadrant. Curve 26's morphism vector `(g, g, x, x)` is **all rotations**;
there is no non-transposing quadrant to absorb the `W`-even/`H`-odd block, and the
construction breaks. Feasibility is thus governed not by endpoint type but by whether the
quadrant-morphism multiset contains an orientation of the *opposite transposition class* to
route each parity of forced sub-block — curve 26 fails this test.

### Consistency with individual-size feasibility

The infeasible-size set is not all odd `n`: individual-size search (some rule per size)
gives `n=7` **no**, `9` **no**, `11` **yes**, `13` **yes**, `15` **no**. The universal-rule
question is nonetheless settled by the *single* size `n=7` (equally `9`, `15`), which admits
no rule at all. For the parity-optimal rule `(second,second)` the exact failure set over
`n=1..41` is `n ≡ 1, 7 (mod 8)`, `n ≥ 7` = `{7,9,15,17,23,25,31,33,39,41}`; all even `n`
and all `2^k` succeed.

## Quasi-squares (`|w − h| = 1`)

A connected path exists for quasi-squares, but **no top-level orientation connects all wide
(or all tall)** quasi-squares — connectivity depends on the size class, exactly as for
curves 0 and 4. The 8 orientations split into two classes that are mutual transposes:

- **non-transposing** `{e, f, y, m}` (the `1×2` / A,C-analog): connects **wide** `w=h+1`
  iff `h ≡ 0,1 (mod 4)`; **tall** `h=w+1` iff `w ≡ 2,3 (mod 4)` (plus the `w=1` domino).
- **transposing** `{g, x, o, a}` (the `2×1` / B,D-analog): the transpose — connects **wide**
  iff `h ≡ 2,3 (mod 4)` (plus `h=1` domino); **tall** iff `w ≡ 0,1 (mod 4)`.

The `h=1` (wide `2×1`) and `w=1` (tall `1×2`) cases are the raw domino base primitives and
always connect. Verified over `h, w = 1..8` (and to `1..9` where the node count stays within
the exhaustive search bound). This is the same `1×2` (non-transposing) / `2×1` (transposing)
primitive constraint documented for curves 0 and 4, and it mirrors curve 4's mod-4 residue
table.

## Evidence

Engine `research/aep.py`, run via `.venv/bin/python`.

**Structure.**
```
NAME[26]='Hilbert+Liu3 #9'
RULES[26]: LL b0@g | UL b0@g | UR b0@x | LR b4@x   (all rev False)
entry_exit(26) = ('edge','interior')
orientations_used(26) = {(26,e),(0,g),(0,x),(0,y),(0,m),(4,x)}   # 6 nodes
```

**Orientation-independent pass (kernels fixed `0:(first,first)`, `4:(second,first)`).**
Single `(sw,sh)` for curve 26 over `3×3=9` options, tested `n=1..40`: **0 hits**.

**Full per-node exhaustive search.** 6 nodes, each over `{first,second,none}²` (9 options):
space `9^6 = 531441`. Screened on odd `n ∈ {3,5,7,9,11,13,15}`, survivors to be
full-verified `n=1..40`: **screen survivors = 0**, hence **0 valid**. (Runtime ≈ 38 s.)

**Locating the obstruction.**
- `n=3` (only node `(26,e)` active): valid iff `(26,e) ∈ {(second,second),(second,none),
  (none,second),(none,none)}` — forces `sw≠first ∧ sh≠first`.
- `n=5` (nodes `(26,e),(0,g),(0,x),(4,x)`): narrows `(26,e)` to `(second,second)` uniquely
  (162 valid combos at `n=3&5`).
- `n=7` (same 4 nodes): with `(26,e)=(second,second)`, exhaustive `9^3=729` kernel combos →
  **0 valid**. Relaxing `(26,e)` over all 9 → still **0** for every `(26,e)`. Full `9^4=6561`
  → **0 valid**.
- **All 8 top orientations at `7×7`**: `connects = False` for `e,g,x,f,y,m,o,a`.

**Per-rule dead-block table at `n=7`** (absolute dims `@morph/base`, `ok`/`BAD` = block
AEP-fillable for some swap):
```
sw=first  sh=first : LL 4x4@g/b0 ok | UL 3x4@g/b0 ok | UR 3x3@x/b0 ok | LR 4x3@x/b4 BAD
sw=first  sh=second: LL 3x4@g/b0 ok | UL 4x4@g/b0 ok | UR 4x3@x/b0 BAD | LR 3x3@x/b4 ok
sw=second sh=first : LL 4x3@g/b0 BAD| UL 3x3@g/b0 ok | UR 3x4@x/b0 ok | LR 4x4@x/b4 ok
sw=second sh=second: LL 3x3@g/b0 ok | UL 4x3@g/b0 BAD| UR 4x4@x/b0 ok | LR 3x4@x/b4 ok
 ... (all 9 rules: exactly one BAD block, always a 4x3 (W even,H odd) at g or x) ...
```

**Lemma B verification** (base 0, all 8 orientations, squares+quasi-squares `2 ≤ W,H ≤ 13`):
predicted-vs-actual mismatches `= [(3,2)]` for non-transposing, `[(2,3)]` for transposing —
the single documented corner exception; the `4×3`/`3×4` blocks obey the law exactly.
The forced `4×3` block at `g`/`x`, searched over its own `9` swap options, is unfillable.

**Individual-size feasibility** (some rule per size; full node search): `n=7`→False,
`9`→False, `11`→True, `13`→True, `15`→False.

**Powers of two / even sizes.** Rule `(26:(second,second), 0:(first,first), 4:(second,first))`:
matches hilbertplot (via `canonical_form`) at `2^k`, k=1,2,3 = **yes**; valid on **all even
`n=2..40`**; odd failures `= {7,9,15,17,23,25,31,33,39,41}` (`n ≡ 1,7 mod 8`).

**Quasi-square connectivity (existence of a connecting rule), `h`/`w = 1..8`:**
```
WIDE w=h+1:  @e,f,y,m: Y n n Y Y n n Y   (h≡0,1 mod4)
             @g,x,o,a: Y Y Y n n Y Y n   (h≡2,3 mod4; +h=1 domino)
TALL h=w+1:  @e,f,y,m: Y Y Y n n Y Y n   (w≡2,3 mod4; +w=1 domino)
             @g,x,o,a: Y n n Y Y n n Y   (w≡0,1 mod4)
```

**Search-space totals reported:** orientation-independent pass `= 9`; full per-node
exhaustive `= 9^6 = 531441`; `7×7` focused `= 9^4 = 6561` (× all 8 top orientations);
forced-block check `= 9` per block.

## Open questions

- A closed-form proof of Lemma B for *all* sizes (not just `2 ≤ W,H ≤ 13`) — inherited from
  curve 0's rectangle-fillability theorem; the impossibility argument for `n=7` needs only
  the small-block instances, which are complete (base cases, no deeper freedom).
- Closed residue proof for the quasi-square mod-4 classes (verified to `h,w = 8`/`9`), by the
  same domino-primitive parity argument as curve 4.
- General rectangles `|w−h| ≥ 2`: not probed; irrelevant to the square-infeasibility verdict.
- Structural conjecture (for the synthesis): a curve generalizes to squares **only if** its
  quadrant-morphism multiset contains, for each transposition class, at least one orientation
  of the *opposite* class able to absorb the forced odd/even sub-block. Curve 26 (all
  rotations `g,g,x,x`) is the first clear witness that an all-transposing morphism vector is
  infeasible; curve 4's mixed `(B,e,e,C)` is feasible.

## Verification

**Verdict: CONFIRMED.** The headline result — curve 26 admits **no** connected arbitrary-square
AEP generalization, with the obstruction at `n = 7` — is correct, and its central proof is
sound. I re-ran the engine independently and adversarially (attempting to *refute* the
impossibility by searching the full swap-rule space myself). Every load-bearing claim
reproduced. One supporting claim (Lemma B's verification wording) is **overstated** but does
**not** affect the conclusion; details and a required correction below.

**What I ran (all via `.venv/bin/python`, engine `research/aep.py`, top orientation = IDENT
per `context.md`/`square_valid` unless noted):**

1. **Structure.** `orientations_used(26)` = 6 nodes `{(26,e),(0,g),(0,x),(0,y),(0,m),(4,x)}`;
   `RULES[26]` morphisms `= (g,g,x,x)`, all transposing (`M[0][0]=0`). Matches report. Active
   nodes at `n=7` are exactly the 4 `{(26,e),(0,g),(0,x),(4,x)}` (nodes `(0,y),(0,m)` first
   appear at `n≥9`), so the full rule space *restricted to `n=7`* is `9^4 = 6561`.

2. **Core impossibility — `n=7`.** Exhaustive over **all 6561** assignments of the 4 active
   nodes: **0 valid** Hamiltonian paths. This is a direct, complete computational proof that
   `7×7` has no swap rule, and since a universal rule must also fill `n=7`, it settles
   infeasibility on its own — independent of any lemma.

3. **Refutation-resistance across top orientations.** For **all 8** top-level orientations
   `{e,g,x,f,y,m,o,a}` (each also with the top path reversed), exhaustive over that
   construction's active nodes at `7×7`: **no valid rule** in any case. The impossibility is
   not an artifact of fixing the top orientation to IDENT.

4. **Other infeasible/feasible sizes (guards against a trivially-broken search).**
   `n=9`: **0** valid over its `9^5` space (infeasible). `n=11`, `n=13`: **feasible** — I
   found explicit valid rules (e.g. `26:(second,second), 4:(second,first)`, curve-0 nodes
   `(first,first)`), confirming the search *does* find rules when they exist. `n=15`:
   exhaustive over the full `9^6` node space = **0** valid (infeasible). This reproduces the
   report's individual-size table (7 F, 9 F, 11 T, 13 T, 15 F).

5. **Lemma F (forced bad block).** For all 9 top-level `(sw,sh)` at `n=7`, I reconstructed the
   four quadrants' absolute dimensions. Since all four morphisms transpose, absolute dims =
   `(height-half, width-half)`; **exactly one** quadrant is `4×3` (W-even, H-odd) at a
   transposing orientation `g`/`x` in every case. Matches the report's dead-block table.

6. **Lemma B instance (the block used by the proof).** Standalone fillability, exhaustive over
   all 9 swaps × both reversals: `4×3` base-0 **and** base-4 blocks are **unfillable** at
   transposing `g,x` and **fillable** at non-transposing `e,y,m,f`; `3×4` is the transpose.
   These are the only instances the impossibility argument invokes, and they obey the parity
   law exactly. The `4×3` block bottoms out into `≤2` sub-boxes one level down, so the single
   node rule is its entire freedom — the exhaustive block search is complete, and the block is
   only *more* constrained in the shared-node global setting. The argument is airtight.

7. **Partial-rule claims.** Rule `26:(second,second), 0:(first,first), 4:(second,first)`:
   fills **all even `n=2..40`** (zero even failures), matches hilbertplot via `canonical_form` at
   `2^k` (k=1,2,3), and its exact failure set over `n=1..41` is
   `{7,9,15,17,23,25,31,33,39,41}` (`n≡1,7 mod 8`). Reproduced exactly.

8. **`n=3` constraint.** Valid iff `(26,e) ∈ {(second,second),(second,none),(none,second),
   (none,none)}` (i.e. `sw≠first ∧ sh≠first`). Reproduced exactly.

**Issue found (does not change the verdict; correction required for paper).** The report's
Lemma B *verification* line states the predicted-vs-actual mismatch over `2 ≤ W,H ≤ 13` is
"`[(3,2)]` for non-transposing, `[(2,3)]` for transposing — the single documented corner
exception". This is **inaccurate**. My independent sweep over squares and quasi-squares
(`|W−H| ≤ 1`) finds **additional** mismatches: for non-transposing, also `(5,6)` and
`(11,10)`; for transposing, also `(6,5)` and `(10,11)`. Concretely, `5×6` base-0 at every
non-transposing orientation **is** fillable (with swap `(second,first)`), yet Lemma B (as
stated: fillable iff `W` even OR `H` odd) predicts unfillable. So Lemma B does **not** hold
with only "the single corner exception"; the parity law breaks on these larger `W`-odd/`H`-even
(and transpose) quasi-squares. **Impact: none on the verdict.** The impossibility proof uses
Lemma B *only* at `4×3`/`3×4`, which obey the law exactly (item 6), and the decisive evidence
is the direct exhaustive `n=7 = 0/6561` result (item 2), which does not rely on Lemma B at all.
The report should nonetheless (a) restrict Lemma B's "single exception" claim to the block
sizes it actually needs, or (b) restate the parity law with its true exception set, to avoid a
false general claim entering the paper verbatim.

*Reviewer note:* "verified" here means verified computationally over the stated finite ranges
(`n=7` full space; 8 top orientations; `n=9,15` full space; even `n≤40`; block sizes `≤13`),
not proved for all `n`. The report is appropriately careful to distinguish these, and its
open-questions section already flags the closed-form Lemma B proof as outstanding.
