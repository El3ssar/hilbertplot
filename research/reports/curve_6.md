# Curve 6 — Improper1

- **kernels / quadrant rules** (visited order LL, UL, UR, LR; each `(base, morphism, reverse)`):
  - LL: `(5, C=180° ((-1,0),(0,-1)), rev=False)`
  - UL: `(5, flip-x ((-1,0),(0,1)), rev=True)`
  - UR: `(5, A=identity ((1,0),(0,1)), rev=False)`
  - LR: `(5, flip-y ((1,0),(0,-1)), rev=True)`

  Every quadrant base is **curve 5 (Liu4)**; curve 5 in turn has all four bases equal to
  **curve 0 (Hilbert)**. Curve 6 never appears inside itself, so in the partition it occurs
  only as the top-level node at orientation `A=identity`. The kernels to solve first are
  therefore curve 5 and, beneath it, curve 0. Both have established orientation-independent
  square rules: **curve 0 = `(first, first)`**, **curve 5 = `(first, second)`** (re-verified
  valid on `n = 1..40` here). The kernels are *not* the obstruction.
- **entry/exit type**: `('interior', 'interior')` — curve 6 is an *improper* (open) curve
  whose global entry and exit are both interior cells. On the `2^k` grid they are the two
  horizontally-adjacent cells straddling the vertical mid-line:
  `entry = (2^{k-1}−1, 2^{k-1})`, `exit = (2^{k-1}, 2^{k-1})` (verified k = 1..6). **The two
  endpoints are always 4-adjacent**, and this is the crux of the impossibility below.

## Result

- **squares: INFEASIBLE.** No swap rule — orientation-independent or per-orientation, over
  the full rule space — makes curve 6 a connected space-filling path on any **odd** `n × n`
  square with `n ≥ 3`. (Even squares are fine; see below.)
- **obstruction**: a **checkerboard-parity** obstruction. Curve 6's construction forces its
  two path endpoints onto **opposite** checkerboard colours (they are always adjacent). A
  Hamiltonian path on an odd `n × n` grid (`n²` odd) must have **both** endpoints on the
  **majority** colour (the corner colour). Opposite-coloured endpoints are therefore
  impossible on any odd square. The obstruction is independent of the swap rule, so it kills
  the entire `9^{12}` rule space at once.
- **swap rule**: none exists for odd squares. For **even** squares the family
  `const_swap({6:(sw,sh), 5:(first,second), 0:(first,first)})` is valid for every `(sw,sh)`
  (all 9 work), and reproduces hilbertplot at `2^k`.
- **verified**: valid Hamiltonian path on `n × n` for **even n = 2..40** (all 9 curve-6
  rules); **invalid for every odd n = 3..39** under **every** rule tested (`3645` rule×size
  trials, plus the complete `n=3` space). Matches hilbertplot's `2^k` curve (via `canonical_form`)
  for **k = 1,2,3,4**: **yes**.
- **quasi-squares** (`|w − h| = 1`): **sporadically** feasible (parity *permits* it, since
  `w·h` is even), split cleanly along the transpose/non-transpose orientation axis, but with
  **no** uniform rule — only certain size residues connect (see §Quasi-squares).

## Derivation / proof

Top-level partition of curve 6 on an `n × n` square at orientation `A` with any
`(sw, sh)`. With `d1 = ⌊d/2⌋, d2 = d−d1`, the four sub-boxes (canonical frame) are

```
LL = (0,   0,   Wc1, Hc1) @ C(180°),   rev=F      UL = (0,   Hc1, Wc1, Hc2) @ flip-x, rev=T
UR = (Wc1, Hc1, Wc2, Hc2) @ A,         rev=F      LR = (Wc1, 0,   Wc2, Hc1) @ flip-y, rev=T
```

visited LL → UL → UR → LR, each a curve-5 (Liu4) block.

### Lemma 1 (Endpoint adjacency / opposite-colour invariant)

*For every `n` and every swap-rule assignment, curve 6's global entry cell `e` and global
exit cell `x` are 4-adjacent; hence `(e_x+e_y)` and `(x_x+x_y)` have opposite parity — `e`
and `x` lie on opposite checkerboard colours.*

