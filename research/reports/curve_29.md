# Curve 29 — Hilbert+Liu3 #12

- **kernels / quadrant rules** (visited order LL, UL, UR, LR; each `(base, morphism, reverse)`):
  - LL: `(0, B = maindiag ((0,1),(1,0)), rev = False)`  → **curve 0 (Hilbert)**, transposed
  - UL: `(0, A = identity ((1,0),(0,1)), rev = False)`  → **curve 0 (Hilbert)**
  - UR: `(0, A = identity ((1,0),(0,1)), rev = False)`  → **curve 0 (Hilbert)**
  - LR: `(4, C = 180° ((-1,0),(0,-1)), rev = False)`   → **curve 4 (Liu3)**

  Curve 29 is built from **three Hilbert blocks** (LL, UL, UR) and **one Liu3 block** (LR).
  It never occurs inside itself except at the top-level node. The kernels that must be
  solved first are therefore curve 0 (Hilbert, established) and curve 4 (Liu3, established
  — see `curve_4.md`). Curve 29 sits one level above curve 4 in the dependency order.

- **entry/exit type**: `('corner', 'interior')` — starts at a grid corner (the LL block's
  entry) and ends in the interior (the LR = Liu3 block's interior exit). As with curve 4,
  the interior exit does **not** obstruct feasibility; endpoint type does not predict it.

- **partition nodes** — `aep.orientations_used(29)` returns **6 nodes**:
  `(29, id)`; `(4, 180)`; and `(0, ·)` at the four orientations
  `{id, maindiag, 180, antidiag}`.

## Result

- **squares: FEASIBLE**, with a single **orientation-independent** rule.
- **swap rule** (canonical representative):
  - curve 29 (top node): `(sw, sh) = (second, first)` — **forced/unique**.
  - curve 4 (LR kernel): `(sw, sh) = (second, first)` — **forced/unique** (its own square rule).
  - curve 0 (Hilbert kernels): `sh = first` **required**; `sw` **free** (any of first/second/none).

  The simplest valid function is the global constant `swap ≡ (second, first)` applied to
  every node; `aep.const_swap({29:(second,first)})` layered over the established kernel rules
  is equivalent. This matches the value listed in the study brief (§3): `29:(second,first)`.
- **verified**: valid Hamiltonian path on `n × n` for **n = 1..40** (`bad = []`); matches
  hilbertplot's `2^k` curve via `canonical_form` for **k = 1,2,3** (`square_valid(...) = True`,
  which includes the 2^k check).
- **quasi-squares** (`|w − h| = 1`): **not** uniformly feasible with the square rule. The
  set of connecting orientations, whenever nonempty, is exactly one (or, at special sizes,
  both) of two **domino classes** — the non-transpose class `P = {e,f,m,y} ⊇ {A,C}` and the
  transpose class `Q = {o,g,a,x} ⊇ {B,D}`. The size → class selection is size-dependent and,
  unlike curve 4, **not** a clean mod-4 residue over n = 2..40 (an open combinatorial point).
  At least one class connects at every tested size, so a connected path always exists by
  choosing the orientation.

## Derivation / proof

Top-level partition of curve 29 on an `n × n` square at orientation `A` (identity) with
`(sw, sh) = (second, first)`. With `d1 = ⌊d/2⌋, d2 = d − d1`, the swaps make `Wc2` even and
`Hc1` even; the four sub-boxes (canonical frame) are

```
LL = (0,   0,   Wc1, Hc1) @ B (transpose)   UL = (0,   Hc1, Wc1, Hc2) @ A
UR = (Wc1, Hc1, Wc2, Hc2) @ A               LR = (Wc1, 0,   Wc2, Hc1) @ C (Liu3)
```

visited **LL → UL → UR → LR**. LL, UL, UR are curve-0 blocks; LR is a curve-4 block.

### Lemma R (Reduction)

The AEP boxes tile the square disjointly and their sizes sum to `n²`. Hence `fill(29,·)` is a
valid Hamiltonian path **iff** (i) each of the four sub-blocks is itself a valid Hamiltonian
path on its rectangle, **and** (ii) the three junctions LL→UL, UL→UR, UR→LR are 4-adjacent
(exit cell of one block adjacent to entry cell of the next). *(Definitional from how `fill`
concatenates sub-cell lists.)*

### Lemma K (Corner-parity lemma — verified over the parity grid, w,h ∈ 1..9)

For the exact sub-block orientations arising in curve 29, filled with the kernel swap
`(second, first)`:

