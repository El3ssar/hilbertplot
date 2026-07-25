# Curve 1 — Moore

- **kernels / quadrant rules** (order LL, UL, UR, LR; each `(base, morphism, reverse)`):
  - LL: `(0, g, False)`   morphism `g = ((0,-1),(1,0))`  (rotation +90°)
  - UL: `(0, g, False)`   morphism `g = ((0,-1),(1,0))`  (rotation +90°)
  - UR: `(0, x, False)`   morphism `x = ((0,1),(-1,0))`  (rotation −90°)
  - LR: `(0, x, False)`   morphism `x = ((0,1),(-1,0))`  (rotation −90°)

  Every quadrant is the **Hilbert curve (curve 0)**; Moore is Hilbert's four quadrants
  each rotated a quarter-turn so the whole traversal closes into a near-cycle. Curve 1
  itself never appears as a kernel of any other curve, so its only responsibility is the
  top level, but it depends on curve 0's swap behaviour at the rotated orientations.

- **partition nodes** (`aep.orientations_used(1)`, the `(curve, orientation)` pairs that
  need a swap rule): **5 nodes** —
  `(1, e)`  and  `(0, y)`, `(0, g)`, `(0, x)`, `(0, m)`
  where `e=id, g=rot+90, x=rot−90, y=reflect-x-axis-vertical ((-1,0),(0,1)), m=reflect-horizontal ((1,0),(0,-1))`.
  The kernel curve 0 is required at the **four rotation/reflection orientations that are
  outside Wu & Chang's A,B,C,D set** `{e,o,f,a}` — this is the crux (see Derivation).

- **entry/exit type** (`aep.entry_exit(1)`): `('edge', 'edge')`.
  On every `2^k` grid the global entry `(2^{k-1}−1, 0)` and exit `(2^{k-1}, 0)` are the two
  **central cells of the bottom edge and are 4-adjacent** (Manhattan distance 1). Moore is a
  Hamiltonian *cycle* opened at one bottom-edge bond: its two endpoints are neighbours.

## Result

- **squares: INFEASIBLE.** No swap rule — orientation-independent **or** per-orientation
  over the full node space — makes `fill(1, ·)` a valid Hamiltonian path on every `n×n`
  square. The construction already fails at **n = 7** (and n = 9) for **every** rule.
- **swap rule: none exists.** (For the *even* subfamily a rule does exist: the trivial
  `(first,first)` at every node is valid on all even `n ∈ 2..40`.)
- **verified:**
  - orientation-independent search (81 combos): **0** valid on `n=1..40`.
  - per-orientation full search (**9^5 = 59049** combos): **0** valid on `n=1..14`
    (hence none on `1..40`; `square_valid` additionally demands the `2^k` hilbertplot match).
  - even `n=2..40`: **valid** (e.g. all-`(first,first)`); matches hilbertplot at `2^k`: **yes**.
  - odd `n`: valid **iff** `n` is a **Jacobsthal number** `J = {1,3,5,11,21,43,85,…}`
    (`J(k)=(2^k−(−1)^k)/3`). Verified: works at `n∈{1,3,5,11,21,43,85}`, fails at every
    other tested odd `n∈{7,9,13,15,17,19,23,25,27,31}`.
- **quasi-squares** (`|w−h|=1`): connectivity is orientation-dependent and splits the 8
  orientations into two classes by whether they transpose the axes
  (`{e,f,y,m}` non-transposing vs `{o,g,a,x}` transposing). Over the tested range
  `side = 2..8`:
  - **wide** (`w=h+1`): `{e,f,y,m}` connect ⟺ `h ≡ 0,1 (mod 4)`; `{o,g,a,x}` connect ⟺ `h ≡ 2,3 (mod 4)`.
  - **tall** (`h=w+1`): the transpose — `{e,f,y,m}` connect ⟺ `w ≡ 2,3 (mod 4)`; `{o,g,a,x}` connect ⟺ `w ≡ 0,1 (mod 4)`.

## Derivation / proof

### Lemma 1 (bipartite parity of a Hamiltonian path on an odd square).
Two-colour the grid by `colour(x,y) = (x+y) mod 2` (call `0` *black*, `1` *white*). On an
`n×n` grid with `n` odd there are `(n²+1)/2` black and `(n²−1)/2` white cells, so black
outnumbers white by exactly one, and the four corners are black. A Hamiltonian path
strictly alternates colours; with one extra black cell it **must begin and end on a black
(majority) cell.** Hence:

> **(P)** On an odd `n×n` square, *both* endpoints of any valid path are black.

### Lemma 2 (Moore forces near-adjacent central-bottom endpoints).
By the quadrant rules, the global entry is the entry of the LL Hilbert block and the global
exit is the exit of the LR Hilbert block; the LL/LR rotations (`g` then `x`) are chosen
precisely so these two ends surface on the **bottom row astride the vertical mid-split**
`x = Wc1`. Concretely the endpoints are `(Wc1−1, 0)` and `(Wc1, 0)` for the `(first,·)`
family, and the swap can shift them by at most one cell each. Consequently the two
endpoints always lie on `y = 0` (occasionally `y = 1` for the exit) with horizontal
separation `Δx ∈ {1, 2}`. This is the open-cycle signature of the Moore curve inherited by
the AEP recursion, and is verified below.

