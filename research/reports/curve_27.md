# Curve 27 — Hilbert+Liu3 #10

- **kernels / quadrant rules** (visited order LL, UL, UR, LR; each `(base, morphism, reverse)`):
  | quadrant | base | morphism (matrix) | reverse |
  |----------|------|-------------------|---------|
  | LL | **0** (Hilbert) | `((-1,0),(0,-1))` = 180° **C** | False |
  | UL | **0** (Hilbert) | `((1,0),(0,1))` = identity **e** | False |
  | UR | **0** (Hilbert) | `((1,0),(0,1))` = identity **e** | False |
  | LR | **4** (Liu3) | `((-1,0),(0,-1))` = 180° **C** | False |

  Curve 27 is built from two kernels: **curve 0 (Hilbert)** in three quadrants and
  **curve 4 (Liu3)** in the lower-right quadrant. It is **not** self-referential (curve 27
  never appears inside itself), so it occurs in the partition only as the top-level node at
  orientation `e`. The kernels must be solved first (bottom-up): curve 0 needs `sh = first`
  at every node (`sw` free); curve 4 needs `(second, first)` at its top node over curve 0.
- **entry/exit type**: `('interior','interior')` — both global endpoints lie in the grid
  interior. (As with curve 4, endpoint type does not by itself decide feasibility.)
- **partition nodes** — `orientations_used(27)` returns **6** nodes (stable and closed;
  identical for size ranges up to `n = 81`):
  `(0, e)`, `(0, C=rot180)`, `(0, B=maindiag ((0,1),(1,0)))`, `(0, D=antidiag ((0,-1),(-1,0)))`,
  `(4, C=rot180)`, `(27, e)`. Curve 4 appears **only** at orientation `C = rot180`; curve 27
  only at `e`. These 6 nodes are the entire per-orientation rule space.

## Result

- **squares: INFEASIBLE.** No swap rule — orientation-independent **or** per-orientation over
  the full node set — makes `fill(27,·)` a connected Hamiltonian path on **every** `n × n`
  square. The obstruction is an infinite family of odd sizes.
- **swap rule**: none exists. The **best achievable** rule (the natural kernel embedding)
  `const_swap({27:(first,first), 4:(second,first), 0:(first,first)})` is valid on **every
  even `n`** and on the odd sizes `n ≡ 3, 5 (mod 8)`, and **fails on exactly the odd sizes
  `n ≡ 1, 7 (mod 8)`**. No other assignment repairs those sizes (proved below and by
  exhaustive search).
- **verified**: exhaustive per-node search over the full space `9^6 = 531441` returns **0**
  valid assignments (screened on odd `n ∈ {3,5}` → 13122 survivors, then `{7,9,11}` → **0**).
  Single-size search proves `n = 7` and `n = 9` infeasible for **any** of the `9^6`
  assignments; `n = 1,3,5` are feasible. Under the natural rule the invalid set for
  `n = 1..40` is exactly `{7,9,15,17,23,25,31,33,39} = {n odd : n ≡ 1,7 (mod 8)}`. Matches
  `hilbertplot` at `2^k` (k = 1,2,3): **yes** (all `2^k` are even, hence covered by the feasible
  even case).
- **quasi-squares** (`|w−h| = 1`): a connected path exists at **every** size, but the top-level
  orientation must be selected by size mod 4 (exactly 4 of the 8 orientations connect each
  quasi-square) — the same domino-class selection as the curve-4 kernel. No orientation is
  uniformly valid.

## Derivation / proof

Top-level partition of curve 27 on `n × n` at orientation `e` with width split
`(Wc1, Wc2)` (rule `sw`) and height split `(Hc1, Hc2)` (rule `sh`), `|Wc1−Wc2|≤1`,
`|Hc1−Hc2|≤1`. The four sub-boxes (canonical frame), visited LL → UL → UR → LR:

```
LL = (0,   0,   Wc1, Hc1) @ C(rot180)   [Hilbert]
UL = (0,   Hc1, Wc1, Hc2) @ e           [Hilbert]
UR = (Wc1, Hc1, Wc2, Hc2) @ e           [Hilbert]
LR = (Wc1, 0,   Wc2, Hc1) @ C(rot180)   [Liu3]
```

The three internal junctions are 4-adjacent for every split (verified `n = 3..40`,
`all junctions adjacent = True`; sample traces in §Evidence), so — exactly as for curve 4 —
the joins impose no parity constraint and **validity reduces to the four sub-blocks each
realizing its prescribed entry→exit path on its rectangle.** Three of those blocks are
Hilbert (curve 0); one is Liu3 (curve 4). The obstruction lives in the interaction between
the Hilbert blocks (which *pin the split parity*) and the Liu3 block (which then cannot fill
the shape it is handed).