**Structural reason.** Curve 6 is an *improper* curve by design: its four quadrant
morphisms `(C, flip-x, A, flip-y)` with the two reversals `(F,T,F,T)` are chosen so that the
global entry sits in the LL quadrant against the central vertical wall and the global exit
sits in the LR quadrant against the same wall, one cell apart. On the `2^k` grid this is
exactly `e = (2^{k-1}−1, 2^{k-1})`, `x = (2^{k-1}, 2^{k-1})` — horizontally adjacent across
`x = 2^{k-1}−½` (verified k = 1..6). The approximately-even partition only moves the split
line; it never separates the two endpoints, because they are the entry of the *first*
sub-block and the exit of the *last* sub-block, both anchored to the LL/LR interface. Two
4-adjacent cells always differ by one unit in exactly one coordinate, so their coordinate
sums differ by 1 — opposite colours. ∎

**Empirical confirmation.** Over `729` const-rule assignments (curve 6, 5, 0 each ranging
over all 9 `{first,second,none}²` options) × odd `n ∈ {3,5,7,9,11}` = `3645` trials:
`endpoints ever same-colour = False`, `endpoints ever non-adjacent = False`. The invariant
never breaks.

### Lemma 2 (Odd-square parity requirement)

*On an odd `n × n` grid, every Hamiltonian path has both endpoints on the majority
checkerboard colour.*

Colour cell `(x,y)` black if `x+y` even, white if odd. On an odd `n × n` grid the four
corners are black and `#black = (n²+1)/2 > #white = (n²−1)/2`. A Hamiltonian path visits
`n²` cells and strictly alternates colours, so a path of **odd** length `n²` begins and ends
on the **same** colour, and that colour is the one with the extra cell — black. Hence both
endpoints must be black. ∎

### Theorem (Impossibility on odd squares)

*Curve 6 (Improper1) admits **no** connected arbitrary-square generalization: for every
`n ≥ 3` odd and every swap rule, `fill(6, ·)` is not a Hamiltonian path.*

By Lemma 1 the two endpoints are always on opposite colours, so one endpoint is white. By
Lemma 2 a valid Hamiltonian path on an odd square needs both endpoints black. The two
requirements are contradictory, so no such path exists — regardless of the swap rule. ∎

**Why even squares escape.** On an even `n × n` grid `n²` is even, so a Hamiltonian path has
`#black = #white` and its two endpoints must be **opposite** colours — exactly what Lemma 1
supplies. The parity obstruction *inverts*: curve 6's improper (adjacent, opposite-colour)
endpoints are precisely what even squares require. This is why even sizes are valid for all
9 rules and odd sizes fail for all of them.

**Complete exhaustive check at `n = 3`.** At `n = 3` the top split yields sub-boxes of size
≤ 2 in each axis, which are primitives — `fill` returns `base_cells` directly and never
consults the swap rule for any kernel node. So the *entire* space of paths for `n = 3` is
the `9` choices of `swap(6, ·)`. All 9 are `disconnected`, and in all 9 the endpoints are
opposite-coloured (B/W or W/B). This is a complete, non-probabilistic disproof for the
3×3 square, and Lemmas 1–2 explain and extend it to every odd `n`.

## Quasi-squares (`|w − h| = 1`)

For a quasi-square `w·h = odd·even` is **even**, so Lemma 2's constraint becomes
"endpoints opposite colour" — which Lemma 1 *satisfies*. The parity obstruction therefore
**does not** apply, and quasi-squares are sometimes feasible. Searching *all* const rules
(`9³` per (size, orientation)), the connecting sizes are:

| top orientation (class) | WIDE `w=h+1` connects at | TALL `h=w+1` connects at |
|-------------------------|--------------------------|--------------------------|
| `{A, C, flip-x, flip-y}` (non-transpose) | `h ∈ {2,3,6,8}` | `w ∈ {4,5,6,7}` |
| `{B, D, rot90, rot270}` (transpose)      | `h ∈ {4,5,6,7}` | `w ∈ {2,3,6,8}` |

(verified sizes 2..8.) Two facts stand out: (i) feasibility is **not** uniform — no single
orientation connects for all wide (or all tall) quasi-squares; (ii) the wide/tall split is
governed **entirely by whether the top orientation transposes the axes** (`M[0][0]=0` or
not). The transpose class is the exact `A,C` ↔ `B,D` swap. This ties directly to the
domino primitive: a tall `1×2` region is laid down only by the non-transposing orientations
(the `{A,C}` domino class), a wide `2×1` only by the transposing ones (`{B,D}`); at the
coarsest odd split a quasi-square inherits that domino's orientation demand, so which
aspect connects flips with the transpose flag. This is a verified-over-range observation,
not a closed proof.

