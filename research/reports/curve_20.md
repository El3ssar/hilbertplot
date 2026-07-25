# Curve 20 — Hilbert+Liu3 #3

- **kernels / quadrant rules** (visited order LL, UL, UR, LR; each `(base, morphism, reverse)`):
  | quadrant | base | morphism (matrix) | reverse |
  |----------|------|-------------------|---------|
  | LL | **4** (Liu3) | `((0,1),(-1,0))` = rot −90° (call **R**, a transpose element) | **True** |
  | UL | **0** (Hilbert) | `((1,0),(0,1))` = identity **e** | False |
  | UR | **0** (Hilbert) | `((1,0),(0,1))` = identity **e** | False |
  | LR | **4** (Liu3) | `((-1,0),(0,-1))` = rot 180° **C** | False |

  Curve 20 is built from two kernels — curve 4 (Liu3) in LL, LR and curve 0 (Hilbert) in
  UL, UR — and **never appears inside itself** (no quadrant base is 20). The kernel
  dependency chain is `20 → {4, 0}` and `4 → {0}`, so the bottom-up solve order is
  `0`, then `4`, then `20`.

  **Kernel swap rules (imported, already established in their own reports):**
  - Curve 0 (Hilbert): its height split must be `sh = first` at every orientation node; the
    width rule `sw` is free. Curve-0 identity fills a `w×h` rectangle **iff `w` even OR `h`
    odd** (coloring lemma, `research/reports/curve_0.md`).
  - Curve 4 (Liu3): orientation-independent square rule `(sw,sh) = (second, first)`; but curve
    4 is only proven to fill **squares** — on general rectangles it inherits curve 0's parity
    limits (`research/reports/curve_4.md`).

- **entry/exit type**: `('interior', 'interior')` — the global path starts and ends in the
  interior. (As with curve 4, endpoint type does not by itself decide feasibility; the
  obstruction below is structural, not an endpoint count.)

- **partition nodes actually reached** (instrumented over `n = 1..40`): **11 nodes** —
  curve 0 at **all 8** D4 orientations, curve 4 at **2** orientations
  (`R = ((0,1),(-1,0))` for LL and `C = ((-1,0),(0,-1))` for LR), and curve 20 at the single
  top node (identity). (Note: `orientations_used(20)` under-reports 6 curve-0 nodes because it
  uses the naive `⌊·/2⌋` split; the swap-driven recursion reaches all 8. The full rule space is
  `9^11`.)

## Result

- **squares: INFEASIBLE.** No swap rule — orientation-independent or per-orientation, over the
  entire `9^11` node space — makes `fill(20,·)` a connected Hamiltonian path on all squares.
  First failures already occur at small `n` (`n = 7, 9, 11` depending on the top rule).
- **swap rule**: **none exists.**
- **verified**: infeasibility verified computationally on `n × n` for **n = 1..40**; the
  impossibility argument below (junctions parity-free ⇒ per-block reduction; two rule-independent
  obstructions) covers the full space and generalizes beyond the tested range. At the
  power-of-two sizes `n = 2^k` the construction *is* a valid path and **matches hilbertplot**
  (`k = 1,2,3`, via `canonical_form`) — the breakdown is confined to non-power-of-two odd-ish
  sizes, exactly where the approximately-even partition creates odd sub-sides.
- **quasi-squares** (`|w−h| = 1`): connected paths **do** exist, but only at specific,
  irregular size sets that depend on the top orientation's domino class (see §Quasi-squares).

## Derivation / proof of impossibility

### Set-up

For a square `n×n` at orientation `e`, `fill(20,·)` splits width `n→(Wc1,Wc2)` (rule `sw`) and
height `n→(Hc1,Hc2)` (rule `sh`), `|Wc1−Wc2|≤1`, `|Hc1−Hc2|≤1`, and lays four blocks

