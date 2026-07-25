# Curve 39 — Moore+Liu2+Liu4 #2

- **kernels / quadrant rules** (order LL, UL, UR, LR; each `(base, morphism, reverse)`):
  - LL: `(3, g, False)`  — **Liu2**, morphism `g = ((0,-1),(1,0))` (rot +90°)
  - UL: `(5, g, False)`  — **Liu4**, morphism `g = ((0,-1),(1,0))` (rot +90°)
  - UR: `(5, x, True )`  — **Liu4**, morphism `x = ((0,1),(1,0))`, traversal **reversed**
  - LR: `(1, m, False)`  — **Moore**, morphism `m = ((1,0),(0,-1))` (reflect vertical)

  So curve 39 is a heterogeneous composite: its four quadrants are three *different*
  kernels — Liu2 (LL), Liu4 (UL and UR), and **Moore (LR)** — not a self-similar curve.
  Each kernel bottoms out (directly or through one level) in the Hilbert curve (curve 0).

- **partition nodes** (`aep.orientations_used(39)`, the `(curve, orientation)` pairs that
  need a swap rule): **12 nodes** —
  `(39, e)`; `(1, m)`; `(3, g)`; `(5, g)`, `(5, o=((0,1),(1,0)))`; and **seven** Hilbert
  nodes `(0, ·)` at the orientations reached through the kernels. The kernel tree is
  `39 → {3, 5, 1} → 0`. A valid fill needs a correct swap at **every** node simultaneously.

- **entry/exit type** (`aep.entry_exit(39)`): `('edge', 'interior')`.
  Like curve 4 (corner→interior) the endpoint types do not by themselves predict
  feasibility; the obstruction lives in an internal kernel.

## Result

- **squares: INFEASIBLE.** No swap rule — orientation-independent **or** per-orientation
  over the full 12-node space — makes `fill(39, ·)` a valid Hamiltonian path on every
  `n×n` square. The construction fails on infinitely many sizes, the first at **n = 14**.
- **swap rule: none exists** (for arbitrary squares). The obstruction is inherited
  wholesale from the **Moore (curve 1) LR quadrant**, which cannot Hamiltonian-path an odd
  square unless the side is a Jacobsthal number.
- **verified:**
  - orientation-independent search, all five curves `{0,1,3,5,39}` free, `9^5 = 59049`
    combos: **0** valid on `n=1..15` (hence **0** on `1..40`).
  - orientation-independent search, kernels pinned to known-good `{0,3,5}` and `{1,39}`
    free, `9^2 = 81` combos: **0** valid on `n=1..40`.
  - relaxed model (per-invocation swaps free — a *superset* of any consistent rule), via
    endpoint-set DP: curve 39 is **infeasible at n = 14, 18, 26, 30, 34, 38** in `1..40`.
    Because the relaxed model dominates every consistent rule, these are unconditional.
  - the Moore LR sub-problem alone, `9^5 = 59049` rules ×2 reversals at the embedded
    orientation `m`: **0** valid fills on `7×7`.
  - matches hilbertplot at `2^k` (k=1,2,3): **yes** (with the trivial power-of-two rule); the
    construction is correct at powers of two — the failure is purely an odd-parity effect.
- **infeasible sizes (exact characterization):** `n` fails ⟺ `n = 2s` with `s` odd and `s`
  **not** a Jacobsthal number. In `1..40`: `n ∈ {14,18,26,30,34,38} = 2·{7,9,13,15,17,19}`.
  Note `n = 22 = 2·11` is feasible because `11` is Jacobsthal.
- **quasi-squares** (`|w−h|=1`): connectivity splits the 8 orientations into the
  non-transposing class `{e,f,y,m}` and the transposing class `{o,g,a,x}`, and **wide and
  tall exchange the two classes** (transpose duality, verified below). No orientation yields
  a connected path for *all* quasi-square sizes — the same Moore odd-square obstruction
  resurfaces in the sub-regions, so feasibility is sporadic in the side length.

## Derivation / proof

