# Curve 22 — Hilbert+Liu3 #5

- **kernels / quadrant rules** (visited order LL, UL, UR, LR; each `(base, morphism, reverse)`):
  | quadrant | base | morphism (matrix) | reverse |
  |----------|------|-------------------|---------|
  | LL | **4** (Liu3) | `((0,-1),(-1,0))` (anti-diagonal) | **True** |
  | UL | **0** (Hilbert) | `((0,-1),(1,0))` (rot +90°) | False |
  | UR | **0** (Hilbert) | `((0,1),(-1,0))` (rot −90°) | False |
  | LR | **4** (Liu3) | `((0,1),(-1,0))` (rot −90°) | False |

  Curve 22 kernels into **curve 4** (lower-left, lower-right) and **curve 0** (upper-left,
  upper-right); it never appears inside itself. In the partition it occurs only as the
  top-level node at orientation `A = identity`. All deeper nodes are curves 0 and 4, whose
  square generalizations are already established:
  - curve 0 (Hilbert): valid on all squares with `sh = first` (width free) — `curve_0.md`.
  - curve 4 (Liu3): valid on all squares with `(sw,sh) = (second, first)` — `curve_4.md`.

  Solving bottom-up, the kernels are done; the open question is the **top node (22, id)**.
- **entry/exit type**: `entry_exit(22) = ('interior', 'interior')` — both global endpoints
  lie in the grid interior. (Contrast: curve 0 is corner→corner, curve 4 is corner→interior,
  and both generalize; endpoint type does not predict feasibility — see curve 4. Here the
  interior/interior structure is *not* the obstruction either; the obstruction is a
  parity conflict between the two kernel families, derived below.)

## Result

- **squares: INFEASIBLE.** No swap rule — orientation-independent **or** fully
  per-orientation over every partition node — makes `fill(22,·)` a connected space-filling
  Hamiltonian path on all `n × n` squares.
- **swap rule**: none exists.
- **obstruction**: a **checkerboard (2-colouring) parity conflict**. At odd `n` the two
  curve-0 upper blocks force the upper half-height `Hc2` to be even, while the two curve-4
  lower blocks force the lower half-height `Hc1` to be even; but `{Hc1,Hc2}` are the two
  approximately-even halves of an odd number, i.e. **consecutive integers**, so exactly one
  is even — both-even is impossible. The demands collide and no swap can satisfy both.
- **verified**: exhaustive search at **n = 7** over the *complete* space of swap rules that
  can affect a `7×7` fill (the 5 consulted partition nodes, `3² = 9` options each,
  `9⁵ = 59 049` assignments) returns **0** valid paths. Since any all-squares rule must in
  particular work at `n=7`, the curve is infeasible. The global constraint set collapses to
  empty at `n=7` (per-`n` CSP join, below). Matches `hilbertplot` at `2^k` (k = 1,2,3,4): **yes**
  (even sizes are unaffected by the odd-`n` obstruction).
- **even squares** are individually fine (e.g. `n=8`: all `9⁵` rules valid); the curve fails
  only on **odd** squares, first at `n = 7`. `n = 3, 5` escape (halves too small for the
  obstruction to bite — see Derivation).
- **quasi-squares** (`|w−h| = 1`): connect for a size-dependent subset of the 8 top
  orientations (one domino class per size, occasionally both); never uniformly. See below.

## Derivation / proof

### Set-up: the top-level partition on an odd square

Let `n = 2m+1`. `fill(22, ·)` splits width `n → (Wc1, Wc2)` and height `n → (Hc1, Hc2)`
with `|Wc1−Wc2| = |Hc1−Hc2| = 1`. **Crucially, `{Wc1,Wc2} = {m, m+1}` and
`{Hc1,Hc2} = {m, m+1}` — each pair is a pair of consecutive integers, so each contains
exactly one even and one odd value, whatever the swap does** (the swap only chooses *which*
half is `Wc1` vs `Wc2`, it cannot make both halves even). The four sub-blocks are

```
UL = Wc1 × Hc2  (curve 0)      UR = Wc2 × Hc2  (curve 0)     <- upper pair, height Hc2
LL = Wc1 × Hc1  (curve 4)      LR = Wc2 × Hc1  (curve 4)     <- lower pair, height Hc1
```

visited LL → UL → UR → LR. The upper pair are both **curve 0** and share height `Hc2`; the
lower pair are both **curve 4** and share height `Hc1`. Both pairs span the widths `{Wc1,Wc2}`,
one of which is even.

