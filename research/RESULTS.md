# Arbitrary-square generalization of the 40 two-dimensional Hilbert curves — classification

Engine: `research/aep.py` (Wu–Chang approximately-even partition generalized to all 40 hilbertplot
curves via the catalog quadrant rules and full D4). A **swap rule** assigns each partition
node `(curve, orientation)` a pair `(sw, sh) ∈ {first, second, none}²` (which half of an odd
split is forced even, per axis); it is a function of `(index, M)` only and **cannot depend on
the region size `n`**. A curve is **FEASIBLE** iff some swap rule makes `fill(index,·)` a
single Hamiltonian path on every `n×n` square (verified here over `n = 1..40`, and matching
hilbertplot at `2^k`); otherwise **INFEASIBLE**.

All feasibility claims below were re-verified with `aep.square_valid(idx, rule,
sizes=range(1,41), check_2k=True)`; all impossibility claims rest on an exhaustive swap search
over the *complete* reachable node set at a witness size (a single square with zero valid rules
suffices, since validity on every square is required).

## Counts

- **FEASIBLE: 8** — curves `0, 3, 4, 5, 24, 29, 30, 31`.
- **INFEASIBLE: 32** — all others.
- Feasible curves use only the two **corner-anchored** kernels Hilbert (0) and Liu3 (4).
- Every curve containing a **Moore (1)** kernel is infeasible (`1, 32–39`): 8 curves.
- Every curve using **Liu4 (5)** as a *sub-block* kernel is infeasible (`6–17, 32–39`): note
  Liu4 itself (curve 5) is feasible standalone but never survives being nested.
- No curve — feasible or not — admits an orientation-independent **quasi-square** rule; every
  quasi-square is connectable only by choosing the top orientation from the size-appropriate
  D4 transpose-coset (the `1×2` (A,C-class) / `2×1` (B,D-class) domino primitive).

## Classification table

Verdict column: **CONFIRMED** = the report's result *and* its impossibility/feasibility proof
were independently reproduced; **conf(proof-nw)** = result confirmed computationally but the
report's derivation has a flaw noted (result unaffected); **conf(needs-repair)** = verdict
holds under all tests but the written proof/evidence is unsound and must be redone.

