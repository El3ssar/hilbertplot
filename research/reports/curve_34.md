# Curve 34 — Moore+Liu4 #3

- **kernels / quadrant rules** (visit order LL, UL, UR, LR):
  | quadrant | base curve | morphism `M` | reverse | transpose? |
  |----------|-----------|--------------|---------|-----------|
  | LL | 5 (Liu4) | `((-1,0),(0,-1))` (180°) | False | no |
  | UL | 5 (Liu4) | `((-1,0),(0,1))` (x-flip) | True  | no |
  | UR | 5 (Liu4) | `((1,0),(0,1))` (identity) | False | no |
  | LR | 1 (Moore)| `((-1,0),(0,-1))` (180°) | False | no |

  The four sub-quadrant morphisms are **all non-transpose** (`M[0][0] ≠ 0`, i.e. axis-preserving; none swaps the x/y axes). Curve 34 therefore has no way to hand a sub-region to a kernel in a transposed frame.

- **partition nodes** — `aep.orientations_used(34)` returns **11** `(curve, orientation)` nodes, spanning curves **{0 (Hilbert), 1 (Moore), 5 (Liu4), 34}**: curve 0 at 6 orientations, curve 5 at 3, curve 1 at 1, curve 34 at identity. Curves 0, 5 are feasible on squares (see below); curve 1 (Moore) is *itself* infeasible (fails at n=7); curve 34 inherits and compounds this.

- **entry/exit type:** `aep.entry_exit(34) = ('interior', 'interior')`.

## Result

- **squares: INFEASIBLE.** No swap rule — orientation-independent **or** per-orientation — makes `fill(34, ·)` a Hamiltonian path on every n×n square.
- **swap rule:** none exists. (Even the weakest requirement fails: the single square **n = 5** admits no valid rule at all.)
- **verified:** exhaustive ground truth n = 1..8 → feasible only for n ∈ {1,2,3,4,6,8}; **n = 5 and n = 7 are infeasible**. A sound relaxation (interface DP, see Evidence) proves rigorous infeasibility for a much larger set including n ∈ {7,11,13,14,15,17,18,19,23,25,26,27,29,30,31,33,34,35,37,38,39}. Match to hilbertplot at 2^k is moot — the arbitrary-square generalization does not exist.
- **quasi-squares:** curve 34 tiles a wide (w=h+1) or tall (h=w+1) quasi-square only at **half** the top orientations, with a size-parity (mod 4) dependent transpose/non-transpose requirement — see §Quasi-squares. This *same* restriction, inherited from the kernels, is exactly what breaks the squares.

## Derivation / proof

### The obstruction is geometric (junction placement), not a global 2-coloring

On the odd square n = 5 (25 cells: 13 black + 12 white under the checkerboard `(x+y) mod 2`), a Hamiltonian path must start and end on the majority (black) color. Tracking colors through the visit order LL→UL→UR→LR with the junction rule "adjacent cells have opposite color", the top-level split with swap `(first,first)` forces `entry = exit = black` — **consistent**. So the classical parity/counting invariant does **not** forbid curve 34; the obstruction lies one level deeper, in the *positions* of the sub-region entry/exit cells.

### Lemma 1 (rigidity of odd kernel boxes)

For a 3×3 box at identity, both curve 5 and curve 1 have a **unique, swap-independent** entry/exit: `entry = (0,0)`, `exit = (2,0)` (both on the bottom edge). The swap rule provides **no freedom** on odd boxes. *(Verified: all 9 swap rules give the identical (entry,exit).)*

### Lemma 2 (quasi-square orientation-parity constraint of the kernels)

Let a *wide* quasi-square be `(2k+1)×(2k)` and a *tall* one `(2k)×(2k+1)`. For the kernels 5 (Liu4) and 1 (Moore), tiling capability depends on the orientation `M` through its transpose parity `t(M) := [M[0][0]=0]`:

| box | size | orientations that admit a tiling |
|-----|------|----------------------------------|
| wide 3×2 | k=1 | only **transpose** M (8/16 (M,rev)); non-transpose: **0** |
| wide 5×4 | k=2 | only **non-transpose** M; transpose: 0 |
| wide 7×6 | k=3 | only **transpose** M |
| tall 2×3 | k=1 | only **non-transpose** M |
| tall 4×5 | k=2 | only **transpose** M |

I.e. a wide quasi-square with `w ≡ 3 (mod 4)` needs a transpose orientation, `w ≡ 1 (mod 4)` a non-transpose one (and dually for tall). By contrast **curve 0 (Hilbert) tiles every quasi-square at all 16 (M,rev)** — it is orientation-free, because two of its four morphisms (`LL, LR`) are transposes, giving it the axis-swap flexibility the odd side needs. This is the structural reason Hilbert-family curves generalize and Moore/Liu4-family ones need transpose access.

