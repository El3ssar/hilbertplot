# Curve 25 — Hilbert+Liu3 #8

- **kernels / quadrant rules** (visited LL, UL, UR, LR):
  | quad | base curve | morphism (matrix) | reverse |
  |------|-----------|-------------------|---------|
  | LL   | 0 (Hilbert) | `((0,-1),(1,0))` = rot +90° | no |
  | UL   | 0 (Hilbert) | `((0,-1),(1,0))` = rot +90° | no |
  | UR   | 0 (Hilbert) | `((0,1),(-1,0))` = rot −90° | no |
  | LR   | **4 (Liu3)** | `((1,0),(0,-1))` = reflect-x (vertical flip) | no |

  So curve 25 is three Hilbert quadrants plus one **Liu3** quadrant in LR. Its kernels are
  curve 0 (Hilbert) and curve 4 (Liu3); curve 4 in turn kernels only curve 0, and curve 0
  is self-kernel. Both kernels are among the eight already-known orientation-independent
  square generalizations (curve 0 → `(first,first)`, curve 4 → `(second,first)`), and both
  are valid on all squares under those rules (re-verified below). **The kernels are not the
  obstruction** — the failure is intrinsic to curve 25's own assembly.

- **entry/exit type**: `entry_exit(25) = ('edge', 'interior')` (enters on an edge, exits in
  the interior). The interior exit is inherited from the Liu3 (LR) quadrant, which is itself
  corner→interior.

## Result

- **squares: INFEASIBLE.** No swap rule — orientation-independent *or* fully
  per-orientation — makes `fill(25,·)` a Hamiltonian path on every `n × n` square. In fact
  **`n = 13` admits no valid path at all**: 0 of the 531 441 rules validate the 13×13 square
  (a *hard per-size* obstruction, stronger than a mere uniformity failure).
- **swap rule: none exists.** The complete per-orientation rule space (6 partition nodes,
  each ∈ {first,second,none}² ⇒ **9⁶ = 531 441** rules) was searched exhaustively and is
  empty: no rule is valid even through `n = 13`. Confirmed for all 8 global top-level
  orientations (each an independent 9⁶ search, all 0 survivors).
- **verified**: valid on `n × n` for `n ∈ {1,2,4,8,16,32}` (all powers of two, needing no
  swap) and matches hilbertplot exactly at `2^k` (`k = 1..4`); but for **odd** sizes no uniform
  rule survives. Exhaustive-search survivor cascade (IDENT, `n = 3,5,7,9,11,13`):
  `236196 → 6561 → 6561 → 1701 → 162 → 0`. Full-range revalidation (`n = 1..40` + `2^k`
  match) on the 162 rules surviving to `n=11`: **0** valid.
- **quasi-squares**: **no top-level orientation connects.** For both aspects (wide `w=h+1`,
  tall `h=w+1`) and all 8 global orientations, the full 9⁶ staged search finds **0** rules
  giving a connected path over sizes up to `8×7`. Curve 25 does not admit a uniform
  quasi-square generalization in any orientation.

## Derivation / proof

### Lemma 1 (the rule space is finite and size-independent: exactly 9⁶).

A swap rule is by definition a function of `(index, M)` only. The set of partition nodes
`(index, M)` that `fill(25, n×n, IDENT)` ever consults is the transitive closure of the
"quadrant-morphism" child relation starting from `(25, IDENT)`; this closure depends on the
catalog rules and D4 only, **not** on `n` (region sizes change which branches bottom out
early, but never introduce a new `(index, M)` pair). Computing the closure gives exactly six
nodes:

```
N0 = (0, mx)     N1 = (0, r90)    N2 = (0, r270)   N3 = (0, my)
N4 = (4, my=reflect-x)            N5 = (25, e)         [root]
child edges]
N5:  LL,UL→N1   UR→N2   LR→N4
N4:  LL→N2  UL,UR→N3  LR→N0
N0..N3 (the four Hilbert orientations) are closed among themselves.
```

`orientations_used(25)` returns these six for the default odd range, and the set is stable
over `n = 1..41` (verified: no new nodes). Hence for **every** `n` the fill of curve 25
consults the swap rule only at these six nodes, and the space of distinct rules is exactly
`9⁶ = 531 441`. ∎

