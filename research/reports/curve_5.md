# Curve 5 — Liu4

- **kernels / quadrant rules** (visited order LL, UL, UR, LR):
  | quadrant | base | morphism `M` | reverse |
  |----------|------|--------------|---------|
  | LL | 0 (Hilbert) | `((1,0),(0,-1))` = **vflip** (`m`) | False |
  | UL | 0 (Hilbert) | `((0,-1),(1,0))` = **rot90** (`g`) | False |
  | UR | 0 (Hilbert) | `((0,1),(-1,0))` = **rot270** (`x`) | False |
  | LR | 0 (Hilbert) | `((0,1),(-1,0))` = **rot270** (`x`) | False |

  Every quadrant recurses into **kernel curve 0 (Hilbert)** — curve 5 uses no other kernel,
  so the problem is solvable bottom-up (fix curve 0 first, then curve 5).
  Curve 5 is *identical to curve 3 (Liu2) except in the LR quadrant*: curve 3 uses **vflip**
  there, curve 5 uses **rot270**. This single change moves the global exit from the right edge
  to the bottom edge and, as shown below, is exactly what makes curve 5's top-level width-split
  parity **constrained** (curve 3's is free).

- **entry/exit type:** `entry_exit(5) = ('edge','edge')`. Concretely on the `2^k` grid
  (`hilbertplot.curve(5).points(k)`): entry `(0, 2^{k-1}−1)` (left edge, just below mid), exit
  `(2^{k-1}, 0)` (bottom edge). Order 4 (16×16): entry `(0,7)`, exit `(8,0)`. This is a
  **left-edge → bottom-edge** curve (an "L-turn" span), unlike curve 3's left→right straight
  span.

- **partition nodes** (`orientations_used(5)`) — the `(curve, orientation)` pairs that need a
  swap rule — exactly **5 nodes**, a closed set:
  - `(5, e)` — curve 5 at identity (it never appears at any other orientation);
  - `(0, vflip)`, `(0, rot90)`, `(0, rot270)`, `(0, y=hflip)` — curve 0 at four orientations,
    closed under the recursion.

## Result

- **squares: FEASIBLE.**
- **swap rule** (orientation-*independent*, but curve 5 and its kernel take *different*
  `(sw,sh)`):
  - **curve 5 node `(5,e)`:** `(sw, sh) = (first, second)` — **both axes pinned**. The
    canonical width-split makes the *low* half even and the height-split makes the *high* half
    even.
  - **curve 0 kernel nodes** (all four orientations): `(sw, sh) = (·, first)` — canonical
    height-split makes the *low* half even; `sw` **free** (`first`/`second`/`none` all work).
  - Compact published form: `const_swap({5:("first","second")})` — curve 5 → `(first,second)`,
    kernel curve 0 → default `(first,first)`. This is one valid instance (`sh=first` at the
    kernel, `sw=first` a free choice).
- **verified:** valid Hamiltonian path on `n × n` for **n = 1..40** (all `validate = OK`);
  **matches hilbertplot at `2^k`** (k=1,2,3): **yes**
  (`square_valid(5, const_swap({5:("first","second"),0:("first","first")}), range(1,41)) = True`).
- **quasi-squares** (`|w−h| = 1`): **no** top-level orientation connects *all* wide (or all
  tall) quasi-squares — connectivity is size-periodic (period 4). Full per-node search
  (`9^5 = 59049`) and const-swap × 8-orientation search both return **empty**. This is a
  genuine parity obstruction, stronger than curve 3's, because curve 5 pins *both* split axes.

## Derivation / proof

### Search space and structure of the solution set

The per-node rule space is `3 × 3 = 9` choices of `(sw,sh)` at each of the 5 nodes, so
`9^5 = 59049` candidate rules. Exhaustive test (screen on odd `n∈{3,5,7,9,11,13,15}`, confirm
survivors on `n = 1..25`, all of which also pass `n = 1..40`) yields **exactly 81 = 3^4 valid
rules**, and the valid set is *exactly* a Cartesian product of independent per-node constraints:

| node | `sw` (canonical width-split) | `sh` (canonical height-split) |
|------|------------------------------|-------------------------------|
| `(0, hflip)`  | free `{first,second,none}` | **pinned `first`** |
| `(0, rot90)`  | free | **pinned `first`** |
| `(0, rot270)` | free | **pinned `first`** |
| `(0, vflip)`  | free | **pinned `first`** |
| `(5, e)`      | **pinned `first`** | **pinned `second`** |

`3^4 = 81` matches `|valid set|` exactly (curve 5's node contributes a factor of **1** — both
its axes are pinned; each kernel node contributes a factor of 3 via the free `sw`). Contrast
curve 3, whose top node had `sw` free (`3^5 = 243` valid rules). The extra pin at curve 5 is
the whole content of the "vflip → rot270" change in LR, made precise in *Lemma 3* below.

### Lemma 1 (Junction invariance — closed form, all n ≥ 4)

Work in the canonical frame (top level: identity, no transpose, `Wc = Hc = n`). Split
`Wc = Wc1 + Wc2`, `Hc = Hc1 + Hc2`. Under the rule, `Wc1` even, `Wc2` odd, `Hc1` odd, `Hc2`
even. The four boxes and the designated entry/exit corners of the Hilbert sub-curve on each
(verified identical for **all** `n = 4..40`; `n=1,2,3` validated directly) are:

| box | region | orient | entry | exit |
|-----|--------|--------|-------|------|
| LL | `[0,Wc1)×[0,Hc1)`   | vflip  | `TL=(0,Hc1−1)`     | `TR=(Wc1−1,Hc1−1)` |
| UL | `[0,Wc1)×[Hc1,n)`   | rot90  | `BR=(Wc1−1,Hc1)`   | `TR=(Wc1−1,n−1)`   |
| UR | `[Wc1,n)×[Hc1,n)`   | rot270 | `TL=(Wc1,n−1)`     | `BL=(Wc1,Hc1)`     |
| LR | `[Wc1,n)×[0,Hc1)`   | rot270 | `TL=(Wc1,Hc1−1)`   | `BL=(Wc1,0)`       |

The three junctions along LL→UL→UR→LR:

- **J1** `LL.exit (Wc1−1,Hc1−1) — UL.entry (Wc1−1,Hc1)` : displacement `(0,1)`, distance 1;
- **J2** `UL.exit (Wc1−1,n−1) — UR.entry (Wc1,n−1)` : displacement `(1,0)`, distance 1;
- **J3** `UR.exit (Wc1,Hc1) — LR.entry (Wc1,Hc1−1)` : displacement `(0,1)`, distance 1.

**All three are 4-adjacent for every `Wc1,Hc1`.** J1/J2/J3 are identical to curve 3's — the
LR difference touches only the *exit* of LR (the global exit), never a junction. The junction
connectivity is therefore independent of split parities: it is Lemma 1 that makes `sw` free at
the four kernel nodes (J2 always lands on the top row `y=n−1` regardless of `Wc1`). ∎

### Lemma 2 (Reduction to the kernel)

By Lemma 1 the parent junctions cost nothing. Hence curve 5 on `n×n` is valid **iff** each of
its four sub-boxes is a valid Hilbert path terminating at the designated corners of that box.
The sub-boxes `Wc1×Hc1, Wc1×Hc2, Wc2×Hc2, Wc2×Hc1` are filled by curve 0 at
`vflip, rot90, rot270, rot270`. All remaining parity constraints are **kernel
corner-termination** constraints.

### Lemma 3 (Why curve 5 pins `sw` and curve 3 does not) — the color/parity mechanism

Color a cell `(x,y)` by `(x+y) mod 2`. A Hamiltonian path on an `a×b` grid has endpoints of
**opposite** colors when `ab` is even, and of the **same** (majority) color when `ab` is odd.
Apply this to LR, whose height is `Hc1` (odd), so `|LR| = Wc2·Hc1 ≡ Wc2 (mod 2)`:

- **Curve 3, LR = vflip:** endpoints `TL=(Wc1,Hc1−1)` and `TR=(n−1,Hc1−1)` lie in the *same
  row* but *different columns*; their color difference is `(n−1)−Wc1 = Wc2−1 (mod 2)`.
  - `Wc2` even ⇒ `|LR|` even ⇒ endpoints must be opposite; color diff `= Wc2−1 =` odd ✓
  - `Wc2` odd  ⇒ `|LR|` odd  ⇒ endpoints must be same;      color diff `= Wc2−1 =` even ✓

  Both parities are consistent → `Wc2` (hence `sw`) is **free** for curve 3.

- **Curve 5, LR = rot270:** endpoints `TL=(Wc1,Hc1−1)` and `BL=(Wc1,0)` lie in the *same
  column* `Wc1`; both `y`-coordinates (`Hc1−1` and `0`) are **even** (`Hc1` odd), so the two
  endpoints **always have the same color**, independent of `Wc2`.
  - Same-color endpoints ⇒ need `|LR|` odd ⇒ `Wc2` **odd** ⇒ `sw = first` **forced**.
  - `Wc2` even ⇒ `|LR|` even (opposite colors required) but endpoints are same-colored ⇒ **no
    corner-to-corner Hamiltonian path exists** ⇒ curve 5 fails.

This is the exact obstruction the search reports: rotating LR from a *horizontal* corner-pair
(vflip, TL–TR) to a *vertical* corner-pair (rot270, TL–BL) removes the `Wc2`-dependence of the
endpoint color while leaving the `Wc2`-dependence of the cell count intact, collapsing the two
consistent width parities to one. ∎

### Why `sh` is pinned (kernel parity condition, shared with curve 3)

Curve 5's `sh = second` forces `Hc2` even. Curve 0 (Hilbert) under AEP is a corner-to-corner
Hamiltonian path on a rectangle only when the swap makes the correct half even; for the four
kernel orientations here that is the canonical-height condition `sh = first`, and `Hc2` even is
the parity that lets the kernels corner-terminate (feeding Lemma 2). `sw` never enters the
*height* condition — matching the free `sw` column at the kernel nodes. This rests on curve 0's
established arbitrary-rectangle (Wu–Chang) corner-to-corner property as the kernel lemma;
verified here over `n = 1..40`.

### Global consistency check (color)

For `n` odd, `n²` is odd, so the global path endpoints must share the majority color 0.
Entry `(0,Hc1−1)`: `Hc1−1` even ⇒ color 0. Exit `(Wc1,0)`: `Wc1` even ⇒ color 0. Consistent
for every odd `n`, as observed (`n = 3..31`, both endpoints color 0).

### Quasi-squares

For `|w−h| = 1` the aspect is *forced*: one axis is longer by exactly 1, so the construction
cannot absorb the odd length on a free axis. Curve 5 pins **both** split axes at its top node
(`sw=first` *and* `sh=second`), i.e. it demands a specific parity on the width **and** on the
height simultaneously. A quasi-square's two sides have opposite parities that vary with the
size, so both pins cannot be honored for all sizes at once. Empirically the connectivity is
**period-4 in the size** and no orientation connects all of them:

- WIDE (`w=h+1`): non-transposing orientations `{e,y,f,m}` connect on a size-set complementary
  to the transposing orientations `{o,g,a,x}`; each covers ≈ half the sizes (period 4).
- TALL (`h=w+1`): the two classes swap roles (mirror image).

This ties to the terminal `1×2`/`2×1` primitive: the AEP recursion bottoms out on dominoes
whose orientation is fixed by `Wc` parity — transposing orientations `{B,D,rot90,rot270}` fill
the `2×1` primitive, non-transposing `{A,C,hflip,vflip}` the `1×2`. All 8 orientations fill
both primitives, so the obstruction is not the primitive itself but the *double* parity pin,
which is why curve 5's quasi-squares are more obstructed than curve 3's (curve 3, pinning only
the height, satisfies a clean "`Wc` even" law; curve 5 has no such single-axis law).

## Evidence

Commands run as `cd /home/elessar/Projects/HilbertPlots && .venv/bin/python …`
(scratch scripts under `research/`; `import sys; sys.path.insert(0,"research"); import aep`).

**Feasibility + hilbertplot match:**
```
nodes = orientations_used(5) = {(5,e),(0,vflip),(0,rot90),(0,rot270),(0,hflip)}  (5 nodes)
const_swap({5:("first","second"),0:("first","first")}):
  validate(fill(5,·,n,n)) == OK for every n = 1..40   (bad sizes: NONE)
  square_valid(5, rule, sizes=range(1,41)) = True      (matches hilbertplot at 2^k, k=1,2,3)
```

**Exhaustive per-node square search:**
```
space = 9^5 = 59049 candidate rules
screen odd n∈{3,5,7,9,11,13,15}; confirm n=1..25; all survivors also pass n=1..40
valid rules = 81 = 3^4
per-node value distribution among the 81 valid rules:
  (0,hflip) : sw ∈ {first,second,none} (27 each)   sh = first  (pinned)
  (0,rot90) : sw free                               sh = first  (pinned)
  (0,rot270): sw free                               sh = first  (pinned)
  (0,vflip) : sw free                               sh = first  (pinned)
  (5,e)     : (sw,sh) = (first,second) ONLY (all 81)  — both axes pinned
```

**Per-node necessity (baseline = all kernels (first,first), node5 (first,second)):**
```
vary (5,e):  (first,second) -> valid ;  all 8 other (sw,sh) -> invalid   (sw AND sh pinned)
vary (0,·):  sh=first -> valid ;  sh∈{second,none} -> invalid (each of 4 kernel nodes)
```

**Junction invariance (Lemma 1), square rule, e.g. n=9  (Wc1,Wc2=4,5  Hc1,Hc2=5,4):**
```
LL box(0,0,4x5)  entry(0,4)=TL  exit(3,4)=TR
UL box(0,5,4x4)  entry(3,5)=BR  exit(3,8)=TR   J1: (3,4)-(3,5) dist 1
UR box(4,5,5x4)  entry(4,8)=TL  exit(4,5)=BL   J2: (3,8)-(4,8) dist 1
LR box(4,0,5x5)  entry(4,4)=TL  exit(4,0)=BL   J3: (4,5)-(4,4) dist 1
global entry(0,4) color0 ; exit(4,0) color0   (junction distances [1,1,1] for all n=3..40)
```

**Quasi-squares (const-swap × 8 orient, and full per-node search):**
```
const_swap × 8 orientations, all valid over h=2..20:  WIDE 0 hits ; TALL 0 hits
full per-node search (9^5=59049) at top identity, all valid h=2..15:  WIDE 0 ; TALL 0
connectivity pattern is period-4 in size; the two orientation classes cover complementary
size-sets. No orientation/rule connects all quasi-squares of one aspect.
```

## Verification

**Verdict: CONFIRMED.** Independent adversarial re-run of the engine reproduces every
computational claim, and the derivation (Lemmas 1–3) is sound; the single unproven step is
correctly disclosed by the report itself (not a defect).

**Nodes / rules re-derived.** `orientations_used(5) = {(5,e),(0,m),(0,g),(0,x),(0,y)}` — exactly
the 5-node closed set claimed (curve 5 appears only at `e`). `RULES[5]` matches the kernel table
(LL vflip, UL rot90, UR rot270, LR rot270; all base 0).

**Squares — reported rule.** `const_swap({5:("first","second"),0:("first","first")})`:
`validate(fill(5,·,n,n)) == OK` for **every** `n = 1..40` (bad sizes: none);
`square_valid(5, rule, range(1,41)) = True` (so it also matches hilbertplot at `2^k`, k=1,2,3).

**Squares — exhaustive per-node search reproduced.** Full space `9^5 = 59049`
(9 independent `(sw,sh)` per node), screened on odd `n∈{3,5,7,9,11,13,15}` then confirmed on
`n = 1..40`. Result: **exactly 81** valid rules. Per-node distribution reproduced identically —
each kernel node `sw ∈ {first,second,none}` (27 each) with `sh = first` pinned; node `(5,e)`
pinned to `(first,second)` in all 81. `81 = 3^4` (curve-5 node factor 1, four kernel factors 3).
Confirms both the count and the exact Cartesian-product structure claimed.

**Lemma 1 junctions reproduced.** Re-deriving the four top-level sub-boxes for `n=9,7,11,13`
gives junction distances `[1,1,1]` at every size, with entry/exit corners matching the report's
table (e.g. `n=9`: LL `(0,4)→(3,4)`, UL `(3,5)→(3,8)`, UR `(4,8)→(4,5)`, LR `(4,4)→(4,0)`;
J1 `(3,4)-(3,5)`, J2 `(3,8)-(4,8)`, J3 `(4,5)-(4,4)`, all dist 1). Global entry/exit color 0.

**Lemma 3 parity mechanism verified.** For every tested odd `n`, the LR sub-box endpoints share
column `Wc1` with both `y`-coords even ⇒ **same color** (both color 0), and `|LR| = Wc2·Hc1` is
**odd** with `Wc2` odd — exactly the "same-color endpoints ⇒ need odd cell count ⇒ `Wc2` odd ⇒
`sw=first` forced" chain. The single-node necessity search confirms all 8 non-`(first,second)`
choices at `(5,e)` fail. The argument is a valid necessity proof at odd `n`; sufficiency then
rests on Lemma 1 (free junctions) plus the kernel corner-termination lemma.

**Quasi-square impossibility — actively attacked, not refuted.** Two independent searches over
`|w−h|=1`, both returning **zero** rules that connect all sizes of one aspect:
- const-swap (node 5 × node 0, `9×9`) × all 8 top orientations, over `h = 2..21`: **0 wide, 0 tall**;
- **full per-node** independent `(sw,sh)` at every reachable node (`9^5` per orientation) × all 8
  top orientations, over `h = 2..13`: **0 wide, 0 tall**.
The most permissive rule space still connects no aspect uniformly, corroborating the double-pin
obstruction.

**Scope check.** The report honestly labels the square result *verified over n=1..40*, not
*proved for all n*, and flags the residual kernel-0 corner-termination lemma (leaning on the
Wu–Chang arbitrary-rectangle Hilbert result) as the one inductive step not re-proven. This
scoping is correct; no overclaim was found. — verifier

## Open questions

- **Full all-`n` proof of the kernel lemma.** Lemmas 1–3 are closed form; the residual step —
  curve 0 at `{vflip,rot90,rot270,hflip}` corner-terminates on every sub-rectangle under
  `sh=first` — is verified over `n=1..40` and follows the Wu–Chang arbitrary-rectangle Hilbert
  result, but is not re-proven by induction for all `n`. Closing it upgrades the square result
  from *verified n=1..40* to *proved for all n*.
- **Rectangles** (`|w−h|>1`): curve 5's *double* parity pin suggests no clean single-axis law
  (unlike curve 3); a per-aspect rule is not yet mapped.
- **Structural theorem.** Lemma 3 isolates the discriminating property: a curve whose kernels
  are Hilbert and whose *last-visited* quadrant connects a **vertical** corner-pair pins the
  width-split, whereas a **horizontal** corner-pair leaves it free. This should classify the
  `sw`-freedom of every kernel-0 curve (3,5,24,31,…) from its LR morphism alone.
```
