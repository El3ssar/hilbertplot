# Curve 36 — Moore+Liu4 #5

- **kernels / quadrant rules** (visited order LL, UL, UR, LR):
  | quadrant | base | morphism `M` | reverse |
  |----------|------|--------------|---------|
  | LL | 5 (Liu4)   | `((0,1),(-1,0))` = **rot270** (`x`) | **True** |
  | UL | 5 (Liu4)   | `((-1,0),(0,1))` = **hflip** (`y`)  | **True** |
  | UR | 5 (Liu4)   | `((1,0),(0,1))`  = **identity** (`e`)| False |
  | LR | 1 (Moore)  | `((-1,0),(0,-1))`= **rot180** (`f`) | False |

  Curve 36 recurses into two kernels: **Liu4 (5)** in three quadrants and **Moore (1)** in
  the LR quadrant. Both kernels in turn recurse only into **Hilbert (0)**. So the dependency
  tree is `36 → {5, 1} → 0`, and the problem is attacked bottom‑up: fix the swap rules of the
  kernels (0, then 1 and 5), then the top node (36). **Both kernels are themselves
  square‑infeasible** (curve 1 = Moore is infeasible; curve 5 = Liu4 is feasible only with the
  orientation‑independent rule `(first,second)`), and curve 36 inherits a *fresh* obstruction
  of its own at the top level.

- **entry/exit type:** `entry_exit(36) = ('edge','interior')`. The global path starts on an
  edge and **ends in the interior**. (Interior exit alone does not preclude a standalone
  square path — the top node is only ever used at the outermost level — so feasibility is
  decided by the junction parities below, not by the endpoint type.)

- **partition nodes** (`orientations_used(36, sizes=range(3,42,2))`) — the `(curve,
  orientation)` pairs that need a swap rule — **13 nodes**, a closed set:
  - `(36, e)` — the top node, identity only;
  - `(5, e)`, `(5, y)`, `(5, x)` — Liu4 at three orientations;
  - `(1, f)` — Moore at rot180;
  - `(0, e), (0, m), (0, y), (0, f), (0, g), (0, x), (0, a), (0, o)` — Hilbert at **all eight**
    orientations.

  (The eighth Hilbert orientation `(0, y)` first appears only at `n = 17`, so the node set
  computed from small odd sizes `range(3,12,2)` returns 12; the complete closure over
  `range(3,42,2)` — equivalently the BFS closure of the morphism transition relation — is 13.
  The full per‑node search below uses all 13.)

## Result

- **squares: INFEASIBLE.** No swap rule — orientation‑independent **or** per‑orientation over
  the full 13‑node space — makes `fill(36, ·)` a valid Hamiltonian path on every `n×n`
  square. The construction already fails at **n = 7** (jointly with **n = 5**) for **every**
  rule.
- **swap rule: none exists.**
- **verified:**
  - orientation‑independent search (**9** combos, one `(sw,sh)` for all curves/orientations):
    **0** valid on `n=1..40`.
  - per‑curve‑constant search (**9⁴ = 6561** combos, one `(sw,sh)` per curve in `{0,1,5,36}`):
    **0** valid on `n=1..40`.
  - full per‑node search (**13 nodes, 9¹³ ≈ 2.54 × 10¹²** combos): exhaustive backtracking with
    sound pruning explored **9027** partial assignments and returned **0** valid on `n=1..40`.
  - matches hilbertplot at `2^k`: **yes** (`k=1..4`, i.e. sides 2,4,8,16 — at powers of two both
    splits are even, the swap is inert, and `fill(36,·)` reproduces `hilbertplot.curve(36)` up to the
    canonical symmetry).