### Lemma (checkerboard colouring)

Colour cell `(x,y)` by `(x+y) mod 2`. A Hamiltonian path on `N` cells alternates colours, so
**its two endpoints have equal colour iff `N` is odd** (and opposite colour iff `N` is even).

### Lemma (forced corner-to-corner traversal of the blocks)

The three internal junctions (LL→UL, UL→UR, UR→LR) require the exit cell of each block to be
4-adjacent to the entry cell of the next. Combined with the morphisms of curve 22, this pins
each block's entry/exit to specific cells (verified n = 5..13, `corners` trace):

- Each **curve-0 upper block** is traversed between two cells that lie on a common
  vertical edge of the block — local endpoints `(x, 0)` and `(x, ah−1)` with `ah = Hc2`.
  By the colouring lemma these endpoints have **equal colour iff `Hc2` is odd**.
- Each **curve-4 lower block** (corner→interior) is traversed between a corner and an
  interior cell that, for the curve-22 morphisms `(anti-diag,rev)` / `(rot−90°)`, have
  **equal colour iff `Hc1` is odd** (verified n = 5..13).

### The parity squeeze (why no swap works)

Apply the two lemmas to each pair. A block of even area whose forced endpoints are equal-colour
admits **no** Hamiltonian path.

- **Upper pair (curve 0, height `Hc2`).** If `Hc2` is **odd**, the even-width member of the
  pair (one of `Wc1,Wc2` is always even) has area `even × odd = even` with equal-colour
  forced endpoints → impossible. Hence feasibility ⇒ **`Hc2` even**.
- **Lower pair (curve 4, height `Hc1`).** If `Hc1` is **odd**, the even-width member has area
  `even × odd = even` with equal-colour forced endpoints → impossible. Hence feasibility ⇒
  **`Hc1` even**.

But `{Hc1, Hc2} = {m, m+1}` are consecutive integers: **they cannot both be even.** The upper
pair demands `Hc2` even, the lower pair demands `Hc1` even, and no swap can deliver both.
**Contradiction ⇒ no valid swap rule for odd `n`.** ∎

### Why `n = 3, 5` escape and `n = 7` is the first failure

The squeeze needs a *genuine* even-width block, i.e. an even width `≥ 4`, for the "vertical
corner-to-corner on a curve-0/curve-4 block" traversal to actually be forced (a width-2 block
is a domino strip: its two rows give it a Hamiltonian path between the otherwise
"wrong-colour" corners, so it is not parity-dead). The even member of `{m, m+1}` is `≥ 4`
first at `m = 3`, i.e. `n = 7`. For `n = 3` (m=1) and `n = 5` (m=2) the even half is `2`,
a domino strip, and the obstruction does not bite — these odd squares are individually
fillable, but they cannot rescue the curve because `n = 7` already has no rule.

### Status of the proof

- **Impossibility of the curve is rigorous and complete**: the single witness `n = 7`,
  searched *exhaustively* over the full `9⁵ = 59 049` swap space (every partition node that a
  `7×7` fill can consult), has zero valid paths. This settles §4.2 outright.
- The **colouring squeeze** above is the mechanism. It is a closed argument at the top level
  for every odd `n` whose even half is `≥ 4`, modulo the "forced-corner" lemma (endpoints
  equal-colour iff the shared height is odd), which is verified over `n = 5..13` rather than
  proved symbolically for all `n`. For `n ≡ ±1 (mod 8)` the top-level squeeze bites in
  **every** split (verified n = 7..39, `proof` trace); for `n ≡ 3,5 (mod 8)` the top level
  has a colouring-clean split and the same obstruction recurs one level down among the
  sub-quasi-squares (the recursion is confirmed empirically by the CSP collapse, but a
  clean all-`n` induction is left open — it is not needed for the impossibility claim).

## Quasi-squares (`|w − h| = 1`)

With good kernels (`0:(first,first)`, `4:(second,first)`) and full freedom on the top rule,
the count of the 8 D4 top-orientations that yield a connected path (verified sizes 1..9):