### Lemma 1 (bipartite parity on an odd square).
Two-colour the grid `colour(x,y) = (x+y) mod 2` (`0` black, `1` white). On an `s×s` grid
with `s` odd there are `(s²+1)/2` black and `(s²−1)/2` white cells; black leads by one and
all four corners are black. A Hamiltonian path alternates colours, so with one surplus
black cell **both of its endpoints must be black.** (Proved in `curve_1.md`, Lemma 1.)

### Lemma 2 (Moore inherits an odd-square obstruction; Jacobsthal feasibility).
Moore (curve 1) is Hilbert's four quadrants each quarter-turned so the traversal closes
into a near-cycle; its global entry and exit are **4-adjacent** (opposite colours). On an
odd square that violates Lemma 1 outright unless the swaps can pull the two ends onto a
same-colour (both-black) pair *and* keep all three internal junctions connected. An
exhaustive sweep of Moore's full `9^5` rule space shows:

> **Moore has a valid Hamiltonian path on an odd `s×s` square ⟺ `s` is a Jacobsthal
> number** `s ∈ {1,3,5,11,21,43,85,…}` (`J(k)=(2^k−(−1)^k)/3`).

Verified over odd `s ≤ 39` (feasible only at `1,3,5,11,21`; infeasible at every other odd
`s`, the first being `s=7,9`). The base cases `s=7,9` fail by Lemma 1: over all `9^5` rules
the reachable endpoint-colour pair never equals `(black,black)`. (Full argument in
`curve_1.md`; reproduced here as the imported obstruction.)

### Lemma 3 (curve 39 forces Moore onto an odd square of side `n/2`, swap-independently).
At the top node `(39, e)` the canonical box is `n×n`. For **even** `n`, both approximately-
even halves equal `n/2`: `_split(n, ·)` returns `(n/2, n/2)` for every swap mode
(`first/second/none`), because when `n/2` is odd the "make-this-half-even" swap merely
exchanges two equal odd values. The LR quadrant box is `(Wc2, Hc1) = (n/2, n/2)` — **a
square of side `n/2`, independent of the chosen swap** (verified: all 9 modes give `7×7` at
`n=14`). The LR quadrant is Moore at orientation `m`, and Moore's feasibility is
`D4`-invariant. Hence:

> On an even `n×n` square, curve 39 restricts to a **Moore fill of the `(n/2)×(n/2)`
> square**, forced regardless of any swap rule.

### Proposition (impossibility on squares).
Let `n = 2s` with `s` odd. By Lemma 3 the LR quadrant is a Moore fill of the `s×s` odd
square; by Lemma 2 that fill exists **only if `s` is Jacobsthal**. For `s` odd and
non-Jacobsthal — an infinite set beginning `7,9,13,15,17,19,23,25,…` — **no** swap rule
produces a valid curve-39 path on `n×n`. Since a single failing size already precludes a
uniform rule, and infinitely many even sizes fail:

> **Curve 39 does not admit a connected arbitrary-square generalization.** ∎

The first obstruction is `n = 14` (`s = 7`). The relaxed-model DP independently certifies
infeasibility at `n = 14,18,26,30,34,38` in `1..40` — exactly `2·{7,9,13,15,17,19}` — and
confirms feasibility at `n = 22 = 2·11` (`11` Jacobsthal), matching the Proposition to the
size.

### Why the failure is intrinsic (structural characterization).
The three internal junctions and the other two kernels (Liu2 in LL, Liu4 in UL/UR) are
*not* the problem: Liu2 and Liu4 each generalize to squares in isolation (`curve_3.md`,
`curve_5.md`), and on **odd** `n` curve 39 can even route Moore onto the *even* half and
survive (the relaxed DP is feasible on all odd `n ≤ 39`). The killer is the arithmetic
coincidence at **`n ≡ 2 (mod 4)`**: there the split is perfectly balanced into two *equal
odd* halves, no swap can rescue Moore's parity, and Moore's own odd-square feasibility is
confined to the sparse Jacobsthal set. This is a concrete instance of the program's
emerging criterion — *a curve containing a near-cycle (4-adjacent-endpoint) kernel such as
Moore inherits that kernel's odd-square infeasibility whenever the recursion forces the
kernel onto an odd square*, which for a Moore quadrant happens on every `n ≡ 2 (mod 4)`
with non-Jacobsthal `n/2`.

