# Curve 31 — Hilbert+Liu3 #14

- **kernels / quadrant rules** (visited LL, UL, UR, LR):
  - LL: base **0** (Hilbert), morph `((1,0),(0,-1))` (reflect‑y), rev `False`
  - UL: base **0** (Hilbert), morph `((0,-1),(1,0))` (rotation), rev `False`
  - UR: base **0** (Hilbert), morph `((0,1),(-1,0))` (rotation), rev `False`
  - LR: base **4** (Liu3),    morph `((1,0),(0,-1))` (reflect‑y), rev `False`

  Curve 31 is an *inverted‑U* whose three "outer" quadrants are the standard Hilbert
  curve (0) and whose lower‑right quadrant is Liu3 (curve 4). Its kernels are therefore
  `{0, 4}` plus itself; both kernels must carry correct swap rules, so the problem is
  solved bottom‑up (kernel 0 and kernel 4 first).
- **entry/exit type**: `('edge', 'interior')` — the global path enters on the left edge
  (mid‑height) and ends in the interior. Note: feasibility is *not* predicted by endpoint
  type (curve 4 is corner→interior and still generalizes); the real condition is derived
  below.

## Result

- **squares: FEASIBLE.**
- **swap rule (orientation‑independent):**

  | curve | width split `sw` | height split `sh` |
  |------:|:----------------:|:-----------------:|
  | 31    | `first`          | `second`          |
  | 4     | `second`         | `first`           |
  | 0     | `first`          | `first`           |

  (`first` = make the low/left half even; `second` = make the high/upper half even.)
  The kernel rules are exactly the known‑good orientation‑independent rules for curves 0
  and 4. Curve 31 needs no per‑orientation dependence: the single pair `(first, second)`
  works at every orientation it is drawn at.

- **verified:** valid `n×n` for **n = 1..40** (Hamiltonian path, confirmed by
  `aep.validate`); **matches hilbertplot at 2^k** (k=1,2,3) up to symmetry: **yes**
  (`square_valid(31, ·, check_2k=True) == True`).

- **quasi‑squares** (`|w−h|=1`): no single top‑level orientation connects all sizes.
  For every quasi‑square there are **exactly 4 of the 8 orientations** that connect
  (except the four small sizes `3×4,4×3,4×5,5×4`, where all 8 connect), and those 4
  always share one transpose class. Equivalently: the 8 orientations collapse to two
  canonical shapes `w×h` (the 4 non‑transpose orientations `{e, 180°, mirror‑x,
  mirror‑y}` ≈ Wu–Chang `A,C` + reflections) and `h×w` (the 4 transpose orientations
  `{diag, anti‑diag, ±90°}` ≈ `B,D` + rotations); the square rule connects a quasi‑square
  in **exactly one** of the two shapes. Which shape is size‑dependent and *irregular*
  (not a simple parity — see Evidence). So every quasi‑square is realizable by choosing
  the correct transpose class, but there is no orientation‑uniform rule.

## Derivation / proof

Throughout, work in the curve's canonical frame (orientation = identity), so the region
is `Wc × Hc`. `_split(d, mode)` returns `(d1, d2)` with `d1 = ⌊d/2⌋, d2 = ⌈d/2⌉`; `first`
forces `d1` even, `second` forces `d2` even (a swap only fires when the target half is
odd, hence only when `d` is odd).

### Lemma 1 (parity of the top split under `(first, second)`)

For **odd** `n`, curve 31's top‑level partition of an `n×n` square yields
`Wc1` **even**, `Wc2` **odd** (`Wc1+Wc2=n`, `first`) and `Hc1` **odd**, `Hc2` **even**
(`Hc1+Hc2=n`, `second`). For **even** `n`, all swaps are inert and
`Wc1=Wc2=Hc1=Hc2=n/2`, giving four equal quadrants — the standard equal‑quadrant
recursion that reproduces hilbertplot at `n=2^k` (verified: 2^k match = yes).

*Proof.* `n` odd ⇒ `⌊n/2⌋` and `⌈n/2⌉` have opposite parity. `first` makes `Wc1` (the
low half) even, so `Wc2=n−Wc1` is odd. `second` makes `Hc2` (the high half) even, so
`Hc1` is odd. `n` even ⇒ `⌊n/2⌋=⌈n/2⌉`, and swapping two equal halves changes nothing. ∎

