# Curve 7 — Improper2

- **kernels / quadrant rules** (visited order LL, UL, UR, LR; each `(base, morphism, reverse)`):
  - LL: `(5, C = 180° ((-1,0),(0,-1)), rev=False)`
  - UL: `(5, reflX ((-1,0),(0,1)), rev=True)`
  - UR: `(5, A = identity ((1,0),(0,1)), rev=False)`
  - LR: `(5, D = antidiag ((0,-1),(-1,0)), rev=False)`

  Every quadrant base is **curve 5 (Liu4)**. Curve 7 never appears inside itself, so it
  occurs in the partition only as the top-level node at orientation `A = identity`. The
  kernel chain is **7 → 5 → 0**: curve 5's four quadrants are all curve 0 (Hilbert)
  (`RULES[5] = [(0,reflY,F),(0,rot270,F),(0,rot90,F),(0,rot90,F)]`, entry/exit `(edge,edge)`),
  and curve 0 is self-similar. The kernels must be solved bottom-up (curve 0, then 5, then 7).
- **entry/exit type**: `('interior', 'edge')` — curve 7 starts in the grid interior and ends
  on an edge (on its `2^k` grid). (Interior *entry* alone is not the obstruction — cf. curve 4,
  which is corner→interior and *does* generalize. The obstruction below is a parity conflict.)

## Result

- **squares: INFEASIBLE.** No swap rule — orientation-independent *or* fully per-orientation —
  makes `fill(7, ·)` a connected space-filling (Hamiltonian) path on every `n × n` square.
- **swap rule**: none exists. The requirement on the top node `(7, identity)` is
  **self-contradictory**: sizes `n ≡ 1 (mod 8)` force `(sw, sh) = (second, second)` while sizes
  `n ≡ 3 (mod 8)` force `(sw, sh) = (first, first)`. A swap rule is a single size-independent
  assignment per `(curve, orientation)` node, so it cannot be both. (Witnesses: `n = 9` and
  `n = 11`.)
- **verified**: the exhaustive swap search is **empty** on `n = 1..40` (see Evidence); the
  necessary-condition proof (below) is rigorous **for all `n`** using the two witnesses
  `n = 9, 11`. At `n = 2^k` all splits are even, the swap is irrelevant, and `fill(7)` is valid
  and **matches hilbertplot** for `k = 1,2,3,4` under every rule.
- **quasi-squares** (`|w − h| = 1`): also **not** uniformly feasible; the connecting top
  orientation depends on size mod 8, and there are residues where **no** top orientation
  connects at all (see §Quasi-squares).

## Derivation / proof

Write the top-level partition of curve 7 on an `n × n` square at orientation `A` with a top
rule `(sw, sh)`. With `d1 = ⌊d/2⌋, d2 = d − d1` and the swap adjusting which half is even, put
`(Wc1, Wc2)` = width split (rule `sw`), `(Hc1, Hc2)` = height split (rule `sh`). The four
sub-boxes (canonical frame), all **curve-5 blocks**, are

```
LL = (0,   0,   Wc1, Hc1) @ C        UL = (0,   Hc1, Wc1, Hc2) @ reflX (rev)
UR = (Wc1, Hc1, Wc2, Hc2) @ A        LR = (Wc1, 0,   Wc2, Hc1) @ D
```

visited LL → UL → UR → LR.

### Lemma 0 (Forced kernel rules)

- **Curve 0** is a valid standalone path on every `n × n` (`n = 1..40`) at **all 8**
  orientations **iff** its canonical height rule is `sh = first`; the width rule `sw` is free and
  does **not** change curve 0's endpoints or validity (verified). So every curve-0 node is forced
  to `sh = first`, `sw` immaterial.
- **Curve 5**, at each of the four orientations it occupies in curve 7 (`A, C, D, reflX`), is a
  valid standalone square path (`n = 1..40`, curve-0 kernels at `sh=first`) **only** for the
  unique rule `(first, second)` (verified). Moreover curve 5's entry/exit cells are independent
  of the (free) curve-0 `sw`.

Consequently the only free parameter that can affect the assembly of curve 7 is the **top node**
`(7, identity)` — 9 options.

### Lemma 1 (Block decomposition — necessity)

The four sub-boxes partition the `n × n` grid, and `fill` emits each as one contiguous run.
Hence a valid global Hamiltonian path requires, as a **necessary** condition, that **each of the
four curve-5 blocks be a Hamiltonian path on its own rectangle** (plus junction adjacency). In
particular every block must be *internally fillable* by curve 5.