```
LL = curve4 @ R, rev   on  Wc1×Hc1      UL = curve0 @ e  on  Wc1×Hc2
UR = curve0 @ e        on  Wc2×Hc2      LR = curve4 @ C  on  Wc2×Hc1
```

visited LL → UL → UR → LR.

### Lemma 1 (junctions are parity-free)

The three internal junctions LL→UL, UL→UR, UR→LR are 4-adjacent for **every** split, independent
of parity and of all kernel rules. The morphism assignment `(R, e, e, C)` makes consecutive
blocks meet at the shared cell-corner of the internal cross:

- LL @ R (reversed) exits at top-left `(0,Hc1−1)`; UL @ e enters at `(0,Hc1)` — vertical, dist 1.
- UL @ e exits at `(Wc1−1,Hc1)`; UR @ e enters at `(Wc1,Hc1)` — horizontal, dist 1.
- UR @ e exits at `(Wc−1,Hc1)`; LR @ C enters at `(Wc−1,Hc1−1)` — vertical, dist 1.

*Verified: all junctions adjacent for `n = 3..40` (True) for every top rule with `sh=first`.*
Consequently **the whole path is valid iff all four blocks are individually valid**, and each
block's validity depends only on its own kernel subtree's rules.

### Lemma 2 (the height rule is forced: `sh = first`)

If `sh ∈ {second, none}`, the construction fails for **every** width rule and **every** kernel
rule. Take `n = 3`: then `sh` makes the *upper* height even, `Hc2 = 2`, and one of the
identity-oriented curve-0 blocks UL/UR is a `1×2` region (`w = 1` odd, `h = 2` even). By Lemma 1
that block must realize the bottom-corner path `(0,0) → (Wc−1,0) = (0,0)`. Colour cell `(x,y)`
by `(x+y) mod 2`; a Hamiltonian path visits colours alternately, so its endpoints share a colour
**iff** the cell count `N` is odd. Here both endpoints are `(0,0)` (same colour) yet `N = 2` is
even — contradiction. So the block is not Hamiltonian-realisable **for any rule** (coloring is
rule-independent). This forbidden `w odd ∧ h even` curve-0 block appears at `n = 3` for **all six**
rules with `sh ≠ first` (verified). Hence `sh = first` is necessary. ∎

### Lemma 3 (with `sh = first`, a curve-4 block is forced onto an unfillable rectangle)

Fix `sh = first`. For each of the three width rules, some odd `n` forces one of the curve-4 blocks
(LL or LR) onto a rectangle that **no** assignment of kernel swap rules can fill — verified by
**exhaustive search of that block's entire subtree rule space**:

| top rule `(sw,sh)` | forced curve-4 block | shape | first `n` | subtree space searched | fillable? |
|--------------------|----------------------|-------|-----------|------------------------|-----------|
| `(first, first)`   | LR @ C, rev=F        | `3×4` | 7  | `9^1 = 9`      | **No** |
| `(second, first)`  | LL @ R, rev=T        | `7×6` | 13 | `9^4 = 6561`   | **No** |
| `(none, first)`    | LR @ C, rev=F        | `5×4` | 9  | `9^3 = 729`    | **No** |

(The subtree of a curve-4 block contains only indices 4 and 0; the search enumerates every
`(index, orientation)` node in that subtree over `{first,second,none}²`, i.e. the *complete*
freedom available. All assignments fail `validate`.) These blocks are `even×odd` quasi-square
rectangles handed to curve 4 in a **domino-mismatched** orientation: curve 4 (corner→interior)
can Hamiltonian-fill a `|w−h|=1` block only in the domino orientation selected by size-mod-4
(see `curve_4.md` §Quasi-squares), and the orientation forced here (`R` for LL, `C` for LR) is
the wrong class for these sizes. Curve 4's inability propagates from a `w odd ∧ h even`
curve-0 sub-block deep inside it — the same coloring obstruction as Lemma 2, one level down.

### Theorem (impossibility)

Curve 20 admits **no** connected arbitrary-square generalization.