The four sub‑boxes (odd `n`) therefore carry fixed parities:

| quad | curve | box (canonical) | size parity |
|:----:|:-----:|:----------------|:-----------:|
| LL | 0 | `(0,0,Wc1,Hc1)`      | even × odd  |
| UL | 0 | `(0,Hc1,Wc1,Hc2)`    | even × even |
| UR | 0 | `(Wc1,Hc1,Wc2,Hc2)`  | odd × even  |
| LR | 4 | `(Wc1,0,Wc2,Hc1)`    | odd × odd   |

### Lemma 2 (invariant entry/exit corners of the sub‑curves)

Under the swap rule above, for every odd `n ≥ 5` the four sub‑curves enter/exit at the
**same corners** of their boxes, independent of `n`:

```
LL (curve 0):  entry TL  →  exit TR
UL (curve 0):  entry BR  →  exit TR
UR (curve 0):  entry TL  →  exit BL
LR (curve 4):  entry TL  →  exit interior
```

(`n=3` is the sole degenerate case: LL is a `2×1` domino and LR a `1×1` cell, so "TL"
collapses to "BL"; connectivity still holds.) This corner‑invariance is a property of the
generalized kernels: curve 0's generalization (Wu–Chang, proven correct) is
corner→corner, and its entry/exit corners are pinned by the parity of the box it is given
— which is exactly what Lemma 1 fixes. Curve 4's generalization is corner→interior.
Verified: across all odd `n = 5..39` the quadruple of (entry, exit) corners takes a single
signature (see Evidence). ∎

### Lemma 3 (the three internal junctions connect)

Place the boxes by Lemma 1. Using the invariant corners of Lemma 2:

- **LL → UL.** LL exit `TR = (Wc1−1, Hc1−1)`; UL entry `BR = (Wc1−1, Hc1)`. Same column
  `x=Wc1−1`, adjacent rows ⇒ 4‑adjacent. ✔
- **UL → UR.** UL exit `TR = (Wc1−1, n−1)`; UR entry `TL = (Wc1, n−1)`. Same top row
  `y=n−1`, adjacent columns ⇒ 4‑adjacent. ✔
- **UR → LR.** UR exit `BL = (Wc1, Hc1)`; LR entry `TL = (Wc1, Hc1−1)`. Same column
  `x=Wc1`, adjacent rows ⇒ 4‑adjacent. ✔

Each junction lands on the shared edge between consecutive quadrants precisely because the
parities of Lemma 1 place the sub‑curve endpoints at the matching corners. ∎

### Theorem (square feasibility of curve 31)

With the swap rule `{31:(first,second), 4:(second,first), 0:(first,first)}`, `fill(31,·)`
is a single Hamiltonian path on every `n×n` square.

*Argument.* By induction on `n`. Base: `n≤2` are the primitives, valid by construction.
Even `n`: Lemma 1 gives four equal quadrants; the recursion is the standard 2^k
construction (matches hilbertplot, valid). Odd `n`: each sub‑curve is a valid Hamiltonian path
on its box — curves 0 (LL, UL, UR) by the Wu–Chang generalization, curve 4 (LR) by its
own verified generalization — and Lemma 3 shows the three junctions joining them are
4‑adjacent, so the concatenation LL·UL·UR·LR is a single Hamiltonian path on the whole
square. The corner invariants (Lemma 2) that Lemma 3 relies on are the induction
hypothesis applied to the kernels. ∎

**Why `(first, second)` and nothing else.** The corners in Lemma 2 are the *only* ones
that make all three junctions align, and they are produced *only* by the parity pattern
`Wc1` even / `Wc2` odd / `Hc1` odd / `Hc2` even. Any other choice for curve 31's split
flips at least one sub‑box parity, moves an endpoint off the matching corner, and breaks a
junction. This is confirmed exhaustively: among the 9 orientation‑independent pairs for
curve 31 only `(first, second)` survives; the other eight fail at small `n` (e.g.
`(first,first)` and `(second,first)` fail already at `n=3`, `(none,none)` at `n=5`,
`(second,second)` at `n=11`). Likewise curve 4 is forced to `(second,first)`.