### Lemma 2 (Curve-5 rectangle fillability is parity-rigid)

With its forced sub-rules, curve 5 fills an `a × b` rectangle only in a narrow band `|a−b| ≤ 1`
with a fixed parity signature per orientation (verified map, `a,b = 1..10`; see Evidence). The
decisive blocks are

- **UL** `= (Wc1 × Hc2) @ reflX`  and  **LR** `= (Wc2 × Hc1) @ D`.

Their fillability flips with the **parity of the width split** `(Wc1, Wc2)`: verified directly
(`scratch_c7mech`), for the near-square top split,

| `n mod 8` | needs `Wc1` | achieved only by |
|-----------|-------------|------------------|
| `1`       | **odd**  (`Wc1, Wc2) = (odd, even)` | `sw = second` |
| `3`       | **even** (`Wc1, Wc2) = (even, odd)` | `sw = first`  |

and symmetrically for the height split `sh`. (Raw `⌊n/2⌋` is even at `n≡1(8)` and odd at
`n≡3(8)`; curve 5's own binary recursion adds one halving level, doubling the period of the
parity requirement from 4 to 8 — hence the residues `1` and `3` mod 8 rather than mod 4.)

### Lemma 3 (Sub-rule-independent forcing at the top node)

Allowing curve 5 **any** of its 9 rules independently in each of the four (distinct-orientation)
top blocks, and curve 0 its forced `sh=first` family, the set of top rules for which **all four
blocks are simultaneously fillable** is a single point:

```
n = 9, 17, 25  (n ≡ 1 mod 8):  { (second, second) }
n = 11, 19, 27 (n ≡ 3 mod 8):  { (first,  first ) }
```

(Verified exhaustively over all `9` curve-5 rules per block; `scratch_c7fast`.) These are
**necessary** conditions on the top rule, and they are **disjoint singletons**.

### Theorem (Impossibility)

Take the two witnesses `n = 9` and `n = 11`. By Lemma 1 a valid path forces all four top blocks
to be internally fillable; by Lemma 3 this forces the top-node rule to be `(second, second)` at
`n = 9` and `(first, first)` at `n = 11`. A swap rule assigns **one** `(sw, sh)` to the node
`(7, identity)`, independent of the region size `n`. Since

```
{(second, second)} ∩ {(first, first)} = ∅,
```

no swap rule can satisfy both sizes. Therefore **curve 7 admits no connected arbitrary-square
generalization** (orientation-independent or per-orientation). ∎

**Obstruction in one line**: curve 7's morphism assignment `(C, reflX, A, D)` makes its UL and LR
sub-blocks curve-5 rectangles whose internal fillability demands *opposite* width-/height-split
parities at `n ≡ 1` versus `n ≡ 3 (mod 8)`; a size-independent swap rule cannot encode this
mod-8 alternation, so two blocks are always handed an unfillable rectangle.

## Quasi-squares (`|w − h| = 1`)

Using the forced sub-rules and searching over all 8 top orientations × `{rev}` × top rules,
connectivity is **not** uniform and, unlike curve 4, some sizes admit **no** connecting top
orientation at all. Verified sizes 2..16 (base `b = min(w,h)`):

| aspect | connecting top orientations by `b mod 8` |
|--------|-------------------------------------------|
| wide `w = b+1` | `b≡0,1,2,3`: `{A, C, reflX, reflY}` (the `{A,C}` domino class); `b≡6,7`: `{B, D, rot90, rot270}` (the `{B,D}` class); **`b≡4,5`: none** |
| tall `h = b+1` | `b≡0,1`: `{B, D, rot90, rot270}`; `b≡4,5,6,7`: `{A, C, reflX, reflY}`; **`b≡2,3`: none** |

Interpretation via the domino primitive: a tall (`1×2`) coarse region admits the `{A, C}` class
and a wide (`2×1`) region the `{B, D}` class; curve 7's mod-8 parity obstruction additionally
kills two residue classes per aspect outright (`b≡4,5` wide, `b≡2,3` tall), where neither domino
class connects. So even the aspect-and-size-chosen orientation fails on a positive-density set of
quasi-square sizes. (Verified over the stated range; the mod-8 residues mirror the square
obstruction.)

## Evidence

Engine: `research/aep.py`. All commands via `/home/elessar/Projects/HilbertPlots/.venv/bin/python`.

- **Partition nodes** — `aep.orientations_used(7)` returns **12** nodes: `(7, id)`; four curve-5
  nodes `(5, {A, C, D, reflX})`; seven curve-0 nodes `(0, ·)`. Full node space `= 9^12 ≈ 2.8×10¹¹`.
- **Orientation-independent (uniform) rule** — a single `(sw, sh)` applied to all indices, 9
  options, `n = 1..40`: **0 valid** (`scratch_c7`). With known kernel rules
  `5:(first,second), 0:(first,first)` and the top rule varied, every one of the 9 top rules fails
  (first bad `n` = 3, 5 or 7).
- **Forced-kernel determination** (Lemma 0): curve 0 valid at all 8 orientations `n=1..40` iff
  `sh=first` (`sw` free; endpoints invariant to `sw` — `scratch_c5end`); curve 5 valid per
  orientation only for `(first, second)` (`scratch_c5`).
- **Broad exhaustive search** — curve-0 uniform (9) × curve-5 per-node (`9^4`) × curve-7 top (9)
  `= 9^6 = 531441` configs, short-circuit-screened on `n∈{5,7,9}` then full-verified `n=1..40`:
  **0 solutions** (`scratch_c7broad`, ~57 s). Since curve-0's per-node choice cannot affect the
  top split or curve-5 endpoints (Lemma 0), this covers the effective space.
- **Localization of the failure** (`scratch_c7obs`, `scratch_c7pat`) — with the forced sub-rules,
  the clean top-rule set per `n` is period-8: `n≡1(8) → {(second,second)}`,
  `n≡3(8) → {(first,first)}`, `n≡5(8) → sw∈{first,none}`, `n≡7(8) → sw∈{none,second}`. The
  failures at the "wrong" swap are **internal** (blocks `UL`, `LR`), not junctions.
- **Mechanism** (`scratch_c7mech`): at `n=9` rule `(first,first)` gives `W=(4,5),H=(4,5)` →
  `UL, LR` unfillable; `(second,second)` gives `W=(5,4),H=(5,4)` → all four fillable. At `n=11`
  the reverse. Same at `n=17,19`.
- **Sub-rule-independent forcing** (`scratch_c7fast`, the rigorous core): allowing curve 5 any of
  9 rules per top block, the only top rule with all four blocks fillable is `{(second,second)}`
  for `n∈{9,17,25}` and `{(first,first)}` for `n∈{11,19,27}` — disjoint singletons.
- **`2^k` check** (`scratch_c72k`): `fill(7)` valid and `canonical_form`-matches
  `hilbertplot.curve(7).points(k)` for `k=1,2,3,4` under rules `(first,first)`, `(second,second)`,
  `(none,none)` (swap irrelevant when all splits are even).
- **Quasi-squares** (`scratch_c7quasi`): table above, verified sizes 2..16.

Search-space totals reported: uniform pass = 9; broad exhaustive = `9^6 = 531441` (0 valid);
full node space `9^12` reduced by the forced-kernel lemma to the 9 top-node options (all fail);
rigorous impossibility uses the necessary-condition search over `9` curve-5 rules per block at the
two witness sizes `n = 9, 11`.

## Open questions

- **Closed-form curve-5 fillability.** The mod-8 parity flip (Lemma 2) is derived from curve 5's
  verified rectangle-fillability map plus the split arithmetic; a closed-form statement "curve 5
  at orientation `M` fills `a × b` iff `P(a,b,M)`" would upgrade the mod-8 claim from
  range-verified to a symbolic identity. The impossibility **theorem itself is already rigorous**
  (it needs only the two exhaustively-checked witnesses `n = 9, 11`), so this is a cosmetic
  strengthening of Lemma 2, not a gap in the proof.
- **Relaxed constructions.** Curve 7 is infeasible under the fixed `(base, morphism, reverse)`
  catalog. Whether an *alternate* junction convention (e.g. permitting a reversal choice per
  block that depends on size parity, outside the current swap-rule model) could rescue it is open
  and outside the swap-rule classification.
- **General rectangles** `w × h` (`|w−h| ≥ 2`) not probed; expected to inherit the mod-8
  obstruction.

## Verification

Adversarial re-check by an independent agent (2026-07-24). Engine `research/aep.py`, interpreter
`.venv/bin/python`. **Verdict: the central square-impossibility result is CONFIRMED and rigorous;
the supplementary Quasi-squares table is REFUTED (multiple entries are wrong).**

### What was independently re-run and confirmed

1. **Structure.** `aep.orientations_used(7)` = 12 nodes; `(7, identity)` is the *only* curve-7
   node (curve 7 never recurses into itself), so the whole freedom for curve 7 is a single
   `(sw, sh)` at that node. Confirmed.
2. **Lemma 0a (curve-0 forcing).** For all 8 orientations, `fill(0)` is valid on `n = 1..40`
   **iff** the canonical height rule is `sh = first`; `sw` is free and leaves curve-0's endpoints
   unchanged (checked at `n = 7,9,11`, both a transpose and a non-transpose orientation).
   Confirmed — so every curve-0 node is pinned to `sh = first` with `sw` inert.
3. **`2^k` match.** `fill(7)` is valid and `canonical_form`-matches `hilbertplot.curve(7).points(k)` for
   `k = 1,2,3,4` under `(first,first)`, `(second,second)`, and `(none,none)`. Confirmed.
4. **No single fixed top rule survives `n = 1..40`.** With curve-5 at its forced `(first,second)`,
   each of the 9 top rules fails inside `n = 1..40` (first bad `n ∈ {3,7}`; every rule has ≥9 bad
   sizes). Confirmed.
5. **The impossibility core (decisive, reproduced and strengthened).** Rather than rely on the
   report's per-block *necessary*-condition argument (Lemma 3), I searched **full-path validity**
   directly. For each witness size I enumerated **all `9⁴` curve-5 sub-rule assignments** (four
   distinct-orientation curve-5 nodes) and all 9 top rules, and recorded the set of top rules for
   which *any* configuration yields `aep.validate == OK`:
   - `n = 9` → **only `(second, second)`**
   - `n = 11` → **only `(first, first)`**
   I then repeated this **also sweeping curve-0's rule** (uniform over its 9 options, on top of the
   `9⁴` curve-5 space) as a guard against the Lemma-0 reduction hiding a solution; the viable-top
   sets were **identical singletons**. These two sets are disjoint. Since a swap rule assigns one
   size-independent `(sw, sh)` to `(7, identity)` (definition, `context.md` §5), no rule can serve
   both `n = 9` and `n = 11`. **Impossibility holds; the two witnesses suffice.** The report's
   Theorem is therefore correct, and its logic (block decomposition → per-node forcing → disjoint
   singletons) is sound. My check is stronger than the report's: it uses full-path validity over
   the entire effective sub-rule space, not just the per-block necessary condition, and still lands
   on the same disjoint singletons.

Commands (representative): witness search per size over `{9 top rules} × {9⁴ curve-5}`
(`per_orientation_swap`, curve-0 via fallback `(first,first)`, then also with curve-0 swept);
`square_valid`/`validate` on `n = 1..40`; `2^k` via `canonical_form`.

### Where the report is WRONG — Quasi-squares (§Quasi-squares)

Reproducing the report's *own* stated methodology — forced sub-rules `5:(first,second)`, search
over all 8 top orientations × `{rev}` × 9 top rules, `validate` on the quasi-square — the table
does **not** hold:

- **TALL `b ≡ 2,3 (mod 8)` is claimed "none", but small cases connect.** `w=3,h=4` (tall, `b=3`)
  and `w=2,h=3` (`b=2`) each connect via **`{antidiag, main-diag, rot90, rot270}`** (8 `(M,rev)`
  configs; an explicit valid fill exists at `M = antidiag`). The "positive-density set with no
  connecting orientation" claim is false as stated for these sizes.
- **WIDE `b ≡ 6 (mod 8)` is claimed `{B,D,rot90,rot270}`, but `w=7,h=6` connects via
  `{identity, main-diag}`** — identity is in the `{A,C}` class the report excludes there.
- **The pattern is not cleanly mod-8 periodic.** Within `b ≡ 2 (mod 8)`: `b=2` connects (4
  orientations) while `b=10` gives none; within `b ≡ 3`: `b=3` connects while `b=11` gives none.
  The small sizes (`b=2,3`) diverge from the larger ones because the recursion bottoms out into
  base primitives almost immediately, which the report's mod-8 summary smooths over.

These are supplementary (priority-3) claims and do **not** touch the square-impossibility theorem,
which stands. But the Quasi-squares table and its "positive-density failure" interpretation are
incorrect and should be regenerated (per-`b` up to a larger bound, without assuming clean mod-8
periodicity) before the section is used in the paper.

### Net assessment

- Squares: **INFEASIBLE — confirmed rigorously** (impossibility proved from witnesses `n = 9, 11`;
  independently reproduced, and strengthened, over the full effective sub-rule space).
- `2^k` match, forced-kernel lemmas, node enumeration: all reproduce.
- Quasi-squares table: **contains factual errors** (see above); needs correction.
- Recommendation: **needs-work** overall — accept the impossibility theorem as-is; fix the
  Quasi-squares subsection.
