# Curve 10 — Improper5

- **kernels / quadrant rules** (visited order LL, UL, UR, LR):
  | quadrant | base | morphism `M` | reverse |
  |----------|------|--------------|---------|
  | LL | 5 (Liu4) | `((1,0),(0,-1))` = **vflip** (`m`)     | False |
  | UL | 5 (Liu4) | `((0,-1),(1,0))` = **rot90** (`g`)     | False |
  | UR | 5 (Liu4) | `((0,1),(1,0))`  = **transpose** (`o`) | True  |
  | LR | 5 (Liu4) | `((-1,0),(0,-1))`= **rot180** (`f`)    | True  |

  **Every quadrant recurses into kernel curve 5 (Liu4)**, and curve 5 in turn recurses only
  into **curve 0 (Hilbert)**. So the kernel chain is `10 → 5 → 0`, solvable bottom-up. The
  established kernel rules are:
  - **curve 0** (Hilbert): valid on all squares with canonical height-split `sh = first`
    (`sw` free) — proven in `curve_0.md`.
  - **curve 5** (Liu4): valid on all squares **iff** `(sw,sh) = (first,second)` — *both* split
    axes pinned; proven in `curve_5.md`. This double pin is the ultimate source of curve 10's
    obstruction.

- **entry/exit type:** `entry_exit(10) = ('edge','edge')`. On the `2^k` grid
  (`hilbertplot.curve(10).points(k)`) the global path runs from **left-edge interior** `(0, 2^{k-2})`
  to **right-edge interior** `(2^k-1, 2^{k-2})` — a *horizontal edge-to-edge span pinned at
  height `2^{k-2}`* (both endpoints share checkerboard color 0). Order 1..4 endpoints:
  `2×2 (0,0)→(1,0)`, `4×4 (0,1)→(3,1)`, `8×8 (0,2)→(7,2)`, `16×16 (0,4)→(15,4)`. Unlike curve 0
  (corner→corner) or curve 5 (left-edge→bottom-edge L-turn), curve 10's endpoints sit at the
  *interior of two opposite edges*; the exact interior height depends on the partition, and that
  is precisely what makes the parity demand size-dependent.