### Theorem (impossibility on squares, all n).

*There is no swap rule making `fill(25,·)` a Hamiltonian path on every `n × n` square.*

**Proof.** A rule valid for all `n` must in particular be valid for `n = 1,3,5,7,9,11,13`.
By Lemma 1 the candidate set is the finite, size-independent space of `9⁶ = 531 441` rules.
Exhaustive evaluation of all `531 441` rules against `n = 3,5,7,9,11,13` eliminates every
candidate (survivor cascade `236196→6561→6561→1701→162→0`; the last survivors die at
`n = 13`). Since no rule passes even this finite necessary condition, no rule is valid for
all `n`. ∎

This is a **complete** impossibility proof (not merely "unverified beyond range"): the rule
space is finite and identical for every `n`, so failure on `n ≤ 13` is decisive for all `n`.

**Sharper form.** The size `n = 13` is *individually* infeasible: exhaustively, **0 of the
531 441 rules** produce a valid `13 × 13` path (whereas `n = 15` *is* individually feasible,
e.g. rule `N5=(second,second)`, all other nodes `(first,first)`). Thus the theorem does not
even rely on incompatibility *across* sizes — a single square size (13) has no construction
at all. This holds for every one of the 8 global orientations (8 independent 9⁶ searches,
all empty).

### Mechanism (where and why it breaks).

Small odd sizes *are* individually solvable (236 196 rules pass `n=3`, 162 pass all of
`n≤11`), but `n = 13` is a **hard per-size wall**: no rule fills the `13 × 13` square. The
obstruction localizes sharply:

1. **All 162 rules surviving to `n = 11` break inside the LR quadrant at `n = 13`** (100% of
   them; the disconnected consecutive pair lies in the top-level LR sub-region in every
   case). LR is node `N4` = **Liu3 under the vertical-flip (reflect-x) orientation**.

2. At `n = 13`, every surviving rule forces the top split to `(second,second)` (the only
   `(25,IDENT)` value compatible with `n ≤ 11`), giving column/row splits `7|6` and `7|6`.
   The LR box is therefore `W_c2 × H_c1 = 6 × 7`.

3. **The 6 × 7 rectangle has no Liu3@reflect-x Hamiltonian path under ANY rule.** Testing all
   `9⁵ · 9 = 59 049` assignments (curve-0 nodes × node `N4`) of the swap rule on this single
   rectangle yields **0** valid paths. This is a *rule-independent* local obstruction: the
   Liu3 quadrant that curve 25 must place in LR at `n = 13` simply cannot be filled.

4. The obstruction is **orientation-specific to the placement**: curve 4 (Liu3) *does* admit
   a `6 × 7` Hamiltonian path in other orientations (8 of the 72 orientation×const-rule
   combinations succeed), and Liu3@reflect-x is valid on all *squares*. It is precisely the
   combination "Liu3, reflect-x, opposite-parity `6 × 7` rectangle" — which curve 25's own
   `(second,second)` split forces at `n = 13` — that is empty. (Checkerboard parity is a
   *necessary* condition on the 42-cell path — endpoints must be opposite-colored — but it is
   not by itself the whole obstruction: both endpoint-colorings occur across rules yet none
   connects. The engine-verified emptiness over all rules is the rigorous statement.)

**Structural reading.** Curve 25 inherits its interior exit from a Liu3 (corner→interior)
quadrant pinned to the reflect-x orientation in LR. At an odd square the approximately-even
split hands that quadrant an opposite-parity near-square rectangle (`⌈n/2⌉ × ⌊n/2⌋+1` type
shape). Liu3 in that fixed orientation is not rectangle-universal there, and — unlike the
top-level Hilbert quadrants, whose orientations `N0..N3` can absorb the odd-parity via their
swap freedom — the LR-Liu3 node has no swap value that works across all the odd sizes. The
top split rule that rescues `n ≤ 11` (`second,second`) is exactly the one that delivers the
fatal `6 × 7` to LR at `n = 13`.

## Evidence

Engine: `research/aep.py`; run as `cd /home/elessar/Projects/HilbertPlots && .venv/bin/python …`.