**The curve‑0 degeneracy.** In the full per‑orientation search the curve‑0 nodes accept
their **height** split fixed at `first` but leave the **width** split free
(`first/second/none` all valid). This is a genuine degeneracy: in the contexts where
curve 0 appears here its width partition does not affect the endpoint corners that the
junctions test, so all three width modes concatenate identically. It accounts for the
solution‑count factorization below (`3^4` free curve‑0 width choices).

## Evidence

Engine: `research/aep.py`; run as `.venv/bin/python` with `sys.path.insert(0,"research")`.

**Partition nodes** (`aep.orientations_used(31)`) — 6 nodes:
```
(31, ((1,0),(0,1)))                       # the top curve
(0,  ((1,0),(0,-1)))  (0, ((0,-1),(1,0)))  (0, ((0,1),(-1,0)))  (0, ((-1,0),(0,1)))  # 4 Hilbert
(4,  ((1,0),(0,-1)))                       # 1 Liu3
kernels used: [0, 4, 31]
```

**(A) Orientation‑independent search for curve 31** (9 candidates, kernels fixed at
`0:(first,first), 4:(second,first)`), validated on `n=1..40` + 2^k match:
```
valid (sw,sh) among 9:  [('first','second')]        # unique
space explored (A):     9
```

**(B) Full per‑orientation search** over all 6 nodes, each ∈ {first,second,none}²:
```
full per-orientation space size = 9^6 = 531441      # exhaustively enumerated
survivors over n=1..15:                 243
confirmed over n=1..40 + 2^k match:      81  =  3^4
per-node valid rules:
  c31 (1,0),(0,1)   : [('first','second')]                                # forced
  c4  (1,0),(0,-1)  : [('second','first')]                                # forced
  c0  (all 4 M)     : [('first','first'),('none','first'),('second','first')]  # height=first forced, width free
```
So the 81 solutions factor as `31=(first,second)` × `4=(second,first)` × `(c0 height=first,
width∈{first,second,none})^4`. The canonical orientation‑independent rule
`0:(first,first)` is the representative used everywhere else in the study.

**Junction geometry** (top split, good rule), confirming Lemmas 1–3:
```
n=5: Wsplit(first)=(2,3) Hsplit(second)=(3,2)
  LL c0 box(0,0,2,3) entry(0,2)TL exit(1,2)TR
  UL c0 box(0,3,2,2) entry(1,3)BR exit(1,4)TR
  UR c0 box(2,3,3,2) entry(2,4)TL exit(2,3)BL
  LR c4 box(2,0,3,3) entry(2,2)TL exit(3,1)interior
  LL->UL dist=1  UL->UR dist=1  UR->LR dist=1   (all OK)
# identical corner signature for all odd n=5..39 (2 signatures total, the second is only n=3)
```

**Forcing evidence** (wrong curve‑31 rule, kernels fixed) — first failing `n`:
```
(first,first): n=3    (second,first): n=3    (none,none): n=5    (second,second): n=11
```

**Quasi‑squares** (`|w−h|=1`), good rule:
```
distribution of #connecting-orientations per size (base 2..39): {4: 72, 8: 4}
of the 72 four-orientation cases, all-same-transpose-flag: 72/72
all-8 sizes: (4,3),(3,4),(5,4),(4,5)
```
IDENT orientation, wide `w=h+1` (irregular in `n`, not a parity):
```
h : 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
w : 2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
OK: Y  .  Y  Y  Y  .  Y  .  Y  .  .  Y  Y  .  Y
```
For any fixed quasi‑square the connecting orientations are exactly one transpose class
(all non‑transpose = present the region as `w×h`, or all transpose = present it as `h×w`),
so choosing the transpose class realizes every quasi‑square; the required class is
size‑dependent. This is the top‑level image of the `1×2`(A,C) / `2×1`(B,D) domino
constraint: the transpose flag decides whether the deepest recursion lays tall (`1×2`) or
wide (`2×1`) dominoes, and the square‑tuned rule connects only the shape whose terminal
dominoes are compatible.

All outputs above are reproducible from `research/aep.py` via the calls named inline
(`orientations_used`, `fill`/`validate`, `square_valid`, and exhaustive `itertools.product`
sweeps of the swap space).

## Open questions

- **All‑`n` formalization.** Lemmas 1–3 give a structural induction resting on the
  entry/exit‑corner invariants of the *generalized* kernels 0 and 4. Curve 0's invariant
  is Wu–Chang (proven); curve 4's corner→interior invariant is verified over `n=1..40` but
  not yet independently proved. Completing curve 4's endpoint‑corner lemma would upgrade
  the square theorem from "verified n=1..40 + structural proof" to fully formal for all
  `n`.