| # | name | kernels | squares | swap rule / obstruction | witness | verdict | quasi-square |
|--:|------|:-------:|:-------:|--------------------------|:-------:|---------|--------------|
| 0 | Hilbert | {0} | **FEASIBLE** | `sh=first` every node, `sw` free (`(first,first)`) | — | CONFIRMED | 4/8 orient. per size; coset by parity |
| 1 | Moore | {0} | INFEASIBLE | near-cycle: 4-adjacent endpoints ⇒ opposite colour, but odd square needs both endpoints majority colour | n=7 (also 9); n=2^k ok; odd-feasible only at Jacobsthal | CONFIRMED | transpose-coset split, mod-4 |
| 2 | Liu1 | {0} | INFEASIBLE | all-N morphisms `(C,A,A,C)`: forced odd×even box lands on non-transpose Hilbert, unfillable | n=7 (9⁵=0) | CONFIRMED | small only; no uniform |
| 3 | Liu2 | {0} | **FEASIBLE** | `3:(·,second)` (`sh=second`, `sw` free), `0:sh=first` | — | CONFIRMED | connect iff canonical width even; coset by parity |
| 4 | Liu3 | {0} | **FEASIBLE** | `4:(second,first)`, `0:sh=first` (`sw` free) | — | conf(proof-nw): Lemma 1 overstated (junction needs Hc1 even), result solid | 4/8 per size, mod-4 |
| 5 | Liu4 | {0} | **FEASIBLE** | `5:(first,second)` both axes pinned, `0:sh=first` | — | CONFIRMED | double-pin; period-4, no uniform |
| 6 | Improper1 | {5} | INFEASIBLE | improper: adjacent opposite-colour endpoints on odd square | n=3 (9 rules all disc.) | conf(proof-nw): n=3 exhaustive is rigorous; "all odd n" Lemma 1 false over per-orient. space | even-area only, transpose split |
| 7 | Improper2 | {5} | INFEASIBLE | edge-drift: UL/LR curve-5 blocks demand opposite split parity at n≡1 vs 3 (mod 8) | n=9 vs 11 | conf(proof-nw): square proof rigorous; quasi-square table has errors | mod-8; some residues connect nowhere |
| 8 | Improper3 | {5} | INFEASIBLE | edge-to-edge curve-5 junction drift: n=3 needs Hc1 even, n=7 needs Hc1 odd | n=3 vs 7 | CONFIRMED (quasi-square aspect claim disputed) | aspect-selected coset |
| 9 | Improper4 | {5} | INFEASIBLE | all-transpose morphisms force a 2×3 curve-5 block; colour-locked, unfillable | n=5 (9⁵=0) | CONFIRMED | incomplete both aspects |
| 10 | Improper5 | {5} | INFEASIBLE | four doubly-pinned curve-5 quadrants force contradictory Hc1 parity | n=5 vs 7 | CONFIRMED | period-8 thinned |
| 11 | Improper6 | {5} | INFEASIBLE | curve-5 edge-drift: S(5) needs sh=second, S(7) needs sh=first | n=5 vs 7 | CONFIRMED | complementary cosets |
| 12 | Liu2+Liu4 #1 | {3,5} | INFEASIBLE | edge kernels straddle horizontal junction: S(3)∩S(7)=∅ | n=3 vs 7 | CONFIRMED | complementary cosets |
| 13 | Liu2+Liu4 #2 | {3,5} | INFEASIBLE | forced 2×3 block on curve 3/5, same-colour endpoints ⇒ no path | n=5 (9⁵=0) | CONFIRMED | transpose duality |
| 14 | Liu2+Liu4 #3 | {3,5} | INFEASIBLE | curve-3 LL exit column drifts: D(3)={first}, D(7)={none,second} | n=3 vs 7 | CONFIRMED | 5×4/4×5 half; no uniform |
| 15 | Liu2+Liu4 #4 | {3,5} | INFEASIBLE | cross-size: 5×5 forces root (second,second), 7×7 forces sh=first | n=5 vs 7 | CONFIRMED | size-dependent duality |
| 16 | Liu2+Liu4 #5 | {3,5} | INFEASIBLE | three co-oriented Liu4 + tall-only kernels; forced wide box unfillable | **n=7** (9⁵=0; n=5 is feasible) | conf(proof-nw): report wrongly anchored n=5; real wall n=7 | best 11/18; aspect asym. |
| 17 | Liu2+Liu4 #6 | {3,5} | INFEASIBLE | endpoint parity: (E,E) pair unreachable on 5×5 | n=5 (9⁵=0) | CONFIRMED | alternating coset |
| 18 | Hilbert+Liu3 #1 | {0,4} | INFEASIBLE | split of 13=6+7 forces a 7×6 block; unfillable by curve 0 and curve 4 | n=13 (exhaustive) | conf(proof-nw): result solid via 7×6 exhaustion; Lemma 1 (parity) false (5×6 counterex.) | odd×even fails both classes |
| 19 | Hilbert+Liu3 #2 | {0,4} | INFEASIBLE | all-N morphisms; 3×4 tall-by-one dead for both kernels | n=7 (9⁴=0) | CONFIRMED | complementary; dead cells 3×4,5×4 |
| 20 | Hilbert+Liu3 #3 | {0,4} | INFEASIBLE | `sh=first` forced by Hilbert, then curve-4 block gets even×odd it can't fill | n=7/9/13 | CONFIRMED | irregular, both classes |
| 21 | Hilbert+Liu3 #4 | {0,4} | INFEASIBLE | kernels disagree on off-square chirality: f4W∧f0W and f4T∧f0T both false | n=13 (also 19) | CONFIRMED | parity-restricted |
| 22 | Hilbert+Liu3 #5 | {0,4} | INFEASIBLE | Hilbert pair needs Hc2 even, Liu3 pair needs Hc1 even; consecutive halves | n=7 (9⁵=0) | CONFIRMED | one class per size |
| 23 | Hilbert+Liu3 #6 | {0,4} | INFEASIBLE | Hilbert forced into foreign D4 orbit; quasi-square parity gate violated | fails n≡±1 (mod 8) | conf(needs-repair): no rule found (11-node search), but Lemma 3 false + node undercount (11≠9) | ~10/20 per orient. |
| 24 | Hilbert+Liu3 #7 | {0,4} | **FEASIBLE** | `24:(first,second), 4:(second,first), 0:sh=first` | — | conf(proof-nw): result solid; Lemma 4 counterfactual false, 5×4 boundary | 4/8 coset (5×4 all-8) |
| 25 | Hilbert+Liu3 #8 | {0,4} | INFEASIBLE | LR Liu3 pinned to reflect-x gets a 6×7 it cannot fill; hard wall | n=13 (9⁶=0) | CONFIRMED | no orient. connects |
| 26 | Hilbert+Liu3 #9 | {0,4} | INFEASIBLE | all-transpose morphisms `(g,g,x,x)`; forced 4×3 (even-w,odd-h) dead at rotation | n=7 (9⁴=0) | CONFIRMED | mod-4 coset |
| 27 | Hilbert+Liu3 #10 | {0,4} | INFEASIBLE | Hilbert blocks force unique split; Liu3@C gets central quasi-square, dead at n≡1,7 (mod 8) | n=7 (9⁶=0) | CONFIRMED | mod-4 coset |
| 28 | Hilbert+Liu3 #11 | {0,4} | INFEASIBLE | morphisms `(f,e,e,a)` make LR curve-4 an odd-width near-square (not a square); unfillable | n=13 (9⁶=0) | CONFIRMED | 4/8 coset (feasible!) |
| 29 | Hilbert+Liu3 #12 | {0,4} | **FEASIBLE** | `29:(second,first), 4:(second,first), 0:sh=first` | — | CONFIRMED | P/Q coset per size |
| 30 | Hilbert+Liu3 #13 | {0,4} | **FEASIBLE** | `30:(second,first), 4:(second,first), 0:sh=first` | — | CONFIRMED | coset; sporadic h≡1,2 (mod 4) |
| 31 | Hilbert+Liu3 #14 | {0,4} | **FEASIBLE** | `31:(first,second), 4:(second,first), 0:sh=first` | — | CONFIRMED | 4/8 coset, irregular |
| 32 | Moore+Liu4 #1 | {1,5} | INFEASIBLE | two Moore@180 + non-transpose kernels; forced wide 3×2 unfillable | n=5 (9⁴=0) | CONFIRMED | wide↔transpose split |
| 33 | Moore+Liu4 #2 | {1,5} | INFEASIBLE | infeasible Moore band needs opposite Hc1 parity at n=5 vs 7 | n=5 vs 7 | CONFIRMED | domino coset |
| 34 | Moore+Liu4 #3 | {1,5} | INFEASIBLE | all-N morphisms, no transpose access; forced wide 3×2 on Moore/Liu4 | n=5 (9⁴=0) | CONFIRMED | half orient., mod-4 |
| 35 | Moore+Liu4 #4 | {1,5} | INFEASIBLE | Moore quadrant demands sh=second at n=5, sh=first at n=7,9 | n=5 vs 7 | CONFIRMED | sporadic |
| 36 | Moore+Liu4 #5 | {1,5} | INFEASIBLE | width-split node forced sw=second at n=5, sw=first at n=7 | n=5 vs 7 | CONFIRMED | transpose split |
| 37 | Moore+Liu4 #6 | {1,5} | INFEASIBLE | height-split node: Hc1 odd needed at n=3,5, even at n=7 (period 8) | n=3 vs 7 | CONFIRMED | orientation-dependent |
| 38 | Moore+Liu2+Liu4 #1 | {1,3,5} | INFEASIBLE | Moore in final quadrant + interior exit; junction/interior conflict | n=7 (9⁵=0) | CONFIRMED | transpose duality |
| 39 | Moore+Liu2+Liu4 #2 | {1,3,5} | INFEASIBLE | n≡2 (mod 4) forces Moore onto odd (n/2)² square; feasible only if n/2 Jacobsthal | n=14 | CONFIRMED | sporadic |