**Structure.**
```
NAME[25] = 'Hilbert+Liu3 #8'
RULES[25] = LL:(0,rot+90) UL:(0,rot+90) UR:(0,rot-90) LR:(4,reflect-x)   all reverse=False
entry_exit(25) = ('edge','interior')
orientations_used(25) = 6 nodes = {(0,mx),(0,r90),(0,r270),(0,my),(4,my),(25,e)}
node set stable over n=1..41 (no new nodes)   ⇒ rule space = 9^6 = 531441
```

**Kernels valid on squares (not the obstruction).**
```
square_valid(0, (first,first))  = True
square_valid(4, (second,first)) = True
Liu3@reflect-x valid on all squares n=1..19 = True
```

**Powers of two (valid, matches hilbertplot).**
```
fill(25,n) valid for n=1,2,4,8,16,32 : OK
canonical match hilbertplot at 2^k, k=1..4 : True
```

**Orientation-independent search (9 rules, n=1..40, +2^k).** hits: `[]` (none).
First-failure size per const rule: `(first,*)`→3, `(second,second)`→11, `(second,none)`→5,
`(none,second/none)`→5.

**Exhaustive per-orientation search (full 9⁶ = 531 441 rule space).**
```
survivors after n=3 : 236196
survivors after n=5 : 6561
survivors after n=7 : 6561
survivors after n=9 : 1701
survivors after n=11: 162
survivors after n=13: 0
FINAL valid on n=1..40 (+2^k): 0
```

**Localization of the break (162 rules surviving to n=11).**
```
break location at n=13 = ('LR','LR')  for 162/162 rules
node values among survivors: N5=(second,second) forced;
   Hilbert nodes N0..N3 and Liu3 node N4 all have sh='first'
```

**Rule-independent local obstruction (the 6 × 7 LR box).**
```
6x7 Liu3@reflect-x valid under SOME rule (all 59049 curve-0 × N4 assignments): 0/59049
curve4 on 6x7 valid across 8 orientations × 9 const rules              : 8/72  (never at reflect-x)
```

**Per-size individual feasibility (∃ rule for that single size).**
```
n=13 : False  (0 / 531441 rules)   <- hard wall
n=15 : True   (e.g. N5=(second,second), all others (first,first))
```

**Quasi-square sweep (full 9⁶ staged, sizes up to 8×7, each of 8 global orientations).**
```
wide (w=h+1):  e,mx,my,r90,r180,r270,d,a  -> survivors 0  (all)
tall (h=w+1):  e,mx,my,r90,r180,r270,d,a  -> survivors 0  (all)
```

**Search-space sizes explored.** Orientation-independent: 9. Full per-orientation
(squares, IDENT): `9⁶ = 531 441`. Squares under all 8 global orientations: `8 × 9⁶`. Both
quasi-square aspects × 8 orientations: `16 × 9⁶` (staged). LR sub-problem (`6×7`): the
`5-node curve-0/Liu3 × N4 = 59 049` assignments evaluated. Per-size individual: `9⁶` per
tested `n`.

## Quasi-squares

For `|w−h| = 1`, **no top-level orientation admits a uniform connected path**. The full 9⁶
staged search over sizes up to `8 × 7` returns 0 survivors for *every* one of the 8 global
orientations, in both the wide (`w = h+1`) and tall (`h = w+1`) aspects (table above). So
curve 25 has no uniform quasi-square generalization in any orientation — consistent with,
and stronger than, its square infeasibility.

Relation to the primitive constraint: the leaf dominoes are orientation-locked — a `1×2`
(tall) domino is only produced by the base-cell code under the identity/anti-diagonal class
(paper orientations A, C), a `2×1` (wide) domino only under the main-diagonal/180 class (B,
D). A quasi-square recursion repeatedly hands its four children opposite-parity near-square
boxes whose forced leaf dominoes must alternate aspect down every branch; curve 25's LR
Liu3 node (fixed at reflect-x) cannot satisfy the resulting alternation for any swap value,
which is why every top-level orientation fails already at small sizes. The same Liu3@reflect-x
box-parity obstruction identified for squares (§Mechanism) is the operative cause here.