## Evidence

Engine: `research/aep.py`. All runs `cd /home/elessar/Projects/HilbertPlots`
(scratch scripts do `import sys; sys.path.insert(0,"research"); import aep`).

**Structure**
```
aep.NAME[39] = 'Moore+Liu2+Liu4 #2'
RULES[39]: LL (3, g, False)  UL (5, g, False)  UR (5, x, True)  LR (1, m, False)
aep.entry_exit(39) = ('edge','interior')
aep.orientations_used(39): 12 nodes = (39,e),(1,m),(3,g),(5,g),(5,o), and 7× (0,·)
kernel tree: 39 -> {Liu2(3), Liu4(5), Moore(1)} -> Hilbert(0)
```

**Exhaustive swap searches (all empty)**
```
(A) orientation-independent, {0,1,3,5,39} each one (sw,sh): 9^5 = 59049 combos
    -> 0 valid on n=1..15  (=> 0 on 1..40)
(B) orientation-independent, kernels pinned {0,3,5}, free {1,39}: 9^2 = 81 combos
    -> 0 valid on n=1..40
(C) per-orientation full node space: 12 nodes x {first,second,none}^2 = 9^12 ~ 2.82e11
    -> not brute-forced; superseded by the relaxed-DP certificate below, which is a
       SUPERSET of (C) and already returns INFEASIBLE.
```

**Relaxed-model DP certificate** (swaps free per invocation ⊇ any consistent rule; a
region is feasible iff some choice yields an internally valid path with connected junctions)
```
DP validation:  curve 0 (Hilbert) feasible all n=1..19    (matches: Hilbert generalizes)
                curve 1 (Moore) infeasible at n=7,9,13,15,17,19,23,25,27,29,31,33,35,37,39
                                = odd non-Jacobsthal        (matches curve_1.md)
Curve 39 relaxed-INFEASIBLE on 1..40:  n = 14, 18, 26, 30, 34, 38   (all = 2s, s odd)
   n=14 -> s=7    n=18 -> s=9    n=26 -> s=13
   n=30 -> s=15   n=34 -> s=17   n=38 -> s=19       (each s odd & non-Jacobsthal)
   n=22 = 2*11  FEASIBLE  (11 is Jacobsthal)
```

**Lemma 3 check — LR (Moore) box is (n/2)² for every swap at n=14**
```
(sw,sh) in {first,second,none}^2  ->  LR box = (7,7)   for all 9 modes
```

**Moore sub-problem is unconditionally dead at 7×7 (the embedded orientation `m`)**
```
fill(1, ., 7,7, M=((1,0),(0,-1)), rev in {False,True}) over all 9^5 = 59049 node rules:
    valid Hamiltonian fills found = 0        (118098 fills tested)
```

**Powers of two are fine**
```
const rule reproduces hilbertplot curve(39) at 2^k, k=1,2,3 : True   (failure is odd-parity only)
```

**Quasi-squares** (relaxed feasibility; `Y` = some orientation-`M` fill connects, sides 3..12)
```
                            h/w = 3 4 5 6 7 8 9 10 11 12
WIDE w=h+1, M non-transpose {e,f,y,m}:  . Y Y . Y . Y . . Y
WIDE w=h+1, M transpose     {o,g,a,x}:  Y . . Y . Y . Y Y .
TALL h=w+1, M non-transpose {e,f,y,m}:  Y . . Y . Y . Y Y .
TALL h=w+1, M transpose     {o,g,a,x}:  . Y Y . Y . Y . . Y
   => wide<->tall exchanges the transposing and non-transposing classes (transpose duality);
      within a class feasibility is sporadic in the side length (the Moore odd-square
      obstruction reappears in sub-regions), so NO orientation connects all quasi-squares.
```

## Open questions

- A closed-form proof (beyond computational verification to `s ≤ 39`) that Moore's exact
  odd-square feasible set is the Jacobsthal numbers — this is the sole remaining gap in the
  curve-39 impossibility, which otherwise reduces cleanly to it via Lemma 3.