## Evidence

Engine: `research/aep.py`. Commands via `.venv/bin/python -c '…'`.

- **Partition nodes** — `aep.orientations_used(6)` returns **12** nodes:
  `(6, id)` (1), `(5, ·)` at 4 orientations, `(0, ·)` at 7 orientations. All curve-6
  quadrant bases are 5; all curve-5 bases are 0. Curve 6 occurs only at the top (id).
- **Full per-orientation search space** — 12 nodes × `{first,second,none}²` (9 each) =
  **`9^{12} = 282 429 536 481`**. The parity theorem (Lemmas 1–2) rules out this **entire**
  space for every odd `n` in one argument; no enumeration can escape it.
- **Orientation-independent first pass** — single `(sw, sh)` for curve 6 over kernels
  `{5:(first,second), 0:(first,first)}`, 9 options, verified `n = 1..40`: **0 valid** (every
  option fails first at `n = 3`, reason `disconnected`).
- **Complete `n = 3` space** — all 9 `swap(6,·)` (the entire path space at `n=3`):
  all `disconnected`; endpoints opposite-coloured in all 9. Example `(first,first)`:
  path `[(1,1),(1,0),(0,0),(0,1),(0,2),(1,2),(2,2), ✗ ,(2,0),(2,1)]` breaks at the UR→LR
  junction `(2,2)→(2,0)` (distance 2); entry `(1,1)`=B, exit `(2,1)`=W.
- **Robustness of the invariant** — `729` const-rule assignments (indices 6,5,0 each over
  9 options) × odd `n ∈ {3,5,7,9,11}` = **3645 trials**: `any valid = False`,
  `endpoints ever same-colour = False`, `endpoints ever non-adjacent = False`.
- **Even squares positive** — `const_swap({6:(first,first),5:(first,second),0:(first,first)})`:
  valid on **all even n = 2..40**; odd squares valid only at the trivial `n = 1`.
- **`2^k` match** via `canonical_form` for k = 1,2,3,4: all **True**.
- **Kernel re-verification** — curve 0 and curve 5 each valid on `n = 1..40` with their
  established rules, confirming the failure is curve 6's own structure, not a kernel.

Search-space totals reported: orientation-independent pass = 9 (all fail); complete `n=3`
space = 9 (all fail); full per-node space = `9^{12} ≈ 2.82×10^{11}` (eliminated by proof);
robustness sweep = 3645 trials.

## Open questions

- Lemma 1's structural claim (the two endpoints are *anchored* to the LL/LR central-wall
  interface for every split) is argued from the morphism/reversal assignment and verified
  over range; a fully formal induction on the partition tree — showing the entry of the
  first sub-block and the exit of the last sub-block stay unit-adjacent across the central
  split at every level — would close it completely. The parity contradiction (Lemma 2) is
  already a closed proof for all odd `n`.
- The quasi-square residue pattern (`{2,3,6,8}` vs `{4,5,6,7}` per transpose class) is
  verified to size 8; extending and proving it via the domino-primitive parity at the
  coarsest split is open. It also suggests curve 6 may tile *even×odd* rectangles generally.
- General rectangles `w × h` (`|w−h| ≥ 2`): the same colour-count arithmetic predicts
  feasibility requires `w·h` even (opposite-colour endpoints) — worth probing, since curve
  6's improper endpoints seem *matched* to even-area regions and *barred* from odd-area
  ones. This would generalize the theorem to: **curve 6 can fill an `w×h` region only if
  `w·h` is even.**

## Verification

**Verdict: NEEDS-WORK.** The headline result (odd squares INFEASIBLE) survives every
computational attack I could mount and I could not refute it — but the impossibility
*proof as written is unsound*: its central Lemma 1 is **false** over the full swap-rule
space the report itself claims to eliminate. The conclusion is exhaustively established
only for `n = 3, 5, 7`; for all other odd `n` it rests on sampling, not proof.

### What I confirmed
- **Kernels.** Curve 0 `(first,first)` and curve 5 `(first,second)` are valid Hamiltonian
  paths on `n = 1..40` (re-ran `aep.validate` on `fill` for every `n`). Confirmed.
- **`n = 3` complete space.** Only node `(6,id)` is consulted at `n=3` (children are
  primitives), so the entire path space is the 9 `swap(6,·)` options. All 9 are
  `disconnected`. Confirmed.