## Open questions

- Is there a closed-form (parity/boundary-vector) characterization of *why* Liu3@reflect-x
  fails on the specific opposite-parity near-square rectangles, matching the engine's
  exhaustive emptiness? (Checkerboard parity is necessary but not sufficient here.)
- Does the same "interior-exit Liu3 quadrant pinned to one orientation" mechanism predict
  infeasibility for the sibling Hilbert+Liu3 curves? (cross-curve synthesis)
- Rectangles `w×h` with `|w−h|>1`: does curve 25 ever connect, or is the LR-Liu3 obstruction
  generic?

## Verification

**Verdict: CONFIRMED.** An independent, from-scratch re-run of the engine reproduces every
load-bearing claim. The impossibility on squares is sound.

**What I ran (all via `research/aep.py`).**

1. *Structure & rule-space finiteness.* `RULES[25]`, `entry_exit(25)=('edge','interior')`,
   and `orientations_used(25)` all reproduced. The 6-node set is stable across `n=1..41`
   (re-computed the recursion-node closure independently: identical set). Lemma 1 is sound —
   the child relation `(index,M) → children` is a pure function of `RULES` and D4 morphisms;
   region size only controls when recursion bottoms out (`w≤2 and h≤2`) and never introduces
   a new `(index,M)` pair. So the distinguishable rule space is exactly `9⁶ = 531 441` for
   every `n`, and enumerating assignments to these 6 nodes covers every rule that can affect
   `fill(25,·)`.

2. *Exhaustive staged square search (my own enumeration of all 531 441 assignments).*
   Survivor cascade reproduced **exactly**:
   `531441 → (n=3) 236196 → (n=5) 6561 → (n=7) 6561 → (n=9) 1701 → (n=11) 162 → (n=13) 0`.
   Since any all-`n` rule must survive `{3,5,7,9,11,13}` and none does, no rule is valid for
   all `n`. Impossibility confirmed.

3. *Hard wall at n=13 (sharper form).* Directly evaluated **all 531 441 rules** on the
   single `13×13` square (not staged): **0 valid** (t≈276 s). So impossibility follows from
   one square size alone, independent of cross-size incompatibility — as claimed.

4. *n=15 is feasible.* Rule `(25,IDENT)=(second,second)`, all other nodes `(first,first)`
   gives `validate = OK` on `15×15`. Confirms the wall is specific to `n=13`, not odd sizes
   generally.

5. *Local `6×7` LR obstruction.* Curve 4 (Liu3) under reflect-x on `6×7`, searched over the
   full node space it consults (4 nodes ⇒ `9⁴ = 6561` rules): **0 valid**. Rule-independent
   local emptiness confirmed; this is the box `(second,second)` forces into LR at `n=13`.

6. *Kernels & powers of two (sanity, not the obstruction).* `square_valid(0,(first,first))`
   and `square_valid(4,(second,first))` both `True`; `fill(25,n)` valid for
   `n∈{1,2,4,8,16,32}`; canonical match to hilbertplot at `2^k`, `k=1..4`: `True`.

**One non-load-bearing numerical discrepancy.** The report's Mechanism §4 states curve 4 on
`6×7` succeeds in "8 of 72" orientation×const-rule combinations. My independent count gives
**24/72** (using `const_swap({4:sw})`). This does not affect any conclusion: the operative
claim — that reflect-x is **never** among the successful orientations on `6×7` — is
confirmed (0 hits at reflect-x in both counts), and the qualitative point (Liu3 *can* fill
`6×7` in other orientations, so the obstruction is placement-specific) holds a fortiori.
The "8/72" figure should be treated as an imprecise illustration, not evidence.

**Assessment of the proof's rigor.** The impossibility argument is complete and correct:
the rule space is genuinely finite and size-independent (Lemma 1, verified structurally and
computationally), and a finite necessary condition (validity at `n≤13`, indeed at `n=13`
alone) is exhaustively falsified. The distinction "verified computationally" vs "proved for
all n" is handled correctly — because the rule space does not grow with `n`, the finite
check is decisive for all `n`. No logical gap found. Verdict: **confirmed**.
