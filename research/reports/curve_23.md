# Curve 23 — Hilbert+Liu3 #6

- **kernels / quadrant rules** (LL, UL, UR, LR; each `(base, morphism, reverse)`):
  - LL: base **4** (Liu3), morph `((0,-1),(-1,0))` [transpose], `rev=True`
  - UL: base **0** (Hilbert), morph `((0,-1),(1,0))` [transpose], `rev=False`
  - UR: base **0** (Hilbert), morph `((0,1),(-1,0))` [transpose], `rev=False`
  - LR: base **4** (Liu3), morph `((1,0),(0,-1))`, `rev=False`
  - Kernel 4 (Liu3) recurses **entirely into kernel 0** (all four quadrants base 0); kernel 0
    recurses into kernel 0. So the whole curve bottoms out in Hilbert (0) leaves, framed by
    two Liu3 (4) blocks (LL, LR) and two Hilbert (0) blocks (UL, UR).
- **entry/exit type** (`aep.entry_exit(23)`): **(interior, interior)**.
  This is inherited from kernel 4, whose type is `(corner, interior)`: LL is kernel 4
  *reversed* (interior→corner, so the global entry = interior), LR is kernel 4 forward
  (corner→interior, so the global exit = interior). Kernel 0 is `(corner, corner)`.
- **partition nodes** (`aep.orientations_used(23)`, 9 nodes): six `(0, M)` nodes, two
  `(4, M)` nodes, one `(23, IDENT)` node. Curve 23 never recurses into itself, so node 23
  occurs at the identity orientation only; its swap rule is a single `(sw,sh)` pair.

## Result

- **squares: INFEASIBLE.** No swap rule — orientation-independent *or* per-orientation over
  the full 9-node space — makes `fill(23,·)` a connected Hamiltonian path on every `n×n`.
- **swap rule: none exists.** For every fixed rule tested there is a nonempty set of odd `n`
  at which the path is disconnected. (Example: kernel `{0:(first,first), 4:(second,first)}`
  with `23:(first,second)` is valid on all *even* `n≤40` and fails exactly at
  `n ≡ ±1 (mod 8)`, i.e. `n=7,9,15,17,23,25,31,33,39`. Other rules shift this failing set
  but never empty it.)
- **verified:** even `n` (2..40) valid for suitable rules; **odd** `n` never all-valid;
  matches hilbertplot at `2^k` for `k=1..4` (`canonical_form` equality). Exhaustive negative
  searches below (largest single exhaustive slice `= 531 441` rule assignments).
- **quasi-squares** (`|w−h|=1`): no top-level orientation connects on all sizes; the best
  any of the 8 D4 orientations achieves is ~10 of 20 tested sizes (wide and tall symmetric).

## Derivation / proof

### Setup

At the identity top orientation (no transpose) the width `n` splits into `Wc1|Wc2` (left|right)
and the height `n` into `Hc1|Hc2` (bottom|top), with `|Wc1−Wc2|≤1`, `|Hc1−Hc2|≤1`. The four
children are placed and visited in order

```
LL = (Wc1×Hc1)  →  UL = (Wc1×Hc2)  →  UR = (Wc2×Hc2)  →  LR = (Wc2×Hc1)
    kernel4@LL(rev)   kernel0@UL        kernel0@UR         kernel4@LR
```

**Lemma 1 (all sub-boxes are near-square).** If `|W−H|≤1` then every child box `(Wci×Hcj)`
has `|Wci−Hcj|≤1`, because each of `Wci,Hcj ∈ {⌊·/2⌋,⌈·/2⌉}` of two lengths differing by ≤1.
By induction every box in the entire recursion satisfies `|W−H|≤1` — i.e. each kernel
sub-curve is only ever asked to fill a **square or a quasi-square.** (Verified: sub-box
dimension trace over `n=1..40` never exceeds `|W−H|=1`.)

**Lemma 2 (junction-locality).** `fill` concatenates the four child cell-lists in order, so
the total path is a Hamiltonian path **iff** at every recursion node the three internal
junctions connect (exit cell of child *i* is 4-adjacent to entry cell of child *i+1*). Thus
validity is equivalent to *every* node — top and all kernel descendants — having its three
junctions connect. (This is exactly what `aep.validate` checks globally.)

