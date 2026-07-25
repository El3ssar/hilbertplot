# Curve 17 — Liu2+Liu4 #6

- **kernels / quadrant rules** (`aep.RULES[17]`, order LL, UL, UR, LR):
  - LL: base **3** (Liu2), morphism `((0,-1),(1,0))` (rot +90°), rev `False`
  - UL: base **5** (Liu4), morphism `((0,-1),(1,0))`, rev `False`
  - UR: base **5** (Liu4), morphism `((0,1),(1,0))`, rev `True`
  - LR: base **5** (Liu4), morphism `((0,1),(-1,0))`, rev `False`
  - Kernel DAG: `17 → {3, 5}`, `3 → {0}`, `5 → {0}`, `0 → {0}` (curve 0 = Hilbert is the
    self-recursive base). Every partition node therefore also needs a correct swap rule;
    the search below solves them jointly (bottom-up would give the same node set).
- **entry/exit type** (`aep.entry_exit(17)`): `('edge', 'interior')` — global entry on a
  non-corner edge cell, global exit in the interior.

## Result

- **squares: INFEASIBLE.** No swap rule (orientation-independent, per-orientation, or even
  size-dependent) makes `fill(17,·)` a Hamiltonian path on the **5×5** square; hence none
  works on all squares. Obstruction = a **bipartite endpoint-parity** contradiction.
- **swap rule:** none exists (for odd squares). For the *even* subfamily a single
  orientation-independent rule works:
  `{0:(first,first), 3:(first,second), 5:(first,second), 17:(first,second)}`.
- **verified:** with that rule, valid on **every even `n`, n = 2..40** (all 20 checked
  OK) and `n = 1`; **disconnected on every odd `n ≥ 3`**. Matches hilbertplot at `2^k`
  (`k = 1,2,3,4`; canonical-form equality **yes**). The 5×5 infeasibility is proved
  **exhaustively** over the complete rule space (9⁵ = 59 049 assignments, all fail).
- **quasi-squares** (`|w−h| = 1`): the admissible top orientation is forced to one D4
  coset that **alternates** with size, then relaxes:
  - wide `3×2`: transpose coset only (4/8) · tall `2×3`: non-transpose coset only (4/8)
  - wide `5×4`: non-transpose coset only · tall `4×5`: transpose coset only
  - wide `7×6`, tall `6×7` and larger: **all 8 orientations** connect.

## Derivation / proof

### Setup — the partition nodes

`aep.orientations_used(17)` reports the `(curve, orientation)` nodes met under the
*default* (unswapped) partition:

```
curve 0 : 7 orientations   curve 3 : 1   curve 5 : 3   curve 17 : 1   (12 nodes)
```

This under-counts, because a `"second"`/`"first"` swap can change which half is even and
thus expose nodes the default split never reaches. Enumerating **all three split modes at
every node** gives the *complete* node set actually reachable at a given size. At `n = 5`
the complete set is only 5 nodes:

```
(17, ((1,0),(0,1)))     (3, ((0,-1),(1,0)))
(5, ((0,-1),(1,0)))     (5, ((0,1),(-1,0)))     (5, ((0,1),(1,0)))
```

Because the engine's `swap(index, M)` reads only `(index, M)`, a rule assigns one of the
9 values `{first,second,none}²` to each node independently. The full rule space at `n = 5`
is therefore `9⁵ = 59 049`, and it is finite and exhaustively searchable.

### Lemma 1 (bipartite endpoint parity)

Color the grid `c(x,y) = (x+y) mod 2`. The `n×n` grid graph is bipartite with parts
`E = {c=0}` and `O = {c=1}`. For **odd** `n`, `|E| = (n²+1)/2` and `|O| = (n²−1)/2`, so
`|E| = |O| + 1` and all four corners lie in `E`. A Hamiltonian path on a bipartite graph
alternates parts; with an odd number `n²` of vertices it visits `E` once more than `O`,
which forces **both endpoints to lie in the majority part `E` (the corner color)**.
*Proof:* a path `v₀…v_{n²−1}` has `v_i ∈ E` iff `i` even; the multiset of visited parts is
`⌈n²/2⌉` from the part of `v₀` and `⌊n²/2⌋` from the other. Equality with `(|E|,|O|)`
requires `v₀ ∈ E`, and by the same count on the reversed path `v_{n²−1} ∈ E`. ∎