- Full `w×h` rectangle map: on odd `n`, and on even `n` with `n/2` Jacobsthal, curve 39 *is*
  relaxed-feasible; is there a consistent rule valid on that (non-square) sub-family, and
  what is it? The relaxed DP proves necessity but not sufficiency for a *uniform* rule there.
- Classification hook: curve 39 is the canonical "composite carrying a Moore quadrant" case.
  The theorem should read *a curve is square-infeasible if any kernel forced onto an odd
  square is a near-cycle (4-adjacent-endpoint) curve outside its Jacobsthal set* — curve 39
  is the exemplar where the forcing happens at `n ≡ 2 (mod 4)`.

## Verification

**Verdict: CONFIRMED.** Independent adversarial re-check of the INFEASIBLE claim. The
impossibility is reproduced rigorously and does **not** depend on the (still-open)
Jacobsthal conjecture — a single unconditional obstruction at `n = 14` settles it.

**What was re-run (all with `research/aep.py`):**

1. *Structure* — `RULES[39]`, `entry_exit(39)=('edge','interior')`, and
   `orientations_used(39)` (12 nodes, LR = Moore `(1,m)`, `m=((1,0),(0,-1))`) all match
   the report exactly.

2. *Lemma 3 (swap-independent forcing)* — at `n=14`, over all `9` swap modes the top split
   `_split(14,·)=(7,7)` and the LR box `(Wc2,Hc1)=(7,7)`; the LR quadrant is therefore
   `fill(1,·,7,7,m,False,swap)` for **every** swap function. Confirmed. Same holds at
   `n=18` → LR box `(9,9)`.

3. *Moore odd-square is unconditionally dead* — I computed the **complete** partition-node
   closure reachable when filling Moore `7×7` at orientation `m` under *any* swap choice
   (BFS over all `first/second/none` at every node): exactly **3 nodes**
   `{(1,m),(0,((0,-1),(-1,0))),(0,((0,1),(1,0)))}`, so the true rule space is `9^3=729`,
   not the `9^5` the report cites (the report tests a harmless superset). Exhaustive sweep
   of all `729` rules × `2` reversals = **1458 fills → 0 valid**. Repeated for Moore `9×9`
   (genuine `9^5` closure, `118098` fills) → **0 valid**.

4. *Reduction* — because each quadrant sub-list must bijectively cover its box for the whole
   path to be distinct/bbox-correct, and the LR box is forced to an odd Moore square with no
   valid fill under any rule, `fill(39,·,14,14)` and `fill(39,·,18,18)` are invalid for
   **every** swap function. Verified: no orientation-independent rule (exhaustive `9^5=59049`
   const combos over `{0,1,3,5,39}`) validates `n=14` — indeed the best const rule is valid
   only through `n=6`.

5. *Powers of two* — with a known-good kernel rule, `fill(39,·,2^k)` for `k=1,2,3` is `OK`
   and matches `hilbertplot.curve(39).points(k)` up to `canonical_form`. The construction is
   correct at `2^k`; the failure is purely an odd-parity effect, as claimed.

**Scrutiny of the argument (gaps found, none fatal):**
- The impossibility (INFEASIBLE for squares) is airtight and *independent* of the Jacobsthal
  characterization: it needs only that **one** even size (`n=14`) forces an infeasible odd
  Moore square, which is exhaustively certified above.
- The **exact** infeasible set `n=2s`, `s` odd non-Jacobsthal (first `14`, and the specific
  list `{14,18,26,30,34,38}` in `1..40`) inherits Moore's odd-square feasible-set claim,
  which is verified computationally to `s≤39` but **not proved for all `n`** — correctly
  logged in Open Questions. This is a "verified over range", not "proved for all `n`",
  distinction; it does not affect the verdict.
- Minor imprecision (not an error): the report's `9^5` Moore-`7×7` rule space overcounts the
  reachable nodes (true closure `9^3`); testing the superset only strengthens the `0-valid`
  result.

Verified computationally over the ranges stated; impossibility proved unconditionally at
`n=14` (and `n=18`). — adversarial verifier
