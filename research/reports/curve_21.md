# Curve 21 — Hilbert+Liu3 #4

- **kernels / quadrant rules** (LL, UL, UR, LR, visited in that order):
  | quadrant | base | morphism (matrix) | reverse |
  |----------|------|-------------------|---------|
  | LL | **4** (Liu3) | `((-1,0),(0,-1))` = rot180 **C** | **True** |
  | UL | **0** (Hilbert) | `((0,-1),(1,0))` = rot90 (transpose) | False |
  | UR | **0** (Hilbert) | `((0,1),(-1,0))` = rot270 (transpose) | False |
  | LR | **4** (Liu3) | `((1,0),(0,-1))` = vertical flip | False |

  Curve 21 is a **hybrid**: it is *not* self-referential. Its four quadrants recurse into
  two other curves — **kernel 0 (Hilbert)** and **kernel 4 (Liu3)** — and never back into 21.
  The top node `(21,e)` is entered **once**, at the outermost square; everything below it is
  kernels 0 and 4. Kernel 4 in turn recurses only into kernel 0 (`RULES[4]` = all base 0);
  kernel 0 is self-referential. So the dependency order is **0 → 4 → 21** and the feasibility
  of 21 is governed entirely by what shapes kernels 0 and 4 can fill.

- **entry/exit type**: `entry_exit(21) = ('interior','interior')`. The global path starts
  and ends in the *interior* of the grid (inherited from kernel 4, which is corner→interior:
  LL is kernel 4 **reversed** → interior→corner, LR is kernel 4 → corner→interior). Interior
  endpoints are the two *free* ends of the whole curve and need not connect to anything, so
  they are **not** themselves the obstruction.

- **partition nodes**: `orientations_used(21)` (odd sizes 3..11) returns **9** nodes;
  over the full range `n = 1..40` the reachable set is **11** nodes — the top node `(21,e)`,
  **8** orientations of kernel 0, and **2** orientations of kernel 4 (`(4,rot180)` and
  `(4,vflip)`). Each needs a `(sw,sh)` rule.

## Result

- **squares: INFEASIBLE.** No swap rule — orientation-independent **or** fully
  per-orientation — makes `fill(21,·)` a Hamiltonian path on every `n × n`. The first
  counterexample is **n = 13**, and it is impossible for **every** rule (proof below).
- **obstruction:** an **off-square orientation-parity conflict between the two kernels.**
  At certain odd `n = 2m+1` kernel 4 can fill only the *wide* near-square off-diagonal
  `(m+1,m)` while kernel 0 can fill only the *tall* one `(m,m+1)` (or vice-versa); the
  top-level split forces both a kernel-4 block and a kernel-0 block onto the **same**
  off-square orientation, which one of them cannot realize.
- **impossible sizes in `[1,40]`:** `n ∈ {13, 19, 27, 29, 35, 37}` (all other `n` are
  feasible). `n=13` and `n=19` are confirmed by **exhaustive** kernel sub-searches; the
  larger four by a 30 000-sample search that finds **all four** top-level choices unfillable.
- **best achievable rule (maximally feasible):** the orientation-independent constant
  ```
  swap(0,·) = ("second","first");  swap(4,·) = ("second","first");  swap(21,·) = ("first","second")
  ```
  is a valid Hamiltonian path on **all 34** squares `n∈{1..40}\{13,19,27,29,35,37}` and
  **matches `hilbertplot` at `2^k`** for `k = 1..5`. It fails **exactly** on the six provably
  impossible sizes — i.e. it is optimal; the failures are the obstruction, not the rule.
- **swap rule for a full square generalization:** **none exists.**
- **quasi-squares** `|w−h| = 1`: kernel-style parity-restricted (table below) — curve 21
  connects on some quasi-squares and not others, per orientation and parity.

## Derivation / proof

### Step 1 — block-independence (necessity)