For `n = 5`: `|E| = 13`, `|O| = 12`; any Hamiltonian path must start **and** end on the
even color.

### Lemma 2 (curve-17 endpoint locus at n = 5)

Over the complete `9⁵` rule space, the realized `(entry, exit)` cell pairs of
`fill(17,·, 5,5, IDENT)` are **exactly** the four

| entry | color | exit | color |
|-------|-------|------|-------|
| (1,0) | 1 (O) | (2,0) | 0 (E) |
| (1,0) | 1 (O) | (2,1) | 1 (O) |
| (1,0) | 1 (O) | (3,0) | 1 (O) |
| (2,0) | 0 (E) | (3,0) | 1 (O) |

*(computational, exhaustive — see Evidence).* Both endpoints sit on/next to the bottom
edge; the entry is always at `(a,0)` with `a ∈ {1,2}` and the exit one step to its right
(`x = a+1`) either on the bottom row or the row above. **In none of the four pairs are
both endpoints on the even color `E`.** Structurally: when the exit stays on the bottom
row it has `x`-parity opposite to the entry (`x = a+1`), so the two endpoints differ in
color; the only pair with matching color is `(1,0)→(2,1)`, which is `(O,O)`. Either way
`(E,E)` is unreachable.

### Theorem (5×5 infeasibility ⇒ square-infeasibility)

By Lemma 1 a Hamiltonian path on the 5×5 grid needs both endpoints in `E`; by Lemma 2 the
AEP realization of curve 17 never places both endpoints in `E`. Hence **no swap rule makes
`fill(17,·)` valid on the 5×5 square.** The endpoint locus of Lemma 2 is exhaustive over
*all* per-node choices at that single size, so the impossibility holds even against a
hypothetical *size-dependent* rule (at a fixed size any such rule collapses to one per-node
assignment). Since a valid all-squares rule would in particular be valid on 5×5, **curve 17
does not generalize to arbitrary squares.** ∎

Consistently, the direct exhaustive search returns **0 / 59 049** valid, every failure
being `"disconnected"` (never a count/bbox failure): each sub-region fills correctly but a
junction always breaks — the geometric shadow of the parity contradiction. The best case
leaves exactly **one** irreparable break, at the LL→UL junction `(0,2)→(0,4)`.

### Why even `n` escapes

For even `n`, `|E| = |O| = n²/2`; Lemma 1 imposes **no** endpoint-color constraint, so the
parity obstruction vanishes. Empirically the rule
`{0:(first,first),3:(first,second),5:(first,second),17:(first,second)}` gives a valid path
on all even `n = 2..40`. (Individual odd `n = 3,7,9,15,17` are also feasible *in isolation*
under other per-node choices, but a single global rule must satisfy `n = 5`, which is
impossible — so no rule is valid on all squares.)

### Quasi-squares (`|w−h| = 1`)

A wide/tall quasi-square forces the top orientation into one D4 coset — **transpose**
(`M[0][0]=0`, the `{B,D}`-family that realizes the `2×1` wide domino) or **non-transpose**
(`M[0][0]≠0`, the `{A,C}`-family that realizes the `1×2` tall domino). Empirically:

```
wide 3×2 : transpose only      tall 2×3 : non-transpose only
wide 5×4 : non-transpose only  tall 4×5 : transpose only
wide 7×6 : all 8               tall 6×7 : all 8
```

The admissible coset is exactly the one whose bottoming-out dominoes tile the residual
strip; because each halving flips the residual domino between `2×1` and `1×2`, the
admissible coset **alternates** as the even side grows `2 → 4 → …`, and once both sides are
`≥ 6` there is enough slack for either coset, so all 8 orientations connect. This is the
same `1×2`↔`A,C` / `2×1`↔`B,D` primitive constraint of Wu & Chang, propagated to the top
node.