- **quasi‑squares** (`|w−h| = 1`): also **infeasible**, and more sharply so — **individual**
  quasi‑square sizes are unrealizable for *every* swap rule. The realizable sizes split the 8
  orientations into the two classes by whether they transpose the axes (non‑transposing
  `{e,m,y,f}` vs transposing `{a,g,x,o}`), mirroring the wide‑domino / tall‑domino base
  constraint. Over exhaustive per‑size tests `h = 1..5`:
  - **non‑transposing** `{e,m,y,f}`: **wide** `(h+1)×h` realizable for `h ∈ {1,2,3}`, blocked
    at `h ∈ {4,5}`; **tall** `h×(h+1)` realizable for `h ∈ {1,2,4,5}`, blocked at `h = 3`.
  - **transposing** `{a,g,x,o}`: the exact transpose — **wide** realizable for `h ∈ {1,2,4,5}`,
    blocked at `h = 3`; **tall** realizable for `h ∈ {1,2,3}`, blocked at `h ∈ {4,5}`.

  No orientation realizes all quasi‑squares of either aspect.

## Derivation / proof

The impossibility has a short, self‑contained certificate: **two square sizes impose
contradictory parity demands on the single width‑split of the top node `(36, e)`.** Because a
swap rule is a function of `(index, orientation)` *only* — it cannot depend on `n` — the two
demands cannot both be met.

Setup. At the top node the canonical frame is `Wc = Hc = n`. The width split produces
`Wc1` (width of the **left** column, holding LL and UL) and `Wc2` (width of the **right**
column, holding UR and LR); the height split produces `Hc1` (bottom band) and `Hc2` (top
band). The four sub‑boxes and their visiting order are

```
LL=(0,0,Wc1,Hc1) → UL=(0,Hc1,Wc1,Hc2) → UR=(Wc1,Hc1,Wc2,Hc2) → LR=(Wc1,0,Wc2,Hc1)
```

with sub‑curves LL,UL = Liu4 **reversed**, UR = Liu4, LR = Moore. Connectivity of the whole
path requires the three internal junctions to be 4‑adjacent:
`LL.exit ~ UL.entry` (vertical, inside the left column), `UL.exit ~ UR.entry` (horizontal,
across the vertical divider `x = Wc1−1 | Wc1`), and `UR.exit ~ LR.entry` (vertical, inside the
right column). The endpoint cells of the edge→edge Liu4 sub‑curves sit at coordinates whose
offsets depend on the **parities** of their box dimensions; the horizontal `UL→UR` and the
right‑column `UR→LR` junctions therefore impose a congruence on the column widths.

**Lemma 1 (n = 5 forces the *right* column even).** For `n = 5`, `fill(36,0,0,5,5,e,·)` is a
valid Hamiltonian path **only if** the width split of `(36, e)` makes `Wc1 = 3` (odd, left) and
`Wc2 = 2` (even, right) — i.e. `sw(36,e) = "second"`.
*Proof (exhaustive).* `n = 5` touches exactly the four nodes `(36,e), (5,e), (5,y), (5,x)`
(the LR box is `2×2`, a base case, so Moore is not exercised). Enumerating all
`9⁴ = 6561` assignments of these four nodes, **432** yield a valid `5×5` path, and **all 432**
have `sw(36,e) = "second"` (the two feasible width/height values are `("second","first")` and
`("second","none")`). ∎

**Lemma 2 (n = 7 forces the *left* column even).** For `n = 7`,
`fill(36,0,0,7,7,e,·)` is valid **only if** `Wc1 = 4` (even, left) and `Wc2 = 3` (odd, right)
— i.e. `sw(36,e) = "first"`.
*Proof (exhaustive).* `n = 7` touches the five nodes `(36,e), (5,e), (5,y), (5,x), (1,f)`.
Enumerating all `9⁵ = 59049` assignments, the feasible ones **all** have `sw(36,e) = "first"`
(feasible values `("first","none")`, `("first","second")`). ∎

