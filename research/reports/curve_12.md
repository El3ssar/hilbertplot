# Curve 12 — Liu2+Liu4 #1

- **kernels / quadrant rules** (visited order LL, UL, UR, LR; each `(base, morphism, reverse)`):
  | quadrant | base | morphism `M` | reverse |
  |----------|------|--------------|---------|
  | LL | 3 (Liu2) | `((0,1),(1,0))` = **maindiag / transpose** (`o`) | False |
  | UL | 5 (Liu4) | `((-1,0),(0,1))` = **xflip** | **True** |
  | UR | 5 (Liu4) | `((1,0),(0,1))` = **id** | False |
  | LR | 3 (Liu2) | `((0,-1),(-1,0))` = **antidiag** | False |

  The two side quadrants are **curve 3 (Liu2)**, the two upper/right quadrants **curve 5
  (Liu4)**. Both kernels have all four quadrant bases equal to **curve 0 (Hilbert)**:
  `RULES[3]` and `RULES[5]` recurse only into curve 0 (they differ solely in the LR
  morphism, `vflip` for curve 3 vs. `rot270` for curve 5). The kernel chain is therefore
  **12 → {3, 5} → 0**. Curve 12 never appears inside itself; in the partition it occurs
  **only as the top-level node at orientation `id`**, and all deeper nodes are curves 3, 5, 0.
  The kernels need correct swap rules too, and the problem is naturally solved bottom-up
  (curve 0, then 3 and 5, then 12) — but, as shown below, the obstruction lives at the
  **top node** and is independent of the kernel rules.

- **entry/exit type**: `entry_exit(12) = ('edge','edge')`. Curve 12 enters and exits on an
  edge. Structurally **both endpoints lie on the bottom edge `y = 0`**: the global entry is the
  entry of LL (curve 3 transposed — canonical curve 3 enters its **left** edge, transpose sends
  that to the **bottom**), and the global exit is the exit of LR (curve 3 antidiagonal, which
  also lands on `y = 0`). Verified on `hilbertplot`'s `2^k` curves: entry/exit are
  `k=1:(0,0)/(1,0)`, `k=2:(0,0)/(3,0)`, `k=3:(1,0)/(6,0)`, `k=4:(3,0)/(12,0)` — all on `y = 0`.

- **partition nodes** (`orientations_used(12)`) — the `(curve, orientation)` pairs that need a
  swap rule — **12 nodes**, a closed set:
  - `(12, id)` — the unique curve-12 node (it never appears at any other orientation);
  - `(3, ·) × 2` — curve 3 at `{maindiag, antidiag}`;
  - `(5, ·) × 2` — curve 5 at `{id, xflip}`;
  - `(0, ·) × 7` — curve 0 at seven orientations, closed under the recursion.

## Result

- **squares: INFEASIBLE.** No swap rule — **orientation-independent or per-orientation, over
  the full `9^12` rule space** — makes `fill(12,·)` a connected space-filling path on every
  `n × n` square. The obstruction is a **contradiction between the height-split parity demanded
  at `n = 3` and at `n = 7`**, both imposed on the *same* size-independent height symbol `sh`
  of the single top node `(12, id)`.
- **swap rule**: **none exists.**
- **verified**: exhaustive search returns **empty**. The certificate is small and complete: the
  viable top-node sets `S(3)` and `S(7)` are **disjoint** (`S(3)` is unconditional — `n=3` has
  only the top node; `S(7)` is an exhaustive `9^4 = 6561`-rule search). Powers of two are
  unconditionally valid and the curve reproduces `hilbertplot` at `n = 2^k` for `k = 1,2,3,4`:
  **yes**. (Not every even `n` is automatically fine — `n = 6 = 3+3` already needs a swap and is
  `disconnected` under the trivial rule; only `n = 2^k` splits evenly at every level. The
  confined failure is odd sizes, and no single rule repairs them all.)
- **individually** each odd size *is* feasible (e.g. `n = 3,5,7` each admit valid rules — see
  `S(n)` below, all non-empty); the impossibility is **global** — no single rule serves `n = 3`
  and `n = 7` simultaneously. A best-effort per-orientation search (coordinate descent, all 12
  nodes) reaches at most **31/40** valid sizes on `n = 1..40`, always failing the odd sizes
  `n ≡ 1, 7 (mod 8)`.