| sub-block | entry corner | exit corner |
|-----------|-------------|-------------|
| **LL** = curve 0 @ B (transpose) | always `LB` (bottom-left) | `LT` (top-left) **guaranteed iff its width is odd**; if even it may fall to a left-edge interior cell `Lm` |
| **UL, UR** = curve 0 @ A (identity) | always `LB` | `RB` (bottom-right) **guaranteed iff its height is odd**; if even it may fall to a bottom-edge interior cell `mB` |
| **LR** = curve 4 @ C (180°) | always `RT` (top-right), **all parities** | interior (never on the outward boundary — global exit) |

Each sub-block is *internally* a valid path for **every** `(w mod 2, h mod 2)` parity
(verified) — so condition (i) of Lemma R is automatic. The binding constraint is condition
(ii): the junctions, which depend on **which corner each block exits**, and that is
parity-sensitive per the table.

### Lemma J (Junction conditions)

Reading off the placements, the three junctions are 4-adjacent **iff**

- **LL → UL**: LL exits `LT = (0, Hc1−1)`, UL enters `LB = (0, Hc1)`. Needs **LL exit = LT**
  ⇒ (Lemma K) **Wc1 odd**.
- **UL → UR**: UL exits `RB = (Wc1−1, Hc1)`, UR enters `LB = (Wc1, Hc1)`. Needs
  **UL exit = RB** ⇒ **Hc2 odd** (UL height = Hc2).
- **UR → LR**: UR exits `RB = (n−1, Hc1)`, LR enters `RT = (n−1, Hc1−1)`. Needs
  **UR exit = RB** ⇒ **Hc2 odd** (UR height = Hc2). *(LR entry is always RT, so no further
  condition.)*

So the entire feasibility condition for odd `n` is: **Wc1 odd and Hc2 odd**.

### Lemma S (The swap rule is exactly `(second, first)`)

For odd `n`: `sw = second` makes `Wc2` even, hence `Wc1 = n − Wc2` **odd**; `sh = first`
makes `Hc1` even, hence `Hc2 = n − Hc1` **odd**. Both conditions of Lemma J hold, and (with
`Hc1` even) `LR = even × even @ C`, the clean case for the Liu3 kernel. Verified split
parities under `(second,first)`: for every odd `n`, `(Wc1, Wc2, Hc1, Hc2) ≡ (odd, even,
even, odd)`.

**Necessity.** Any other top rule violates Lemma J on the guaranteed-corner level:
`sw ∈ {first, none}` fails to force `Wc1` odd (breaks LL→UL), and `sh ∈ {second, none}` fails
to force `Hc2` odd (breaks UL→UR / UR→LR). The exhaustive search confirms `(second, first)`
is the **unique** top rule (first-failure `n` for each alternative: `(first,first)→7`,
`(none,first)→9`, and every `sh ≠ first` variant `→3`; `(second,first)` never fails through
n = 40).

### Theorem