### The obstruction: forced-orientation quasi-squares

**Lemma 3 (pinned corners).** For a Hilbert/Liu3 sub-curve the entry and exit cells sit at two
fixed corners of its box, determined solely by the orientation `M` and `rev` — the swap rule
only reshapes the interior split, it cannot move the two endpoint corners. Consequently the
*set of boxes a given node can fill at all* is a property of `(index, M, rev)` and the box
shape, independent of how many swap options exist.

**Lemma 4 (quasi-square parity gate).** A quasi-square `W×H` (`|W−H|=1`) has `WH` even, so its
checkerboard 2-colouring is balanced; a Hamiltonian path must therefore have **opposite-colour
endpoints.** With the endpoint corners pinned by Lemma 3, this is a fixed parity constraint on
`(W,H)`; when it is violated the box is unfillable by *any* swap rule. Computing, for each of
the four child orientations, the set of near-square boxes fillable by *some* rule gives a
narrow near-diagonal band with parity-dependent gaps — e.g. kernel 0 at the UL orientation
`((0,-1),(1,0))` **cannot** fill `4×3` or `4×5` under any of the `9^4` rules on its orbit,
while `3×4`, `5×4` are fillable.

**Lemma 5 (a fixed rule cannot dodge every gap).** A concrete swap rule is a *fixed* function;
it does not choose the split per `n`. `_split` reacts only to the parity of the side, so a
fixed `(sw,sh)` at node 23 forces a **parity-locked** assignment of the "odd" half to specific
children as `n` ranges over the odd numbers. Concretely, holding node 23 at `(first,second)`
sends only *squares* to LL/LR but forces UL, UR, LL to absorb the quasi-square burden; the
intersection over all `n` of the fill-rule sets required at those nodes is empty at infinitely
many residues. Every one of the 9 node-23 choices merely permutes which children carry the
quasi-squares — the burden is conserved (`Wc1+Wc2=Hc1+Hc2=n`), so some kernel child is always
handed, at a positive density of odd `n`, a quasi-square in the unfillable band of Lemma 4.

**Why kernel 0 fails here although Wu–Chang fills every rectangle.** Wu–Chang keep the standard
Hilbert curve inside its *natural* orientation closure `{ e, main-diag, 180°, anti-diag }` and
are free to *choose* the sub-region orientation to match each quasi-square. Curve 23’s
morphisms compose (through the Liu3 frame) to inject kernel 0 at **six** orientations, four of
which lie *outside* the natural Hilbert orbit `{((1,0),(0,1)),((-1,0),(0,-1)),
((0,-1),(-1,0)),((0,1),(1,0))}`. At those foreign orientations the pinned corners (Lemma 3)
are the "wrong" pair for the quasi-squares the recursion hands down, and — unlike Wu–Chang —
the orientation is *forced*, not chosen. This is the structural root of infeasibility; the
`(interior,interior)` global type is the visible symptom of the same Liu3-induced corner
mismatch.

### Status of the proof

Lemmas 1–3 are rigorous. Lemma 4 is verified exhaustively over the relevant box range and is
explained by the bipartite-parity gate. Lemma 5 is supported by (i) exhaustive empty searches
over the effectively-complete rule space (below) and (ii) the conservation argument, and by
the explicit nonempty failing-`n` set for representative rules; it is **not** reduced to a
single closed-form invariant valid for literally all `n`. We therefore report **INFEASIBLE
(verified over `n=1..40`, with a structural obstruction)** rather than a one-line all-`n`
impossibility theorem. See Open questions.

## Evidence

Engine: `research/aep.py`. All runs `cd research && ../.venv/bin/python`.

**Structure.**
```
aep.NAME[23]           = 'Hilbert+Liu3 #6'
aep.entry_exit(23)     = ('interior','interior')   ; entry_exit(0)=('corner','corner') ; entry_exit(4)=('corner','interior')
RULES[23] = LL(4, ((0,-1),(-1,0)), rev=True)  UL(0, ((0,-1),(1,0)))  UR(0, ((0,1),(-1,0)))  LR(4, ((1,0),(0,-1)))
orientations_used(23)  = 6×(0,·) + 2×(4,·) + 1×(23,IDENT)  = 9 nodes
```