This is precisely the **1×2 (orientations A,C) / 2×1 (orientations B,D) primitive constraint**: at the bottom of the recursion a kernel lays a fixed-axis domino, so the odd dimension of a quasi-square can only be absorbed when the current frame aligns that domino with the odd side; the required frame flips with each halving, giving the mod-4 alternation.

### Lemma 3 (the split always produces a wide quasi-square, handed to a non-transpose kernel)

For odd n, the approximately-even partition gives `n = Wc1+Wc2` and `n = Hc1+Hc2` with **exactly one** of `{Wc1,Wc2}` odd and one of `{Hc1,Hc2}` odd (their sums are odd). The four quadrant boxes `(Wc1,Hc1),(Wc1,Hc2),(Wc2,Hc2),(Wc2,Hc1)` therefore comprise exactly one even×even, one **odd×even (wide)**, one **even×odd (tall)**, and one odd×odd box — *for every choice of swap rule*. The swap only permutes **which quadrant** is wide; it can never eliminate the wide box nor change any quadrant's morphism. Since all four morphisms of curve 34 are **non-transpose**, the wide box is always delivered to curve 5 or curve 1 in a **non-transpose** frame.

### Theorem (infeasibility)

At **n = 5** the wide box is `3×2`. By Lemma 3 it is handed to a non-transpose kernel; by Lemma 2 a `3×2` wide box has **no** tiling under any non-transpose orientation. Hence that quadrant is untileable and the path cannot close, for **all 9 top swaps** and **all** child-rule assignments. Therefore curve 34 is infeasible at n = 5, so no swap rule can make it valid on every square. ∎

*(For larger odd n the wide box grows and its required parity oscillates (Lemma 2), so the top-level obstruction can move to a deeper level rather than vanish; e.g. n = 7,11,13,… remain infeasible while some individual larger n survive the relaxation. The minimal, cleanest witness is n = 5.)*

### Structural characterization

Curve 34 fails because **its quadrant morphisms give it no transpose access, while its kernels (Liu4, Moore) require a transpose frame to absorb a wide odd side.** A curve generalizes to arbitrary squares only if, at every odd size, each quasi-square quadrant can be routed to a kernel in an orientation compatible with that kernel's quasi-square parity — automatic when the kernel is Hilbert (orientation-free) or when the morphisms supply the needed transpose. Curve 34 satisfies neither.

## Evidence

Run from `/home/elessar/Projects/HilbertPlots` (`.venv/bin/python`, `sys.path` includes `research`).

**Nodes / kernels.** `aep.orientations_used(34)` → 11 nodes over curves {0,1,5,34}; all four `RULES[34]` morphisms have `M[0][0] ≠ 0` (non-transpose).

**No orientation-independent rule.** Exhaustive over one `(sw,sh) ∈ {first,second,none}²` per curve for curves {0,1,5,34}: search space **9⁴ = 6561**, tested on n = 1..40 → **0 solutions**.

**No per-orientation rule.** Lazy backtracking assigns a rule to each of the 11 partition nodes on demand (full per-node space **9¹¹ ≈ 3.14×10¹⁰**), pruning on the smallest failing n, exhaustive over consistent assignments → **0 solutions** valid on n = 1..40; max n reachable = 4. The same solver confirms curves 0, 5, 3 feasible (max n = 40) and curve 1 (Moore) infeasible (max n = 6), validating the method.

**n = 5 is the witness (two independent methods).**
- Per-node exhaustive backtracking on the single square: `feasible_single(34,5) = False`, `feasible_single(34,7) = False`, while `feasible_single(34,4)=True`, `feasible_single(34,6)=True`.
- Direct enumeration: for every one of the 9 top swaps, no child-rule assignment even makes all four child boxes individually tileable — the wide `3×2` quadrant (curve 1 @180, or curve 5 @x-flip for other swaps) has **0** valid rules.

**Lemma 1 (rigidity).** curve 5 and curve 1 on 3×3 @identity: all 9 swaps give `entry=(0,0)`, `exit=(2,0)`.

**Lemma 2 (kernel quasi-squares).** For curves 5 and 1: wide 3×2 → 8/16 (M,rev), all with `M[0][0]=0` (transpose), non-transpose = 0; wide 5×4 → all non-transpose; tall 2×3 → all non-transpose; tall 4×5 → all transpose. Curve 0: **16/16** for both wide and tall.