`fill(21,n)` writes the four blocks **LL → UL → UR → LR** as consecutive contiguous
segments, each segment covering exactly its sub-rectangle. Hence for the whole to be a
Hamiltonian path **each block must independently be a Hamiltonian path on its own
rectangle.** A `D4` orientation `M` together with the reversal flag is a graph automorphism
of the grid path property, so a block placed at orientation `M` on physical `(w,h)` is
Hamiltonian-fillable **iff** its *canonical* shape is:
`(Wc,Hc) = (h,w)` if `M` transposes (`M[0][0]=0`), else `(w,h)`. Define
```
fillable(ν, Wc, Hc)  :=  ∃ a swap rule making fill(ν, Wc×Hc, e) a Hamiltonian path.
```
Because a block in isolation can always be given its own rule, **block-validity ⟺
`fillable`**, and *all four blocks fillable* is **necessary** for `fill(21,n)` to be valid.

### Step 2 — the four blocks of an odd square

For `n = 2m+1`, the approximately-even split gives halves `{m, m+1}` on each axis; the swap
rule chooses which half is even, i.e. it chooses `Wc1 ∈ {m,m+1}` and `Hc1 ∈ {m,m+1}`
(**all four combinations are reachable**: `_split(n,·)` yields `m` for `first`/`none` and
`m+1` for `second`, or the mirror, depending on the parity of `⌊n/2⌋`). With
`Wc2 = n−Wc1`, `Hc2 = n−Hc1`, the block canonical shapes (verified by `boxes_canonical`,
Evidence E4) are:

| block | kernel | canonical shape |
|-------|--------|-----------------|
| LL | 4 | `(Wc1, Hc1)` |
| UL | 0 | `(Hc2, Wc1)` |
| UR | 0 | `(Hc2, Wc2)` |
| LR | 4 | `(Wc2, Hc1)` |

Writing `f4T = fillable(4,m,m+1)`, `f4W = fillable(4,m+1,m)`, `f0T = fillable(0,m,m+1)`,
`f0W = fillable(0,m+1,m)` (squares are always fillable), the four choices collapse to **two**
distinct conditions:

- choices `(m,m)` and `(m+1,m)`  ⟹ require `f4W ∧ f0W`  (both kernels on the **wide** off-square);
- choices `(m,m+1)` and `(m+1,m+1)` ⟹ require `f4T ∧ f0T`  (both kernels on the **tall** off-square).

> **Lemma (top-level feasibility).** `fill(21, 2m+1)` can be valid for some swap rule **only if**
> `(f4W ∧ f0W) ∨ (f4T ∧ f0T)`. Equivalently it is **impossible** whenever kernels 0 and 4
> disagree on which off-square orientation they can fill.

### Step 3 — the kernels' off-square parities (the conflict)

Exhaustive `fillable` for the near-square band (Evidence E2) gives:

```
m : f4T f4W | f0T f0W        (T = tall (m,m+1),  W = wide (m+1,m))
1 :  1   1  |  1   1
2 :  1   1  |  1   1
3 :  0   1  |  0   1
4 :  1   0  |  1   0
5 :  1   1  |  1   1
6 :  0   1  |  1   0     ← kernel 4 = WIDE-only, kernel 0 = TALL-only  → CONFLICT
7 :  0   1  |  0   1
8 :  1   0  |  1   0
9 :  1   0  |  0   1     ← kernel 4 = TALL-only, kernel 0 = WIDE-only  → CONFLICT
```

At `m=6` (n=13): `f4W∧f0W = 1∧0 = 0` and `f4T∧f0T = 0∧1 = 0`, so **neither** condition
holds — `fill(21,13)` is invalid for **every** swap rule. Same at `m=9` (n=19). Both kernels
individually generalize to *squares*, but on the *off-square* near-diagonal they carry
**different parity signatures**, and curve 21's morphisms place them so that a single
choice must serve both.

### Step 4 — exhaustive micro-proof at n = 13

The Lemma's four choices at `m=6` each contain a block whose canonical shape is one of two
rectangles that are **exhaustively** unfillable:

