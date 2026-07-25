# Curve 24 — Hilbert+Liu3 #7

- **kernels / quadrant rules** (visited order LL, UL, UR, LR; each `(base, morphism, reverse)`):
  | quadrant | base | morphism `M` | reverse |
  |----------|------|--------------|---------|
  | LL | 0 (Hilbert) | `m = ((1,0),(0,-1))` = **vflip** | False |
  | UL | 0 (Hilbert) | `g = ((0,-1),(1,0))` = **rot90 (CCW)** | False |
  | UR | 0 (Hilbert) | `x = ((0,1),(-1,0))` = **rot270 (CW)** | False |
  | LR | **4 (Liu3)** | `x = ((0,1),(-1,0))` = **rot270 (CW)** | False |

  Three quadrants recurse into **kernel curve 0 (Hilbert)**; the LR quadrant recurses into
  **kernel curve 4 (Liu3)**. Curve 4's own four quadrants are all curve 0. So the kernel
  dependency chain is `24 → {0, 4}` and `4 → {0}`, solvable **bottom-up**: fix curve 0,
  then curve 4, then curve 24. Curve 24 never appears inside itself; it occurs only as the
  top-level node.
- **entry/exit type:** `entry_exit(24) = ('edge','interior')` — global entry on a grid edge,
  global exit in the interior. (As with curve 4, the interior exit does **not** block square
  feasibility; endpoint type is not the criterion.)
- **partition nodes** (`orientations_used(24)`), the `(curve, orientation)` pairs that need a
  swap rule — exactly **6 nodes**, a closed set:
  - `(24, e)` — curve 24 at identity (the only curve-24 node);
  - `(4, x)` — curve 4 at rot270 (the only curve-4 node);
  - `(0, m)`, `(0, g)`, `(0, x)`, `(0, y)` — curve 0 at vflip / rot90 / rot270 / hflip.
  The curve-0 orientation coset `{m,g,x,y}` is closed under the recursion (curve 0 folds
  into these four orientations of itself).

## Result

- **squares: FEASIBLE**, with an **orientation-independent** rule (one `(sw,sh)` per curve
  index; each curve appears only at orientations sharing that rule).
- **swap rule** — the composite
  ```
  const_swap({24: (first, second),   # curve 24 top node
              4:  (second, first),   # LR kernel = curve 4
              0:  (first,  first)})  # Hilbert kernels: only sh = first is required
  ```
  Per-node, over the full valid set the pins are:
  | node | `sw` (canonical width-split) | `sh` (canonical height-split) |
  |------|------------------------------|-------------------------------|
  | `(24, e)` | **pinned `first`** | **pinned `second`** |
  | `(4, x)`  | **pinned `second`** | **pinned `first`** |
  | `(0, m/g/x/y)` | free `{first,second,none}` | **pinned `first`** |

  Note curve 24's own rule `(first,second)` matches the curve-3/5/24/31 family, and the LR
  child carries **curve 4's own square rule** `(second,first)` verbatim — curve 24's
  generalization is literally curve-3's construction with its LR quadrant replaced by an
  embedded curve-4 square.
- **verified:** valid Hamiltonian path on `n × n` for **n = 1..40** (`bad = []`); **matches
  hilbertplot at `2^k`** for k = 1,2,3,4 (via `canonical_form`): **yes**. Also valid on squares
  under **all 8 top-level D4 orientations** (both `rev` values, n = 1..25), so the rule is
  genuinely orientation-independent even at the top level.
  `square_valid(24, comp, sizes=range(1,41)) = True`.
- **quasi-squares** (`|w−h| = 1`): **not** uniformly feasible with the square rule. At every
  quasi-square size exactly **4 of the 8** orientations connect, and they always form a
  complete D4 transpose-coset — either the non-transposing class `{e,f,m,y}` (identity,
  rot180, vflip, hflip) or the transposing class `{a,g,o,x}` (rot90, rot270, main-diag,
  anti-diag). Which coset connects is selected by the size; **no single orientation connects
  all** wide (or all tall) quasi-squares. (Verified n = 3..40.)

## Derivation / proof

Work in the canonical frame (top level `M = e`, no transpose, `Wc = Hc = n`). With rule
`(sw,sh) = (first, second)`: `sw = first` makes the **low** width-half `Wc1` even, `sh =
second` makes the **high** height-half `Hc2` even. For odd `n` (`n = Wc1+Wc2 = Hc1+Hc2`):

```
Wc1 even, Wc2 odd ;  Hc1 odd, Hc2 even.
```

The four sub-boxes (canonical frame), visited LL → UL → UR → LR, are