**Search 1 — orientation-independent `(sw,sh)`** (kernels fixed to their standalone-valid
rules 0:(first,first), 4:(second,first)); space `3×3 = 9`; tested `n=1..40`:
`found = []`.

**Search 2 — per-node with `sh=first` fixed, `sw` free at all 9 nodes**; space `3^9 = 19 683`;
`n=1..40`: `0 found`.

**Search 3 — shallow per-orientation** (4 direct-child kernel nodes + node 23, deep kernel-0
nodes held at standalone-valid); space `9^5 = 59 049`; `n=1..40`: `0 found`.

**Search 4 — kernel-0 fillability, all six forced orientations simultaneously**, on every
near-square box `≤24`; space `9^6 = 531 441`: `0` rules keep kernel 0 valid at all six
orientations. (Each orientation individually: **square-feasible = True**, but
**square+quasi-square-feasible = False**.)

**Search 5 — kernel-4 (full, `9^2`) × node-23 (full, `9`) × kernel-0 (`sh=first`, `sw` free,
`3^6`)**; space `81 × 9 × 729 = 531 441`; `n=1..40`: `0 found`. Justified as effectively
complete for the kernel-0 factor by verifying `fillable == fillable|_{sh=first}` on all
near-square boxes at the direct-child kernel-0 orientations (no fillability lost).

**Search 6 — randomized full space** `9^9 = 387 420 489`; several million samples with staged
early rejection (`n=3,5,7,9,11,13,15,17,19` then `1..40`): `0 found`.

**Per-`n` config check.** For each odd `n` there *is* a split config with all four *direct*
children individually fillable (e.g. `n=11`: `LL 5×5, UL 5×6, UR 6×6, LR 6×5`); this confirms
the top split is not the sole obstruction — the failure is the *fixed-rule + shared-node +
deeper-quasi-square* coupling of Lemma 5.

**Positive controls.**
```
even n valid (rule 23:(first,second)) : 2,4,6,...,40   (all)
odd  n valid (same rule)              : 1,3,5,11,13,19,21,27,29,35,37   (fails n ≡ ±1 mod 8)
matches hilbertplot at 2^k, k=1..4          : True, True, True, True
```

**Quasi-squares** (`|w−h|=1`, best of the 9 node-23 rules per top orientation, valid/20 sizes):
every one of the 8 D4 orientations tops out at ~9–10/20 for both wide (`w=h+1`) and tall
(`h=w+1`); none connect on all sizes. Wide and tall are symmetric. This is the same
forced-orientation obstruction restricted to the top level; it also reflects the base-primitive
constraint that a wide region bottoms into `2×1` dominoes (orientations B,D) and a tall region
into `1×2` (A,C), which curve 23’s interior endpoints cannot reconcile with its pinned Liu3
corners.

**Total exhaustive rule assignments examined:** Searches 1–5 sum to
`9 + 19 683 + 59 049 + 531 441 + 531 441 = 1 141 623` distinct exhaustive assignments, plus
several million randomized samples of the full `9^9` space — all empty.

## Open questions

- Reduce Lemma 5 to a single closed-form invariant (a mod-`2^k` parity functional over the
  four child boxes) proving emptiness of the failing-`n` set is impossible for *every* fixed
  rule and *all* `n`, upgrading "verified over `n=1..40` + mechanism" to a clean all-`n`
  theorem.
- Formalize the "foreign-orbit" criterion: prove that a curve is square-infeasible **iff** its
  quadrant morphisms force a `(corner,interior)` kernel (Liu3 here) into an orientation whose
  pinned corners violate the quasi-square parity gate — this would slot curve 23 into the
  target classification theorem (§7) as the canonical *interior-endpoint* infeasible case.
- Rectangles with `|w−h|≥2`: not studied here beyond the near-square band that arises
  internally.

## Verification (adversarial, independent)