## Evidence

Complete-node exhaustive search at `n=5` (the certificate):

```
COMPLETE n=5 node set: 5   full search space: 9^5 = 59049
tested 59049/59049, feasible=False
failure reasons over all rules: {'disconnected': 59049}
achievable (entryP,exitP) parities: {(1,0), (1,1), (0,1)}   # (0,0) NEVER
min breaks over all rules: 1   (break at LL→UL junction (0,2)->(0,4))
distinct (entry,exit) cells: (1,0)->(2,0); (1,0)->(2,1); (1,0)->(3,0); (2,0)->(3,0)
```

Orientation-independent searches (both empty):

```
kernels fixed to known rules, 9 options for node 17 on n=1..40 : 0 valid
all 4 indices {0,3,5,17} free, 9^4 = 6561, prune n=1..12 then n=1..40 : 0 valid
```

Full per-orientation space over the 12 default nodes ≈ `9^12 ≈ 2.8·10^11`, explored by
randomized coordinate descent (55 restarts): best assignment still fails **8 of 18** odd
sizes; never reaches 0 — consistent with the `n=5` impossibility.

Even-square validity and `2^k` match (rule
`{0:(first,first),3:(first,second),5:(first,second),17:(first,second)}`):

```
EVEN n in 2..40 valid : [2,4,6,...,40]   (all 20 OK)
ODD  n in 1..40 valid : [1]              (all odd n>=3 disconnected)
2^k match vs hilbertplot    : k=1,2,3,4 -> match=True
5x5 color balance     : 13 even / 12 odd
```

Reproduce:

```bash
cd /home/elessar/Projects/HilbertPlots
.venv/bin/python -c 'import sys; sys.path.insert(0,"research"); import aep, itertools
# complete node set at n=5 (all split modes), then exhaustive 9^5
def all_nodes(idx,w,h,M):
    seen=set(); memo=set()
    def rec(i,ww,hh,MM):
        tr=(MM[0][0]==0); Wc,Hc=(hh,ww) if tr else (ww,hh)
        if ww<=2 and hh<=2: return
        if (i,ww,hh,MM) in memo: return
        memo.add((i,ww,hh,MM)); seen.add((i,MM))
        for sw in ("first","second","none"):
          for sh in ("first","second","none"):
            W1,W2=aep._split(Wc,sw); H1,H2=aep._split(Hc,sh)
            for k,(cw,ch) in enumerate([(W1,H1),(W1,H2),(W2,H2),(W2,H1)]):
                b,mo,_=aep.RULES[i][k]; sM=aep.matmul(MM,mo); st=(sM[0][0]==0)
                aw,ah=(ch,cw) if st else (cw,ch); rec(b,aw,ah,sM)
    rec(idx,w,h,M); return sorted(seen,key=str)
nodes=all_nodes(17,5,5,aep.IDENT); opts=list(itertools.product(["first","second","none"],repeat=2))
ok=any(aep.validate(aep.fill(17,0,0,5,5,aep.IDENT,False,
        aep.per_orientation_swap(dict(zip(nodes,c)))),5,5)=="OK"
       for c in itertools.product(opts,repeat=len(nodes)))
print("nodes",len(nodes),"space",9**len(nodes),"feasible",ok)'
```

## Open questions

- Characterize *exactly* which odd `n` are feasible in isolation (sampling found
  `3,7,9,15,17` feasible and `5,11,13,19` not). `n=5` is the only one proved infeasible by
  the pure parity locus (Lemma 2); `n=11,13,19` may hide a distinct, deeper junction
  obstruction or merely need a rarer assignment — worth an exhaustive complete-node search
  at those sizes.
- General rectangles `w×h`: the even-side/odd-side parity dichotomy seen for squares and
  quasi-squares suggests a `(⌊w/2⌋,⌊h/2⌋)`-parity classification; not yet proved.