```
LL = (0,   0,   Wc1, Hc1) @ m   (even × odd, Hilbert)
UL = (0,   Hc1, Wc1, Hc2) @ g   (even × even, Hilbert)
UR = (Wc1, Hc1, Wc2, Hc2) @ x   (odd  × even, Hilbert)
LR = (Wc1, 0,   Wc2, Hc1) @ x   (odd  × odd,  CURVE 4)
```

### Lemma 1 (Junction auto-adjacency — parity-free joins)

For **every** split `(Wc1,Wc2,Hc1,Hc2)` the three internal junctions are 4-adjacent,
independent of parity. Verified for n = 3..40: junction displacement vector is `[1,1,1]`
at every n (`all junctions=[1,1,1] n=3..40: True`). Example n=5, boxes `(Wc1,Wc2,Hc1,Hc2)
= (2,3,3,2)`, junctions `[1,1,1]`. The morphism assignment `(m,g,x,x)` is chosen precisely
so consecutive blocks meet at the shared cell-corner of the internal cross and those corner
cells are always unit-adjacent — exactly the curve-3/curve-4 mechanism. Hence the joins
impose **no** parity constraint; this is why curve 24 is feasible despite its interior exit.

### Lemma 2 (Reduction to the four sub-blocks)

By Lemma 1 the parent junctions cost nothing, and each block is entered/exited once (single
contiguous run). Therefore curve 24 on `n × n` is a valid path **iff every sub-block is
itself valid** on its rectangle: LL, UL, UR as **curve-0** blocks and LR as a **curve-4**
block. All remaining parity constraints come from sub-block fillability, not from curve 24's
own geometry. Verified: with the composite rule all four sub-blocks are valid for n = 3..40
(`all sub-blocks valid (origin-normalized) n=3..40: True`).

### Lemma 3 (The three Hilbert blocks — `sh = first` on the kernel)

LL, UL, UR are curve-0 rectangles at orientations `{m,g,x}`. Curve 0 under AEP is a valid
corner-terminating Hilbert path on these rectangles exactly when the swap makes the correct
half even; for this orientation coset the condition is the canonical-**height** pin `sh =
first` on every curve-0 node (the same pin curve 3 requires). This is what the exhaustive
search reports as the forced column, and it rests on curve 0's established Wu–Chang
arbitrary-rectangle corner-to-corner property.

### Lemma 4 (The LR block is a curve-4 SQUARE — this is why curve-24 `sw` is pinned)

The decisive structural fact distinguishing curve 24 from curve 3: its LR child is **curve
4**, and curve 4 generalizes only to *squares* (and a restricted parity of rectangles) at a
given orientation. With `sw = first` (`Wc2` odd) and `sh = second` (`Hc1` odd) the LR box is
`Wc2 × Hc1 = odd × odd` — always a **square** (`Wc2 = Hc1` for odd n, since `Wc2 = ⌈n/2⌉ =
Hc1`). Curve 4 fills it with its own square rule `(second, first)`:

```
sw = first  ⇒ LR shapes (n=5..25): 3x3,3x3,5x5,5x5,7x7,7x7,...  all valid = True
sw = second ⇒ LR shapes (n=5..25): 2x3,4x3,4x5,6x5,6x7,...      all valid = False
```

Choosing `sw = second` instead makes `Wc2` even, turning LR into a non-square `even × odd`
rectangle at orientation `x`, which curve 4 **cannot** fill (disconnected). Hence `sw =
first` is **forced** — not by any junction, but by the requirement that the LR quadrant hand
curve 4 the one shape it fills: an odd×odd square. This is the precise reason curve 24's
`sw` is pinned whereas curve 3's (all-Hilbert kernels) `sw` is free.

### Theorem

Curve 24 (Hilbert+Liu3 #7) admits a connected arbitrary-square generalization. The
orientation-independent composite swap rule
`{24:(first,second), 4:(second,first), 0:(·,first)}` yields a single space-filling
Hamiltonian path on every `n × n` square and reproduces hilbertplot at `n = 2^k`.

**Mechanism in one line:** curve 24 is curve 3's construction (parity-free junctions from
morphisms `m,g,x,x`; three Hilbert blocks pinned by `sh=first`) with its LR quadrant an
embedded **curve-4 odd×odd square**, whose squareness forces the extra pin `sw=first` and
whose fill uses curve 4's own square rule `(second,first)`.

## Quasi-squares (`|w − h| = 1`)

With the square rule the aspect ratio is forced and the odd length cannot be absorbed on a
free axis. Empirically (n = 3..40) exactly **4 of 8** orientations connect at each size, and
they always form one complete transpose-coset:

- non-transposing class `{e, f, m, y}` (= the tall-domino `1×2` class), or
- transposing class `{a, g, o, x}` (= the wide-domino `2×1` class).

Sample (wide `w = h+1`): `h=5 → {e,f,m,y}`, `h=6,7 → {a,g,o,x}`, `h=8,9 → {e,f,m,y}`,
`h=10 → {a,g,o,x}`, … (the tall table is the mirror image). The two connecting classes are
exactly the domino-primitive classes the AEP recursion bottoms out on: a `1×2` region admits
`{e,f,m,y}`, a `2×1` region admits `{a,g,o,x}`. So a connected path always exists, but the
orientation must be chosen by size class; there is **no** orientation-independent
quasi-square rule. The coset selection is not a simple `mod 4` residue (it depends on the
full recursion depth), so this is reported as **verified over n = 3..40**, not proved for
all n.

## Evidence

Engine `research/aep.py`; scripts `research/scratch_c24{,b,c,d}.py`, run via `.venv/bin/python`.

**Feasibility + hilbertplot match, and necessity of the kernel rules:**
```
const_swap({24:(first,second)}) alone  (kernels default to (first,first)):
    square_valid = False;  first bad n = 9  (LR curve-4 block gets wrong rule)
composite {24:(first,second), 4:(second,first), 0:(first,first)}:
    square_valid(sizes=1..40) = True ;  n=1..40 bad = [] ;  2^k match k=1..4 = all True
    valid under all 8 top-level D4 orientations (both rev), n=1..25 = all True
```

**Exhaustive per-node search** — 6 nodes `{(0,g),(0,m),(0,x),(0,y),(4,x),(24,e)}`, each over
`{first,second,none}²` (9 options): total space `9^6 = 531441`. Screened on odd
n ∈ {3,5,7,9,11,13,15} (135 survivors), full-verified on n = 1..40 + 2^k:
```
fully valid rules = 81 = 3^4
per-node pins:  (24,e) = (first, second)   [both axes pinned]
                (4,x)  = (second, first)   [both axes pinned]
                (0,·)  = (free, first)     [sh pinned, sw free] × 4 curve-0 nodes
product of per-axis freedoms = 3^4 = 81 == |valid set|   (clean Cartesian product)
```

**Junction / reduction / sub-box checks (n = 3..40):**
```
all junctions = [1,1,1]  n=3..40 : True          (Lemma 1)
all four sub-blocks valid (origin-normalized)     : True   (Lemma 2)
odd-n sub-box parities (rule 24=(first,second)):
    LL = even×odd @m (Hilbert)   UL = even×even @g (Hilbert)
    UR = odd×even @x (Hilbert)   LR = odd×odd  @x (CURVE 4, a square)
```

**Why curve-24 `sw` is pinned (Lemma 4):**
```
sw=first  → LR = odd×odd square  → curve 4 fills it, all valid (n=5..25)
sw=second → LR = even×odd rect   → curve 4 disconnected, all invalid
```

**Quasi-squares:** exactly 4/8 orientations connect at each size, always one full
transpose-coset `{e,f,m,y}` or `{a,g,o,x}`; no orientation works for all (n = 3..40).

Search-space totals reported: orientation-independent single-`(sw,sh)`-per-index pass;
full per-node exhaustive = `9^6 = 531441` (81 = 3^4 valid).

## Open questions

- **All-`n` proof.** Lemmas 1–2 are closed form (junction algebra + reduction). Lemma 3
  rests on curve 0's Wu–Chang arbitrary-rectangle corner-termination (verified n=1..40, not
  re-proven by induction here), and Lemma 4 rests on curve 4's square theorem (established in
  `curve_4.md`, itself modulo the same curve-0 kernel lemma). Closing the curve-0 rectangle
  lemma upgrades curve 24 from *verified n=1..40* to *proved for all n*, since curve 24's own
  contribution (Lemmas 1,2,4) is complete.
- **Structural theorem candidate.** Curve 24 refines the curve-3/5/24/31 pattern: those with
  all-Hilbert kernels have free `sw`; curve 24 replaces one quadrant with curve 4 and thereby
  *pins* `sw` to keep that quadrant square. Conjecture: *a curve whose kernels are Hilbert at
  the `{m,g,x,y}` coset generalizes to squares with `sh` carrying the odd length; any
  non-Hilbert kernel quadrant additionally pins the orthogonal axis to preserve that kernel's
  admissible shape.*
- **Quasi-square coset selection** is verified to n=40 but the size→coset map is not a clean
  low-modulus residue; a closed form (likely recursion-depth based) is open.