### Lemma 1 (Checkerboard condition for the Hilbert blocks)

Colour `(x,y)` by `(x+y) mod 2`. A Hamiltonian path on a `W×H` block visits colours
alternately, so its two endpoints have equal colour **iff** `WH` is odd. Applying this to
each Hilbert block's fixed corner endpoints (entry/exit read off the morphism):

- **LL** `@C`, entry `(Wc1−1,Hc1−1)`, exit `(0,Hc1−1)`: feasible ⟺ **`Wc1` even OR `Hc1` odd**.
- **UL** `@e`, entry `(0,Hc1)`, exit `(Wc1−1,Hc1)`: feasible ⟺ **`Wc1` even OR `Hc2` odd**.
- **UR** `@e`, entry `(Wc1,Hc1)`, exit `(Wc−1,Hc1)`: feasible ⟺ **`Wc2` even OR `Hc2` odd**.

(These are the curve-0 corner-path parity conditions; they are *necessary* for any fill,
independent of the swap chosen inside the block.)

### Lemma 2 (The Hilbert blocks force a unique split parity at odd `n`)

Let `n` be odd. Then `{Wc1,Wc2} = {Hc1,Hc2} = {(n−1)/2, (n+1)/2}`: consecutive integers, one
even and one odd, and the swap rule can put the even one in **either** position. Examine the
four parity choices against Lemma 1:

- If `Wc2` is even (so `Wc1` odd): LL needs `Hc1` odd; UL needs `Hc2` odd. But `Hc1,Hc2` have
  **opposite** parity, so both cannot be odd — **contradiction**. Hence `Wc2` even is impossible.
- Therefore `Wc1` **even**, `Wc2` **odd** (forced). Then LL, UL are automatically satisfied,
  but UR needs `Wc2` even (false) **OR** `Hc2` odd — so `Hc2` **odd**, i.e. `Hc1` **even** (forced).

So for every odd `n` there is a **unique** split parity making LL, UL, UR simultaneously
Hilbert-fillable:
```
Wc1 even, Wc2 odd, Hc1 even, Hc2 odd.
```
(Confirmed computationally: number of colour-consistent splits `= 1` for all odd `n = 3..39`.)

### Lemma 3 (The forced split hands the Liu3 block the central quasi-square at a fixed orientation)

Under the forced split, the LR block is **curve 4 @ C(rot180)** on `Wc2 × Hc1` with
`Wc2` odd, `Hc1` even, `{Wc2,Hc1} = {(n−1)/2,(n+1)/2}`. Hence `|Wc2 − Hc1| = 1`: LR is always
a **quasi-square** (odd width × even height), and its orientation is **fixed** to `C` — the
curve-27 rules give the LR kernel no orientational freedom. Concretely:
```
n ≡ 1 (mod 4):  LR = ((n+1)/2) × ((n−1)/2)   (wide, W odd, H even)
n ≡ 3 (mod 4):  LR = ((n−1)/2) × ((n+1)/2)   (tall, W odd, H even)
```

### Lemma 4 (Liu3 does not fill that quasi-square at orientation `C` for `n ≡ 1,7 (mod 8)`)