- **quasi-squares** (`|w−h| = 1`): connected only under an aspect-selected, **size-periodic**
  orientation class, and **no** orientation connects *all* wide (or all tall) quasi-squares.
  See §Quasi-squares.

## Derivation / proof

### Setup — the top-level split

Curve 12 on an `n × n` square at orientation `id` (no transpose) splits into four kernel
blocks, visited `LL → UL → UR → LR`:

```
UL = (0,   Hc1, Wc1, Hc2) @ xflip, rev            UR = (Wc1, Hc1, Wc2, Hc2) @ id
LL = (0,   0,   Wc1, Hc1) @ maindiag              LR = (Wc1, 0,   Wc2, Hc1) @ antidiag
```

with width split `(Wc1, Wc2)` and height split `(Hc1, Hc2)` governed by
`swap(12, id) = (sw, sh)`. The two **lower** blocks `LL, LR` have height `Hc1`; the two
**upper** blocks `UL, UR` have height `Hc2`. The horizontal junctions `LL→UL` and `UR→LR`
straddle the internal line `y = Hc1`; the vertical junction `UL→UR` straddles `x = Wc1` along
the upper tier. The path enters on the bottom edge inside LL and exits on the bottom edge
inside LR.

### Lemma 1 (`sh` fixes the parity of `Hc1` by a fixed function of `n`)

For odd `n = 2m+1`, `_split(n, ·)` gives `d1 = m, d2 = m+1`; exactly one of `m, m+1` is even,
and the swap symbol selects which becomes the **lower** tier `Hc1`, *identically for every odd
`n`*:

- `sh = "first"` ⟹ `Hc1` is the **even** half — `(Hc1,Hc2) = (even, odd)` — for all odd `n`;
- `sh = "second"` ⟹ `Hc1` is the **odd** half — `(Hc1,Hc2) = (odd, even)` — for all odd `n`;
- `sh = "none"` ⟹ `Hc1 = n//2 = m`, parity `= m mod 2` (`n≡1 (mod4) → even`, `n≡3 (mod4) → odd`).

Thus a single fixed `sh` symbol determines the parity of `Hc1` by a fixed function of `n`.
Concretely (`aep._split`):

```
n=3: first→Hc1=2 (even)   second→Hc1=1 (odd)   none→Hc1=1 (odd)
n=7: first→Hc1=4 (even)   second→Hc1=3 (odd)   none→Hc1=3 (odd)
```

### Lemma 2 (Curves 3 and 5 are edge-to-edge, so junction cells drift with block size)

Both kernels are `('edge','edge')`: they meet a shared internal edge at a cell that is **not
pinned to a corner** — it moves with the block size. In the top split the global entry is the
LL entry (curve 3 at `maindiag`) at `(≈Wc1/2, 0)`, and the global exit is the LR exit (curve 3
at `antidiag`) at `(≈Wc1 + Wc2/2, 0)` — both on `y = 0`, both at the **centre of a width-half**.
Their columns therefore drift with the half-widths, and the horizontal junctions across
`y = Hc1` (between the drifting top-edge exit of a lower block and the drifting bottom-edge
entry of the upper block) become 4-adjacent **only for one parity of the tier height `Hc1`**;
on the other parity they miss by Manhattan distance `≥ 2`. This is the size-dependent adjacency
that the *fixed* `sh` symbol of Lemma 1 must satisfy **simultaneously at every odd `n`**.

Concretely, at `n = 3` (only the top node is active, kernel rules irrelevant) the three
internal junctions are all 4-adjacent iff `Hc1 = 2` (even):

```
n=3, sh=first  (Hc1=2): J1 exit(LL)(0,1)→entry(UL)(0,2) d=1 | J2 d=1 | J3 (2,2)→(2,1) d=1  → OK
n=3, sh=second (Hc1=1): J1 exit(LL)(1,0)→entry(UL)(0,1) d=2 |            J3 (2,2)→(2,0) d=2  → broken
```

### Lemma 3 (`n = 3` and `n = 7` demand opposite `Hc1` parity — exhaustive certificate)

The top node `(12, id)` is the **unique** curve-12 node and appears in the decomposition of
*every* square, so its `(sw, sh)` value is shared across all `n`. Define
`S(n) = { top ∈ {first,second,none}² : some completion of the other active nodes makes
fill(12, n, n) valid }`, computed exhaustively over the active node set at size `n`:

- `S(3) = {(first,first), (none,first), (second,first)}` — **requires `sh = "first"`**
  (`Hc1` **even**). This is *unconditional*: at `n = 3` the only active node is `(12, id)`
  itself (`9^0 = 1`), and direct enumeration shows validity iff `sh = "first"`.
- `S(7) = {(none,none), (none,second), (second,none), (second,second)}` — **requires
  `sh ∈ {none, second}`** (`Hc1` **odd**). Exhaustive over `9^4 = 6561` completions of the four
  other active nodes `{(3,maindiag),(3,antidiag),(5,id),(5,xflip)}`; no completion with
  `sh = "first"` is valid.

They are **disjoint**: `S(3) ∩ S(7) = ∅`.

### Theorem (impossibility)

There is no swap rule making `fill(12,·)` valid on all `n × n` squares.

*Proof.* Any rule fixes a single value `sh` at the unique top node `(12, id)`. By Lemma 3,
validity at `n = 3` requires `Hc1` even (`sh = "first"`), while validity at `n = 7` requires
`Hc1` odd (`sh ∈ {second, none}`). No symbol yields both: `"first"` → `Hc1` even at every odd
`n` (fails `n = 7`); `"second"` → `Hc1` odd at every odd `n` (fails `n = 3`); `"none"` →
`Hc1 = 1` odd at `n = 3` (fails `n = 3`). Since these are *necessary* conditions established by
exhaustive search over all completions of the remaining nodes, no assignment of the full `9^12`
per-orientation rule space can satisfy both sizes. ∎

### Corroborating obstruction — checkerboard parity of the endpoints

An independent, rule-independent necessary condition confirms the picture. On an `n × n` grid
with `n` odd, colour cells `(x+y) mod 2`; the majority colour (that of the corners) has
`(n²+1)/2` cells, so **both endpoints of any Hamiltonian path must be that colour 0**. Curve 12
places both endpoints on `y = 0`, so both `entry_x` and `exit_x` must be even. The top width
symbol `sw` merely *moves* a fixed parity defect between the two endpoints:

```
sw=first : entry colour [0,0,1,1,0,0,1,1,…] (bad at n≡1,7 mod 8),  exit colour ≡ 0
sw=second: entry colour ≡ 0,                                       exit colour bad at n≡1,7 mod 8
```

so for the odd sizes `n ≡ 1, 7 (mod 8)` one endpoint always lands on the minority colour under
these top choices — the same odd sizes at which the best per-orientation search fails. This is
the width-axis face of the same edge-endpoint drift that Lemma 2 expresses on the height axis.

## Quasi-squares (`|w − h| = 1`)

