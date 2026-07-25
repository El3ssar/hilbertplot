# Curve 30 — Hilbert+Liu3 #13

- **kernels / quadrant rules** (visited order LL, UL, UR, LR; each `(base, morphism, reverse)`):
  - LL: `(0, B=maindiag ((0,1),(1,0)), rev=False)`
  - UL: `(0, A=identity ((1,0),(0,1)), rev=False)`
  - UR: `(0, A=identity ((1,0),(0,1)), rev=False)`
  - LR: `(4, D=antidiag ((0,-1),(-1,0)), rev=False)`

  Curve 30 sits at the top of a clean **kernel tower**: quadrants LL, UL, UR are
  **curve 0 (Hilbert)**, and quadrant LR is **curve 4 (Liu3)**. The three curves differ only
  in their LR quadrant:
  `0.LR = (0, C=180°)` → `4.LR = (0, C=180°)` differs from `0.LR` (Liu3 rotates its LR
  Hilbert 180° instead of anti-diagonally) → `30.LR = (4, D=antidiag)` (curve 30's LR is a
  whole Liu3 block). So the dependency is strictly bottom-up: solve curve 0, then curve 4,
  then curve 30. Curve 30 never appears inside itself except as the top-level node.
- **entry/exit type**: `('corner', 'interior')` — starts at a grid corner, ends in the
  interior (inherited from the curve-4 LR block). As with curve 4, the interior exit does
  **not** obstruct feasibility; endpoint type does not predict feasibility.

## Result

- **squares: FEASIBLE**, with a single **orientation-independent** rule.
- **swap rule** (composite, bottom-up):
  - curve 30 (top-level node): `(sw, sh) = (second, first)`.
  - kernel curve 4: `(sw, sh) = (second, first)` (its own established, unique square rule).
  - kernel curve 0: `sh = first` on the height axis is required; the width rule `sw` is
    **free** (curve 0's established rule `(first, first)` satisfies this; `second`/`none`
    also work).

  The composite `const_swap({30:(second,first), 4:(second,first), 0:(first,first)})` is valid.
- **verified**: valid Hamiltonian path on `n × n` for **n = 1..40** (`bad = []`); matches
  hilbertplot's `2^k` curve (via `canonical_form`) for **k = 1,2,3**: **yes**. Robust to the free
  curve-0 width choice (`sw ∈ {first, second, none}` all pass).
- **quasi-squares** (`|w−h| = 1`): **not** uniformly feasible with the square rule, and —
  unlike curve 4 — **not** governed by a clean mod-4 rule. At each size exactly one domino
  class `{A,C}` (tall 1×2) or `{B,D}` (wide 2×1) connects; the selection is regular for
  `h ≡ 0, 3 (mod 4)` and **sporadic** (binary-recursion dependent) for `h ≡ 1, 2 (mod 4)`.
  See §Quasi-squares.

## Derivation / proof

Write the top-level partition of curve 30 on an `n × n` square at orientation `A` with
`(sw, sh) = (second, first)`. With `d1 = ⌊d/2⌋, d2 = d−d1`, the swap makes the width split
`(Wc1, Wc2)` use rule `second` (make `Wc2` even) and the height split `(Hc1, Hc2)` use rule
`first` (make `Hc1` even). The four sub-boxes (canonical frame) are

```
LL = (0,   0,   Wc1, Hc1) @ B  [curve 0]   UL = (0,   Hc1, Wc1, Hc2) @ A  [curve 0]
UR = (Wc1, Hc1, Wc2, Hc2) @ A  [curve 0]   LR = (Wc1, 0,   Wc2, Hc1) @ D  [curve 4]
```

visited LL → UL → UR → LR.

### Lemma 1 (Junction auto-adjacency)

For **any** split sizes, the three internal junctions are 4-adjacent, independent of parity
and of the swap rule:

- **LL → UL**: LL @ B runs the left column from `(0,0)` up to `(0,Hc1−1)`; UL @ A begins at
  `(0,Hc1)`. Differ by 1 in `y`. Adjacent. ✔
- **UL → UR**: UL @ A ends at `(Wc1−1,Hc1)`; UR @ A begins at `(Wc1,Hc1)`. Differ by 1 in
  `x`. Adjacent. ✔
- **UR → LR**: UR @ A ends at `(Wc−1,Hc1)` (Wc = Wc1+Wc2); LR @ D begins at `(Wc−1,Hc1−1)`.
  Differ by 1 in `y`. Adjacent. ✔