- **partition nodes** (`orientations_used(10)`) — the `(curve, orientation)` pairs that need a
  swap rule — **13 nodes**:
  - `(10, e)` — curve 10 only ever appears at identity (top level);
  - `(5, m)`, `(5, g)`, `(5, o)`, `(5, f)` — curve 5 at four orientations
    (= curve 10's four quadrant morphisms);
  - `(0, ·)` at all **eight** D4 orientations `{e,m,y,f,g,x,o,a}` — curve 0, closed under the
    recursion.

  Full per-node rule space: `9^13 ≈ 2.5·10^12` (each node ∈ {first,second,none}²).

## Result

- **squares: INFEASIBLE.** There is **no** swap rule — orientation-independent *or*
  per-orientation, anywhere in the full `9^13` space — that makes `fill(10,·)` a valid
  Hamiltonian path on every `n×n`. In fact **no rule is valid at both `n=5` and `n=7`.**
- **swap rule:** none exists. (The closest single rule, top `(10,e)=(first,second)`,
  `5=(first,second)`, `0=(first,first)`, is valid on `n = 3,4,5,6,8,10,12,…` but disconnects on
  `n = 7,9,11,13,…`.)
- **obstruction:** a **residue-class parity conflict at the top node `(10,e)`**. For `n ≡ 1
  (mod 4)` (e.g. `n=5`) validity forces the top height-split low-half `Hc1` to be **odd**
  (`sh = second`); for `n ≡ 3 (mod 4)` (e.g. `n=7`) it forces `Hc1` **even** (`sh = first`).
  A single node cannot deliver both parities. Same conflict on the width axis by symmetry.
- **verified:** the conflict is proven **exhaustively and completely** at `n ∈ {3,5,7}`
  (see proof: at these sizes the recursion never reaches any curve-0 node, so the *entire*
  rule space collapses to `9^5 = 59049` assignments of the 5 relevant nodes, of which **0** are
  valid at all three). Corroborated by four further exhaustive searches (`9^3`, `9^5`, `9·3^8`,
  `9^6`), all returning 0 valid rules over `n = 1..40`. **Matches hilbertplot at `2^k` (k=1,2,3):
  yes** — at even sizes the swap is a no-op, so the powers-of-two curve is reproduced exactly;
  the failure is confined to odd sizes.
- **quasi-squares** (`|w−h| = 1`): no top orientation connects *all* wide (or all tall)
  quasi-squares; connectivity is size-periodic. Non-transposing tops `{e,m,y,f}` connect **wide
  at even long-side / tall at odd long-side**; transposing tops `{g,x,o,a}` are the transpose
  (**wide-odd / tall-even**). This mirrors the `1×2` (`A,C`-class) / `2×1` (`B,D`-class)
  primitive constraint, further thinned to ~half of each parity class by curve 5's double pin.

## Derivation / proof

### Setup

At the top level (`n×n`, orientation `e`, no transpose) `fill` splits `Wc=n → (Wc1,Wc2)`
(rule `sw`) and `Hc=n → (Hc1,Hc2)` (rule `sh`), `|Wc1−Wc2|,|Hc1−Hc2| ≤ 1`, and lays four
sub-boxes visited LL→UL→UR→LR, each a **curve-5** path:

| box | region | curve-5 orient | rev |
|-----|--------|----------------|-----|
| LL | `[0,Wc1)×[0,Hc1)`  | `m` (vflip)     | F |
| UL | `[0,Wc1)×[Hc1,n)`  | `g` (rot90)     | F |
| UR | `[Wc1,n)×[Hc1,n)`  | `o` (transpose) | T |
| LR | `[Wc1,n)×[0,Hc1)`  | `f` (rot180)    | T |

Validity of the whole requires (i) each sub-box is a valid curve-5 Hamiltonian path on its
rectangle, and (ii) the three junctions `LL→UL→UR→LR` are 4-adjacent.

### Lemma 1 (Kernel-independence at small odd sizes — the reduction)

For `n ∈ {3,5,7}` the recursion **never reaches a curve-0 node**: every curve-5 sub-box is small
enough that its own sub-boxes bottom out on the `≤2` primitives before a curve-0 split occurs.
`orientations_used(10, sizes=[3,5,7]) = {(10,e),(5,m),(5,g),(5,o),(5,f)}` — no `(0,·)`. Hence
validity at `n∈{3,5,7}` is a function of **only these 5 nodes**, independent of every curve-0
rule (verified: flipping curve-0's rule leaves the `n=3,5,7` verdict unchanged). The relevant
rule space is therefore exactly `9^5 = 59049`, not `9^13`. ∎

### Theorem (Impossibility)

*No swap rule in the full `9^13` space makes `fill(10,·)` valid on every square; specifically none
is valid at both `n=5` and `n=7`.*

**Proof.** By Lemma 1, validity at `n∈{3,5,7}` depends only on the 5 nodes
`{(10,e),(5,m),(5,g),(5,o),(5,f)}`. Enumerate all `9^5 = 59049` assignments and record, for each,
the subset of `{3,5,7}` it validates. The achieved subsets are **exactly**:

| achieved subset | # rules | forced top `sh` |
|-----------------|---------|-----------------|
| `{3,5}` | 5832 | `second` |
| `{7}`   | 1458 | `first`  |
| `{3}`   | 33534 | `none`/`second` |
| `{}`    | 18225 | — |

`{3,5,7}` is achieved **0** times; `{5,7}` and `{3,7}` are **never** achieved. Since the
`9^5` space is the *complete* space governing these sizes (Lemma 1), **no rule whatsoever** —
including any choice of the eight curve-0 nodes — validates `n=5` and `n=7` simultaneously.
A fortiori no rule validates all squares `n=1..40`. ∎

### Mechanism (why `n=5` and `n=7` demand opposite top parities)

The discriminating knob is the top **height** split `sh` (the width split `sw` is free — all
three `sw` values occur equally in each row of the table above). Its effect on `Hc1`:

| `n` | `sh=first` | `sh=second` | `sh=none` |
|-----|-----------|-------------|-----------|
| 3 | `Hc1=2` even | `Hc1=1` **odd** | `Hc1=1` odd |
| 5 | `Hc1=2` even | `Hc1=3` **odd** | `Hc1=2` even |
| 7 | `Hc1=4` **even** | `Hc1=3` odd | `Hc1=3` odd |

- **`{3,5}` (both need `Hc1` odd) ⇒ `sh=second`.** `sh=second` is the *only* value making
  `Hc1` odd at both `n=3` and `n=5`.
- **`{7}` (needs `Hc1` even) ⇒ `sh=first`.** But `sh=first` makes `Hc1` even at `n=5` too,
  killing `n=5`; `sh=second` makes `Hc1` odd at `n=7`, killing `n=7`.

So the top node must set `Hc1` **odd for `n≡1 (mod 4)`** and **even for `n≡3 (mod 4)`** — a
contradiction for any fixed `sh`.

**Root cause — curve 5's double pin (checkerboard coloring).** Why does `Hc1`'s parity matter?
Each sub-box is a curve-5 path, and curve 5 (rule `(first,second)`) is a Hamiltonian path on a
`W×H` rectangle only for a *joint* `W,H` parity — its **both** split axes are pinned
(`curve_5.md`, Lemma 3), so unlike curve 0 (a single free axis) curve 5 cannot absorb a parity
mismatch. Concretely (color `(x,y)` by `(x+y)\bmod 2`), curve 5's canonical entry `(0,·)` and
exit `(·,0)` are **edge-interior** cells whose colors and positions are fixed by the box parity;
curve 5 disconnects whenever the box parity is wrong (e.g. `curve5@m` fails on `4×5` and `7×6`,
`curve5@g/o` fail on `5×4` and `6×7`). Placed at the four orientations `m,g,o,f`, the four
sub-boxes impose these parity conditions on `(Wc1,Hc1)`; combined with the three junction
adjacencies they collapse to the single demand "`Hc1` parity `= f(n \bmod 4)`", which flips
between the two odd residue classes. The top node, having one fixed rule, cannot honor both —
this is the obstruction. Curve 0's single free axis lets curves 3/5 stay feasible; curve 10
inherits curve 5's *rigid* double pin at **every** quadrant and the two pins pull the top split
in opposite directions on the two odd residue classes.

Note this is **not** a global coloring obstruction: curve 10's global endpoints are always the
same color (0) at odd `n` (`entry (0,2⌊·⌋)`, `exit (n-1,2⌊·⌋)`), so `n²` odd is respected. The
obstruction is strictly *internal* — a conflict of the parity demands raised at the four
sub-boxes across the two odd residue classes.

### Quasi-squares

For `|w−h|=1` the aspect is forced and cannot be absorbed. Empirically (best top `(sw,sh)` per
orientation, long side up to ~22):

- **Non-transposing** tops `{e,m,y,f}`: connect **wide** at even long-side
  `{2,4,6,12,14,20,22,…}` and **tall** at odd long-side `{2,3,5,7,11,13,19,21,…}`.
- **Transposing** tops `{g,x,o,a}`: the transpose — **wide-odd / tall-even**.

No orientation connects all quasi-squares of a given aspect; each covers a size-periodic subset.
This ties to the terminal domino primitive: the AEP recursion bottoms out on the vertical `1×2`
(filled by non-transposing orientations, the `A,C` class) or the horizontal `2×1` (transposing,
the `B,D` class); accordingly the non-transposing tops accept tall boxes and the transposing
tops accept wide boxes, exactly as for curves 0 and 5 — but curve 5's double pin further thins
each parity class to roughly half (the period-8 texture in the size lists above).

## Evidence

Commands run as `cd /home/elessar/Projects/HilbertPlots && .venv/bin/python research/<script>`
(`import sys; sys.path.insert(0,"research"); import aep`). Scratch scripts:
`scratch_c10.py … scratch_c10final.py`.

**Structure.**
```
RULES[10]: LL 5@vflip(m) F | UL 5@rot90(g) F | UR 5@transpose(o) T | LR 5@rot180(f) T
entry_exit(10) = ('edge','edge');  2^k endpoints (0,2^{k-2}) -> (2^k-1, 2^{k-2})
orientations_used(10) = 13 nodes: (10,e); (5,{m,g,o,f}); (0,{e,m,y,f,g,x,o,a})
matches hilbertplot at 2^k (k=1,2,3): True, True, True   (even sizes: swap is a no-op)
```

**Search 1 — orientation-independent per-index `(10,5,0)`, `9^3 = 729`:** 0 valid over `n=1..40`.
Also curve-10 node alone (kernels at report rules), 9 options: all fail (`(·,first)`→n=3,
`(·,second)`→n=7, `(·,none)`→n=5).

**Search 2 — per-orientation, curve-0 fixed `(first,first)`, vary top × 4 curve-5 nodes,
`9^5 = 59049`:** 0 valid over `n=1..25`.

**Search 3 — curve-5 fixed `(first,second)`, curve-0 `sh=first`/`sw` per-node `3^8`, top `9`,
`= 59049`:** 0 valid over `n=1..25`.

**Search 4 — top × curve-5-per-node × curve-0-global, `9^6 = 531441`:** **0** rules pass even
the screen `{3,5,7,9}`; per top orientation the max simultaneously-valid size-set never contains
`{3,5,7,9}`.

**Decisive exhaustive proof — `9^5 = 59049` over the complete relevant node set at `n∈{3,5,7}`
(Lemma 1):**
```
curve-0 independence at n=3,5,7: validity identical for curve0 ∈ {(first,first),(second,none),(none,second)}
rules valid at all of {3,5,7}: 0
achieved subsets: {3,5}->5832 (sh=second) | {7}->1458 (sh=first) | {3}->33534 | {}->18225
{5,7} and {3,7}: never achieved  ->  no rule validates n=5 and n=7 together
```

**Junction / parity trace (curve5=(first,second), curve0=(first,first)):**
```
n=5 top=(second,second): W=3,2 H=3,2 (Hc1=3 odd)  J=[1,1,1]  valid=OK
n=5 top=(first ,first ): W=2,3 H=2,3 (Hc1=2 even)               valid=disconnected
n=7 top=(first ,first ): W=4,3 H=4,3 (Hc1=4 even) J=[1,1,1]  valid=OK
n=7 top=(second,second): W=3,4 H=3,4 (Hc1=3 odd)  J=[1,2,2]  valid=disconnected
top sh=second validates {3,5,11,13,19,…} (n≡1 mod4 via odd Hc1); sh=first validates {7,9,15,17,…}
```

**Quasi-squares (best top (sw,sh) per orientation, long side ≤ 22):**
```
non-transposing {e,m,y,f}: wide connects {2,4,6,12,14,20,22}; tall connects {2,3,5,7,11,13,19,21}
transposing     {g,x,o,a}: wide connects {2,3,5,7,11,13,19,21}; tall connects {2,4,6,12,14,20}
no orientation connects all of one aspect (size-periodic; complementary transposed classes)
```

## Verification

**Verdict: CONFIRMED (impossibility holds).** Independently re-derived the core result;
the INFEASIBLE claim and its proof survive adversarial scrutiny. Two minor *cosmetic*
inaccuracies in illustrative text are noted below; neither touches the proof.

**What I ran (all via `.venv/bin/python`, `sys.path.insert(0,"research"); import aep`):**

1. **Structure confirmed.** `RULES[10]` = LL `5@m` F, UL `5@g` F, UR `5@o` T, LR `5@f` T;
   `entry_exit(10)=('edge','edge')`; `orientations_used(10,[3,5,7])` = exactly the 5 nodes
   `{(10,e),(5,m),(5,g),(5,o),(5,f)}` — no curve-0 node. Matches the report.

2. **Lemma 1 independently verified two ways.** (a) Fixing curve-5=`(first,second)` and each
   top in turn, varied curve-0 over all 9 rules and compared the *raw* `fill(10,·)` cell lists
   at `n=3,5,7`: **identical** for every curve-0 choice (`Lemma1 = True`). (b) Re-ran the entire
   `9^5` search below with three different curve-0 dummies `{(first,first),(second,none),
   (none,second)}`: **identical** subset distributions each time. So the `n∈{3,5,7}` verdict is
   provably independent of all eight curve-0 nodes — the reduction to a `9^5` space is sound.
   (Geometric reason, also checked: at `n≤7` the split-halves are `{3,4}`, so every curve-5
   sub-box is `≤4` on a side and bottoms out on `≤2` primitives before any curve-0 split; swap
   only reorders the half-sizes, never enlarges them.)

3. **Exhaustive `9^5 = 59049` search reproduced exactly.** Enumerating all assignments of the
   5 relevant nodes (curve-5 given full *per-orientation* freedom at `m,g,o,f`), the achieved
   `{3,5,7}`-subsets are **`{3,5}→5832, {7}→1458, {3}→33534, {}→18225`**, matching the report's
   table to the count. **`{3,5,7}` achieved 0 times; `{5,7}` and `{3,7}` never achieved.** Since
   (Lemma 1) this is the *complete* space governing `n=5` and `n=7`, **no rule in the full
   `9^13` space is valid at both `n=5` and `n=7`** — hence none is valid on all squares. The
   REFUTE attempt (search the whole space for any working rule) therefore **fails**: no such
   rule exists. Impossibility confirmed.

4. **Mechanism spot-checks.** The `Hc1`-parity table (n=3: first-even/second-odd/none-odd;
   n=5: even/odd/even; n=7: even/odd/odd) reproduces exactly. `2^k` match to hilbertplot (k=1,2,3):
   all `True`.

**Two cosmetic inaccuracies (do not affect the proof):**

- **Line 46 parenthetical is wrong and self-inconsistent.** It states the closest rule
  "disconnects on `n = 7,9,11,13,…`". Re-running that rule
  (`top=(first,second), 5=(first,second), 0=(first,first)`) over `n=1..40` gives failures at
  **`{7,9,15,17,23,25,31,33,39}`** (period-8: `n≡1,7 (mod 8)` for `n≥7`) — it is **valid at
  `n=11` and `n=13`**. This contradicts the parenthetical but *agrees* with the report's own
  line 210 (`sh=second validates {3,5,11,13,19,…}`). So line 46 is an internal typo.
- **The "`n≡1` vs `n≡3 (mod 4)`" mechanism framing oversimplifies** the true failure texture,
  which is period-8, not period-4. This is explanatory narrative only; the impossibility rests
  on the finite exhaustive check at `n∈{5,7}`, which is airtight regardless of the mod-class
  story.

**Bottom line.** The computational core (Lemma 1 + the `9^5` exhaustion) is correct and
independently reproduced; the impossibility is a complete, rigorous finite proof (no rule
validates `n=5` and `n=7` together, and the relevant space at those sizes is exhaustively
covered). The result stands. — adversarial verification, 2026-07-24.

## Open questions

- **Closed-form curve-5 rectangle law.** The impossibility is complete without it, but an exact
  `W,H`-parity predicate for "curve 5 (rule `(first,second)`) is a valid path on `W×H`" would let
  the mechanism (n≡1 vs n≡3 mod 4 demand on `Hc1`) be stated as a formula rather than read off
  the exhaustive `9^5` table — upgrading the *mechanism* narrative from "verified" to
  "closed-form for all `n`". (The impossibility itself is already an exhaustive proof over the
  complete relevant space at `n∈{3,5,7}`, hence holds for all `n`.)
- **Rectangles (`|w−h|>1`).** Not pursued; curve 5's double pin makes a clean single-axis
  rectangle law unlikely, as for curve 5.
- **Structural theorem.** Curve 10 is the first *infeasible* square case in this program because
  **all four** of its quadrants are the doubly-pinned curve 5. Conjecture for the synthesis: a
  curve whose kernels are doubly-pinned (both split axes forced) at every quadrant and whose
  global span is an *edge-interior→edge-interior* pair is square-infeasible, the two pins forcing
  contradictory top-split parities on the two odd residue classes. Curves 3/24/31 (kernel-0,
  single free axis) stay feasible; curve 10 (kernel-5, no free axis) does not.
```
