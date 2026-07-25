# Curve 33 — Moore+Liu4 #2

- **kernels / quadrant rules** (visited order LL, UL, UR, LR; each `(base, morphism, reverse)`):
  | quadrant | base | morphism `M` | reverse |
  |----------|------|--------------|---------|
  | LL | **1 (Moore)** | `((1,0),(0,-1))` = **vflip** `m` | False |
  | UL | **5 (Liu4)**  | `((0,-1),(1,0))` = **rot90** `g` | False |
  | UR | **5 (Liu4)**  | `((0,1),(1,0))`  = **main-diag transpose** `o` | **True** |
  | LR | **1 (Moore)** | `((1,0),(0,-1))` = **vflip** `m` | False |

  Curve 33 is a **composite**: its lower band (LL, LR) is two **Moore** blocks, its upper
  band (UL, UR) two **Liu4** blocks. It uses kernels **1** and **5**, which in turn both
  recurse into **0 (Hilbert)**. Curve 33 never appears as a kernel of itself or any other
  curve, so it must be solved **bottom-up**: Hilbert (0), then Moore (1) and Liu4 (5), then 33.
  The relevant established kernel facts (sibling reports):
  - **curve 0 (Hilbert): FEASIBLE**, canonical rule needs `sh=first` (low height-half even),
    `sw` free.
  - **curve 5 (Liu4): FEASIBLE** with `(5,e)→(first,second)`.
  - **curve 1 (Moore): INFEASIBLE** — no swap rule makes Moore a Hamiltonian path on every
    square; standalone it is realizable only at Jacobsthal odd sizes. Curve 33 **inherits a
    Moore block in each of LL, LR**, which is the seed of the obstruction below.

- **partition nodes** (`aep.orientations_used(33)`, extended to all squares `n=1..40`):
  **12 `(curve,orientation)` nodes** — `(33,e)`; `(1,m)`; `(5,g)`, `(5,o)`; and eight
  `(0,·)` Hilbert nodes. The **complete** node set reached at sizes `n ≤ 7` is exactly the
  four nodes `{(33,e), (1,m), (5,g), (5,o)}` — this small closed set already decides
  feasibility (see proof).

- **entry/exit type** (`aep.entry_exit(33)`): `('interior','interior')`. Both global
  endpoints lie strictly inside the `2^k` grid — there is no entry/exit corner, so the
  "make the entry-corner-side half even" heuristic that fixes the corner-type curves has no
  anchor here.

## Result

- **squares: INFEASIBLE.** No swap rule — orientation-independent **or** per-orientation
  over the full 12-node space — makes `fill(33,·)` a valid Hamiltonian path on every `n×n`
  square. The obstruction appears already at the pair **n = 5 vs n = 7**.
- **swap rule: none exists.** (There is *no* single rule; individual sizes need mutually
  contradictory rules — see below.)
- **verified:**
  - orientation-independent search (all **9** single `(sw,sh)`): **0** valid on `n=1..40`
    (earliest failure at `n=3`, latest at `n=7`).
  - full-space incremental survivor search over `n=1..40` (the pruned equivalent of
    enumerating `9^{12}=282 429 536 481` rules): survivor set collapses to **0 at n=7**,
    using only the 4 nodes fixed by `n≤6`.
  - exhaustive certificate on the complete 4-node set for `n≤7` (`9^4=6561` rules):
    `|valid(5)|=648`, `|valid(7)|=216`, **`valid(5) ∩ valid(7) = ∅`**.
  - matches `hilbertplot` at `2^k` (k=1,2,3): **yes** (even sizes; swap is a no-op on the top
    split there).
- **quasi-squares** `|w−h|=1`: no orientation sustains a rule over any full range; wide
  quasi-squares connect (up to `(5,4)`) only under the **four transpose orientations**
  `{g,x,o,a}`, tall quasi-squares (up to `(4,5)`) only under the **four non-transpose
  orientations** `{e,f,m,y}` — exactly the `2×1`(B,D) / `1×2`(A,C) primitive split. Both
  break beyond max-dim 5.

## Derivation / proof

### The decision variable

