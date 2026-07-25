# Curve 4 — Liu3

- **kernels / quadrant rules** (visited order LL, UL, UR, LR; each `(base, morphism, reverse)`):
  - LL: `(0, B=maindiag ((0,1),(1,0)), rev=False)`
  - UL: `(0, A=identity ((1,0),(0,1)), rev=False)`
  - UR: `(0, A=identity ((1,0),(0,1)), rev=False)`
  - LR: `(0, C=180° ((-1,0),(0,-1)), rev=False)`

  Every quadrant base is **curve 0 (Hilbert)**. Curve 4 never appears inside itself, so
  in the partition it occurs only as the top-level node at orientation `A=identity`; all
  deeper nodes are curve 0. The kernel to solve first is therefore curve 0.
- **entry/exit type**: `('corner', 'interior')` — curve 4 starts at a grid corner and ends
  in the interior. (This is notable: despite the interior exit, curve 4 *does* generalize
  to all squares. Endpoint type does not predict feasibility.)

## Result

- **squares: FEASIBLE**, with a single **orientation-independent** rule.
- **swap rule**:
  - curve 4 (top-level node): `(sw, sh) = (second, first)`.
  - kernel curve 0: `sh = first` on the height axis is required; the width rule `sw` is
    **free** (curve 0's own established square rule `(first, first)` satisfies this).

  The composite `const_swap({4:(second,first), 0:(first,first)})` is valid.
- **verified**: valid Hamiltonian path on `n × n` for **n = 1..40** (`bad = []`); matches
  hilbertplot's `2^k` curve (via `canonical_form`) for **k = 1,2,3,4**: **yes**. Also valid on
  squares under **all 8 top-level D4 orientations** (n = 1..25), so the rule is orientation-
  independent even at the top level.
- **quasi-squares** (`|w−h| = 1`): **not** uniformly feasible with the square rule. For each
  quasi-square size exactly one of the domino orientation-pairs connects, selected by size
  mod 4 (see §Quasi-squares). No single orientation works for all wide (or all tall)
  quasi-squares.

## Derivation / proof

Write the top-level partition of curve 4 on an `n × n` square at orientation `A` with
`(sw, sh) = (second, first)`. With `d1 = ⌊d/2⌋, d2 = d−d1`, the swap makes:

- width split `(Wc1, Wc2)` with rule `second` (make `Wc2` even when possible),
- height split `(Hc1, Hc2)` with rule `first` (make `Hc1` even when possible),

and the four sub-boxes (canonical frame) are

```
LL = (0,   0,   Wc1, Hc1) @ B       UL = (0,   Hc1, Wc1, Hc2) @ A
UR = (Wc1, Hc1, Wc2, Hc2) @ A       LR = (Wc1, 0,   Wc2, Hc1) @ C
```

visited LL → UL → UR → LR, each a curve-0 (Hilbert) block.

### Lemma 1 (Junction auto-adjacency — the structural reason curve 4 is feasible)

For **any** split sizes, the three internal junctions are 4-adjacent, independent of parity:

- **LL → UL**: LL @ B runs the left column from `(0,0)` up to `(0,Hc1−1)`; UL @ A begins at
  `(0,Hc1)`. These differ by 1 in `y`. Adjacent. ✔
- **UL → UR**: UL @ A ends at `(Wc1−1,Hc1)`; UR @ A begins at `(Wc1,Hc1)`. Differ by 1 in
  `x`. Adjacent. ✔
- **UR → LR**: UR @ A ends at `(Wc−1,Hc1)` (Wc = Wc1+Wc2); LR @ C begins at `(Wc−1,Hc1−1)`.
  Differ by 1 in `y`. Adjacent. ✔

The four morphisms `(B, A, A, C)` are chosen precisely so consecutive blocks meet at the
shared cell-corner of the internal cross, and those corner cells are always unit-adjacent.
Verified for n = 3..40: `all junctions adjacent = True`. Hence the *joins* impose **no**
parity constraint — this is why curve 4 is feasible even though its global exit is interior.

### Lemma 2 (Reduction)

Because junctions are always adjacent (Lemma 1) and each block is entered/exited exactly
once (single contiguous run — verified n = 3..40), the full path is a valid Hamiltonian
path **iff every sub-block is itself a valid curve-0 path** on its rectangle. Thus curve-4
validity reduces entirely to curve-0-on-sub-rectangle validity.

### Lemma 3 (Parity of the sub-rectangles fixes the swap)

The reduction (Lemma 2) means the swap's only job is to hand curve 0 sub-rectangles it can
fill. For **odd n**, the rule `(second, first)` forces `Wc2` even and `Hc1` even (verified),
giving

```
LL = odd × even @ B,  UL = odd × odd @ A,  UR = even × odd @ A,  LR = even × even @ C.
```

Necessity of exactly this choice is shown by the failure mode: with `(first, first)` or
`(none, first)` at n = 5 the width splits as `Wc1 = 2, Wc2 = 3`, making `LR = 3 × 2 @ C`;
this Hilbert block is **internally disconnected** (`internal_path_ok = False`) even though
all three junctions remain adjacent. So the break is never at a junction — it is a
sub-rectangle whose parity curve 0 cannot fill. Forcing `Wc2` even (`sw = second`) and
`Hc1` even (`sh = first`) is exactly what keeps all four sub-rectangles curve-0-fillable.
(For even n all halves are even or the two-odd case n ≡ 2 mod 4 arises; both are handled —
verified n = 3..40, all sub-blocks valid.)

### Theorem

Curve 4 (Liu3) admits a connected arbitrary-square generalization. The orientation-
independent swap rule `(second, first)` for curve 4, over the kernel curve 0 filled with
its square rule (`sh = first` required; `sw` free), yields a single space-filling
Hamiltonian path on every `n × n` square, and reproduces hilbertplot at `n = 2^k`.

**Mechanism in one line**: curve 4's morphism assignment `(B, A, A, C)` makes the four
Hilbert blocks meet corner-to-corner with parity-free junctions (Lemma 1), so feasibility
reduces to sub-rectangle fillability (Lemma 2), and `(second, first)` is the unique
top-rule giving all four sub-rectangles curve-0-valid parities (Lemma 3).

## Quasi-squares (`|w − h| = 1`)

With the square rule `(second, first)`, quasi-squares are **not** uniformly feasible, but at
every size exactly **8 of 16** `(orientation, rev)` combinations connect. The connecting
orientations always form a domino-class pair — `{A, C}` (the 1×2 tall-domino class) or
`{B, D}` (the 2×1 wide-domino class) — selected by size mod 4:

| aspect | pair `{A, C}` connects | pair `{B, D}` connects |
|--------|------------------------|------------------------|
| wide `w = h+1` | `h ≡ 2, 3 (mod 4)` | `h ≡ 0, 1 (mod 4)` |
| tall `h = w+1` | `w ≡ 0, 1 (mod 4)` | `w ≡ 2, 3 (mod 4)` |

(Verified for sizes 3..40; `B, D` are the transposes of `A, C`, so the tall table is the
wide table with axes swapped.) Interpretation: at the coarsest odd level a quasi-square
behaves like the primitive domino — a tall (1×2) region admits orientations `A, C`, a wide
(2×1) region admits `B, D`. So a connected path always exists, but the orientation must be
chosen by the size class; there is **no** orientation-independent quasi-square rule. This is
a verified-over-range observation (mod-4 residues), not yet a closed proof for all sizes.

## Evidence

Engine: `research/aep.py`. Commands run via `.venv/bin/python`.

- **Partition nodes** — `aep.orientations_used(4)` returns 5 nodes:
  `(4, id)` and `(0, ·)` at the four orientations `{id, maindiag, 180, antidiag}`. All
  quadrant bases of curve 4 are 0; curve 4 occurs only at the top (id).
- **Exhaustive per-node search** — each of the 5 nodes over `{first,second,none}²` (9
  options): total space `9^5 = 59049`. Screened on odd n ∈ {3,5,7,9,11,13,15}, survivors
  full-verified on n = 1..40. **Result: 81 valid assignments.** All 81 share
  `node(4,id) = (second, first)` (forced, unique) and `sh = first` on every curve-0 node
  (forced); the curve-0 `sw` is free (3 choices per node → `3^4 = 81`).
- **Orientation-independent first pass** — single `(sw, sh)` for curve 4 over kernel curve 0
  = `(first,first)`, 9 options, verified n = 1..40: **only `(second, first)`** passes.
- **Necessity** — with curve 0 fixed correctly and only the top rule varied, all 8 non-
  `(second,first)` top rules fail (first bad n = 3 or 5, reason `disconnected`); the n = 5
  failure of `(first,first)` is an internal break of the `3×2 @ C` LR block, **not** a
  junction.
- **Positive verification**:
  - `aep.square_valid(4, const_swap({4:(second,first),0:(first,first)})) = True`
    (includes the 2^k check).
  - Explicit `n = 1..40`: `bad = []`.
  - `2^k` match via `canonical_form` for k = 1,2,3,4: all `True`.
  - Valid on squares under all 8 top-level D4 orientations (n = 1..25).
- **Junction / reduction checks** (n = 3..40): `all junctions adjacent = True`,
  `all sub-blocks internally valid = True`, each block a single contiguous run.

Search-space totals reported: orientation-independent pass = 9; full per-node exhaustive =
`9^5 = 59049` (81 valid).

## Verification

**Adversarial re-check by an independent agent.** Engine `research/aep.py`, `.venv/bin/python`.

### Computational claims — all reproduce exactly (CONFIRMED)

- **Reported rule on squares.** `const_swap({4:(second,first),0:(first,first)})`: `validate(fill(4,·))=="OK"` for **n = 1..40** with `bad = []`; `square_valid(4,·) = True`; `canonical_form` matches hilbertplot for **k = 1,2,3,4**. Reproduced.
- **Full swap-rule space.** `orientations_used(4)` = 5 nodes: `(4,id)` plus curve 0 at `{id, maindiag, 180, antidiag}`. Exhaustively searched all `9^5 = 59049` assignments (each node over `{first,second,none}²`), full-verified survivors on n = 1..40: **exactly 81 valid**. `node(4,id)` is forced to `(second,first)`; every curve-0 node is forced to `sh = first` with `sw` free (3 choices) → `3^4 = 81`. Matches the report precisely.
- **Necessity / failure mode.** At n = 5 with `(first,first)`, the width split is `Wc1=2, Wc2=3`; the LR block is `3×2 @ C` and validates as `disconnected`, while all three junctions remain adjacent. The break is an internal sub-rectangle, not a junction — exactly as the report states.
- **Quasi-squares.** Spot-checked the wide `w=h+1` table over h = 2..13: `{A,C}` connects for `h ≡ 2,3 (mod 4)`, `{B,D}` for `h ≡ 0,1 (mod 4)`. Consistent with the report (a verified-over-range observation, not a proof).

### Flaw found in the proof — Lemma 1 is overstated (needs correction)

Lemma 1 asserts: *"For **any** split sizes, the three internal junctions are 4-adjacent, independent of parity … the joins impose **no** parity constraint."* This is **false as stated**. Junction adjacency requires `Hc1` even, i.e. `sh = first` on the height axis:

- Counterexample **n = 3, top rule `(first, second)`** (so `Hc1 = 1`, odd): the four sub-blocks decompose as `LL=2×1@B (valid), UL=2×2@A (valid), UR=1×2@A (valid), LR=1×1@C (valid)` — **all four are individually valid Hilbert paths** — yet `LL` exits at `(1,0)` and `UL` enters at `(0,1)`: **junction distance 2, disconnected.** So the break is at a junction even though every sub-block is fillable, contradicting the "no parity constraint at junctions" claim.
- Systematic check: junctions are adjacent for all n = 3..40 and all `top_sw`, all curve-0 `sw` **iff `top_sh = first`**; for `top_sh ∈ {second, none}` junctions fail. So `Hc1` even (`sh = first`) is genuinely required for junction adjacency.

**Consequence.** The report's mechanism decomposition — Lemma 1 (junctions parity-free, from morphisms alone) + Lemma 3 (swap's *only* job is sub-rectangle fillability) — mischaracterizes the role of `sh = first`. That component serves **double duty**: it is needed both for junction adjacency (correcting Lemma 1) *and* for sub-rectangle fillability (Lemma 3). The correct Lemma 1 statement is: *"When `Hc1` is even (`sh = first`), the three internal junctions are 4-adjacent for any width split"* — verified n = 3..40 across all width rules. Within the report's actually-verified regime (`sh = first` throughout) the junction conclusion holds, so **the final result and swap rule are unaffected**; only the generality of the lemma is wrong.