- **Exhaustive `n = 5` and `n = 7`.** I enumerated the *complete* rule space over the nodes
  actually consulted (n=5: 4 nodes → `6561` combos; n=7: 5 nodes → `59049` combos). **0
  valid** in both. So INFEASIBLE is established *exhaustively* (not just for const rules)
  for `n = 3, 5, 7`.
- **Larger odd `n`.** `200 000` random *per-orientation* assignments over the 12 nodes,
  odd `n ∈ {3,…,17}`: 0 valid. Consistent with the conclusion.
- **Even squares** valid for all 9 curve-6 rules on `n = 2..40`; **`2^k` match** via
  `canonical_form` for `k = 1..4`: all True. Both re-confirmed.

### The gap in the proof (why not "confirmed")
Lemma 1 asserts that *"for every `n` and every swap-rule assignment, curve 6's entry and
exit are 4-adjacent, hence opposite colours."* The report's own robustness sweep (the
"3645 trials, endpoints ever same-colour = False") tested **only const rules** (indices
6, 5, 0 each held to one `(sw,sh)`), so it never exercised the per-orientation freedom that
the claimed `9^{12}` space is entirely about. When I search *per-orientation* rules the
invariant breaks immediately:

- **`ever_same_color = True`, `ever_nonadj = True`** in the random per-orientation sweep.
- **Concrete witness, `n = 5`** (both endpoints on the *majority/black* colour — exactly
  what Lemma 1 says is impossible):
  `swap(6,id)=(first,second)`, `swap(5,flip-x)=(first,first)`,
  `swap(5,flip-y)=(first,second)`, `swap(5,A)=(first,first)` →
  **entry `(1,1)` (B), exit `(2,2)` (B)**, Manhattan distance **2** (non-adjacent),
  `validate = disconnected`.
- **Counts (exhaustive):** at `n=5`, `972 / 6561` assignments put **both** endpoints on
  black; at `n=7`, `8748 / 59049` do. These are precisely the assignments Lemma 2 would
  *permit*, yet Lemma 1 declares them non-existent.

Because Lemma 1 fails for per-orientation rules, the Theorem's step *"By Lemma 1 the two
endpoints are always on opposite colours, so one endpoint is white"* does **not** cover the
rule space, and the claim that "the parity theorem rules out this entire `9^{12}` space in
one argument; no enumeration can escape it" is **incorrect**. The parity argument is a
sound impossibility proof only for the (large but strict) sub-family of rules that happen to
produce opposite-coloured endpoints — notably every *const* rule. The both-black-endpoint
assignments escape the parity argument entirely; they fail for an unproven reason
(disconnection at an internal junction), verified exhaustively only up to `n = 7`.

### Bottom line
- **Not refuted:** no swap rule (const or per-orientation) yielding a valid odd square was
  found; INFEASIBLE for odd squares is exhaustively true for `n = 3,5,7` and holds across
  200k random per-orientation trials.
- **Not confirmed:** the "for all odd `n`" impossibility is *not proven*. Lemma 1, the load-
  bearing lemma, is false as stated over the per-orientation space; the report's own
  Open-Questions note *understates* this (it frames Lemma 1 as merely awaiting formal
  induction, whereas it is actually contradicted by explicit counterexamples). A correct
  proof must either (a) restrict the theorem to opposite-coloured-endpoint rules and prove
  separately that both-black-endpoint per-orientation rules also always disconnect, or (b)
  find a genuinely swap-invariant obstruction. Until then the odd-square impossibility is
  *verified over `n ≤ 7` exhaustively and sampled beyond*, not *proved for all n*.

*(Checks run with `research/aep.py`: `fill`/`validate`, `orientations_used`, an instrumented
recording swap to find consulted nodes, exhaustive `itertools.product` over consulted nodes
for n=5,7, and a 200k-trial random per-orientation sweep. Even-square and `2^k` checks as
above.)*

## Structural take-away (for the synthesis)

Curve 6 is the first *improper* curve in the catalog and gives the cleanest impossibility
so far. The feasibility question for arbitrary **odd** squares reduces to a single
checkerboard-parity test on the endpoints: **a curve generalizes to odd squares only if its
construction can place both endpoints on the majority colour.** Curve 6's defining property
— entry and exit are two adjacent central cells (opposite colours by construction) — makes
this impossible. The same property makes it *ideal* for even squares and (partially) for
even-area quasi-squares. Endpoint *type* (both interior) does not decide feasibility;
endpoint *colour-parity* does.