At the top node `(33,e)` (identity, non-transpose) curve 33 splits the `n×n` square (n odd)
into a **lower band** of height `Hc1` and an **upper band** of height `Hc2=n−Hc1`, with a
width split `Wc1,Wc2`. The four boxes, in visit order, are
```
LL=(0,0,Wc1,Hc1)  →  UL=(0,Hc1,Wc1,Hc2)  →  UR=(Wc1,Hc1,Wc2,Hc2)  →  LR=(Wc1,0,Wc2,Hc1)
   Moore(vflip)         Liu4(rot90)             Liu4(main-diag,rev)      Moore(vflip)
```
The **height-split label `sh` at node `(33,e)` is the only variable that sets the parity of
`Hc1`** (`sh=first` ⟹ `Hc1` even, `sh=second` ⟹ `Hc1` odd; `sh=none` ⟹ `Hc1=⌊n/2⌋`). The
two **Moore** blocks LL, LR both have height `Hc1`; the two **Liu4** blocks UL, UR both have
height `Hc2`.

### Lemma (parity of the lower band is pinned, but not consistently)

*For the composite path to be Hamiltonian, each sub-block must itself be internally
Hamiltonian at the shape handed to it. The Moore blocks LL, LR are internally realizable only
for a specific parity of their height `Hc1`, and that required parity is `n`-dependent.*

Concretely, exhaustively enumerating the complete node set `{(33,e),(1,m),(5,g),(5,o)}`
reached at `n≤7` (`9^4=6561` assignments) and projecting the surviving rules onto the `sh`
component of `(33,e)`:

| n | achievable `sh` at `(33,e)` | realized lower-band height `Hc1` |
|---|-----------------------------|----------------------------------|
| 3 | `{none, second}` (⟹ `Hc1` odd) | 1 |
| 5 | **`{second}`** (⟹ `Hc1` odd) | 3 |
| 7 | **`{first}`** (⟹ `Hc1` even) | 4 |

The mechanism: the internal realizability of a Moore block (curve 1, the near-cycle) at a
rectangle shape, together with the two vertical junctions LL→UL and UR→LR that cut across the
height `Hc1`, forces `Hc1` to a definite parity; but because `⌊n/2⌋` has **opposite parity for
`n=5` (=2) and `n=7` (=3)**, the same physical requirement maps to **opposite `sh` labels**.
The top-level junctions themselves always connect (verified: LL→UL, UL→UR, UR→LR are 4‑adjacent
for both `sh` values at n=5,7); the failure is the internal collapse of the Moore/Liu4 blocks
when handed the wrong-parity band height.

### Theorem (impossibility)

*There is no swap rule `swap(33,·)` making `fill(33,·)` a Hamiltonian path on every square.*

**Proof.** A swap rule assigns node `(33,e)` a **single** value `(sw,sh)`, hence a single
`sh∈{first,second,none}`. By the Lemma, validity at `n=5` requires `sh=second` and validity
at `n=7` requires `sh=first`. These are distinct singletons, so no value of `sh` satisfies
both. Since a global rule must validate **all** sizes simultaneously, none exists. Equivalently
and independently of the projection argument, the two size‑constraints are jointly
unsatisfiable over the complete node set they touch:
`valid(n=5) ∩ valid(n=7) = ∅` (both computed over all `9^4=6561` assignments of
`{(33,e),(1,m),(5,g),(5,o)}`, the exact set of nodes those two sizes reach). ∎

This is the *"contradictory parity demands at two sizes on the same split"* obstruction: a
single split (`Hc1` at `(33,e)`) is asked for even parity by one size and odd parity by
another. The root cause is structural — curve 33 carries an **infeasible Moore kernel** in
each of LL, LR, and the Moore block's shape constraint cannot be met at a fixed lower-band
parity across all `n`.

### Stronger observed pattern (verified where exhaustively checkable; not proved for all n)

Restricting to the 4-node set (Hilbert nodes at default), the composite admits *some* rule at
odd `n∈{3,5,7,9,15,17,23,25}` and **no** rule at `n∈{11,13,19,21,27,29}` — i.e. for `n≥7`,
individually feasible **iff `n ≡ ±1 (mod 8)`**. A 120 000-sample randomized search over the
full 11-node space at `n=11` and `n=13` also found **no** valid rule. This suggests curve 33
is not merely globally-inconsistent but individually unrealizable on a positive-density set of
odd sizes; we state it as an **observation**, since exhausting `9^{11}` per size was not
tractable. The `n=5`/`n=7` certificate above does not depend on it.