**Interface DP (sound infeasibility relaxation).** A memoised DP computes, for each `(curve,M,w,h)`, the set of achievable `(entry,exit)` pairs, allowing free reversal of every subcurve — a *superset* of the real construction (which fixes `rev`). Hence **DP-infeasible ⟹ truly infeasible**. Result over n = 1..40:
```
INFEASIBLE (rigorous): 7,11,13,14,15,17,18,19,23,25,26,27,29,30,31,33,34,35,37,38,39
```
(The DP marks n = 5 "feasible" only because its reversal-relaxation is looser there; the exhaustive method above proves n = 5 truly infeasible. Note several **even** squares — 14, 18, … — are rigorously infeasible too, so the obstruction is not confined to odd sizes.)

## Quasi-squares

Curve 34 on a single quasi-square, per top orientation (any per-node rule allowed):

| shape | which top (M,rev) connect |
|-------|---------------------------|
| wide 3×2 | only **non-transpose** M (8/16) |
| wide 5×4 | only **transpose** M |
| tall 2×3 | only **transpose** M |
| tall 4×5 | only **non-transpose** M |

So curve 34 **can** tile quasi-squares, but only at half the orientations, with the transpose/non-transpose requirement alternating with size mod 4 (opposite parity to its kernels, reflecting the extra recursion level). This is the same fixed-axis domino primitive as Lemma 2, propagated to the top level: a quasi-square is connectable exactly when the top frame aligns curve 34's internal primitive axis with the odd side. It is this constraint, forced onto the wide quadrant of every odd square by curve 34's all-non-transpose morphisms, that makes the square problem infeasible.

## Open questions

- Exact per-n feasibility for the finitely many DP-"feasible" odd n (e.g. 9, 21) under the true (rev-fixed) construction — the exhaustive solver is slow past n ≈ 8; a tightened DP that tracks `rev` would settle these.
- A closed-form description of the DP-infeasible set (it includes all n ≡ 3 mod 4 in the tested range and select others) and whether any n > 8 is truly feasible.
- Whether an *extended* construction that permits transpose morphisms in curve 34's quadrant rules (i.e. a different but equivalent kernel embedding) could restore square-feasibility — this would test the structural characterization directly.

## Verification

**Verdict: CONFIRMED.** Curve 34 is INFEASIBLE on squares. Reproduced independently and skeptically; the impossibility argument is sound and I found no swap rule that works.

Commands run (from repo root, `.venv/bin/python`, `sys.path` includes `research`):

1. **Structure.** `orientations_used(34)` → 11 nodes over curves {0,1,5,34}; all four `RULES[34]` morphisms have `M[0][0]≠0` (non-transpose); `entry_exit(34)=('interior','interior')`. Matches report.

2. **Orientation-independent search (attempt to refute).** Exhaustively tried all `9⁴ = 6561` const-swap assignments over curves {0,1,5,34}, testing n=1..40 → **0 solutions**. Confirms no orientation-independent rule.

3. **n=5 exhaustive per-node search (the decisive refutation attempt).** Instrumented `fill(34,·,5,5,·)` to record every `(index,M)` it queries: exactly **4 nodes**, and this set is **identical** to `orientations_used(34,sizes=[5])` — so an exhaustive search over the reached nodes is provably complete. Brute-forced all `9⁴ = 6561` independent per-node rule assignments → **0 valid**. Therefore *no* swap rule (orientation-independent or fully per-orientation) makes the n=5 square a Hamiltonian path. Since every all-squares rule must work at n=5, curve 34 is infeasible. This is a full exhaustive proof, stronger than the report's DP relaxation — and it resolves the report's own noted DP/exhaustive discrepancy (the DP wrongly marks n=5 "feasible"; the exhaustive result is authoritative and says infeasible). n=7 likewise: 0 of `9⁵=59049` assignments valid.

4. **Geometric mechanism (Lemma 2/3) checked.** A 3×2 box is tileable by curve 5 under **8/16** (M,rev), all transpose, and **0** non-transpose; identically for curve 1; curve 0 tiles **16/16**. Combined with all-non-transpose `RULES[34]`, the wide 3×2 quadrant forced by the n=5 split is unavoidably delivered to a non-transpose kernel that cannot fill it — matching the report's Theorem. The argument is rigorous.

5. **Not globally broken.** Even squares n=4,6,8 ARE feasible under some per-node rule (verified by exhaustive per-node search) — the obstruction is genuinely the odd-square wide-box parity conflict, not a construction bug.

No swap rule was found despite an exhaustive attempt to refute; the impossibility proof has no gap I could identify. Verified computationally over n=1..40 (searches) with the n=5 exhaustive result constituting a rigorous per-square proof of infeasibility.