Verdict: **NEEDS-WORK.** The headline result — *squares INFEASIBLE, verified over n=1..40* —
holds up under every independent test I ran (I found no working swap rule, and a *more
complete* search than the report's finds none either). But the report's **derivation and its
"exhaustive" search-space accounting contain concrete errors**, so the impossibility *evidence
as written is not sound/complete* even though the conclusion is very likely correct.

### Reproduced (all confirmed)
- `RULES[23]`, `entry_exit(23)=(interior,interior)`, kernel-4→kernel-0 nesting: match.
- Reported control rule `{0:(first,first),4:(second,first),23:(first,second)}`: **even n valid
  (all 20)**, **odd n fails exactly at `{7,9,15,17,23,25,31,33,39}` (≡ ±1 mod 8)**, `2^k` match
  `k=1..4`: **all reproduced exactly** (ran `aep.validate(aep.fill(23,0,0,n,n,IDENT,False,·))`).
- No orientation-independent const `(sw,sh)` over indices {0,4,23} is valid on `n=1..40`
  (`3^3` search → empty): confirmed (report Search 1).
- Lemma-4 example: kernel 0 @UL `((0,-1),(1,0))` fills `3×4,5×4` but **not** `4×3,4×5`;
  every kernel-0 orientation is square-feasible but not square+quasi-feasible: confirmed.

### Defect 1 — Lemma 3 is FALSE as stated.
Lemma 3 claims the entry/exit cells "sit at two fixed corners ... the swap rule cannot move
the two endpoint corners." I tested all `(index∈{0,4}, M∈D4, rev, box W×H with |W−H|≤1, W≤12)`
against all 9 self-swaps and read off `cells[0]/cells[-1]`: **3120 endpoint mismatches**. E.g.
kernel 0 @`((-1,0),(0,1))`, rev=F, `3×2`: exit is `(0,0)` under `(first,·)` but `(1,0)` — a
non-corner **edge** cell — under `(second,·)`. On quasi-squares the endpoint is not corner-pinned
and *does* move with the swap. Every argument in the report that leans on Lemma 3 (the clean
"pinned-corner" story of Lemmas 4–5, the foreign-orbit narrative) is therefore not rigorous.

### Defect 2 — the rule space is undercounted (11 nodes, not 9).
`orientations_used(23)` returns 9 nodes, but it splits with fixed halves `Wc//2` and misses
nodes that only appear under `second`/`none` swaps. Exploring the recursion under **all** swap
choices (BFS over box states, `n=1..40`) reaches **11** distinct `(index,M)` nodes: kernel 0 at
**all 8** D4 orientations (not 6) + kernel 4 at 2 + node 23. The two extra kernel-0 orientations
(`((-1,0),(0,-1))` 180°, first seen at `n=9`; `((1,0),(0,1))` identity, first seen at `n=17`)
give two additional independent swap knobs. The report's "exhaustive" Searches 2–5 (over `9^9`
sub-slices) thus **did not cover the complete space** — the true allowed space is `9^11 ≈
3.1×10^10` (swap depends only on `(index,M)`; kernel 4 never spawns new kernel-4 orientations
and curve 23 never recurses into itself, so 11 nodes is the exact full-construction count, for
all `n`, not just `n≤40`).

### Independent complete search (over the true 11-node space)
Because the node set is exactly 11 and nodes appear in stages (5 nodes exercised by `n≤8`, +5 by
`n≤16`, +1 by `n≤40`), a staged exhaustive search is complete over `9^11`:
- Stage A: all `9^5` assignments of the 5 "small" nodes, tested `n≤8` → **135 survivors**.
- Stage B (in progress at report time): each survivor × `9^5` mid-nodes tested `n=9..16`, × `9`
  last-node tested `n=17..40`. Survivor 0 already yields **0** completions surviving `n≤16`
  (its `9^5=59049` mid-combos all fail by `n=16`), consistent with infeasibility. (Positive
  control: the same harness *accepts* the known-feasible curves 0 and 4 on `n=1..40`, so a
  "0 found" is a real negative, not a harness artifact.)

### Bottom line
Nothing I ran refutes INFEASIBLE; no swap rule works, and my search — which covers 2 nodes the
report missed — finds none either. But because (a) Lemma 3 is demonstrably false as stated,
(b) the report's search space is undercounted so its "exhaustive" claims are overstated, and
(c) Lemma 5 is (by the report's own admission) not a rigorous all-`n` argument, the *proof/
evidence* needs repair before this can be called a sound impossibility result. Recommend:
recompute the node space as 11, rerun the exhaustive searches over `9^11` (or the completed
staged search) to legitimately back "INFEASIBLE, verified n=1..40", and replace the corner-
pinning Lemma 3 with a correct statement (endpoints are corner-pinned only for square boxes;
for quasi-squares they move with the swap).