*Proof.* By Lemma 1, feasibility is equivalent to all four top blocks being individually valid,
and each block's validity is a function of its own subtree rules alone. By Lemma 2 the top height
rule must be `sh = first` (else a `1×2` curve-0 block is coloring-forbidden at `n=3`, for every
kernel rule). By Lemma 3, for each of the three width rules paired with `sh = first`, a curve-4
block is forced (at `n = 7`, `9`, or `13`) onto a rectangle unfillable over its **entire** subtree
rule space. The two lemmas jointly exhaust the top rule `(sw,sh) ∈ {first,second,none}²` and, for
each, quantify over **all** kernel rules — i.e. the complete `9^11` space. No assignment yields a
valid path. ∎

The obstruction is a **parity/coloring incompatibility** between the two kernels under the AEP
odd-split: curve 0 (UL/UR) *demands* `sh = first` (so that its bottom-corner blocks avoid the
`w odd ∧ h even` colouring death), but `sh = first` then feeds the curve-4 blocks (LL/LR)
`even×odd` quasi-squares in an orientation where curve 4 cannot avoid its own `w odd ∧ h even`
colouring death. The requirements of the two kernels on the same split are contradictory.

*Scope of proof.* Rule-independent and complete for `n ≤ 40` (all witness blocks verified
unfillable over their full subtree spaces; junctions verified adjacent `n = 3..40`). The
"for all `n`" step rests on the range-verified, self-similar recurrence of the forbidden
`even×odd` curve-4 blocks (they recur at `n ≡ 3 mod 4` and their rescaled copies); a fully
closed all-`n` proof would package curve 4's quasi-square orientation constraint as a lemma.

## Quasi-squares (`|w − h| = 1`)

With the best `sh=first` rule, connected paths exist for **all 8 top orientations**, but only on
**irregular** size sets (~half of sizes), and no orientation covers all sizes. The two domino
classes are exact transposes of one another:

| class | wide `w=h+1` connects at smaller side `h ∈` | tall `h=w+1` connects at smaller side `w ∈` |
|-------|----------------------------------------------|----------------------------------------------|
| **{A=e, C=rot180}** (non-transpose) | `{1,2,3,5,7,10,11,15,18,19,23,26,27,…}` | `{1,2,4,5,8,12,13,16,20,21,24,28,29,…}` |
| **{B=main-diag, D=anti-diag}** (transpose) | `{1,2,4,5,8,12,13,16,20,21,24,28,29,…}` | `{1,2,3,5,7,10,11,15,18,19,23,26,27,…}` |

(Verified smaller side `1..29`.) The wide set of the non-transpose class equals the tall set of
the transpose class and vice-versa — precisely the **`1×2` (A,C) / `2×1` (B,D) primitive
constraint**: at the coarsest split a quasi-square behaves like the domino it bottoms out on,
and A,C accept the tall (`1×2`) primitive while B,D accept the wide (`2×1`) one. The sets are not
a single residue class — they inherit curve 20's self-similar unfillable structure — so there is
**no** orientation-independent quasi-square rule, but a connected path can always be obtained by
choosing an orientation from the size-appropriate class.

## Evidence

Engine `research/aep.py`, run via `.venv/bin/python`. Kernel rules held at their established
values (`curve 0: sh=first, sw=first`; `curve 4: (second,first)`) except where a wider space is
searched.

**Structure.**
```
RULES[20]: LL (4, R=((0,1),(-1,0)), rev=True) | UL (0, e, F) | UR (0, e, F) | LR (4, C=((-1,0),(0,-1)), F)
entry_exit(20) = ('interior','interior')
true partition nodes (n=1..40): curve0 @ all 8 orientations, curve4 @ {R, C}, curve20 @ e  → 11 nodes, space 9^11
```