**Theorem (squares infeasible).** There is no swap rule `swap(36, ·)` (with any swap rules for
the kernels) under which `fill(36, ·)` is a valid Hamiltonian path on every `n×n` square.
*Proof.* A swap rule assigns `swap(36, e)` a single value, in particular a single width mode
`sw(36,e) ∈ {first, second, none}`, independent of `n`. Lemma 1 requires
`sw(36,e) = "second"` at `n = 5`; Lemma 2 requires `sw(36,e) = "first"` at `n = 7`. These are
incompatible, so no rule validates both `n = 5` and `n = 7`. ∎

**Mechanism (why the demanded even‑side flips).** The requirement is a parity of the left
column width `Wc1`. The AEP width split of an odd side `n = 2q+1` yields the halves `{q, q+1}`;
the swap mode chooses which of them is `Wc1`. Being able to place a *chosen parity* on the left
is exactly `q mod 2`: at `n = 5` (`q = 2`, halves `{2,3}`) an **odd** left column means
`Wc1 = 3` = the *larger* half (`sw="second"`), whereas at `n = 7` (`q = 3`, halves `{3,4}`) an
**even** left column means `Wc1 = 4` = again the *larger* half but now `sw="first"`, because
the larger half flips parity as `q` increments. The junction algebra fixes the *required*
`Wc1` parity (even at `n=7`, odd at `n=5` — a value tied to the Liu4/Moore endpoint offsets),
while the *available* `Wc1` parity per swap mode alternates with `q`; the two go out of phase,
so a fixed mode cannot track the requirement. Concrete valid witnesses exhibit the geometry:

```
n=5 (sw=second):  Wc1=3, Wc2=2 ;  junctions
   LL exit (0,1) → UL entry (0,2)      [left column, vertical]     ✓
   UL exit (2,2) → UR entry (3,2)      [across divider, row y=Hc1] ✓
   UR exit (4,2) → LR entry (4,1)      [right column, vertical]    ✓
n=7 (sw=first):   Wc1=4, Wc2=3 ;  junctions
   LL exit (1,2) → UL entry (1,3)                                  ✓
   UL exit (3,4) → UR entry (4,4)                                  ✓
   UR exit (6,3) → LR entry (6,2)                                  ✓
```

The `UL→UR` junction sits on the top‑band bottom row `y = Hc1` at the divider; its horizontal
adjacency needs UL’s (reversed‑Liu4) exit at the right edge `x = Wc1−1` to face UR’s (Liu4)
entry at `x = Wc1`, and the right‑column `UR→LR` junction needs UR’s exit and LR’s (Moore)
entry to share a column of the right block — the two conditions pin `Wc1`’s parity to opposite
residues at `n=5` and `n=7`.

**Corollary (quasi‑squares).** The same top‑node split governs quasi‑squares, and there the
obstruction is per‑size rather than only per‑family: for a fixed orientation there exist quasi‑
square sizes (e.g. `5×4` at identity `e`, or `4×3` transposed) for which *no* assignment of the
13 nodes yields a valid path (verified exhaustively for `h=1..5`). The wide/tall realizable
residues are exchanged by transposition, which is exactly the base‑primitive dichotomy: a
`2×1` wide domino is filled in the axis‑orientations `{e,m,y,f}` and a `1×2` tall domino in the
transposing `{a,g,x,o}`; the AEP recursion carries this parity of the terminal domino up to the
top, so wide vs tall connectivity tracks the transpose class of the orientation.

## Evidence

All commands run from `/home/elessar/Projects/HilbertPlots` with `.venv/bin/python`,
`sys.path.insert(0,"research"); import aep`.

**Structure.**
```
NAME[36]                    = 'Moore+Liu4 #5'
RULES[36]  LL (5, rot270 x, rev=True)  UL (5, hflip y, rev=True)
           UR (5, ident e, rev=False)  LR (1, rot180 f, rev=False)
entry_exit(36)              = ('edge','interior')
orientations_used(36, range(3,42,2)) : 13 nodes
   (36,e); (5,e),(5,y),(5,x); (1,f); (0,{e,m,y,f,g,x,a,o})
```

