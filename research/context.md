# Arbitrary-size generalization of the 40 two-dimensional Hilbert curves — study brief

**Read this file and `research/aep.py` in full before doing anything.** This is a
research program aimed at a publishable paper. Every claim must be either (a) verified
computationally with the shared engine over a stated range, or (b) proved with a
rigorous mathematical argument. Hand-waving is not acceptable; the verification phase
will reject unsupported claims.

## 1. Background

* **hilbertplot** implements the complete set of forty 2-D Hilbert-type space-filling curves
  of Estevez-Rams et al., *Rev. Cub. Fis.* 34, 9 (2017). Each curve `index` (0..39) is
  defined recursively by four **quadrant rules** for the sub-quadrants LL, UL, UR, LR
  (lower-left, upper-left, upper-right, lower-right), visited in that order and joined by
  unit steps. A quadrant rule is `(base, morphism, reverse)`: `base` is the kernel curve
  index used in that quadrant, `morphism` a D4 symmetry, `reverse` a traversal reversal.
  In the standard `2^k x 2^k` construction all four sub-quadrants have equal size.
* **Wu & Chang**, *IET Image Process.* 6(6):746 (2012), "Approximately even partition
  algorithm for coding the Hilbert curve of arbitrary-sized image", generalize **only the
  standard Hilbert curve** to any `n x m` region by the *approximately even partition*:
  split each side `d` into `d1 = floor(d/2), d2 = ceil(d/2)`, recurse into 4 (now
  unequal) sub-regions, bottoming out at `1x1, 1x2, 2x1, 2x2` primitives. To keep the
  path connected at odd sizes they use a per-orientation **swap rule** that forces a
  chosen half to be even (their Fig 5). Their four orientations A,B,C,D are the D4 subset
  `{identity, main-diagonal reflection, 180° rotation, anti-diagonal reflection}`.

## 2. The engine (`research/aep.py`)

`fill(index, x0, y0, w, h, M, rev, swap)` produces the ordered cell list for curve
`index` on region `(x0,y0,w,h)` with orientation matrix `M` (reversed if `rev`), driven
by hilbertplot's catalog rules and full D4. `swap(index, M) -> (sw, sh)` supplies the swap rule
(`"first"` = make the low half even, `"second"` = make the high half even, `"none"`) for
the width- and height-split when partitioning that curve at that orientation.

Helpers: `validate(cells,w,h)` (returns `"OK"` or the failure reason — count / distinct /
bbox / disconnected); `square_valid(index, swap, sizes)`; `const_swap({index:(sw,sh)})`
and `per_orientation_swap({(index,M):(sw,sh)})`; `entry_exit(index)`;
`orientations_used(index)` (the `(curve, orientation)` partition nodes that need a rule);
`D4` (the 8 matrices), `IDENT`, `RULES`, `NAME`.

Run everything as: `cd /home/elessar/Projects/HilbertPlots && .venv/bin/python -c '...'`
or a scratch script that does `import sys; sys.path.insert(0,"research"); import aep`.

## 3. Known results (already established — do not redo, but you may re-verify)

* Curve 0 (Hilbert) reproduces Wu & Chang exactly: valid on all squares, matches hilbertplot at
  `2^k`. Swap rule is orientation-dependent: `{A,B} -> (first,first)`, `{C,D} ->
  (second,second)` — equivalently "make the half on the entry-corner side even".
* Eight curves already generalize to arbitrary **squares** with a single orientation-
  *independent* `(sw, sh)`:
  0:(first,first); 3,5,24,31:(first,second); 4,29,30:(second,first).
* `entry_exit` gives each curve's global start/end type (corner/edge/interior). Note
  curve 4 is corner→interior yet generalizes — so **feasibility is NOT simply predicted
  by endpoint type**. The true condition must be derived.

## 4. The central problem (per curve)

For your assigned curve `index`, in order of priority:

1. **Squares.** Determine whether there exists a swap rule `swap(index, ·)` (orientation-
   independent if possible, else per-orientation) that makes `fill(index,·)` a single
   connected space-filling path on **every** `n x n` square. Verify over `n = 1..40` at
   least (state the exact range tested). If such a rule exists, report it precisely and
   **derive why it works** from the curve's quadrant/entry-exit/boundary-vector structure
   (not just "the search found it").
2. **Impossibility.** If no swap rule works, prove it. A rigorous impossibility proof
   should identify the obstruction (e.g. a parity/counting invariant, a boundary-vector
   incompatibility between adjacent sub-regions at odd sizes, or a conflict between the
   parity constraints imposed at two different internal junctions that cannot be
   simultaneously satisfied). Support it with computational evidence (the exhaustive swap
   search returning empty over the full rule space) AND a mathematical argument.
3. **Quasi-squares** (`|w-h| = 1`). Which top-level orientations yield a connected path
   for wide (`w=h+1`) vs tall (`h=w+1`) quasi-squares? Relate to the 1x2 (orientations
   A,C) / 2x1 (orientations B,D) primitive constraint.
4. **Rectangles** (stretch, optional now): note any evidence about general `w x h`.

## 5. Rigor & definitions (use these exact terms in every report)

* *Valid* / *space-filling* = a Hamiltonian path on the grid (all cells once, consecutive
  cells 4-adjacent). Always confirm with `validate`.
* *Swap rule* per axis ∈ {first, second, none}; may depend on the orientation `M`.
* *Junction* = the boundary between two consecutively-visited sub-regions; connectivity
  requires the exit cell of one and the entry cell of the next to be 4-adjacent.
* When you claim "no rule works", you must have searched the **full** rule space for that
  curve (all relevant `(index, M)` nodes, each over {first,second,none}²) — use
  `orientations_used` to enumerate the nodes, then exhaustively test. Report the search
  size.
* Distinguish clearly: *verified computationally over range R* vs *proved for all n*.

## 6. Report format — write `research/reports/curve_<index>.md`

```
# Curve <index> — <name>
- kernels / quadrant rules: ...
- entry/exit type: ...
## Result
- squares: FEASIBLE (rule) | INFEASIBLE (obstruction)
- swap rule: <precise, per-orientation if needed>
- verified: valid on n x n for n in <range>; matches hilbertplot at 2^k: yes/no
- quasi-squares: <orientations that work, per aspect>
## Derivation / proof
<the mathematics: why the rule works, or the impossibility proof, with lemmas>
## Evidence
<commands run and their outputs; search space size>
## Open questions
```

Also return the structured summary requested by the harness. Keep the markdown rigorous
and self-contained — it will be assembled verbatim into the paper.

## 7. Target theorems (for the synthesis)

* A classification: exactly which of the 40 curves admit a connected arbitrary-square
  generalization, with the swap rule for each feasible one and an impossibility proof for
  each infeasible one.
* A structural characterization: the property of a curve's quadrant rules / boundary
  vectors that determines feasibility and the swap rule (the goal is a theorem of the form
  "curve ν generalizes to squares iff <condition on its rules>").