### Proposition (impossibility on odd squares; hard cases n = 7, 9).
Combine (P) with Lemma 2. Both endpoints on the bottom row are black **iff both have even
`x`**, i.e. iff `Δx` is even and both land on even columns. When Moore forces the endpoints
**4-adjacent** (`Δx = 1`) they have *opposite* colours and (P) is violated outright — this
is the generic behaviour and matches the `2^k` structure (adjacent endpoints, legal only
because even grids have balanced colours). Making `Δx = 2` with both columns even requires
the swaps to split the bottom row symmetrically about an even mid-column *and* keep all
three internal junctions connected; whether both can hold simultaneously is an arithmetic
condition on `n`.

For **n = 7 and n = 9** it provably **cannot** hold: an exhaustive sweep of all `9^5`
rules shows the achievable endpoint-colour pair `(colour(entry), colour(exit))` is
`{(0,1),(1,0),(1,1)}` — the black–black pair `(0,0)` **never occurs**. Every reachable
colouring violates (P). Therefore no rule yields a valid path at `n=7` or `n=9`. ∎

Because a single failing size suffices, this proves **curve 1 is infeasible on arbitrary
squares**: no fixed rule can be valid on all `n`, the first obstruction appearing at `n=7`.

### Why Moore fails where Hilbert (curve 0) succeeds — the structural characterization.
Curve 0 is **corner→corner**: on an odd square both its endpoints sit at corners, which are
black, so (P) is satisfied automatically and Hilbert generalizes to all squares. Curve 1 is
**edge→edge with 4-adjacent endpoints** (an opened Hamiltonian cycle): its two ends are
*forced neighbours*, hence opposite colours, which is exactly what (P) forbids on an odd
grid. The obstruction is therefore intrinsic to Moore's cyclic entry/exit geometry, not to
any particular swap choice. This is the mechanism behind the general rule emerging from the
program: **a curve whose global entry and exit are 4-adjacent (a closed/near-cycle curve)
cannot generalize to odd squares**, independent of the kernel swap rules.

### The Jacobsthal refinement (feasible odd sizes).
Even when (P) *can* be met (e.g. `n=11,13`, where `(0,0)` endpoints are reachable),
connectivity of the three internal junctions imposes a further parity demand that
propagates into the unique **odd×odd sub-quadrant** produced by the approximately-even
split. Writing an odd `n = (n−1)/2 + (n+1)/2`, exactly one half is odd; the recursion is
benign **iff** that odd half is itself a feasible odd size. The fixed points of this
descent are the Jacobsthal numbers: for `n ∈ J` the odd half equals the previous Jacobsthal
number (`11→5→…`, `21→11→…`, `43→21→…`, `85→43→…`), so feasibility recurses down to the
`1×1` base; for any other odd `n` the descent reaches a `(P)`-violating size such as `7` or
`9`. This yields the observed characterization

> **odd `n` feasible (some rule connects) ⟺ `n` is a Jacobsthal number**,

proven at the base by (P) for `n=7,9` and **verified computationally** for all tested odd
`n ≤ 31` plus the Jacobsthal values `43, 85`. A fully general proof of the descent is left
open (see Open questions); the headline result — infeasibility on arbitrary squares — is
proven outright.

### Quasi-squares.
For `|w−h| = 1` the bottom/top mid-edge junction of Moore must bridge two sub-regions whose
shared side has odd length, reducing to the `1×2` (orientations A,C) vs `2×1` (orientations
B,D) domino-orientation constraint at the primitive level. The non-transposing orientations
`{e,f,y,m}` present a horizontal entry/exit edge and the transposing orientations
`{o,g,a,x}` a vertical one, so wide and tall exchange their roles — exactly the observed
transpose symmetry — and within each class the reachable sizes are governed by the residue
of the odd side mod 4 (data below).

## Evidence

Engine: `research/aep.py`. All runs `cd /home/elessar/Projects/HilbertPlots`.

**Partition nodes and entry/exit geometry**
```
aep.orientations_used(1)  ->  {(1,e), (0,y), (0,g), (0,x), (0,m)}   # 5 nodes
aep.entry_exit(1) = ('edge','edge')
hilbertplot curve(1) 2^k endpoints: entry (2^{k-1}-1,0), exit (2^{k-1},0), Manhattan = 1  (k=1..4)
```

**Exhaustive swap search (both levels empty)**
```
(A) orientation-independent (curve0 one (sw,sh), curve1 one (sw,sh)): 81 combos
    -> 0 valid on n=1..40
(B) per-orientation over the 5 nodes, each {first,second,none}^2 : 9^5 = 59049 combos
    -> 0 valid on n=1..14  (=> 0 on 1..40; square_valid also enforces the 2^k hilbertplot match)
```