**Cheap searches (both empty).**
```
global const (9)              hits: []          # scratch_36.py
per-curve const (9^4 = 6561)  full-range hits: 0 # scratch_36.py
```

**Full per‑node exhaustive search (empty).**  `scratch_csp.py` — backtracking over all 13
nodes (`9¹³ ≈ 2.54×10¹²`), testing `fill(36,0,0,n,n,e,·)` for `n=1..40`, pruning as soon as a
fully‑determined size is invalid:
```
DFS nodes explored: 9027
NO SOLUTION EXISTS over full per-node space (exhaustive).
```

**Minimal infeasible prefix.**  `scratch_minconflict.py`:
```
n=1.. 6 : SAT
n=1.. 7 : UNSAT     -> smallest infeasible N = 7
```

**The two‑size obstruction (Lemmas 1–2).**  `scratch_obstruction.py` (shared nodes =
`(36,e),(5,e),(5,y),(5,x)`):
```
n=5 shared-feasible count: 432     v36 values: [('second','first'), ('second','none')]
n=7 shared-feasible count: 162     v36 values: [('first','none'),  ('first','second')]
intersection: 0
```
so `n=5 ⟹ sw(36,e)="second"` and `n=7 ⟹ sw(36,e)="first"`, disjoint.

**Junction witnesses.**  `scratch_mech.py` — the `n=5 (sw=second)` and `n=7 (sw=first)`
sub‑box boundaries and the three adjacent junction cell‑pairs shown above (all `adjacent=True`).

**2^k reproduction.**
```
k=1..4 (sides 2,4,8,16): canonical_form(fill(36,...)) == canonical_form(hilbertplot.curve(36).points(k))  -> True
```

**Quasi‑squares.**  `scratch_quasi2.py` — exhaustive per‑size SAT (does *any* swap make that
single size valid), `h=1..5`:
```
non-transposing e,m,y,f :  wide h1+h2+h3+h4-h5-   tall h1+h2+h3-h4+h5+
transposing     a,g,x,o :  wide h1+h2+h3-h4+h5+   tall h1+h2+h3+h4-h5-
```

**Even‑n note.**  With the trivial all‑`(first,first)` rule, `fill(36,·)` is valid on even
`n ∈ {2,4,8,12,16,20,24,28,32,36,40}` (the powers/multiples of 4, plus 2) but not on
`n ≡ 2 (mod 4)` beyond 2; the odd sizes fail from `n=5` on. The square generalization requires
*all* `n`, so this is subsumed by the theorem — but it indicates the even subfamily has its own
(separate) parity structure.

## Open questions

- **Symbolic junction congruence.** Lemmas 1–2 are proved by exhaustive enumeration and the
  mechanism is illustrated by concrete witnesses; a closed‑form congruence for the *required*
  `Wc1 mod 2` in terms of the Liu4/Moore endpoint offset would upgrade the "mechanism" to a
  fully symbolic derivation and predict the demanded even‑side for all odd `n`.
- **Feasible n‑subfamilies.** Which exact set of odd (and even) `n` admits a *fixed* rule (cf.
  curve 1’s Jacobsthal family)? A per‑`n` scan of the necessary `sw(36,e)` would characterize
  it; only `n=5` (right‑even) and `n=7` (left‑even) are established exhaustively here.
- **Structural predictor.** Curve 36’s LR quadrant is Moore (curve 1, itself infeasible) while
  the other three are Liu4 (feasible). Is the top‑node obstruction attributable specifically to
  the Liu4(reversed)→Liu4→Moore junction chain across the width divider, i.e. does replacing LR
  by a right/bottom‑edge‑exiting kernel restore feasibility? This connects to the sought
  classification theorem "curve ν generalizes to squares iff ⟨condition on its quadrant rules⟩".