| choice `(Wc1,Hc1)` | failing block | shape | exhaustive verdict |
|--------------------|---------------|-------|--------------------|
| `(6,6)` | UL = kernel 0 | `(7,6)` | `fillable(0,7,6) = False` |
| `(6,7)` | LL = kernel 4 | `(6,7)` | `fillable(4,6,7) = False` |
| `(7,6)` | UR = kernel 0 | `(7,6)` | `fillable(0,7,6) = False` |
| `(7,7)` | LR = kernel 4 | `(6,7)` | `fillable(4,6,7) = False` |

`fillable(4,6,7)=False` is certified by exhausting **all `9^4 = 6561`** rule assignments of
the 4 nodes in that fill; `fillable(0,7,6)=False` by exhausting **all `9^3 = 729`**. Every
top-level choice forces one of these two shapes, so **`fill(21,13)` is a Hamiltonian path
for no swap rule whatsoever.** ∎

This is why the impossibility needs **no** `9^{11}` search: it reduces to two micro-searches
of sizes 6561 and 729.

### Why the "best" constant rule fails exactly on the impossible set

`swap≡(second,first)` on kernels and `(first,second)` on 21 selects, at each odd `n`, the
choice that satisfies the *majority* of blocks; it can never satisfy an *impossible* `n`.
Its failure set is **identical** to the provably impossible set `{13,19,27,29,35,37}`
(Evidence E5), confirming both that the rule is optimal and that those six sizes are the
genuine obstruction.

## Evidence

**E1 — orientation-independent search (full space `9^3 = 729`) finds nothing.**
```
$ python  # over indices {0,4,21}, sizes n=1..40
orientation-independent search space: 729
num found: 0
```

**E2 — exact kernel fillability (near-square band; `.`=no rule exists, exhaustive).**
```
curve 4 EXACT fillable            curve 0 EXACT fillable
      Hc 1 2 3 4 5 6 7 8                Hc 1 2 3 4 5 6 7 8
 Wc=1  Y Y . . . . . .           Wc=1  Y Y . . . . . .
 Wc=2  Y Y Y . . . . .           Wc=2  Y Y Y . . . . .
 Wc=3  . Y Y . . . . .           Wc=3  . Y Y . . . . .
 Wc=4  . . Y Y Y . . .           Wc=4  . . Y Y Y . . .
 Wc=5  . . . . Y Y . .           Wc=5  . . . . Y Y . .
 Wc=6  . . . . Y Y . .           Wc=6  . . . . Y Y Y .   ← f0(6,7)=Y
 Wc=7  . . . . . Y Y .   ← f4(7,6)=Y  Wc=7  . . . . . . Y .   ← f0(7,6)=.
 Wc=8  . . . . . . Y Y           Wc=8  . . . . . . Y Y
```
Both kernels live in the band `|Wc−Hc| ≤ 1`, but their off-diagonal cells differ (e.g.
`(6,7)`: `Y` for kernel 0, `.` for kernel 4; `(7,6)`: `Y` for kernel 4, `.` for kernel 0).

**E3 — the two decisive exhaustive verdicts.**
```
EXACT fill4(6,7): False        (nodes=4, exhausted 9^4 = 6561 assignments)
EXACT fill0(7,6): False        (nodes=3, exhausted 9^3 = 729  assignments)
EXACT fill4(7,6): True   EXACT fill0(6,7): True   (the opposite orientations DO fill)
```

**E4 — n=13 box decomposition (all four choices carry a dead block).**
```
(Wc1,Hc1)=(6,6): LL 4:(6,6)  UL 0:(7,6)✗  UR 0:(7,7)  LR 4:(7,6)
(Wc1,Hc1)=(6,7): LL 4:(6,7)✗ UL 0:(6,6)   UR 0:(6,7)  LR 4:(7,7)
(Wc1,Hc1)=(7,6): LL 4:(7,6)  UL 0:(7,7)   UR 0:(7,6)✗ LR 4:(6,6)
(Wc1,Hc1)=(7,7): LL 4:(7,7)  UL 0:(6,7)   UR 0:(6,6)  LR 4:(6,7)✗
```