For each top orientation `M`, per-size feasibility (does *any* swap rule connect; exhaustive
over the size's active node set), on small quasi-squares (`Y` = some rule connects, `N` = none):

**Wide** `(w,h) = (h+1,h)`:
```
orientation               2x1  3x2  4x3  5x4  6x5
id, xflip, 180, yflip      Y    Y    Y    N    Y     (axis-preserving)
maindiag,rot90,            Y    Y    N    Y    N     (transposing)
antidiag,rot270
```
**Tall** `(w,h) = (w,w+1)`:
```
orientation               1x2  2x3  3x4  4x5  5x6
id, xflip, 180, yflip      Y    Y    N    Y    N     (axis-preserving)
maindiag,rot90,            Y    Y    Y    N    Y     (transposing)
antidiag,rot270
```

Observations:
- The 8 orientations split into the two D4 cosets by **transpose parity** (`M[0][0]=0`?), and
  the wide/tall tables are **exact complements** between the cosets: a transposing top
  orientation turns a wide region into a *tall* canonical frame and vice versa, so it inherits
  the opposite coset's pattern.
- **No orientation connects all wide (or all tall) quasi-squares**: the axis-preserving coset
  fails wide `5×4`, the transposing coset fails wide `4×3` and `6×5` (mirror for tall). The Y/N
  pattern is size-periodic — the quasi-square analogue of the odd-square obstruction.
- **Primitive link.** At the bottom the recursion terminates on `1×2` (a *tall* domino,
  reachable canonically under orientations A, C) and `2×1` (a *wide* domino, orientations
  B, D). A wide quasi-square handled by an axis-preserving orientation bottoms out through
  wide `2×1` dominoes; a transposing orientation re-expresses it through tall `1×2` dominoes.
  The complementary tables are exactly this primitive-orientation alignment propagated up the
  recursion — the same `1×2` / `2×1` dichotomy that sets the parity of the lower tier in
  Lemma 1.

## Evidence

Environment: `cd /home/elessar/Projects/HilbertPlots && .venv/bin/python`, with
`import sys; sys.path.insert(0,"research"); import aep`.

**Structure.**
```
aep.NAME[12] = 'Liu2+Liu4 #1'
aep.RULES[12] = [(3, maindiag, False), (5, xflip, True), (5, id, False), (3, antidiag, False)]
aep.entry_exit(12) = ('edge', 'edge')
orientations_used(12): 12 nodes = (12,id)×1, (3,·)×2, (5,·)×2, (0,·)×7
unique curve-12 node: (12, ((1,0),(0,1)))            # only orientation id ever occurs
hilbertplot 2^k endpoints (all on y=0): k=1 (0,0)/(1,0); k=2 (0,0)/(3,0); k=3 (1,0)/(6,0); k=4 (3,0)/(12,0)
```

**No orientation-independent rule.** Searching a single `(sw,sh)` for curve 12 layered over the
known kernel rules `{0:(first,first),3:(first,second),5:(first,second)}`, tested on `n = 1..40`:
**0 hits** of the 9. Searching an independent const `(sw,sh)` per curve for `{0,3,5,12}`
(`9^4 = 6561` combinations), tested on `n = 1..40`: **0 solutions**.

**Exhaustive impossibility certificate** (`scratchpad/Sn.py`):
```
S(3) [9^0 = 1     search] = {(first,first),(none,first),(second,first)}   → sh ∈ {first}   (Hc1 even)
S(5) [9^3 = 729   search] = {(first,first),(first,none),(none,first),(none,none)}
S(7) [9^4 = 6561  search] = {(none,none),(none,second),(second,none),(second,second)} → sh ∈ {none,second} (Hc1 odd)
S(3) ∩ S(7) = ∅        (S(5) ∩ S(7) = {(none,none)} is non-empty — 5,7 alone do not contradict)
n=7 with sh=first: any valid completion? False       # exhaustive 9^4
full per-orientation rule space = 9^12 = 282,429,536,481
```
The empty intersection `S(3) ∩ S(7)` is a complete proof: `n = 3` needs `sh = "first"`
(unconditional — one node) and `n = 7` needs `sh ∈ {second, none}` (exhaustive over all
completions), contradictory at the single shared top node.

**`n = 3` direct enumeration** (all 9 top values, no other active nodes):
```
(first,first) OK    (first,second) disc   (first,none) disc
(second,first) OK   (second,second) disc  (second,none) disc
(none,first) OK     (none,second) disc    (none,none) disc      → valid iff sh = "first" (Hc1=2)
```

**Even sizes / `2^k` match** (trivial swap `(first,first)`):
```
n=2 OK, n=4 OK, n=6 disconnected, n=8 OK, n=16 OK, n=32 OK
2^k match to hilbertplot (canonical_form): k=1,2,3,4 → all True
```
(`n=6 = 3+3` needs a swap; not a counterexample to the theorem, which concerns a *single* rule
for all sizes.)

**Best-effort per-orientation search.** Coordinate descent over all 12 nodes reaches at most
**31/40** valid sizes on `n = 1..40`; the failures are exactly the odd sizes
`n ∈ {7,9,15,17,23,25,31,33,39}` (i.e. `n ≡ 1, 7 mod 8`), matching the endpoint-parity
corroboration.

**Search space explored.** Orientation-independent (curve-12 layered over kernels): 9.
Per-curve const over `{0,3,5,12}`: `9^4 = 6561`. Impossibility certificate: `S(3)` over `9^0`,
`S(5)` over `9^3`, `S(7)` exhaustive over `9^4 = 6561`. The full per-orientation space
`9^12 ≈ 2.82×10^11` is *ruled out in bulk* by the two-size argument: the top node has only 9
values, of which `n = 3` eliminates all but `sh = first` and `n = 7` eliminates all with
`sh = first`.

## Verification

**Verdict: CONFIRMED.** Independent adversarial re-check reproduces the impossibility by two
separate routes and finds no refuting rule.

**Structure re-derived.** `RULES[12] = [(3,maindiag,F),(5,xflip,T),(5,id,F),(3,antidiag,F)]`,
`entry_exit(12)=('edge','edge')`. Curve 12 appears at **only** orientation `id` over the full
tested range (`orientations_used(12, sizes=range(3,41,2))` yields exactly one curve-12 node,
`(12,IDENT)`), so its `(sw,sh)` is genuinely shared across all `n` — the load-bearing premise
holds throughout `n = 3..40`.

**Active-node counts reproduced.** Per-size active nodes: `n=3` → 1 node (top only); `n=5` → 4;
`n=7` → 5 (top + `{(3,maindiag),(3,antidiag),(5,id),(5,xflip)}`) — matching the `9^4` completion
claim.

**Impossibility certificate reproduced (exhaustive).** Computing `S(n)` (top-node values
admitting *some* completion of the other active nodes) directly:
```
S(3) = {(first,first),(none,first),(second,first)}         sh ∈ {first}          (Hc1 even)
S(5) = {(first,first),(first,none),(none,first),(none,none)}
S(7) = {(none,none),(none,second),(second,none),(second,second)}  sh ∈ {none,second} (Hc1 odd)
S(3) ∩ S(7) = ∅
```
Identical to the report. Since any global rule's top value must lie in `S(n)` for every `n`
(necessary condition: the rule's own completion witnesses membership), and `S(3) ∩ S(7) = ∅`,
no global rule exists over the full `9^12` space. The projection argument is logically sound.

**Second independent route — direct joint brute force.** Over the union of active nodes for
`n ∈ {3,5,7}` (5 nodes, `9^5 = 59049` rules), exhaustively testing each rule for simultaneous
validity on `n = 3,5,7`: **0 solutions**. Because any `9^12` rule restricts to one of these
`9^5` assignments on the relevant nodes, this alone refutes the existence of a global rule —
a self-contained confirmation not relying on the `S(n)`-projection reasoning.

**Ancillary claims checked.** `2^k` reproduces hilbertplot for `k=1,2,3,4` (all `True`); even sizes
`n=2,4,8,16,32` valid; `n=6` disconnected under the trivial rule (correctly a non-counterexample,
as the theorem concerns a single fixed rule). Each odd size is individually feasible
(`S(3),S(5),S(7)` all non-empty).

**Minor discrepancies (non-material).** (1) The report states 12 partition nodes with `(0,·)×7`;
this reflects the default range `range(3,12,2)`. Over `n=3..40` one additional curve-0
orientation activates (13 nodes, `(0,·)×8`). This does not affect the proof — the top node stays
unique at `id`. (2) The checkerboard-parity section is corroborative only; the proof rests
entirely on `S(3) ∩ S(7) = ∅`, which is airtight independent of it.

**Commands run:** `aep.RULES/entry_exit/orientations_used`; per-size `active_nodes` recursion;
exhaustive `S(n)` via `per_orientation_swap` + `validate` over `fill(12,·)`; joint `9^5`
brute force on `n∈{3,5,7}`; `canonical_form` match to `hilbertplot.curve(12).points(k)` for the `2^k`
check. All on `n×n` squares up to `n=40`.

## Open questions

- **Exact junction lemma.** Lemma 2 is stated structurally and verified computationally
  (`n = 3` shown in closed form; `n = 7` via exhaustive `S(7)`). A closed-form expression for
  the drifting bottom-edge column of curves 3/5 as a function of block `(w,h)` under `maindiag`
  / `antidiag` / `id` / `xflip` would pin the exact `n mod k` at which the required `Hc1` parity
  flips (the data show `n = 3` even, `n = 7` odd; individually feasible odd sizes use *both* `sh`
  values, so the required-parity function is not a plain `n mod 4`).
- **General rectangles.** Whether any `w × h` family beyond squares/quasi-squares admits a
  connected generalization is untested here.
- **Classification hook.** Curve 12 joins the edge-to-edge kernel families (`·→{3,5}→0`) whose
  infeasibility stems from the kernels' *edge* endpoints forcing a size-dependent tier parity
  at a straddling horizontal junction — the same mechanism proved for curve 11 (`·→5→0`). This
  supports the conjecture: *a curve whose top split places an edge-to-edge kernel across a
  straddling horizontal (or vertical) junction is infeasible on squares, because the junction
  adjacency demands a lower-tier parity that flips with `n` while the swap symbol is fixed.*
```