**Per-size feasibility (does ANY of the 59049 rules connect?)**
```
n :  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 27 31 43 85
ok :  T  T  T  T  T  T  F  T  F  T  T  T  F  T  F  T  F  T  F  T  T  T  F  T  F  F  F  T  T
```
All even `n` valid; odd `n` valid exactly at Jacobsthal `{1,3,5,11,21,43,85}`.

**Parity obstruction at n = 7, 9** (endpoint-colour pairs reachable over all 59049 rules)
```
n=7 : reachable (colour_entry, colour_exit) = {(0,1),(1,0),(1,1)}   # (0,0)=black-black ABSENT
n=9 : reachable                             = {(0,1),(1,0),(1,1)}   # (0,0) ABSENT
=> Lemma 1 (both endpoints black) unsatisfiable  =>  no valid path.
n=11,13 : (0,0) reachable  (so n=7,9 fail by parity; n=13 fails by the junction/Jacobsthal
          obstruction despite legal endpoint colours).
```

**Even squares have a rule**
```
rules valid on ALL even n=2..40 : 729 of 59049; e.g. (first,first) at every node.
```

**Quasi-squares** (`anyrule` = some rule connects; sizes 2..8, orientations labelled by D4 code)
```
WIDE  w=h+1 :  {e,f,y,m} valid at h=4,5,8      {o,g,a,x} valid at h=2,3,6,7
TALL  h=w+1 :  {e,f,y,m} valid at w=2,3,6,7    {o,g,a,x} valid at w=4,5,8
   =>  non-transposing {e,f,y,m}: wide ok iff h≡0,1 (mod4); tall ok iff w≡2,3 (mod4)
       transposing     {o,g,a,x}: wide ok iff h≡2,3 (mod4); tall ok iff w≡0,1 (mod4)
```

## Open questions

- A closed-form proof (not just computational verification) that the odd-size descent has
  the Jacobsthal numbers as its exact feasible set, and an explicit per-size rule realizing
  the valid Jacobsthal paths.
- Whether the "4-adjacent global endpoints ⇒ infeasible on odd squares" criterion is
  *sufficient as well as necessary* across the full 40-curve catalog (Moore is the
  canonical near-cycle instance; the classification theorem should quote this).
- Full rectangle (`w×h`) map for Moore; the quasi-square mod-4 law is verified only for
  side ≤ 8 and should be proved from the mid-edge domino constraint.

## Verification

**Verdict: CONFIRMED.** Independent adversarial re-run of the engine (`research/aep.py`,
`.venv/bin/python`) reproduces every load-bearing claim; the INFEASIBLE result is
rigorously established.

**What I ran and found:**

1. *Partition-node completeness.* `orientations_used(1)` returns the 5 nodes
   `{(1,e),(0,g),(0,m),(0,x),(0,y)}`, and this set is **stable** — identical when computed
   over `sizes=range(3,42,2)`. Since `fill` only ever queries `swap(index,M)`, these 5
   nodes fully parameterize the swap-rule space, so `9^5 = 59049` genuinely exhausts it
   (no hidden nodes at larger `n`). This closes the potential gap in the "full search" claim.

2. *Impossibility at n=7 (the headline).* Exhaustive sweep of all **59049** per-orientation
   rules: **0** are valid at `n=7` (`validate != OK` for every rule). A single failing size
   suffices, so curve 1 admits no arbitrary-square generalization. Independently confirmed.

3. *Parity mechanism.* Over all 59049 rules the reachable endpoint-colour pairs at both
   `n=7` and `n=9` are `{(0,1),(1,0),(1,1)}` — the black–black pair `(0,0)` is **never**
   reachable. Lemma 1 (on an odd square, both Hamiltonian-path endpoints must lie on the
   majority/black colour: 25 black vs 24 white at `n=7`, corners black) is standard and
   correct. Together these give a clean, rigorous obstruction that does **not** depend on
   the informal Δx geometry of Lemma 2 — Lemma 2 is intuition, not a load-bearing step.

4. *Orientation-independent search.* **0 of 81** const rules (`curve0×curve1`) valid on
   `n=1..40`. Matches the report.

5. *Even subfamily.* `(first,first)` at every node is valid on **all even** `n=2..40`, and
   matches hilbertplot at `2^1,2^2,2^3`. Matches the report.

6. *Jacobsthal data (spot-check).* "ANY-rule feasible?" reproduced: `n=11` **True** (J),
   `n=13` **False**, `n=15` **False** — consistent with the reported table.

**Scrutiny of the argument for gaps:** The headline infeasibility is proven outright
(Lemma 1 + exhaustive reachability at `n=7`), with no overclaiming. The report correctly
flags as *open / computational-only* (not proved): the Jacobsthal characterization of the
feasible odd set, and the "4-adjacent endpoints ⇒ infeasible" structural criterion across
the catalog. Lemma 2's "endpoints astride the mid-split, Δx∈{1,2}" is prose intuition and
is not required for the proof; this is appropriately hedged. No logical gap undermines the
INFEASIBLE verdict. Attempt to refute (find any rule valid on all `n=1..40`) failed as it
should: none exists, first obstruction at `n=7`.