### Quasi-squares and the primitive constraint

`fill(33,·)` on `|w−h|=1` regions was tested by an incremental survivor search per top
orientation over `w,h ≤ 8`:
- **wide** (`w=h+1`): survives (to `(5,4)`) only under the **transpose** orientations
  `{g,x,o,a}`; the four **non-transpose** orientations `{e,f,m,y}` fail past the `2×1` domino.
- **tall** (`h=w+1`): the mirror image — survives (to `(4,5)`) only under the **non-transpose**
  orientations `{e,f,m,y}`; transpose orientations fail past the `1×2` domino.

This is precisely the base-primitive constraint: the terminal domino of a wide region is `2×1`
(realizable by the B,D / transpose class), of a tall region `1×2` (A,C / non-transpose class).
An orientation whose class mismatches the aspect ratio cannot even close the first non-trivial
quasi-square. Neither aspect connects over a full range — consistent with the square
infeasibility.

## Evidence

Engine: `research/aep.py`; all runs `cd /home/elessar/Projects/HilbertPlots && .venv/bin/python …`.

**Structure.**
```
NAME[33]='Moore+Liu4 #2'   entry_exit(33)=('interior','interior')
RULES[33] = [ (1, m=vflip, False), (5, g=rot90, False), (5, o=maindiag, True), (1, m=vflip, False) ]
orientations_used over n=1..40 → 12 nodes: (33,e);(1,m);(5,g),(5,o); + 8×(0,·)
complete node set reached at n≤7 = {(33,e),(1,m),(5,g),(5,o)}  (4 nodes)
```

**Orientation-independent search (9 single (sw,sh), n=1..40):** all fail —
```
(first,first)→n=3  (first,second)→n=5  (first,none)→n=5
(second,first)→n=3 (second,second)→n=7 (second,none)→n=5
(none,first)→n=3   (none,second)→n=7   (none,none)→n=5     hits: []
```

**Full-space incremental survivor search, n=1..40** (`glob33.py`):
```
n=1 surv=1 | n=2 surv=1 | n=3 surv=6 | n=4 surv=6 | n=5 surv=648 | n=6 surv=432 |
n=7 surv=0  ⇒ EMPTY at n=7 : INFEASIBLE   (total nodes fixed = 4)
```

**Exhaustive certificate on the 4-node set (`9^4=6561`)** (`conflict33.py`):
```
|valid(3)|=4374  |valid(5)|=648  |valid(6)|=1296  |valid(7)|=216
valid(5) ∩ valid(7) = 0     valid(3)∩valid(5)∩valid(6)∩valid(7) = 0
sh at (33,e):  n=5 → {second}   n=7 → {first}      (disjoint)
```

**Per-size achievable `sh` at `(33,e)` (4-node projection)** (`sh33.py`):
```
n= 3:[none,second]  5:[second]  7:[first]  9:[first,none]  11:[]  13:[]
n=15:[first] 17:[first,none] 19:[] 21:[] 23:[first] 25:[first,none] 27:[] 29:[]
```

**Even sizes / 2^k match** (`rand33.py`): default rule fails on even `n≡2 (mod 4)`
(6,10,14,…) because the top split is a no-op there and the odd sub-blocks are mis-parities;
`canonical_form` matches `hilbertplot.curve(33).points(k)` at k=1,2,3 = True. Randomized 120k-sample
search at n=11,13 (full 11-node space): no valid rule found.

**Quasi-squares** (`quasi33.py`, incremental survivor search per orientation, w,h≤8):
```
WIDE : transpose {g,x,o,a} sustain to max-dim 5 ; non-transpose {e,f,m,y} die at domino
TALL : non-transpose {e,f,m,y} sustain to max-dim 5 ; transpose {g,x,o,a} die at domino
```

Search-space accounting: orientation-independent = **9**; full per-orientation rule space =
`9^{12} = 282 429 536 481`; impossibility certificate exhausts the complete relevant subspace
`9^4 = 6561` for sizes `n≤7`, plus the pruned full-range survivor search (equivalent to the
whole `9^{12}`) collapsing at `n=7`.

## Verification

**Verdict: CONFIRMED (INFEASIBLE).** Independent adversarial re-check reproduces every
load-bearing number and finds the impossibility proof sound.