- Structural theorem: relate the `(E,E)`-unreachability of the endpoint pair to curve 17's
  `edge → interior` type and the reversed UR quadrant — the mechanism that pins entry and
  exit onto the same bottom strip.

## Verification

**Verdict: CONFIRMED** (adversarial, independent re-check).

Reproduced every load-bearing claim; actively tried to refute the impossibility and could not.

- **Even-subfamily rule** `{0:(first,first),3:(first,second),5:(first,second),17:(first,second)}`:
  independently re-ran `aep.validate` on `n×n` for `n=1..40`. Valid on `n=1` and **all**
  even `n=2..40` (20/20); **disconnected on every odd `n=3..39`**. `2^k` canonical-form
  match vs `hilbertplot.curve(17)` holds for `k=1,2,3,4`. Matches the report exactly.
- **5×5 impossibility (the crux) — reproduced two independent ways.** (a) Re-ran the
  report's complete-node exhaustive search: 5 nodes, `9^5 = 59 049` assignments, **0
  feasible, all 59 049 `disconnected`**. Realized `(entry,exit)` cells are exactly
  `(1,0)→(2,0)`, `(1,0)→(2,1)`, `(1,0)→(3,0)`, `(2,0)→(3,0)`; realized endpoint parities
  `{(0,1),(1,0),(1,1)}` — parity `(0,0)`/`(E,E)` **never** occurs. (b) I did **not** trust
  the report's `all_nodes` helper — it computes each sub-region's absolute dimensions from
  the *sub*-orientation's transpose `st=(sM[0][0]==0)`, whereas `fill` derives them from the
  *parent* orientation `M`, so the helper is not a faithful mirror of `fill`. I therefore
  re-derived the complete node set by **instrumenting `fill` itself** (a recording `swap`
  callable, iterated to a fixpoint over all `9`-per-node assignments). This authoritative
  method returns the **identical 5-node set**, and the exhaustive search over its closure is
  again **0/59 049 feasible**. The helper's shortcut is thus non-load-bearing here.
- **Parity lemmas.** Lemma 1 is the standard bipartite argument and is correct: for odd `n`
  the `n×n` grid has `|E|=(n²+1)/2`, `|O|=(n²−1)/2`, all corners in `E`, and a Hamiltonian
  path on `n²` (odd) vertices must have **both** endpoints in the majority part `E`. Checked
  `n=5`: 13 `E` / 12 `O`. Lemma 2's endpoint locus is confirmed exhaustively above; since
  `(E,E)` is unreachable, no swap assignment can yield a Hamiltonian path on 5×5. The
  step "valid on all squares ⇒ valid on 5×5" is sound, and the engine's `swap(index,M)`
  cannot even depend on `n`; the report's stronger argument against a *hypothetical*
  size-dependent rule (at fixed `n=5` it collapses to one per-node assignment, all
  exhausted) is also valid. **The impossibility holds.**
- **Refutation attempt.** Searched the full per-node rule space at `n=5` (including all
  `"none"` options) via both the report's enumeration and my independent instrumented
  closure — no valid rule exists. No logical gap found in the obstruction.
- **Quasi-squares (secondary).** Independently confirmed the alternating coset pattern for
  the small cases: `wide 3×2` transpose-only (4/8), `tall 2×3` non-transpose-only (4/8),
  `wide 5×4` non-transpose-only (4/8), `tall 4×5` transpose-only (4/8). The larger
  `7×6`/`6×7` "all 8" claim was not re-verified exhaustively (search space too large under
  the enlarged node closure); it is plausible and consistent with the trend but remains
  *asserted, not independently confirmed here*.

Commands run: `aep.validate`/`aep.fill` over `n=1..40` with the even rule and `2^k` match;
exhaustive `9^5` search over the report's node set; an independent fixpoint node-closure
built by instrumenting `fill`, then exhaustive over that closure; capped per-orientation
searches for the four small quasi-squares. All outputs matched the report (save the noted
non-load-bearing `all_nodes` imperfection and the un-rechecked `7×6`/`6×7` claim).