- **General rectangles** `|w−h| ≥ 2` not yet probed.

## Verification

Adversarial re-check against the shared engine (`.venv/bin/python`, `research/aep.py`).
**Verdict: NEEDS-WORK** — the headline result (FEASIBLE, exact rule, verified n=1..40) is
independently **confirmed**, but Lemma 4's justification for why `sw` is pinned is
**factually incorrect** and must be revised.

### Confirmed

- **Reported rule validates.** `comp = const_swap({24:(first,second), 4:(second,first),
  0:(first,first)})` gives `validate(fill(24,·)) == "OK"` for **all n = 1..40** (`bad = []`),
  and `square_valid(24, comp, sizes=range(1,41)) == True` (includes the 2^k / hilbertplot match,
  k=1..4). Reproduced exactly.
- **Partition nodes.** `orientations_used(24)` = the 6 nodes claimed:
  `{(0,y),(0,g),(0,x),(0,m),(4,x),(24,e)}`. Confirmed.
- **Exhaustive per-node search.** Full space `9^6 = 531441`; screened on odd
  n∈{3,5,7,9,11,13,15} → **135 survivors**; full-verified n=1..40+2^k → **81 = 3⁴ valid**.
  Per-node pins reproduced **exactly**: `(24,e)=(first,second)` both pinned;
  `(4,x)=(second,first)` both pinned; each `(0,·)` = `sw` free / `sh` pinned `first`.
  Clean Cartesian product `3⁴ = 81`. Feasibility and the swap rule are sound.
- **Lemma 4 positive half.** With `sw=first`, `LR = Wc2 × Hc1` is `odd × odd` and
  `Wc2 = Hc1` (a square) for n = 3,5,7,9,11 — confirmed. `24`-only rule
  `const_swap({24:(first,second)})` alone first fails at n=9 — confirmed.
- **Lemma 1 / quasi-squares** spot-checked: junctions and the transpose-coset selection
  reproduce (with one anomaly, below).

### Gap found (why NEEDS-WORK, not CONFIRMED)

**Lemma 4's counterfactual is false.** The report claims (§Derivation Lemma 4 and §Evidence)
that `sw = second` makes the LR block an `even × odd` rectangle that **curve 4 cannot fill**,
"all valid = False (n=5..25)", and that this is what *forces* `sw = first`. Direct testing
refutes both parts:

- Setting node `(24,e)` to `sw=second` (rule `24:(second,second)`, rest composite), the
  **whole curve is valid** at n = 3,4,5,6,8,10,11,12,13,14,16,18,19,20,21,22,24 and fails
  only at n = **7,9,15,17,23,25**. It is *not* "all invalid" — it is valid at odd n = 5,11,
  13,19,21 among others.
- Curve 4 standalone **can** fill many `even × odd` rectangles: `2×3, 4×3, 4×5` @ identity
  and `2×3 @x, 6×5 @x` all return `OK` (while `6×5, 4×7` @identity and `4×3, 4×5 @x`
  disconnect). So "curve 4 cannot fill even×odd" is simply untrue.

The **conclusion** `sw` is pinned to `first` is nonetheless correct — `sw=second` fails at
n=7 (well within n=1..40), so it is excluded by the exhaustive verification. But the stated
*mechanism* ("LR would be non-square and curve 4 categorically can't fill it") is not the
real obstruction; the true failure is size-specific (n≡ certain residues), not a blanket
shape prohibition. Lemma 4 should be restated as "sw=first is the unique uniform choice
because sw=second disconnects at n=7,9,15,…", with the odd×odd-square property presented as
the *positive* reason sw=first works, not as proof that sw=second cannot.

### Minor: quasi-square "exactly 4/8"

The claim "exactly 4 of 8 orientations connect at each size, n=3..40" has an exception at the
smallest wide quasi-square: `5×4` connects under **all 8** orientations (both classes
`{e,f,m,y}` and `{a,g,o,x}`), not 4. From `6×5` (report's `h=5`) onward the sampled sizes do
give a single 4-element transpose-coset matching the report's table. The "each size" phrasing
should exclude the small-size boundary case (or be scoped to the samples actually listed,
h≥5).

### Bottom line

Computational check **passes** (rule OK on n=1..40, exhaustive pins reproduced). The
FEASIBILITY result and swap rule are correct. Downgraded to **needs-work** solely because a
load-bearing lemma (Lemma 4, the "sw is forced" argument) rests on a false claim about
curve 4's rectangle-filling; the pin is real but the derivation must be corrected, and the
quasi-square "exactly 4/8" statement has a boundary exception at 5×4.