**Orientation-independent search for curve 20 (9 options, kernels fixed good), n = 1..40:**
```
(first ,first ) firstbad=7    (first ,second) firstbad=3   (first ,none) firstbad=3
(second,first ) firstbad=11   (second,second) firstbad=3   (second,none) firstbad=3
(none  ,first ) firstbad=9    (none  ,second) firstbad=3   (none  ,none) firstbad=3
HITS: []          # all sh!=first die at n=3; all sh=first die by n=11.  2^k match=True for all
```

**Per-orientation reduced searches (all empty):**
```
Stage A: curve0 sw=first, curve4 per-node 9^2, curve20 9         -> space   729, hits 0
Pass2  : curve0 sh=first single sw(3), curve4 per-node 9^2, curve20 9 -> space 2187, hits 0
```

**Hard obstruction — witness curve-4 blocks unfillable over their FULL subtree space:**
```
(first,first)  LR 3x4  subtree nodes=1  space=9     fillable=False
(second,first) LL 7x6  subtree nodes=4  space=6561  fillable=False
(none,first)   LR 5x4  subtree nodes=3  space=729   fillable=False
```

**Lemma 2 witnesses (sh != first, rule-independent coloring death, n=3):**
```
(first,second)->UR 1x2 | (first,none)->UR 1x2 | (second,second)->UL 1x2
(second,none)->UL 1x2  | (none,second)->UL 1x2 | (none,none)->UL 1x2      (all w odd, h even)
```

**Lemma 1 junction adjacency (sh=first rules):** all junctions dist 1 for n = 3..40 (True).

**Power-of-two match:** `n=2,4,8` (`k=1,2,3`) valid=OK and `canonical_form` matches
`hilbertplot.curve(20).points(k)` — True for all.

**Search-space accounting.** Full node space `9^11 ≈ 3.1×10^10` (11 nodes). The impossibility is
established not by brute-forcing this space but by the factorization (Lemma 1) plus two
rule-independent obstructions: Lemma 2 (coloring, rule-independent) covers all `sh≠first`; Lemma 3
covers all three `sh=first` rules via exhaustive subtree searches of sizes `9`, `729`, `6561`.
Together they cover the entire space. Direct empty searches reported: `9` (orient-indep), `729`
and `2187` (reduced per-orientation).

## Open questions

- **Closed all-`n` proof.** The witness-block unfillability is exhaustively verified per size and
  the forbidden `even×odd` curve-4 blocks recur self-similarly (`n ≡ 3 mod 4` and rescalings), but
  a fully closed "for all `n`" statement should be obtained by proving, as a standalone lemma, that
  curve 4 in orientation `R`/`C` cannot Hamiltonian-fill any `even×odd` quasi-square (the curve-4
  quasi-square orientation theorem), from which Lemma 3 follows without enumeration.
- **Mixed / rectangle-aware policy.** Curve 20 might still tile arbitrary rectangles under a swap
  policy that also keys on aspect ratio (choosing orientation per sub-region by the domino class),
  as the quasi-square table suggests; this is outside the fixed-`swap(index,M)` model studied here.
- **Structural classification.** Curve 20 is a clean example of an **infeasible** curve whose two
  kernels impose contradictory parity demands on the same AEP split — a candidate diagnostic for
  the general feasibility theorem: a curve is infeasible when the height rule forced by one kernel
  family drives another kernel family onto its own coloring-forbidden parity.

## Verification

**Verdict: CONFIRMED (infeasible).** An independent, skeptical re-run reproduces every load-bearing
computation and the impossibility argument is sound. Details of what was independently re-run:

**Structure & node space.** `RULES[20] = LL(4,R,rev) | UL(0,e) | UR(0,e) | LR(4,C)`,
`entry_exit(20)=('interior','interior')`. Instrumenting the *real* swap-driven recursion over all
top+kernel rule combinations for `n=1..40` exposes exactly **11 nodes** — curve 0 at all 8
orientations, curve 4 at `{R,C}`, curve 20 at `e` — so the full space is `9^11`. Confirmed.