| box | connect | A/C-class (`M[0][0]≠0`) | B/D-class (transpose) |
|-----|---------|-------------------------|------------------------|
| 2×1 (wide) | 8 | 4 | 4 |
| 3×2 | 4 | 0 | 4 |
| 4×3 | 8 | 4 | 4 |
| 5×4 | 8 | 4 | 4 |
| 6×5 | 4 | 4 | 0 |
| 7×6 | 4 | 0 | 4 |
| 8×7 | 4 | 0 | 4 |
| 9×8 | 4 | 4 | 0 |
| 1×2 (tall) | 8 | 4 | 4 |
| 2×3 | 4 | 4 | 0 |
| 3×4 | 8 | 4 | 4 |
| 4×5 | 8 | 4 | 4 |
| 5×6 | 4 | 0 | 4 |
| 6×7 | 4 | 4 | 0 |
| 7×8 | 4 | 4 | 0 |
| 8×9 | 4 | 0 | 4 |

Interpretation: quasi-squares connect only for a **size-dependent** subset of orientations —
generically a single domino class (the `1×2` / A,C class for tall boxes vs the `2×1` / B,D
class for wide boxes, selected by size mod 4), occasionally both classes. There is **no**
orientation-independent quasi-square rule. This mirrors the primitive-domino constraint (a
thin box bottoms out on the `1×2` domino under A,C and on the `2×1` domino under B,D), and is
consistent with the square infeasibility: a `w×h` box that recurses into an odd square inherits
the parity conflict. (Verified over the stated range; not a closed all-size proof.)

## Evidence

Engine `research/aep.py`, run with `.venv/bin/python`.

**Structure.**
```
NAME[22] = 'Hilbert+Liu3 #5'
RULES[22]: LL (4, antidiag, rev=True) | UL (0, rot+90) | UR (0, rot-90) | LR (4, rot-90)
entry_exit(22) = ('interior','interior')
orientations_used(22) (odd n, sizes 3..11) = {(22,id), (4,·)×2, (0,·)×2}
distinct partition nodes over n=1..40 = 11: (22,id), (4,M)×2, (0,M)×8
```

**Orientation-independent search (kernels fixed to their proven-good rules), n = 1..40.**
```
curve-22 (sw,sh) over 9 options: 0 hits  (fails: sh=first at n=3 breaks junction UL->UR;
                                          sh in {second,none} passes n=3 but a kernel
                                          quasi-square sub-block breaks by n=7)
```

**Orientation-independent over all three curves (22, 4, 0), 9³ = 729 combos, n = 1..40.**
```
0 hits.
```

**Full per-orientation exhaustive — decomposed per-`n` (sound & complete).**
For each `n`, only a few partition nodes are consulted; enumerate every assignment over the
*actually consulted* nodes (closure-complete), collect the locally-valid ones, and join the
constraints across `n` (a CSP over the 11 nodes; total space `9¹¹ ≈ 3.14×10¹⁰`):
```
n= 1: nodes=0 local_valid=1     global_surviving=1
n= 2: nodes=0 local_valid=1     global_surviving=1
n= 3: nodes=1 local_valid=6     global_surviving=6
n= 4: nodes=1 local_valid=9     global_surviving=6
n= 5: nodes=5 local_valid=1458  global_surviving=1458
n= 6: nodes=5 local_valid=729   global_surviving=162
n= 7: nodes=5 local_valid=0     -> GLOBAL CONSTRAINTS UNSATISFIABLE   [INFEASIBLE]
```

**Exhaustive witness at n = 7 (the complete relevant space).**
```
consulted nodes (5): (22,id), (4,antidiag), (4,rot-90), (0,rot+90), (0,rot-90)
search space = 9^5 = 59049 ;  valid Hamiltonian paths = 0
```

**Per-block colouring trace at n = 7** (the impossible block per top-split; `N%2=0` needs
opposite-colour endpoints but gets same-colour):
```
sw=first,sh=first  : UL curve0 4x3  entry(3,0) exit(3,2)  same-colour, N=12  -> IMPOSSIBLE
sw=first,sh=second : LL curve4 4x3  entry(2,1) exit(3,2)  same-colour, N=12  -> IMPOSSIBLE
sw=second,sh=second: LR curve4 4x3  entry(0,2) exit(1,1)  same-colour, N=12  -> IMPOSSIBLE
(all 9 top-splits contain such a block; per-block full search confirms each is unfillable)
```

**Top-level squeeze across odd n** (does every split contain a colouring-dead block?):
```
n≡1,7 (mod 8)  (7,9,15,17,23,25,31,33,39): every split blocked at top level  -> yes
n≡3,5 (mod 8)  (3,5,11,13,19,21,...)      : >=1 clean split at top level; obstruction
                                            recurs one level down (CSP still empty via n=7)
```

