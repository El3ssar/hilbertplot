# Curve 9 — Improper4

- **kernels / quadrant rules** (`aep.RULES[9]`, order LL, UL, UR, LR):
  | quadrant | base | morphism `M` | reverse |
  |---|---|---|---|
  | LL | 5 | `((0,-1),(-1,0))` | True |
  | UL | 5 | `((0,-1),( 1,0))` | False |
  | UR | 5 | `((0, 1),( 1,0))` | True |
  | LR | 5 | `((0, 1),(-1,0))` | False |

  All four quadrants use kernel **curve 5 (Liu4)**, and every morphism is a
  *transposition* (`M[0][0]==0`). Curve 5 in turn kernels into **curve 0 (Hilbert)**
  in all four of its quadrants, so the dependency chain is `9 → 5 → 0`.
- **entry/exit type** (`aep.entry_exit(9)`): `('interior','interior')`.

## Result

- **squares: INFEASIBLE.** There is **no** swap rule — orientation-independent *or*
  per-orientation, over the entire rule space — that makes `fill(9, …)` a Hamiltonian
  path on every `n × n` square. The obstruction is the **5 × 5 square**, which admits
  no valid path under the construction for any swap assignment.
- **swap rule: none exists.**
- **verified:** every candidate rule fails at `n = 5`. Exhaustive proof below. Matches
  hilbertplot at `2^k`: N/A (no admissible rule exists; the standard `2^k` curve is of course
  recovered by the plain recursion, but that recursion does not extend to `n = 5`).
- **quasi-squares:** connectivity is aspect- and orientation-dependent and *incomplete*
  for both aspects (details in §Quasi-squares). This is consistent with — and reinforces
  — square infeasibility.

## Derivation / proof of impossibility

The partition nodes that need a swap rule are `aep.orientations_used(9)` **plus** the one
node first reached only at the even size `n = 12` (which `orientations_used`'s odd-only
sampling misses): curve 9 at the identity, curve 5 at its 4 transpose orientations, and
curve 0 at **all 8** orientations — 13 nodes total. The full rule space is therefore
`9^13`. We never need to search it: the obstruction lives entirely at `n = 5`, which
exercises only 4 of these nodes.

### Lemma A (curve 5 cannot fill a 2×3 block in curve 9's frame)

For each of curve 9's four quadrant morphisms `M ∈ {((0,∓1),(±1,0))}`, curve 5 admits
**no** valid Hamiltonian path on a `2 × 3` region, for any swap rule. A `2 × 3` region
reaches exactly one partition node (`(5, M)`; its sub-boxes are all `≤ 2`, i.e. base
dominoes), so "any swap rule" is the 9 values of that single node.

*Evidence (exhaustive):* for every one of the four morphisms, `2×3` gives `0/9` valid,
whereas the transposed shape `3×2` gives `6/9` valid. Curve 5 is, in curve 9's frame,
**"wide-admissible / tall-forbidden"** at the `2`-vs-`3` scale: it can tile the wide
`3×2` but never the tall `2×3`.

### Lemma B (the AEP pinwheel at n = 5 always contains a 2×3 block)

The approximately-even split of `5` is `5 = 2 + 3` — the *only* possibility, so
`{Wc1, Wc2} = {Hc1, Hc2} = {2, 3}` regardless of the swap value at `(9, IDENT)` (the swap
merely reorders the pair). The four pinwheel boxes are
`LL=(Wc1×Hc1)`, `UL=(Wc1×Hc2)`, `UR=(Wc2×Hc2)`, `LR=(Wc2×Hc1)`.
Enumerating the four split parities `(Wc1,Hc1) ∈ {2,3}²`, in **every** case exactly one
box has shape `2×3` and exactly one has `3×2` (the other two are the squares `2×2`,
`3×3`), and the `2×3` box always lands on a quadrant whose morphism is one of the four
tall-forbidden ones of Lemma A. The verified table:

| split `(Wc1,Wc2)/(Hc1,Hc2)` | LL | UL | UR | LR | un-fillable box |
|---|---|---|---|---|---|
| `(2,3)/(2,3)` | 2×2 | **2×3** | 3×3 | 3×2 | UL |
| `(2,3)/(3,2)` | **2×3** | 2×2 | 3×2 | 3×3 | LL |
| `(3,2)/(2,3)` | 3×2 | 3×3 | **2×3** | 2×2 | UR |
| `(3,2)/(3,2)` | 3×3 | 3×2 | 2×2 | **2×3** | LR |

### Theorem (5×5 is infeasible → squares infeasible)