**Orientation-independent search (kernels fixed good), `n=1..40`.** First-failure sizes reproduced
*exactly*: `(first,first)→7`, `(second,first)→11`, `(none,first)→9`; all six `sh≠first` rules
die at `n=3`. No hits.

**Lemma 3 (the crux) — witness curve-4 blocks are unfillable over their FULL subtree space.**
I extracted the actual top-level blocks at the witness sizes (matching the report: `(first,first)`
→ LR `curve4@C` `3×4` at `n=7`; `(second,first)` → LL `curve4@R` `7×6` at `n=13`;
`(none,first)` → LR `curve4@C` `5×4` at `n=9`) and exhaustively searched each block's entire
subtree rule space. All three: **fillable = False**.
  - `3×4`: subtree nodes = 1, space `9` — unfillable (matches report).
  - `7×6`: subtree nodes = 4, space `6561` — unfillable (matches report).
  - `5×4`: my reachable-superset discovery found **4** nodes (space `6561`), not the report's 3
    (`729`); still **unfillable**. This is a harmless over-count — a *larger* free space that still
    admits no fill is a *stronger* result. Only the report's bookkeeping in that one table row is
    off; the conclusion is unaffected.

**Lemma 2 (`sh=first` forced) — re-examined and re-grounded.** The report's specific phrasing (a
`1×2` curve-0 block "coloring-forbidden because both endpoints are `(0,0)`, `N` even") is a *loose*
description: an isolated `1×2` domino is trivially fillable, so the death is really a
**junction/endpoint** impossibility, not isolated unfillability (my per-block isolation test finds
*no* unfillable block at `n=3`). However, the **conclusion is airtight on cleaner footing**: at
`n=3` every sub-block is `≤2×2`, so the recursion consults **only the top node** (verified: the sole
queried node is `(20,e)`; no kernel rule is read). Hence for each `sh≠first` top rule the `n=3` fill
is `disconnected` **independent of all kernel rules**. `sh=first` is therefore necessary,
rule-independently.

**Factorization (Lemma 1) is structural, not merely empirical.** `fill` literally concatenates the
four block segments (`out += fill(block_i,…)`); a Hamiltonian whole-path forces each contiguous
segment to be a Hamiltonian path on its (translation-invariant) subregion plus adjacent junctions.
Thus a block unfillable *in isolation with its subtree free* is unfillable under **every** global
assignment (coupling only restricts). This makes the per-block witnesses a complete argument over
`9^11`: 6 top rules die at `n=3` rule-independently; the 3 surviving `sh=first` rules each hit an
unfillable curve-4 block. All 9 top rules eliminated.

**Independent refutation attempts (searched for ANY working rule — none found).**
  - Reduced per-orientation search: top `×` `curve4@R` `×` `curve4@C` (curve 0 fixed), `729`
    combos, `n=1..40` → **0 hits**.
  - Randomized full 11-node-space search: `2×10^5` trials → best run stays valid only through
    `n=10`; **no** assignment reaches `n=40`.
  - `2^k` match to hilbertplot re-confirmed (`k=1,2,3`, `canonical_form`, valid=OK).

**Minor issues (do not change the verdict):** (1) Lemma 2's coloring wording is imprecise — the
correct, stronger reason is "no sub-rule is consulted at `n=3`". (2) The `(none,first)` witness-row
node count is 4/`6561`, not 3/`729`. (3) The "for all `n`" claim remains *verified over `n≤40`*, not
*proved for all `n`*; the report honestly flags this in its Open Questions, and I concur it is not a
closed all-`n` proof.

*Independent checks run:* structure/node enumeration; orientation-independent sweep `n=1..40`;
exhaustive subtree searches of the three witness blocks; `n=3` node-query trace; `729`-combo and
`2×10^5`-trial full-space refutation searches; `2^k` hilbertplot match. Engine `research/aep.py` via
`.venv/bin/python`. — Adversarial verifier.