Curve 4 (Liu3) does **not** fill quasi-squares uniformly: its connecting orientation is
selected by size mod 4 (established in the curve-4 report — the domino-class selection). At
the **fixed** orientation `C`, exhaustive search over curve 4's entire swap subtree shows the
forced LR quasi-square is fillable **iff** `n ≡ 3,5 (mod 8)** and **unfillable** for
`n ≡ 1,7 (mod 8)`:
```
n :  3   5   7   9  11  13  15  17  19   (odd)
LR:  OK  OK  X   X   OK  OK  X   X   OK
```
(`OK`/`X` = some / no curve-4 swap fills the forced LR; period 8.)

### Theorem (Impossibility)

Curve 27 admits **no** swap rule that is valid on every `n × n` square. For every odd
`n ≡ 1,7 (mod 8)` the construction is infeasible: by Lemma 2 the three Hilbert blocks force
the unique split parity (any other split violates a checkerboard condition and disconnects a
Hilbert block, *regardless of swap*), and by Lemmas 3–4 that split hands the Liu3 block a
central quasi-square at orientation `C` that Liu3 cannot fill (again *regardless of swap*).
Thus no assignment over the 6-node rule space works. ∎

**Independent confirmation.** The complete per-node search (`9^6 = 531441` assignments,
node set closed and stable to `n = 81`) returns **0** valid rules, and single-size exhaustive
search proves `n = 7` and `n = 9` infeasible for **every** assignment. The obstruction is an
infinite family (`n ≡ 1,7 mod 8`), not a boundary artefact.

**Mechanism in one line.** Curve 27's three Hilbert blocks force the split parity so tightly
that the lower-right Liu3 block is always dealt the central odd×even quasi-square at the fixed
orientation `C`; Liu3 fills that shape only for `n ≡ 3,5 (mod 8)`, so half the odd sizes are
unfillable and no swap can rescue them.

## Quasi-squares (`|w − h| = 1`)

With the best rule, quasi-squares are **not** uniformly feasible, but at every size exactly
**4 of the 8** top-level orientations connect (the `rev` flag is irrelevant — interior→interior
is reversal-symmetric). The connecting orientations form a domino class selected by size mod 4:

| aspect | class `{A(e), C(rot180), mx, my}` connects | class `{B(maindiag), D(antidiag), rot90, rot270}` connects |
|--------|--------------------------------------------|------------------------------------------------------------|
| wide `w = h+1` | `h ≡ 2,3 (mod 4)` (e.g. 3×2, 4×3, 7×6, 8×7) | `h ≡ 0,1 (mod 4)` (e.g. 5×4, 6×5, 9×8, 10×9) |
| tall `h = w+1` | `w ≡ 0,1 (mod 4)` (e.g. 4×5, 5×6, 8×9, 9×10) | `w ≡ 2,3 (mod 4)` (e.g. 2×3, 3×4, 6×7, 7×8) |

(Verified sizes 1..14. The `{B,D,rot90,rot270}` rows are the transposes of the `{A,C,mx,my}`
rows.) Interpretation — the **1×2 (A,C) / 2×1 (B,D) primitive constraint**: the axis-aligned
class bottoms out on the vertical `1×2` domino and accepts wide boxes of even height (odd
width) / tall boxes of even width; the transposing class accepts the swapped set. So a
connected quasi-square path always exists, but the orientation must be chosen by the size class
— there is **no** orientation-independent quasi-square rule. This is the same structure the
curve-4 kernel exhibits, which is expected since curve 27's non-trivial kernel *is* curve 4.

## Evidence

Engine `research/aep.py`, run via `.venv/bin/python`.

**Structure.**
```
RULES[27]: LL (0, C=((-1,0),(0,-1)), F) | UL (0, e, F) | UR (0, e, F) | LR (4, C=((-1,0),(0,-1)), F)
entry_exit(27) = ('interior','interior')
orientations_used(27) = { (0,e),(0,C),(0,B),(0,D),(4,C),(27,e) }   # 6 nodes
node set stable/closed for size ranges up to n=81 : True
```

**Exhaustive per-node search, space = `9^6 = 531441`:**
```
survivors screened on odd n ∈ {3,5}   : 13122
survivors then screened on {7,9,11}   : 0
survivors on full n = 1..40           : 0        => INFEASIBLE
```

**Single-size existence (full `9^6`, early-exit):**
```
n = 1  feasible = True     n = 3  feasible = True     n = 5  feasible = True
n = 7  feasible = False    n = 9  feasible = False    (each: complete 531441-assignment scan)
n = 11,13,19,21 feasible = True  (all n ≡ 3,5 mod 8; witnessed by the natural rule)
```

**Best (natural) rule** `const_swap({27:(first,first), 4:(second,first), 0:(first,first)})`,
`n = 1..40`:
```
valid   : 1,2,3,4,5,6,8,10,11,12,13,14,16,18,19,20,21,22,24,26,27,28,29,30,32,34,35,36,37,38,40
invalid : 7,9,15,17,23,25,31,33,39   = { n odd : n ≡ 1,7 (mod 8) }
all even n valid;  2^k match (k=1,2,3) = True, True, True
```

**Forced-split lemma (colour-consistent splits per odd n):** number of splits satisfying
LL, UL, UR = **1** for every odd `n = 3..39`; the unique split is
`(Wc1,Wc2,Hc1,Hc2) = (even, odd, even, odd)`, giving `LR = Wc2 × Hc1` = the central
quasi-square at `@C`. Sample:
```
n= 5: forced (2,3,2,3)  LR = 3x2 @C  (wide)   -> Liu3-fillable  -> n valid
n= 7: forced (4,3,4,3)  LR = 3x4 @C  (tall)   -> NOT fillable   -> n invalid
n= 9: forced (4,5,4,5)  LR = 5x4 @C  (wide)   -> NOT fillable   -> n invalid
n=11: forced (6,5,6,5)  LR = 5x6 @C  (tall)   -> Liu3-fillable  -> n valid
```

**Liu3-at-`C` quasi-square fillability (exhaustive over curve-4 swap subtree):**
```
LR 1x2:OK  3x2:OK  3x4:X  5x4:X  5x6:OK  7x6:OK  7x8:X  9x8:X  9x10:OK   (period 8: OK iff n≡3,5 mod8)
```

**Junction trace** (natural rule): all three internal junctions distance 1 for `n = 3..40`;
at the failing `n = 7` the break is **internal to the LR (Liu3 3×4 @C) block**
(`validate = disconnected`), not at any junction — confirming the obstruction is
sub-block fillability, exactly as the proof predicts.

**Quasi-square connectivity** (natural rule, sizes 1..14): 4 of 8 orientations connect each
quasi-square, split into the two domino classes by size mod 4 (table above); `rev` irrelevant.

## Open questions

- **Closed-form Lemma 4.** The period-8 fillability of Liu3 at fixed orientation `C` on the
  central odd×even quasi-square is verified by exhaustive subtree search and matches curve 4's
  quasi-square mod-4 classification; a fully closed proof for all `n` should follow from the
  curve-4 quasi-square lemma once that is stated for all sizes (currently range-verified).
- **Partial generalization.** Curve 27 *does* generalize to all **even** squares and to odd
  `n ≡ 3,5 (mod 8)` with the natural rule; the infeasible set is precisely `n ≡ 1,7 (mod 8)`.
  Whether an alternative (non-AEP) local patch at the LR quasi-square could rescue those sizes
  is outside the swap-rule framework and left open.
- **General rectangles** (`|w−h| ≥ 2`) not probed; expected to inherit the curve-4 kernel's
  rectangle limitations.

## Verification

**Verdict: CONFIRMED.** Independent, adversarial re-run of the engine reproduces every
load-bearing claim. The impossibility holds both computationally (decisive) and via the
stated mechanism.

**What I re-ran (engine `research/aep.py`, `.venv/bin/python`):**

1. **Structure & node completeness.** `RULES[27]`, `entry_exit(27)=('interior','interior')`,
   and `orientations_used(27)` = the exact 6 nodes claimed; stable to `n=81`. I additionally
   *instrumented the real recursion* (not just the static estimator) across ~1800 random swap
   assignments over odd `n=3..13` and confirmed **exactly these 6 nodes are ever reached, none
   outside**. This closes the one gap that could have invalidated the search: the `9^6` space
   is genuinely the *complete* reachable rule space, so pinning-to-default never hid a free node.

2. **Decisive impossibility — full `9^6` scan at `n=7`.** I built a per-node swap over all 6
   nodes (each ∈ {first,second,none}²) and scanned **all 531441 assignments** at `n=7`,
   validating each fill. **Zero** are valid (complete scan, ~73 s, no early-exit hit). A single
   odd size infeasible over the entire rule space is sufficient for INFEASIBLE. Confirmed. ∎

3. **Natural rule** `const_swap({27:(first,first),4:(second,first),0:(first,first)})`, `n=1..40`:
   invalid set = `{7,9,15,17,23,25,31,33,39}` — reproduced exactly. `2^k` matches hilbertplot for
   k=1,2,3.

4. **Mechanism (Lemmas 1–4) all reproduced.** Three internal junctions are 4-adjacent for all
   `n=3..40` (joins impose no constraint). Colour-consistent splits per odd `n` = **exactly 1**,
   always `(Wc1,Wc2,Hc1,Hc2)=(even,odd,even,odd)`, matching the forced splits in §Evidence.
   The forced LR block (curve 4 @ `C`) exhaustively searched over curve-4's swap subtree is
   **FILLABLE iff `n≡3,5 (mod 8)`, UNFILLABLE for `n≡1,7 (mod 8)`** — period-8 pattern
   `1×2 OK, 3×2 OK, 3×4 X, 5×4 X, 5×6 OK, 7×6 OK, 7×8 X, 9×8 X, 9×10 OK`, identical to Lemma 4.

**Logical soundness.** The reduction is valid: since (i) each Hilbert sub-block is corner→corner
(fixed-corner endpoints), (ii) `validate` = internal Hamiltonicity of the 4 blocks + adjacency
of the 3 junctions, and (iii) junctions are always adjacent — whole-grid infeasibility at `n=7`
combined with "only 1 colour-consistent split exists and under it LR is unfillable" is consistent
and the checkerboard necessity (Lemma 1) correctly rules out the other 3 splits. No gaps found.

**Minor imprecision (does not affect verdict).** The phrase "infeasible set `= {n odd : n≡1,7
(mod 8)}`" literally includes `n=1`, which is in fact *valid* (trivial `1×1`). The report's own
invalid list correctly excludes `n=1`; only the mod-8 shorthand overstates it. Cosmetic.