The morphism assignment `(B, A, A, D)` makes consecutive blocks meet at the shared cell-corner
of the internal cross; those corner cells are always unit-adjacent. Verified for n = 3..41 for
**both** the correct rule and a deliberately wrong `(first,first)` rule: *all three junctions
adjacent = True in both cases*. Hence the joins impose **no** parity constraint — this is why
curve 30 is feasible despite its interior global exit, and why any failure is **never** at a
top junction.

### Lemma 2 (Reduction)

Because junctions are always adjacent (Lemma 1) and each block is a single contiguous run
(verified n = 3..41), the full path is a valid Hamiltonian path **iff every sub-block is
itself valid** on its rectangle: LL, UL, UR as curve-0 paths and LR as a curve-4 path. Curve
30's validity reduces to sub-rectangle validity of its two kernels.

### Lemma 3 (The sub-square invariant fixes the swap)

For a square `n`, the even halves of the width and height splits are equal (both are the even
integer nearest `n/2`), and likewise the odd halves. Write `e` = even half, `o` = odd half
(`e + o = n`, `|e − o| = 1`). The rule `(second, first)` forces

```
Wc1 = o, Wc2 = e   (sw = second → Wc2 even)
Hc1 = e, Hc2 = o   (sh = first  → Hc1 even)
```

so the **width split is the reverse of the height split**. Substituting into the boxes:

```
LL = Wc1×Hc1 = o × e   (quasi-square, |Δ|=1)      [curve 0]
UL = Wc1×Hc2 = o × o   = ODD SQUARE               [curve 0]
UR = Wc2×Hc2 = e × o   (quasi-square, |Δ|=1)      [curve 0]
LR = Wc2×Hc1 = e × e   = EVEN SQUARE              [curve 4]
```

The two blocks visited 2nd and 4th (UL, LR) become **exact sub-squares** — an odd curve-0
square and an even curve-4 square — while LL and UR are `|w−h| = 1` quasi-squares. This
recreates the Wu–Chang AEP self-similar structure one level down. Verified for **all**
n = 3..41: UL square (odd when n odd), LR square (even when n odd), LL and UR quasi-squares —
**0 failures**. For even n both halves are equal, so all four boxes are `m × m` squares
(`m = n/2`); the invariant is trivial.

**Two-step forcing (why `(second, first)` is the unique const rule).**

1. `sh = first` is inherited from the kernels. Curve 0's own square rule requires `sh = first`
   (its valid const rules are exactly `{(first,first),(second,first),(none,first)}` — height
   axis forced), and curve 4's unique rule is `(second, first)` — also `sh = first`. The
   Hilbert/Liu3 sub-blocks enter and exit on their **bottom** edge, so the even half must be
   the **low** half for the vertical junctions LL→UL and UR→LR to land at integer parity —
   the "make the entry-corner-side half even" principle. Empirically, with `sw = second`
   fixed, `sh ∈ {first}` passes and `{second, none}` fail (first bad n = 3).
2. Given `sh = first`, `sw = second` is forced by Lemma 3: only `sw = second` makes the width
   split the reverse of the height split, delivering UL and LR as squares (of the correct
   parity for their respective kernels). With `sw = first` or `none`, UL/LR become wrong-parity
   quasi-squares outside the kernels' fillable domain. Empirically, with `sh = first` fixed,
   `sw = second` passes and `sw ∈ {first, none}` fail.

**Necessity is deep, not local.** The wrong rule `(first, first)` keeps all three top
junctions adjacent (Lemma 1) *and* is even valid up to n = 10; it first breaks at **n = 11**,
where the accumulated parity mismatch produces a sub-rectangle the kernel cannot fill. This is
exactly why verification must run past small n (to n = 40), and why the mechanism is the
*recursive sub-square invariant* (Lemma 3), not top-junction adjacency (Lemma 1).

### Theorem