**What I re-ran** (`cd /home/elessar/Projects/HilbertPlots && .venv/bin/python …`, engine
`research/aep.py`):

1. **Structure / node set.** `RULES[33]`, `entry_exit(33)=('interior','interior')`, and
   `orientations_used` reproduced exactly: `[(1,m),(5,g),(5,o),(33,e)]` at **both** n=5 and
   n=7 (4 nodes); 12 nodes over n=1..40 (the extra 8 are all Hilbert `(0,·)`). Crucially I
   confirmed **n=5 and n=7 each reach only the 4-node set** — so the other 8 nodes cannot
   affect validity at those sizes, and the 4-node exhaustion is *complete* for the two sizes
   the certificate rests on.

2. **Impossibility certificate (9⁴=6561 assignments of the 4 nodes).** Reproduced exactly:
   `|valid(3)|=4374, |valid(5)|=648, |valid(6)|=1296, |valid(7)|=216`;
   `valid(5)∩valid(7)=∅`; `valid(3)∩valid(5)∩valid(6)∩valid(7)=∅`. Projecting onto `sh` at
   `(33,e)`: **n=5 → {second}, n=7 → {first}** (disjoint singletons). Both valid sets are
   non-empty, so the emptiness of the intersection is a genuine conflict, not a vacuous one.

3. **Survivor collapse.** Incremental survivor search over the 4-node space:
   `n=1..4` survive, `n=5 surv=648`, `n=6 surv=432`, **`n=7 surv=0`** — exhausted at n=7.
   (My per-`n` survivor counts at n=3,4 differ from `glob33.py`'s reported `6` because I
   count full 4-tuples where the report counts partial assignments over only the
   nodes-reached-so-far; the decisive figures `n=5→648`, `n=7→0` match exactly.)

4. **Orientation-independent search (all 9 single `(sw,sh)`), n=1..40: 0 hits** — reproduced.
   Applying the single rule to *all* curves reproduces the report's first-fail column
   verbatim (incl. `(second,second)→7`, `(none,second)→7`). Applying it only to node
   `(33,e)` gives those two a first fail at n=5 instead, but still 0 hits — the conclusion is
   interpretation-independent.

5. **2^k / hilbertplot match.** `canonical_form(fill(33,·,2ᵏ))==canonical_form(hilbertplot.curve(33).
   points(k))` is **True** for k=1,2,3.

**Logical soundness.** The proof is airtight *for the concrete `aep` construction*: a swap
rule is an `n`-independent map `(index,M)↦(sw,sh)`; validity at n=5 forces `sh@(33,e)=second`
and at n=7 forces `sh@(33,e)=first`; these are disjoint, so no single rule validates both,
hence none validates all squares. Because n=5 and n=7 touch only the 4 enumerated nodes, the
6561-assignment exhaustion is exhaustive for these sizes — the argument does **not** rely on
the pruned "equivalent of 9¹²" heuristic, and does **not** depend on the (correctly hedged)
`n≡±1 (mod 8)` observation. No gaps found; the report properly labels the individual-size
pattern as an unproved observation and the quasi-square results as verified-over-range.

**Scope note (unchanged from report, restated for honesty):** this is *verified over the
engine's construction for n=5,7* (and the pruned range n≤40), which suffices for a rigorous
impossibility of a global `aep` swap rule. It is **not** a from-first-principles proof that
the underlying geometry forbids every conceivable arbitrary-square generalization of curve 33
outside the aep/swap framework — that broader claim is not made.

## Open questions

1. **Prove** the observed `n≡±1 (mod 8)` individual-feasibility pattern (and the individual
   infeasibility at `n≡3,5 (mod 8)`), which would upgrade the obstruction from
   "globally inconsistent" to "no rule at a positive-density set of sizes." Requires a shape
   theorem for Moore/Liu4 blocks on rectangles.
2. Characterize exactly which rectangle shapes each Moore block (curve 1 at orientation `m`)
   and Liu4 block (curve 5 at `g`,`o`) admit as internal Hamiltonian paths — the missing
   lemma that would make the parity-flip mechanism fully symbolic rather than enumerative.
3. Structural conjecture for the synthesis: a composite curve inheriting an **infeasible
   near-cycle kernel (Moore, curve 1)** in a band is square-infeasible whenever that band's
   required internal parity is not a fixed function of `n`. Curve 33 is a witness.