- **Curve‑0 width degeneracy.** A clean statement of *why* the curve‑0 width split is a
  don't‑care in these contexts (rather than case‑checked) would tighten the derivation.
- **Quasi‑square selector.** Characterize, as a function of `n`, which transpose class
  connects the `(n±1)×n` quasi‑square. Empirically irregular; likely governed by the
  binary structure of `n` (the recursion of splits), analogous to Wu–Chang's odd‑size
  bookkeeping.
- **Rectangles** (`w×h`, general): not probed here beyond quasi‑squares.

## Verification

Independent adversarial re-check against `research/aep.py` (all runs via
`.venv/bin/python` with `sys.path.insert(0,"research")`). **Verdict: CONFIRMED.**

**1. Computational confirmation of the reported rule.** With
`const_swap({31:(first,second), 4:(second,first), 0:(first,first)})`:
- `aep.validate(fill(31,0,0,n,n,IDENT,False,sw),n,n)=="OK"` for **every** `n=1..40`
  (0 failures).
- `square_valid(31, sw, sizes=range(1,41), check_2k=True) == True` (Hamiltonian on all
  40 squares AND matches hilbertplot at `2^k`, k=1,2,3). The two kernels also independently
  pass: `square_valid(0,·)` and `square_valid(4,·)` are both `True` over `n=1..40`.

**2. Uniqueness / forcing (reproduced).**
- `orientations_used(31)` = the **6** nodes listed (kernels `{0,4,31}`). ✔
- Orientation‑independent search over the 9 candidates for curve 31 (kernels fixed):
  only `('first','second')` survives `n=1..40`+2^k. ✔
- Wrong‑rule first‑failure sizes reproduced exactly:
  `(first,first)→3, (second,first)→3, (none,none)→5, (second,second)→11`. ✔

**3. Full per‑orientation search (independently re‑run, not trusted from the report).**
Exhaustive enumeration of all `9^6 = 531441` assignments over the 6 nodes, cheap‑filtered
on odd `n∈{3..15}` then confirmed on `n=1..40`+2^k, gives **exactly**:
```
total space 531441 → 243 cheap survivors → 81 confirmed  (= 3^4)
c31 (1,0),(0,1) : [('first','second')]                                   # forced
c4  (1,0),(0,-1): [('second','first')]                                   # forced
each c0 node    : [('first','first'),('none','first'),('second','first')] # height=first forced, width free
```
This matches §Evidence (B) line-for-line, including the `3^4` factorization and the
curve‑0 width don't‑care.

**4. Junction geometry (Lemmas 1–3 re‑derived from cells).** Extracting the actual
sub‑curve endpoint corners under the good rule:
- Single corner signature for **all** odd `n=5..39`:
  `LL TL→TR, UL BR→TR, UR TL→BL, LR TL→interior` — exactly Lemma 2.
- `n=3` is the sole degenerate signature (LL domino / LR `1×1`), as the report states.
- All three internal junctions have Manhattan distance `1` for every odd `n=3..39`
  (verified, not just `n=5`), so Lemma 3's adjacency holds throughout the tested range.

**5. Quasi‑squares (reproduced).** Distribution `{4:72, 8:4}`; all 72 four‑orientation
cases have a single transpose flag (`72/72`); the four all‑8 sizes are the small
`3×4,4×3,4×5,5×4`. The IDENT wide row is reproduced identically:
`Y . Y Y Y . Y . Y . . Y Y . Y` for `h=1..15`.

**6. Rigor assessment of the derivation.** The FEASIBILITY claim is correct and the
structural proof (Lemmas 1–3 + induction) is internally sound: Lemma 1's parities follow
from `_split`; Lemmas 2–3 are exactly the observed corner/adjacency data. The **one
genuine gap is honestly disclosed by the report itself**: the induction rests on the
entry/exit‑corner invariants of the *generalized* kernels — curve 0's is Wu–Chang
(proven), but curve 4's corner→interior invariant is only *verified* over `n=1..40`, not
proved for all `n`. The report does not overclaim: it labels the result
"verified n=1..40 + structural proof" and lists the all‑`n` formalization as an open
question. No error or overreach found. — verifier