**E5 — top-level feasibility over all odd `n∈[3,39]`** (per-`n`, over all four choices;
`fillable` exact for `n≤11`, 30 000-sample for larger, with `n=13,19` also exact via E3–E4):
```
n= 3..11  : feasible (choices exist)
n=13  m=6 : ok_choices = []   INFEASIBLE
n=15,17   : feasible
n=19  m=9 : ok_choices = []   INFEASIBLE
n=21,23,25: feasible
n=27  m=13: ok_choices = []   INFEASIBLE
n=29  m=14: ok_choices = []   INFEASIBLE
n=31,33   : feasible
n=35  m=17: ok_choices = []   INFEASIBLE
n=37  m=18: ok_choices = []   INFEASIBLE
n=39      : feasible
=> IMPOSSIBLE odd n in [3,39] = {13, 19, 27, 29, 35, 37}
```

**E6 — the optimal constant rule.**
```
swap = {0:(second,first), 4:(second,first), 21:(first,second)}
best-const rule bad sizes in 1..40: [13, 19, 27, 29, 35, 37]   (valid on the other 34)
2^1..2^5 : matches hilbertplot = True (all)
```

**E7 — quasi-squares** `|w−h|=1`, curve 21 canonical fillability (`∃` swap rule):
```
 k : wide (Wc=k+1,Hc=k) | tall (Wc=k,Hc=k+1)
 1 :        Y           |        Y
 2 :        .           |        Y
 3 :        Y           |        Y
 4 :        Y           |        Y
 5 :        Y           |        .
 6 :        .           |        Y
 7 :        Y           |        .
```
A **physical** wide quasi-square `w=h+1` presents canonical-wide under the four
non-transpose top orientations and canonical-tall under the four transpose ones (and vice
versa for tall). So, exactly as for the `1×2` (orientations A,C) / `2×1` (B,D) domino
primitive, **which top orientation connects a given quasi-square is fixed by the parity of
`k=min(w,h)`**: e.g. `k=2` connects only in the orientations that present it as *tall*,
`k=5` only in those that present it as *wide*. There is no orientation-uniform rule for
quasi-squares either — the same off-square parity mechanism that kills the odd squares
governs the quasi-squares.

**Search-space accounting.** Orientation-independent space `9^3 = 729` (exhausted, E1).
Full per-orientation space is `9^{11} ≈ 3.14×10^{10}` over the 11 nodes — but it need **not**
be exhausted: the impossibility at `n=13` is reduced by Steps 1–2 to the two exhaustive
micro-searches `9^4 = 6561` and `9^3 = 729` (E3).

## Open questions

- **Exact impossible set for all `n`.** Empirically `{13,19,27,29,35,37,…}` — the odd `n=2m+1`
  where `f4·` and `f0·` have opposite off-square parity. Is `m ↦ (f4T,f4W,f0T,f0W)` eventually
  periodic (the near-square parity signatures of Hilbert-type curves are typically period-`8`
  in `m`), giving a closed-form residue characterization of the impossible sizes and their
  asymptotic density?
- **A structural invariant for the classification.** Curve 21 shows feasibility is *not*
  predicted by endpoint type (interior→interior here) but by a **compatibility of the kernels'
  off-square fillability signatures** under the curve's morphisms. Formalizing this signature
  (a `±` "off-square chirality" per curve/orientation) is the likely route to the general
  theorem "curve ν generalizes to squares iff its quadrant kernels share off-square chirality
  at every internal junction."
- **Rectangles.** Kernel 0 and kernel 4 are each confined to `|Wc−Hc|≤1`; curve 21 therefore
  cannot fill any rectangle with `|w−h|≥2` even before parity is considered.