### Verdict

**needs-work.** The result — squares FEASIBLE with the orientation-independent rule `(second,first)` over kernel curve 0 (`sh=first` forced, `sw` free), the `81`-valid forcing structure, the n = 1..40 verification, and the `2^k` match — is **fully confirmed computationally** and nothing is refuted. But the derivation is **not sound as written**: Lemma 1's parity-independence claim is false (junction adjacency requires `Hc1` even). Restate Lemma 1 with the `sh = first` hypothesis and the proof is repaired; the already-flagged reliance on an unproven curve-0 rectangle-fillability lemma remains an honest open input.

## Open questions

- A closed-form proof of Lemma 3 (that `(second, first)` keeps *all* four sub-rectangles
  curve-0-fillable for every n) currently rests on the reduction plus the range-verified
  claim that curve 0 fills exactly the arising rectangle parities; it should be closed once
  curve 0's rectangle-fillability theorem (which parities/orientations Hilbert fills) is
  stated as a lemma. Curve 4's part above is complete modulo that curve-0 input.
- The quasi-square mod-4 residue classification is verified to size 40 but not yet proved
  for all sizes; a proof should follow from the domino-primitive parity at the coarsest odd
  split, analogous to Lemma 3.
- General rectangles `w × h` (`|w−h| ≥ 2`) not yet probed.