## The structural condition (feasibility criterion that emerges)

Feasibility is **not** predicted by endpoint type (curve 4 is corner→interior yet feasible;
curve 18 is interior→interior yet infeasible). The criterion is on the **kernels and their
morphism assignment**:

> A curve generalizes to arbitrary squares **iff** (i) every kernel in its recursion is a
> *corner-anchored* curve — Hilbert (0) or Liu3 (4) — never the near-cyclic Moore (1) or the
> edge-to-edge, doubly-pinned Liu4 (5) used as a sub-block; **and** (ii) its four quadrant
> morphisms form one of the four *parity-free-junction* templates (those of the feasible base
> curves 0, 3, 4, 5), so consecutive blocks meet corner-to-corner and each block is handed a
> shape its kernel can fill — Hilbert any parity-correct rectangle (under `sh=first`), Liu3
> only an **odd×odd square**.

The three feasible composites 24/29/30/31 are exactly curves 5/4/0/3's morphism templates with
the last-visited Hilbert quadrant replaced by a Liu3 block that the template hands an odd×odd
square. Infeasibility arises from four disjoint mechanisms, each proved per-curve:

1. **Homogeneous morphisms** (all-transpose or all-non-transpose) cannot route both parities of
   the forced odd/even sub-block: curves 1, 2, 9, 19, 22, 26, 27, 32, 34.
2. **Near-cyclic Moore kernel** (4-adjacent endpoints) inherits an odd-square checkerboard
   obstruction: curves 1, 32–39.
3. **Edge-to-edge Liu4 kernel** nested as a sub-block drifts its junction cell with block size,
   forcing contradictory split parities across two sizes: curves 6–17.
4. **Mis-routing** with good kernels {0,4}: a Hilbert or Liu3 block is forced onto an
   odd×even near-square it cannot fill: curves 18, 20, 21, 23, 25, 28 (and 7-style two-witness
   conflicts throughout).