Curve 30 (Hilbert+Liu3 #13) admits a connected arbitrary-square generalization. The
orientation-independent swap rule `(second, first)`, layered over kernel curve 4 with its
rule `(second, first)` and kernel curve 0 with `sh = first` (width free), yields a single
space-filling Hamiltonian path on every `n × n` square and reproduces hilbertplot at `n = 2^k`.

**Mechanism in one line**: the morphisms `(B, A, A, D)` make the three Hilbert blocks and the
Liu3 block meet corner-to-corner with parity-free junctions (Lemma 1), so feasibility reduces
to sub-block fillability (Lemma 2); `(second, first)` is the unique top rule making the
width split the mirror of the height split, which hands UL an odd Hilbert square and LR an even
Liu3 square and LL, UR the two fillable quasi-squares (Lemma 3).

## Quasi-squares (`|w − h| = 1`)

With the square rule `(second, first)`, quasi-squares are **not** uniformly feasible. At every
size the connecting orientations form a single domino class — `{A, C}` (the 1×2 tall-domino
class) or `{B, D}` (the 2×1 wide-domino class) — consistent with the primitive constraint that
a tall `1×2` region admits `A, C` and a wide `2×1` region admits `B, D`. But unlike curve 4,
the **selection is not a clean mod-4 function**:

| aspect | `h ≡ 3 (mod 4)` | `h ≡ 0 (mod 4)` | `h ≡ 1 (mod 4)` | `h ≡ 2 (mod 4)` |
|--------|-----------------|-----------------|-----------------|-----------------|
| wide `w = h+1` | `{A,C}` (regular) | `{B,D}` (regular) | sporadic | sporadic |

(Tall `h = w+1` is the transpose: `w ≡ 3 → {B,D}`, `w ≡ 0 → {A,C}` regular; `w ≡ 1, 2`
sporadic.) Examples of the sporadic classes (wide): `h = 5 → all four`; `h = 9 → {A,C}`;
`h = 13 → {B,D}`; `h = 17 → {A,C}` (all `h ≡ 1`); `h = 6 → {B,D}`; `h = 10 → {A,C}`;
`h = 14 → {B,D}`; `h = 18 → {A,C}` (all `h ≡ 2`). The `h ≡ 1, 2` selection tracks the finer
binary structure of `h`, not its residue mod 4.

The loss of the clean mod-4 law (which curve 4 *does* have) is attributable to curve 30's LR
kernel being a whole **Liu3** block rather than a Hilbert block: at `|w−h| = 1` the two split
axes carry opposite parities, the width split can no longer be the exact mirror of the height
split (Lemma 3 fails), and the LR = curve-4 sub-block — itself only conditionally fillable —
breaks the residue symmetry. So a connected path still exists at every quasi-square size, but
the orientation must be chosen per size and there is **no** orientation-independent quasi-square
rule. This is a verified-over-range observation (sizes 3..40), not a closed proof.

## Evidence

Engine: `research/aep.py`. Commands run via `.venv/bin/python`; scratch scripts under the
session scratchpad.

- **Partition nodes** — `aep.orientations_used(30)` returns **6 nodes**:
  `(30, id)`; `(4, antidiag)`; and `(0, ·)` at the four orientations
  `{id, maindiag, 180, antidiag}`. Distinct kernel curves: `{0, 4, 30}`.
- **Bottom-up const search** (kernels fixed as solved, then search the node above):
  - curve 0, 9 options, n = 1..40: valid set `{(first,first),(second,first),(none,first)}`
    → **`sh = first` forced, `sw` free**.
  - curve 4 over kernel-0, 9 options, n = 1..40: **unique `(second,first)`**.
  - curve 30 over kernels {0:(first,first), 4:(second,first)}, 9 options, n = 1..40:
    **unique `(second,first)`**. Robust to the free curve-0 width: all of
    `sw₀ ∈ {first,second,none}` (with `sh₀ = first`) keep curve 30 valid.
- **Forcing tables** (n = 1..40): with `sh = first` fixed, only `sw = second` passes
  (`first`, `none` fail); with `sw = second` fixed, only `sh = first` passes
  (`second`, `none` fail).
- **Necessity is non-local**: first-invalid-n by rule — `(second,first)`: none (n≤40);
  `(first,first)`: **n = 11**; `(second,second)`: n = 3. All three match hilbertplot at 2^k, so the
  distinguishing test is the odd-square connectivity at larger n.
- **Structural invariant** (n = 3..41): UL is a square (odd when n odd), LR is a square (even
  when n odd), LL and UR are `|w−h| = 1` quasi-squares — **0 failures**.
- **Junction / reduction checks** (n = 3..41): all three top junctions 4-adjacent under the
  correct rule **and** under a wrong `(first,first)` rule (adjacency is parity-free, Lemma 1);
  each block a single contiguous run.
- **Positive verification**:
  - `aep.square_valid(30, const_swap({30:(second,first),4:(second,first),0:(first,first)})) = True`
    (includes the 2^k check for k = 1,2,3).
  - Explicit n = 1..40: `bad = []`; `check_2k=False` also True.

**Search-space accounting.** Feasibility is established by an explicit orientation-independent
witness, so no exhaustive per-orientation sweep is required. Spaces actually explored:
orientation-independent passes = `9 (curve 0) + 9 (curve 4) + 9 (curve 30) = 27` const
configurations. The full per-orientation node space (for reference / any impossibility claim)
is the 6 nodes each over `{first,second,none}²`: `9^6 = 531 441` assignments — **not**
brute-forced, since the const witness already proves feasibility and is a member of it.

## Open questions

- A fully closed proof of Lemma 3 rests on the reduction (Lemma 2) plus the range-verified
  claim that curve 0 fills its arising `o×e`/`o×o` rectangles and curve 4 fills its `e×e`
  square. It closes once the kernels' rectangle-fillability lemmas (Hilbert on `|w−h|≤1`
  parities; Liu3 on even squares) are stated as standalone results — curve 30's argument is
  complete modulo those kernel inputs.