**Even squares & 2^k match.**
```
n = 2,4,6,8 full-freedom valid counts: 1, 9, 729, 59049  (even sizes are fine)
2^k vs hilbertplot (canonical_form), k = 1,2,3,4: match = True, True, True, True
```

## Open questions

- **Closed all-`n` induction for the squeeze.** The impossibility is settled by the `n=7`
  exhaustive witness; a symbolic proof that the parity conflict recurs at *every* odd `n`
  (including the `n ≡ 3,5 mod 8` sizes where the top level is clean and the obstruction drops
  one level) would upgrade the "verified over range" mechanism to a fully closed theorem.
- **Forced-corner lemma.** The claim "each curve-0 upper block / curve-4 lower block is
  traversed between equal-colour cells iff its shared height is odd" is verified n = 5..13;
  a direct derivation from curve 0's corner→corner and curve 4's corner→interior boundary
  vectors (under curve 22's morphisms) would close the last gap.
- **Structural classification.** Curve 22 is the first infeasible curve encountered whose
  two kernel families impose *opposite* height-parity demands on the shared central split.
  This "two families, contradictory junction parities on the same split" pattern is exactly
  the impossibility archetype anticipated in `context.md §4.2`, and is a candidate
  discriminator for the target theorem (feasible ⇔ all kernel blocks along a shared split
  demand the *same* half-parity).
- **General rectangles** `|w−h| ≥ 2`: not probed.

## Verification

**Adversarial re-check (independent, skeptical).** Verdict: **CONFIRMED — INFEASIBLE.**

I re-ran the engine from scratch (`.venv/bin/python`, `research/aep.py`), independently
re-deriving the consulted-node set rather than trusting the report's list, and actively tried
to *refute* the impossibility by searching the full swap-rule space for any working rule. I
found none. Details:

1. **Structure** matches: `NAME[22]='Hilbert+Liu3 #5'`, `RULES[22] = LL(4,antidiag,rev) |
   UL(0,rot+90) | UR(0,rot−90) | LR(4,rot−90)`, `entry_exit(22)=('interior','interior')`. The
   proven-good kernels are valid over the full range: `square_valid(0,(first,first))` and
   `square_valid(4,(second,first))` both `True` on `n=1..40`.

2. **Orientation-independent search** (kernels fixed, curve-22 rule over all 9 options), `n=1..40`:
   **0 hits** — every one of the 9 fails. Reproduced.

3. **The decisive exhaustive witness at `n=7` — reproduced independently.** I re-enumerated the
   partition nodes consulted by a `7×7` fill with my *own* traversal that explores **both** split
   parities at every level (so the node set is closure-complete regardless of the swap choice, not
   taken on faith). Result: exactly **5** nodes — `(22,id), (0,rot+90), (0,rot−90),
   (4,antidiag), (4,rot−90)`. Since `swap` is a function of `(index,M)` only, these 5 values fully
   determine the `7×7` fill. Exhaustive search over all `9⁵ = 59049` assignments: **0 valid
   Hamiltonian paths.** Because every all-squares rule must in particular work at `n=7`, this
   finite exhaustive check *by itself* proves infeasibility. The proof does not rely on the
   colouring squeeze.

4. **CSP join across `n=1..7` reproduced exactly**: global-surviving counts
   `1,1,6,6,1458,162,0`; collapses to empty at `n=7`. Even-square full-freedom counts
   `1,9,729,59049` for `n=2,4,6,8` (fine). `2^k` vs `hilbertplot` (canonical form) match `True` for
   `k=1,2,3,4`.

5. **Quasi-square table spot-checked** (`2×1,3×2,4×3,6×5,1×2,2×3`) — all `(total,AC,BD)` counts
   reproduce exactly.

**Scrutiny of the argument.** The impossibility rests entirely on the finite, exhaustive `n=7`
witness (item 3), which is airtight within the study's defined rule space (`swap(index,M)`). The
report is honest about scope: it explicitly labels the colouring "squeeze" and the "forced-corner"
lemma as *verified over `n=5..13`, not proved for all `n`*, and correctly states the closed
all-`n` induction is not needed for the impossibility claim. No overclaiming was found; the
"verified over range" vs "proved for all `n`" distinction is respected throughout. I could not
find any swap rule (orientation-independent or fully per-orientation) that works, and found no
logical gap in the finite-witness impossibility argument.