By Lemmas A–B, for every swap assignment at least one of the four sub-blocks of the
`5×5` partition is not a Hamiltonian path, so the concatenation cannot be a Hamiltonian
path on `5×5`. Since a swap value can only permute `{2,3}`, no choice escapes the toxic
`2×3` block. Because a valid arbitrary-square generalization must in particular be valid
on `5×5`, **none exists**. ∎

*The obstruction is sharp and localized to n = 5.* `5 = 2 + 3` is the minimal odd split
that produces the un-fillable `2×3` pair. Adjacent sizes avoid it and are **individually**
feasible: `n = 6` splits `{3,3}` (all sub-blocks square, 11664 valid assignments) and
`n = 7` splits `{3,4}` (sub-blocks `3×4`/`4×3`, which curve 5 can tile, 2916 valid
assignments). It is precisely the impossibility of the single size `n = 5` — not a global
parity failure — that forbids a uniform rule.

### Why curve 9 differs from the feasible curves

The feasible square-generalizing curves (0; 3,5,24,31; 4,29,30) place their kernels so
that the transposed off-diagonal sub-block always meets a kernel orientation able to tile
it. Curve 9's four quadrant morphisms are *all* transpositions of the *same* handedness
relative to curve 5's intrinsic "wide-admissible" bias, so the two off-diagonal aspects
`2×3` and `3×2` cannot both be satisfied — the structural cause of infeasibility. This is
the boundary case for the structural theorem: feasibility requires the kernel's
admissible-aspect set to cover *both* transposed off-diagonal shapes forced by the split.

## Quasi-squares (|w − h| = 1)

For each top-level orientation `M` we asked whether *some* swap rule connects `fill(9,…,M)`
on wide (`w = h+1`) and tall (`h = w+1`) quasi-squares (exhaustive over the reached nodes
where feasible; verified sizes below).

- **Non-transpose** orientations (`M[0][0] ≠ 0`: identity, 180°, and the two axis
  reflections):
  - wide `2×1, 3×2, 4×3, 5×4, 6×5, 7×6` → `T, F, T, T, T, T` (only `3×2` fails)
  - tall `1×2, 2×3, 3×4, 4×5, 5×6, 6×7` → `T, T, T, F, F, T`
- **Transpose** orientations (`M[0][0] = 0`): the exact mirror image (wide ↔ tall).

Both `F` results at `4×5` and `5×6` were confirmed by *exhaustive* search
(`9^3 = 729` and `9^5 = 59049`, zero valid), so they are genuine, not search-cap
artifacts. **Conclusion:** neither aspect connects at *all* sizes for *any* orientation —
quasi-squares do not rescue curve 9, matching square infeasibility.

The `w=2`/`h=2` boundary case (`3×2` vs `2×3`) is governed directly by the primitive
**domino constraint**: at thickness 2 the sub-blocks bottom out as base dominoes, and only
the orientation-matched domino is available — the `1×2` tall domino for the
A/C-type orientations vs. the `2×1` wide domino for the B/D-type — exactly the
Wu–Chang 1×2 (A,C) / 2×1 (B,D) primitive split. For thickness `≥ 3` the recursion re-enters
the curve-5 aspect obstruction of Lemma A, making connectivity size-dependent.

## Evidence (commands and outputs)

Run from `/home/elessar/Projects/HilbertPlots` with `.venv/bin/python`, importing
`aep` from `research/`.

**Structure.**
```
aep.NAME[9]        -> 'Improper4'
aep.entry_exit(9)  -> ('interior','interior')
aep.RULES[9]       -> LL(5,((0,-1),(-1,0)),T) UL(5,((0,-1),(1,0)),F)
                      UR(5,((0,1),(1,0)),T)   LR(5,((0,1),(-1,0)),F)
```

**Default recursion (`const (first,first)` everywhere) is valid only on multiples of 4:**
```
OK sizes (n=1..32): [1, 2, 4, 8, 12, 16, 20, 24, 28, 32]
```

**Exhaustive infeasibility of 5×5** (the `5×5` partition exercises exactly 4 nodes —
`(9,IDENT)` and `(5,·)` at three orientations):
```
n=5 exercises 4 nodes: [(5,((0,-1),(1,0))), (5,((0,1),(-1,0))), (5,((0,1),(1,0))), (9,IDENT)]
EXHAUSTIVE 5x5: tested 6561 assignments (9^4), valid = 0
```

**Lemma A (exhaustive, per morphism):**
```
morph ((0,-1),(1,0)):  2x3 valid = 0/9 |  3x2 valid = 6/9
morph ((0,1),(-1,0)):  2x3 valid = 0/9 |  3x2 valid = 6/9
morph ((0,1),(1,0)):   2x3 valid = 0/9 |  3x2 valid = 6/9
morph ((0,-1),(-1,0)): 2x3 valid = 0/9 |  3x2 valid = 6/9
```