- The quasi-square selection for `h ≡ 1, 2 (mod 4)` is sporadic (binary-recursion dependent);
  a closed description likely requires unfolding the AEP recursion on the curve-4 LR block.
  The `h ≡ 0, 3` classes are clean and should admit a domino-primitive proof analogous to
  curve 4's.
- General rectangles `w × h` with `|w−h| ≥ 2` not yet probed.

## Verification

Adversarial, independent re-check by a second agent. Engine `research/aep.py`, `.venv/bin/python`.
Every computational claim in the report was re-run from scratch; all reproduce exactly.

**Confirmed computationally:**

- **Positive witness (the central claim).** `const_swap({30:(second,first), 4:(second,first),
  0:(first,first)})` gives `validate == "OK"` on every `n × n` for **n = 1..40** (`bad = []`),
  and `square_valid(30, rule, sizes=range(1,41)) == True` (this includes the `2^k` match to
  hilbertplot for k = 1,2,3). Reproduced independently.
- **Global uniqueness of the top rule — stronger than the report's bottom-up search.** I brute-
  forced the *entire* orientation-independent space over the three curves that appear
  (`{0,4,30}`, each of 9 options → `9³ = 729` configs) against n = 1..40. Exactly **3** configs
  are valid, and **all 3 have curve-30 top rule = `(second,first)`** and curve-4 = `(second,first)`;
  they differ only in curve 0's *width* (`sw₀ ∈ {first, second, none}`, `sh₀ = first`). So
  `(second,first)` is the unique curve-30 top rule not merely relative to fixed kernels but
  across the whole const space — this is a stronger result than the report states and it
  supports, rather than weakens, the forcing narrative.
- **Kernel forcing.** curve 0 standalone valid set = `{(first,first),(second,first),(none,first)}`
  (⇒ `sh = first` forced, `sw` free) ✔; curve 4 over kernel-0 = unique `(second,first)` ✔;
  curve 30 robust to `sw₀ ∈ {first,second,none}` ✔.
- **Non-local necessity.** First-invalid-n by curve-30 top rule matches the report exactly:
  `(second,first)` → none (≤40); `(first,first)` → **n = 11**; `(second,second)` → n = 3.
- **Lemma 3 shape invariant.** For all odd n = 3..41 under `(second,first)`: UL is an odd
  square, LR an even square, LL and UR are `|w−h| = 1` quasi-squares — **0 violations**.
- **Quasi-square examples.** Re-tested wide `w = h+1` over all 8 D4 matrices: `h=5`→all four
  classes; `h=9`→{A,C}; `h=13`→{B,D}; `h=6`→{B,D}; `h=10`→{A,C}; `h=14`→{B,D}. All match the
  report's table.

**Scope caveats (not errors — flagged for the paper's rigor standard):**

- The Theorem is phrased "every `n × n` square", but the actual support is *verified over
  n = 1..40* plus a structural reduction (Lemmas 1–3) that is itself **conditional on kernel
  rectangle-fillability lemmas** (curve 0 on `o×e`/`o×o`, curve 4 on `e×e`) which are
  range-verified, not proved for all n. The report honestly flags this in Open Questions; read
  the result as "verified over n = 1..40, structurally reduced to two kernel lemmas", not a
  closed all-n proof.
- Lemma 1's "for any split sizes" is verified for n = 3..41, not proved for all sizes; for the
  correct rule it is in any case subsumed by `validate == "OK"` over n = 1..40.

**Verdict: CONFIRMED.** The computational check passes robustly (independently reproduced,
including a full 729-config sweep the original did not run), and the feasibility derivation is
logically sound as a reduction with its residual dependency transparently disclosed. No
counterexample or logical error was found.