## Verification

**Verdict: CONFIRMED.** Independent adversarial re‑derivation reproduces the report's central
claim — squares are INFEASIBLE for curve 36 — and the impossibility proof is sound. I re‑ran the
engine from scratch with my own search code (not the report's scripts) and actively tried to
refute the impossibility by searching the full swap‑rule space; no rule survives.

**What I re‑ran (all from `/home/elessar/Projects/HilbertPlots`, `.venv/bin/python`,
`sys.path.insert(0,"research"); import aep`):**

1. *Structure/nodes.* `RULES[36]`, `entry_exit(36)=('edge','interior')`, and
   `orientations_used(36, range(3,42,2))` = **13 nodes** — all match the report exactly
   (`(36,e)`; `(5,e),(5,y),(5,x)`; `(1,f)`; `(0,·)` at all 8 orientations).

2. *Lemma 1 (n=5).* An independent **lazy backtracking** enumerator — assigning each `(index,M)`
   node only when the recursion actually queries it, so no touched node is left at a default —
   found **432** valid `5×5` assignments, and **every one** has `sw(36,e) = "second"` (values
   `("second","first")`, `("second","none")`). Confirms Lemma 1. (Note: a naïve enumeration over
   only the *default‑split* touched nodes returns 0 valid, because a valid solution shifts the
   split and reaches a node the naïve set omits; the report's lazy‑query approach is the correct
   one, and I reproduced its numbers.)

3. *Lemma 2 (n=7).* Same enumerator: **every** valid `7×7` assignment has `sw(36,e) = "first"`
   (values `("first","none")`, `("first","second")`). Confirms Lemma 2. (My full‑node valid count
   is 648 rather than the report's 162; the two differ only by counting convention — the report's
   `scratch_obstruction.py` counts over the 4 *shared* nodes projecting out `(1,f)`, and
   648 = 162 × 4. The load‑bearing fact — `sw(36,e)` forced to `"first"` — is identical.)

4. *Contradiction / global impossibility.* `swap` in `aep.fill` takes only `(index, M)` — no `n`
   dependence (verified in the source), and `(36,e)` is queried at the top of every square `n>2`.
   So its value is fixed across all `n`; Lemma 1 forces `"second"`, Lemma 2 forces `"first"` —
   disjoint. I cross‑checked directly: **0** assignments valid on `{5,7}` jointly, and an
   independent global backtracking search over all 13 nodes found **0** rules valid on `n=1..40`
   (my DFS explored 4411 partial assignments vs the report's 9027 — different pruning order, same
   empty result). The orientation‑independent const‑9 search is likewise **empty** on `n=1..40`.

5. *Corroborating claims.* `matches hilbertplot at 2^k` (k=1..4): **True**. Minimal infeasible prefix:
   `n=1..6` **SAT**, `n=1..7` **UNSAT** → smallest infeasible `N = 7` (matches). Quasi‑squares
   (exhaustive per‑size SAT, `h=1..5`): orientation `e` gives wide realizable `{1,2,3}` / blocked
   `{4,5}`, tall realizable `{1,2,4,5}` / blocked `{3}`; transposing orientation `a` gives the
   exact transpose — **both match the report's table**.

**Assessment of the proof.** The impossibility argument is rigorous and does not rely on the
heuristic "mechanism" paragraph (which the report itself honestly flags as not yet symbolic, in
Open Questions). It rests only on two exhaustively‑verified necessary conditions on a single
`n`‑independent quantity `sw(36,e)` that are mutually exclusive. No logical gap found. The
attempt to refute — a from‑scratch full‑space search for any working rule — returned empty,
consistent with the theorem.

*Minor, non‑blocking:* the report's illustrative junction‑witness coordinates require a full
valid kernel assignment (fixing `(36,e)` alone yields a disconnected path, as expected); they are
illustrative and not part of the proof's logical chain.