**Lemma B (split-parity table):** see the table in the proof; every parity leaves exactly
one `2×3` block on a tall-forbidden quadrant.

**Obstruction is localized to n = 5** (per-size exhaustive over each size's nodes):
```
n=5: 9^4 = 6561 tested, valid = 0      (INFEASIBLE)
n=6: 9^5 = 59049 tested, valid = 11664 (feasible; split {3,3})
n=7: 9^5 = 59049 tested, valid = 2916  (feasible; split {3,4})
```

**Global search corroboration.** A complete layered exhaustive search over all 13 nodes
(gate: validate `n ≤ 8`, which touches only the curve 9 + curve 5 nodes, then extend to
curve 0) returns **0** full solutions on `n = 1..40`; the gate is already empty at
`n ≤ 8` because `n = 5` cannot be satisfied. Orientation-independent `(sw,sh)` (9 options)
and per-curve-constant rules (`9^3 = 729`) were also both exhaustively empty.

## Open questions

- The exact fillable-aspect band of curve 5 (`fill(5,·)` valid region in the `w×h` plane)
  is a diagonal band slightly wider than `w ≥ h`; a closed-form of this band would let the
  structural feasibility theorem be stated purely in terms of each kernel's admissible-
  aspect set vs. the two off-diagonal shapes a split forces.
- Rectangles `w × h` with `|w−h| ≥ 2`: not systematically probed here; the same
  `2×(2k+1)` aspect obstruction is expected to recur wherever a `2×3` sub-block is forced.
- Curve 9 is the natural witness for the "both off-diagonal aspects must be coverable"
  clause of the general classification theorem; confirm which other infeasible curves fail
  by the *same* aspect mechanism vs. a genuine parity/counting invariant.

## Verification

**Verdict: CONFIRMED (INFEASIBLE for squares).** An independent, skeptical re-run of the
engine reproduces every load-bearing claim, and the impossibility argument is sound.

**What I ran** (scratch scripts importing `aep` from `research/`, `.venv/bin/python`):

- *Structure.* `RULES[9]`, `RULES[5]`, `entry_exit(9)=('interior','interior')`,
  and default `const(first,first)` OK-sizes `[1,2,4,8,12,16,20,24,28,32]` — all match.
- *5×5 exhaustive (decisive).* Using an independent node tracer that enumerates **all**
  nodes reachable at `n=5` under **any** swap (not a single fixed swap), I find **5**
  reachable nodes: `(9,IDENT)` plus curve 5 at **all four** morphisms
  `{((0,-1),(-1,0)), ((0,-1),(1,0)), ((0,1),(-1,0)), ((0,1),(1,0))}`. Exhaustive search
  over `9^5 = 59049` per-node assignments gives **0 valid**. This is a strict superset of
  the report's search and still empty.
- *Lemma A.* Reproduced exactly: for each of curve 9's four morphisms, curve 5 on `2×3`
  = **0/9** valid, on `3×2` = **6/9** valid.
- *Localization.* `n=5`: 0/59049; `n=6`: **11664**/59049 (feasible, split {3,3});
  `n=7`: **2916**/59049 (feasible, split {3,4}) — exact match to the report.
- *Quasi-squares.* `4×5` and `5×6` both **0/59049** (exhaustive, genuine `F`), matching
  the report. Top-level `3×2`=0/9 (`F`), `2×3`=9/9 (`T`) also match.
- *Global rules.* No orientation-independent `(sw,sh)` is valid on `n=1..40` (empty), and
  none even passes `n=5` (empty).

**Why the conclusion is airtight.** The `swap` callable is a function of `(index, M)`
only — it *cannot* depend on the region size `n`. Therefore any global rule, restricted to
the nodes reachable at `n=5`, is one of the assignments enumerated in the exhaustive
`9^5` search above, all of which fail on `5×5`. Since a valid arbitrary-square
generalization must be valid on `5×5`, none exists. The Lemma A/B mechanism (`5 = 2+3`
forces exactly one `2×3` block onto a tall-forbidden quadrant) correctly explains the
obstruction and does not depend on the node count.

**Minor issue found (does not affect the verdict).** The report states `n=5` "exercises
exactly 4 nodes" and searches `9^4 = 6561`; the LL node `(5,((0,-1),(-1,0)))` is omitted
because under the *default* split it happens to bottom out as a `2×2` base block. Across
all swap values that node *is* reachable, so the fully-general search space is `9^5`, not
`9^4`. The report's stated search implicitly pins that node at the default rule rather than
varying it. I closed this gap with the complete `9^5 = 59049` search (still 0 valid), so
the impossibility stands unchanged; only the node count / search-space figure in §Evidence
is slightly understated.