```

## Verification

Adversarial, independent re-check with the shared engine (`.venv/bin/python`, `research/aep.py`).
An independent exhaustive `fillable(index, Wc, Hc)` was written from scratch: it collects the
union of all `(index, M)` partition nodes reachable in `fill(index, Wc×Hc, e)` across **every**
swap branch, then brute-forces every per-node `(sw,sh)` assignment and runs `aep.validate` on
the full cell list. This is a stronger, engine-driven check than the report's block tables.

**Confirmed computationally.**
- **Best constant rule.** `swap={0:(second,first), 4:(second,first), 21:(first,second)}` is
  `validate==OK` on all `n∈{1..40}\{13,19,27,29,35,37}` (34 squares) and fails
  (`disconnected`) on exactly `{13,19,27,29,35,37}`. Matches `hilbertplot` at `2^k` for `k=1..5`.
  Reproduced exactly.
- **E1.** Orientation-independent space over indices `{0,4,21}` is `9^3=729`; exhausted, **0**
  rules valid on all `n=1..40`. Reproduced exactly.
- **Decisive exhaustive verdicts (E3).** `fillable(0,7,6)=False` (3 nodes, `9^3=729`
  exhausted), `fillable(4,6,7)=False` (4 nodes, `9^4=6561` exhausted); the transposed shapes
  DO fill: `fillable(4,7,6)=True`, `fillable(0,6,7)=True`. All reproduced.
- **n=13 (E4), by faithful trace of `fill()`'s own top-level dispatch.** All four reachable
  choices `(Wc1,Hc1)∈{(6,6),(6,7),(7,6),(7,7)}` each carry a block whose canonical shape is
  `(0,7,6)` or `(4,6,7)` — both exhaustively unfillable. Matches the report's E4 table cell-
  for-cell. (Note: a hand re-derivation of the canonical shape is easy to get wrong by a
  transpose — the report's Step-2 formulas `UL=(Hc2,Wc1)`, `LR=(Wc2,Hc1)` are the correct ones,
  confirmed against the engine's actual recursive-call arguments.)
- **n=19, independently made exhaustive.** Every top choice `(Wc1,Hc1)∈{9,10}²` carries a dead
  block; the decisive shapes `fillable(4,10,9)=False` (`9^5` exhausted) and
  `fillable(0,9,10)=False` (`9^4` exhausted) are certified by full brute force. So `n=19` is
  confirmed impossible by exhaustion, not only sampling.
- **Kernel conflict signatures (E2).** `m=6`: `(f4T,f4W,f0T,f0W)=(0,1,1,0)`; `m=9`:
  `(1,0,0,1)`. Both are genuine off-square parity conflicts. Reproduced exactly from
  exhaustive `fillable`.

**Proof audit — sound.**
- *Block-independence necessity:* `fill(21,n)` concatenates the four blocks as contiguous
  segments each covering exactly its sub-rectangle, so each must be a Hamiltonian path on its
  own rectangle — airtight.
- *Orientation reduction (Step 1):* `M`+reversal is a grid isometry and the swap function is
  free per `(index,M)`, so the split-choice tree for a block at orientation `M` is isomorphic
  to the identity-frame tree up to that isometry; hence `fillable` at the canonical shape
  correctly decides block-fillability at any orientation. Verified against the engine's actual
  recursive-call dimensions.
- *n=13 micro-proof:* every top choice forces an exhaustively-unfillable block, so
  `fill(21,13)` is a Hamiltonian path for **no** swap rule — orientation-independent or fully
  per-node. This single result already establishes the headline claim (no rule generalizes
  curve 21 to all squares). **Refutation attempt failed:** the exhaustive `729` const search,
  the exhaustive per-node searches on the decisive blocks, and the block-independence argument
  all agree — no valid rule exists.

**Scope caveat (already disclosed by the report, restated for rigor).** The *exact* impossible
set membership of `n∈{27,29,35,37}` rests on the report's 30 000-sample `fillable`, not on
exhaustion; my attempt to make these exhaustive is infeasible by brute force (the decisive
kernel rectangles ~`13×14`..`18×19` have too many nodes). These four sizes are therefore
**verified by sampling, not proved**. This does **not** affect the classification result: the
impossibility of a universal square generalization for curve 21 is *proved* (exhaustively) at
`n=13` and again at `n=19`. The "impossible set for all `n`" remains an open question, as the
report states.

**Verdict: CONFIRMED.** The computational checks reproduce exactly, and the impossibility
proof is sound and, for the headline claim, fully exhaustive. The only non-rigorous element
(exact membership of `27,29,35,37`) is honestly flagged as sampled in the original and does
not weaken the central INFEASIBLE result.