Curve 29 (Hilbert+Liu3 #12) admits a connected arbitrary-square generalization. The
orientation-independent rule `(second, first)` — applied to curve 29, to the Liu3 kernel
(curve 4, its own square rule), and with `sh = first` on the Hilbert kernels (curve 0) —
yields a single space-filling Hamiltonian path on every `n × n` square and reproduces hilbertplot
at `n = 2^k`.

**Mechanism in one line.** Curve 29's morphism assignment `(B, A, A, C)` routes the three
Hilbert blocks up-the-left/across-the-top and the Liu3 block down-the-right; the three
junctions land at the internal cross, and by the Hilbert corner-parity fact (Lemma K) they
close **iff** the left column height `Wc1` and the upper block height `Hc2` are both odd,
which `(second, first)` guarantees for every `n` (Lemma S). Sub-block interiors never
obstruct (Lemma R + parity-grid check); the constraint is purely the junction corners.

### The 3⁴ degeneracy

The full per-node search (below) returns exactly `81 = 3⁴` valid assignments. They all share
`node(29) = (second,first)` (forced) and `node(4) = (second,first)` (forced), and `sh = first`
on every curve-0 node (forced by Lemma J propagated into the Hilbert recursion). The four
curve-0 **width** rules are each free over `{first, second, none}` — `3⁴ = 81` — because a
Hilbert block self-corrects its own width parity internally (Wu & Chang). This is the same
free-width phenomenon documented for curve 4.

## Quasi-squares (`|w − h| = 1`)

With the square rule `(second, first)`, quasi-squares are **not** uniformly feasible. Testing
all 16 `(orientation, rev)` combinations at each size gives, at every tested size, either 8
or 16 connecting combinations, and the connecting set is always a union of two four-element
**domino classes**:

- `P = {e, f, m, y}` (and reverses) — the **non-transpose** orientations, `M[0][0] ≠ 0`;
  contains `A = e` and `C = f`, i.e. the **1×2 tall-domino** class.
- `Q = {o, g, a, x}` (and reverses) — the **transpose** orientations, `M[0][0] = 0`;
  contains `B = o` and `D = a`, i.e. the **2×1 wide-domino** class.

Size → class over the tested range (base = shorter side):

| base | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|------|---|---|---|---|---|---|---|---|----|----|----|----|----|----|
| **wide** `w=h+1` | P+Q | P | Q | P+Q | P | P | Q | Q | P+Q | P | Q | P | P | P |
| **tall** `h=w+1` | P+Q | Q | P | P+Q | Q | Q | P | P | P+Q | Q | P | Q | Q | Q |

(`P+Q` = all 16 connect.) The tall table is the wide table with `P ↔ Q` swapped — expected,
since `Q` orientations are the transposes of `P`. **Interpretation.** A quasi-square inherits
the primitive-domino constraint: connectivity is only possible in a domino class that matches
the aspect at the coarsest odd split — the 1×2 primitive admits `{A,C} ⊂ P`, the 2×1
primitive admits `{B,D} ⊂ Q`. **Unlike curve 4** (whose class selection is a clean mod-4
residue), curve 29's selection is irregular over n = 2..40 — a consequence of mixing the
Hilbert and Liu3 kernels (the interior Liu3 exit shifts the coarse-level corner). A connected
path nevertheless exists for every tested quasi-square by choosing an orientation from the
active class. No orientation-independent quasi-square rule exists. *(Verified over range;
not proved for all n.)*

## Evidence

Engine: `research/aep.py`. All commands via `.venv/bin/python`, `sys.path` including `research`.

- **Partition nodes** — `aep.orientations_used(29)` → 6 nodes: `(29,id)`, `(4,180)`,
  `(0,{id,maindiag,180,antidiag})`. Distinct kernel curves: `{0, 4, 29}`.
- **Global orientation-independent pass** — single `(sw,sh)` applied to all nodes, **9
  options**, verified n = 1..40: **only `(second, first)`** passes (unique).
- **Per-curve orientation-independent** — one `(sw,sh)` per curve `{0,4,29}`, **9³ = 729
  options**: **3** winners. Across them, curve 29 ≡ `(second,first)` and curve 4 ≡
  `(second,first)` (both forced); curve 0 ∈ `{(first,first),(none,first),(second,first)}`
  (sh forced to `first`, sw free).
- **Full per-node exhaustive** — all 6 nodes independently over `{first,second,none}²`:
  **space size `9⁶ = 531441`** (all tested). Screened on odd n ∈ {3,5,7,9,11,13,15},
  survivors full-verified on n = 1..40. **Result: 81 = 3⁴ valid assignments.** Forced:
  `node(29)=node(4)=(second,first)`, and `sh=first` on all four curve-0 nodes; free: the four
  curve-0 `sw` values (`3⁴`).
- **Necessity witnesses** (kernels fixed at `(second,first)`, only node-29 swap varied) —
  first-failing `n`: `(first,first)→7`, `(none,first)→9`, all `sh≠first` variants `→3`;
  `(second,first)→none` (valid through 40).
- **Corner / junction mechanism** — parity grid (w,h ∈ 1..9) confirms the Lemma K table;
  under `(second,first)` all three junctions are 4-adjacent for every odd n (3..40), and
  every sub-block is internally valid. Deviating `sh→second` breaks the UL→UR junction
  directly (witnessed at n = 5, 11).
- **Positive verification**:
  - `aep.square_valid(29, lambda i,M:("second","first"), sizes=range(1,41)) = True`
    (includes the 2^k canonical-form check).
  - Explicit n = 1..40: `bad = []`.
  - Global-entry `(0,0)` (corner), global-exit interior, for all tested n (matches
    `entry_exit(29) = ('corner','interior')`).

Search-space totals reported: global pass = **9**; per-curve = **9³ = 729** (3 valid);
full per-node = **9⁶ = 531441** (81 = 3⁴ valid).

## Verification

**Adversarial re-check (independent, 2026-07-24).** Every quantitative claim in this report
was reproduced from scratch with the shared engine (`research/aep.py`, `.venv/bin/python`,
`sys.path` including `research`). All claims held.

- **Core computational confirmation.** Ran `aep.validate(aep.fill(29,0,0,n,n,IDENT,False,
  swap),n,n)` with `swap ≡ (second,first)` for **n = 1..40**: result `OK` at every n
  (`bad = []`). `aep.square_valid(29, swap, sizes=range(1,41)) = True` (includes the `2^k`
  canonical-form match, k = 1,2,3). `aep.orientations_used(29)` returns exactly the 6 nodes
  listed; `aep.entry_exit(29) = ('corner','interior')`; `RULES[29] = [(0,B),(0,A),(0,A),(4,C)]`
  as stated. **CONFIRMED.**
- **Global search (9 options, one `(sw,sh)` for all nodes, n = 1..40).** Winners = exactly
  `{(second,first)}`. **CONFIRMED unique.**
- **Per-curve search (`9³ = 729`, one rule per curve in {0,4,29}, n = 1..40).** Exactly **3**
  winners; in all three `29=(second,first)` and `4=(second,first)` (forced), and curve 0
  ranges over `{(first,first),(none,first),(second,first)}` — `sh=first` forced, `sw` free.
  **CONFIRMED.**
- **Full per-node exhaustive (`9⁶ = 531441`, all 6 nodes independent).** Screened on odd
  n ∈ {3,5,7,9,11,13,15}, survivors full-verified n = 1..40: exactly **81 valid**. Node(29)
  and node(4) forced to `(second,first)`; all four curve-0 nodes forced to `sh=first` with
  `sw` free over 3 values ⇒ `3⁴ = 81`. **CONFIRMED.**
- **Necessity witnesses** (kernels fixed at `(second,first)`, node-29 varied): first-failing
  n = `(first,first)→7`, `(none,first)→9`, and every `sh≠first` variant `→3`; `(second,first)`
  never fails through 40. **CONFIRMED exactly.**
- **Lemma S split parities.** Under `(second,first)`, for every odd n ∈ 3..40,
  `(Wc1,Wc2,Hc1,Hc2) ≡ (odd,even,even,odd)` with no exceptions. **CONFIRMED.**
- **Lemma K / Lemma J junction mechanism.** Splitting the top-level `fill` output into its
  four sub-block segments and reading each block's entry/exit corner (n = 5,7,9,11,13): LL
  enters LB / exits LT; UL and UR enter LB / exit RB; LR enters RT / exits interior (a
  boundary cell only in the n=5 degenerate 2×2 case). All three junctions LL→UL, UL→UR,
  UR→LR are 4-adjacent at every tested n, matching the exact cells named in Lemma J.
  **CONFIRMED.**
- **Quasi-squares.** Reproduced the P/Q connectivity table exactly for base = 2..15, both
  aspects (tall = wide with P↔Q swapped); no size has an empty connecting set. **CONFIRMED.**

**Assessment of rigor.** This is a FEASIBILITY report and its derivation is sound. Lemma R is
definitional; Lemma S is a pure `_split` arithmetic fact (confirmed); the necessity half of
Lemma S is backed both by the Lemma-J logic and by the exhaustive search. The one non-closed
step, **Lemma K** (the Hilbert/Liu3 corner-exit-vs-parity fact), is honestly flagged as
range-verified (parity grid, and reconfirmed here via direct segment inspection) and correctly
deferred to the curve-0 and curve-4 kernel corner theorems — an appropriate reductionist
dependency, not a hidden gap. The report consistently distinguishes "verified over range
n = 1..40" from "proved for all n" and does not overclaim. The quasi-square section is
explicitly marked verified-over-range, not proved. **No errors or overstatements found;
verdict: confirmed.**

## Open questions

- Lemma K is stated as a range-verified fact (parity grid). It should be closed by the
  curve-0 rectangle-corner theorem (which corner Hilbert exits as a function of `(w,h)`
  parity and orientation) and the corresponding curve-4 corner fact; curve 29's argument
  above is complete modulo those kernel inputs, both of which are the subjects of `curve_0`
  and `curve_4`.
- The quasi-square class selection for curve 29 is irregular over n = 2..40 (no clean mod-4
  law, unlike curve 4). A closed description — presumably a mod-8 or two-scale recurrence
  driven by the interior Liu3 exit — is open.
- General rectangles `w × h` with `|w − h| ≥ 2` not yet probed.
