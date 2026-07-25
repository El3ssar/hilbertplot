# Curve 0 — Hilbert

- **kernels / quadrant rules** (LL, UL, UR, LR, visited in that order):
  | quadrant | base | morphism (matrix) | reverse |
  |----------|------|-------------------|---------|
  | LL | 0 | `((0,1),(1,0))` = main-diagonal transpose **B** | False |
  | UL | 0 | `((1,0),(0,1))` = identity **e** | False |
  | UR | 0 | `((1,0),(0,1))` = identity **e** | False |
  | LR | 0 | `((0,-1),(-1,0))` = anti-diagonal **D** | False |

  Curve 0 is **self-referential**: every quadrant base is `0`. It has **no kernel dependency**
  on other curves, so its swap rule can be solved in isolation (no bottom-up ordering needed).
- **entry/exit type**: `('corner','corner')`. On the `2^k` grid the global path runs
  from corner `(0,0)` to corner `(2^k-1,0)` — both endpoints on the bottom edge.
- **partition nodes** `orientations_used(0)` = exactly the four Wu & Chang orientations
  `{A=e, B=main-diag, C=rot180, D=anti-diag}` (all base 0). These four `(curve,orientation)`
  nodes are the ones that need a swap rule.

## Result

- **squares: FEASIBLE.**
- **swap rule (aep canonical-frame `(sw,sh)`):** the **height split must be `first`
  (make the low height-half `Hc1` even) at every orientation node; the width split `sw`
  is free** (`first`, `second`, or `none`). The simplest valid choice is the
  orientation-independent
  ```
  swap(0, ·) = ("first", "first")
  ```
  (this is the documented rule and reproduces Wu & Chang).
- **verified:** valid Hamiltonian path on `n × n` for **n = 1..40** for all three
  orientation-independent rules `(first,first)`, `(second,first)`, `(none,first)`;
  `(first,first)` re-verified on **n = 1..80**. Matches `hilbertplot` at `2^k` (k=1,2,3): **yes**.
- **full solution set:** exhaustive per-orientation search over `9^4 = 6561` combinations
  returns exactly **81 = 3^4** valid rules — precisely those with `sh = first` at every
  one of the four nodes and `sw ∈ {first,second,none}` free at each. No rule with
  `sh ∈ {second,none}` at any node survives.
- **quasi-squares** `|w−h| = 1`:
  - orientations **A(e), C(rot180)**: connect on **wide** (`w=h+1`) iff `h` odd; on
    **tall** (`h=w+1`) iff `w` even (plus the `1×2` domino base case `w=1`).
  - orientations **B(main-diag), D(anti-diag)**: the transpose — connect on **wide** iff
    `h` even (plus `h=1`); on **tall** iff `w` odd.

> **Note on the "orientation-dependent" phrasing in the brief.** context.md §3 quotes the
> rule as `{A,B}→(first,first), {C,D}→(second,second)`. That is Wu & Chang's *original*
> parametrization ("make the half on the entry-corner side even"), stated in the entry-corner
> frame. In the aep engine's **canonical-frame** `(sw,sh)` parametrization it is a *different*
> object and it **fails** (first failure at `n=5`; verified below). The engine-native answer,
> consistent with context.md §3's second bullet `0:(first,first)`, is `sh=first` at every node.

## Derivation / proof

### Set-up: the partition and its junctions

For a square `n × n` in orientation `e`, `fill` splits width `n → (Wc1,Wc2)` (rule `sw`)
and height `n → (Hc1,Hc2)` (rule `sh`) with `|Wc1−Wc2|≤1`, `|Hc1−Hc2|≤1`, and lays down
four sub-blocks, each itself curve 0 in a rotated frame:

| block | region | orientation | required corner path |
|-------|--------|-------------|----------------------|
| LL | `Wc1 × Hc1` | **B** (transpose) | `(0,0) → (0, Hc1−1)` (up the left edge) |
| UL | `Wc1 × Hc2` | **e** | `(0,Hc1) → (Wc1−1, Hc1)` (bottom corners) |
| UR | `Wc2 × Hc2` | **e** | `(Wc1,Hc1) → (Wc−1, Hc1)` (bottom corners) |
| LR | `Wc2 × Hc1` | **D** (anti-diag) | `(Wc−1,Hc1−1) → (Wc−1, 0)` (down the right edge) |

**Junction identities (unconditional).** Given each block realizes its corner path above,
the three internal junctions are automatically 4-adjacent, *independent of any parity*:
```
LL exit (0, Hc1−1)   →  UL entry (0, Hc1)     vertical, dist 1
UL exit (Wc1−1, Hc1) →  UR entry (Wc1, Hc1)   horizontal, dist 1
UR exit (Wc−1, Hc1)  →  LR entry (Wc−1, Hc1−1) vertical, dist 1
```
and the global endpoints are LL-entry `(0,0)` and LR-exit `(Wc−1,0)` — the corner→corner
invariant, reproduced. **So the whole path is valid iff each of the four sub-blocks can
realize its prescribed corner-to-corner path.** The feasibility question reduces to a
parity condition on those corner paths.

### Lemma (checkerboard / coloring obstruction)

Color cell `(x,y)` by `(x+y) mod 2`. A Hamiltonian path on a `W×H` grid (`N=WH` cells)
visits colors alternately, so **its two endpoints have equal color iff `N` is odd.**
Applying this to each block's endpoint pair:

- **Orientation e, bottom-corner path `(0,0)→(W−1,0)`.** Endpoint colors `0` and `(W−1)`;
  equal iff `W` odd. Path can exist ⟺ `[W odd ⟹ N=WH odd] ⟺ [W odd ⟹ H odd]`
  ⟺ **`W even OR H odd`** (impossible exactly when `W` odd and `H` even).
- **Orientation B, left-edge path `(0,0)→(0,H−1)`** (transpose of the above). Endpoint
  colors `0` and `(H−1)`; equal iff `H` odd. Path can exist ⟺ **`H even OR W odd`**
  (impossible exactly when `H` odd and `W` even).
- **Orientation D, right-edge path** — same parity condition as B by the anti-diagonal
  symmetry: **`H even OR W odd`**.

*Computational confirmation of the lemma.* For orientation `e` over the entire reachable
box family (squares and quasi-squares, `w ≤ 49`), AEP-validity equals the predicted
`w even OR h odd` with **zero mismatches** (evidence below). This shows the parity
condition is not only necessary but is *exactly achieved* by the AEP construction.

### Why `sh = first`, and why `sw` is free

Apply the lemma to the four blocks of a square `n×n`:

- **LL (orient B, `Wc1×Hc1`)** needs `Hc1 even OR Wc1 odd`.
- **LR (orient D, `Wc2×Hc1`)** needs `Hc1 even OR Wc2 odd`.
- **UL (orient e, `Wc1×Hc2`)** needs `Wc1 even OR Hc2 odd`.
- **UR (orient e, `Wc2×Hc2`)** needs `Wc2 even OR Hc2 odd`.

Because the width rule `sw` is a *free knob* — it may make `Wc1` (or `Wc2`) even — the LL
and LR conditions can only be guaranteed for **all** `sw` by taking the other disjunct:
**`Hc1` even**. This is exactly `sh = first`. Conversely, if `Hc1` is odd (`sh=second`,
or `sh=none` at sizes where `⌊n/2⌋` is odd, e.g. `n=3`), then whenever `sw` makes `Wc1`
even the LL block is parity-**impossible** — matching the observed first failure at `n=3`
(`sh=second`, `sw=first`: `Hc1=1`, `Wc1=2`; LL is a `2×1` strip that under transpose exits
at `(1,0)` instead of `(0,0)`, giving junction `LL→UL` distance `2`).

With `sh = first` the upper blocks are automatically fine, which is *why the width is free*:

- **`n` odd.** The halves `{⌊n/2⌋, ⌈n/2⌉}` are consecutive integers — one even, one odd.
  `sh=first` selects the **even** one as `Hc1`, forcing `Hc2` **odd**. Then LL, LR satisfy
  `Hc1 even`; UL, UR satisfy `Hc2 odd`. **All four conditions hold for every `sw`.** ∎
- **`n` even.** Both halves equal `n/2` (the swap cannot change equal halves), for both
  axes and every `sw`. If `n ≡ 0 (mod 4)`: `Hc1=n/2` even ⟹ LL, LR ok; `Wc*` even ⟹ UL,
  UR ok. If `n ≡ 2 (mod 4)`: `Hc1=Hc2=n/2` odd and `Wc1=Wc2=n/2` odd, so LL, LR satisfy
  `Wc odd` and UL, UR satisfy `Hc2 odd`. **All four hold for every `sw`.** ∎

Hence `sh=first` (any `sw`) yields a valid path on every square, and the induction closes:
each sub-block is itself a square or quasi-square in `{e,B,D}` whose corner path is
guaranteed by the same lemma, so the corner→corner invariant is preserved at every level.
This proves validity **for all `n`** (not merely the tested range), matching the exhaustive
`n=1..40` / `n=1..80` verification.

### Quasi-squares and the domino primitive

The top-level box `w×h` is itself governed by the lemma. For orientation `A=e`, `w×h` is
valid iff `w even OR h odd`:
- **wide** `w=h+1`: `w even OR h odd ⟺ h odd` (since `w=h+1`). → connects iff `h` odd.
- **tall** `h=w+1`: `w even OR h odd ⟺ w even`. → connects iff `w` even.

`C=rot180` shares e's parity class (central symmetry preserves the coloring parity), and
`B,D` are the transposes, swapping the roles of `w,h`. This is precisely the
**`1×2` (A,C) / `2×1` (B,D) primitive constraint**: A and C bottom out (in a thin box) on
the vertical `1×2` domino and so accept tall boxes of even width / wide boxes of odd height;
B and D bottom out on the horizontal `2×1` domino and accept the transposed set. The lone
exceptions `w=1` (A,C) and `h=1` (B,D) are the raw domino base cases, which are Hamiltonian
by construction even though they violate the corner-exit invariant.

## Evidence

Commands run from `research/` with `../.venv/bin/python` (`import aep`).

**Structure.**
```
RULES[0]: LL base0 morph((0,1),(1,0)) rev F | UL base0 morph e rev F
          UR base0 morph e rev F | LR base0 morph((0,-1),(-1,0)) rev F
entry_exit(0) = ('corner','corner')
orientations_used(0) = {(0,e),(0,main-diag),(0,rot180),(0,anti-diag)}   # 4 nodes, all base 0
```

**Orientation-independent search (9 options), validity over n=1..40:**
```
(first ,first )=True   (first ,second)=False(n=3)  (first ,none  )=False(n=3)
(second,first )=True   (second,second)=False(n=3)  (second,none  )=False(n=3)
(none  ,first )=True   (none  ,second)=False(n=3)  (none  ,none  )=False(n=3)
hits = (first,first), (second,first), (none,first)     # all have sh=first
square_valid(1..13, check_2k=True) = True for all three hits
(first,first) valid n=1..80 = True
```

**Exhaustive per-orientation search, space = 9^4 = 6561:**
```
survivors over n=1..21 : 81      survivors over n=1..40 : 81   (= 3^4)
per node A,B,C,D:  sw ∈ {first,none,second}   sh ∈ {first}   (sh=first forced everywhere)
```

**Coloring-lemma confirmation (orientation e):**
```
AEP-validity vs predicted (w even OR h odd), square+quasi-square, w<=49: mismatches = []
exit corner always (W-1,0); disconnected exactly when W odd AND H even, e.g. 3x2,3x4,5x4,5x6,7x6
```

**Junction trace at n=3** (`sw=first`):
```
sh=second (Hc1=1 odd): LL 2x1/B exit(1,0) -> UL entry(0,1)  dist 2  -> DISCONNECTED
sh=first  (Hc1=2 even): LL 2x2/B exit(0,1) -> UL entry(0,2)  dist 1;
                        all junctions dist 1 -> OK
```

**Wu & Chang entry-corner rule in aep canonical frame** (`{A,B}→(f,f),{C,D}→(s,s)`):
`fails at n = 5,6,7,9,10,...` — confirming it is a distinct object from the engine's `(sw,sh)`.

**Quasi-square connectivity, top-level orientation, h (or w) = 1..12:**
```
A,C: wide connects h∈{1,3,5,7,9,11} (h odd);  tall connects w∈{1,2,4,6,8,10,12} (w even + domino)
B,D: wide connects h∈{1,2,4,6,8,10,12} (h even + domino);  tall connects w∈{1,3,5,7,9,11} (w odd)
```

## Open questions

- **General rectangles `w×h`.** The coloring lemma gives the necessary parity condition
  `w even OR h odd` for the corner→corner path in orientation `e`; but for `|w−h|>1` the
  reachable sub-boxes leave the square/quasi-square family and the AEP recursion is not
  guaranteed (thin boxes such as `1×k`, `k≥3`, already fail). A separate swap policy keyed
  on aspect ratio would be needed; not required for the square generalization.
- **Uniqueness framing.** The 81-element solution set is exactly `{sh=first}⁴ × {sw free}⁴`.
  It would be cleaner to prove directly (rather than by exhaustion) that `sh=first` at every
  node is *necessary*, via the LL/LR parity obstruction under an adversarial choice of `sw`;
  the argument above sketches this but a fully formal "for all n" necessity proof of
  `sh=first` (matching the empirical necessity) is left as a tightening.

## Verification

**Verdict: CONFIRMED** (adversarial re-check, independent engine runs). The FEASIBLE result,
the swap rule (`sh=first` at every node, `sw` free), and every computational claim reproduce
exactly. The proof's core parity argument is sound; the gaps found are minor write-up
tightenings, not errors, and do not affect the result.

**What I re-ran (all from `research/`, `../.venv/bin/python`, `import aep`):**

1. *Orientation-independent rules, squares n=1..40.* Reproduced the report's table exactly:
   `(first,first)`, `(second,first)`, `(none,first)` are valid on **every** `n×n`, `n=1..40`;
   all six rules with `sh∈{second,none}` **fail at n=3**. `square_valid(0, (first,first),
   sizes=1..40, check_2k=True) = True` (so it matches hilbertplot at `2^k`, k=1,2,3). **Confirms the
   swap rule and the hilbertplot match.**
2. *Exhaustive per-orientation search, full rule space.* `orientations_used(0)` = 4 nodes
   `{e, o(main-diag), f(rot180), a(anti-diag)}`. Enumerated all `9^4 = 6561` assignments of
   `(sw,sh)∈{first,second,none}²` to the four nodes and validated each on `n=1..40`: exactly
   **81 survivors**, **every** survivor has `sh=first` at all four nodes, and each node
   independently ranges over `sw∈{first,none,second}`. So the solution set is precisely
   `{sh=first}⁴ × {sw free}⁴ = 3^4`. **Confirms the 81-survivor claim and that no
   `sh∈{second,none}` rule survives** — there is no refuting rule.
3. *Induction family-closure (a claim the "for all n" proof depends on).* Instrumented the
   recursion to log every `(w,h)` box and orientation reached while drawing squares `n=1..40`:
   **zero boxes with `|w−h|≥2`** (the recursion never leaves the square/quasi-square family),
   and the orientations reached are exactly `{e,o,f,a}`. This corroborates the inductive step.
4. *Coloring lemma (orientation e).* Validity vs. predicted `(w even OR h odd)` over
   `|w−h|≤1`, `w≤49`: **one mismatch, `(w,h)=(1,2)`** — the tall `1×2` domino, which is a valid
   Hamiltonian path yet the parity formula flags it invalid. This is the domino base-case the
   report already carves out in the quasi-square section; the Evidence block's
   "`mismatches = []`" evidently used a narrower box set (the listed disconnected examples are
   all wide `w>h`). Immaterial to the square result (a `1×1`/`2×2` is never a `1×2`), but the
   Evidence line is a slight overstatement.
5. *Quasi-squares.* Reproduced the connectivity table **exactly**: A,C(=`e,f`) connect wide
   iff `h` odd and tall iff `w` even (+`w=1` domino); B,D(=`o,a`) are the transpose. And the
   Wu & Chang entry-corner rule `{A,B}→(f,f),{C,D}→(s,s)` in the canonical frame **first fails
   at n=5**, confirming it is a distinct object.

**Proof scrutiny.** The reduction to four block corner-paths via the unconditional junction
identities is correct, and I independently reproduced the parity case analysis (n odd: `sh=first`
forces `Hc1` even, `Hc2` odd → all four block conditions hold for any `sw`; n≡0 mod 4 and
n≡2 mod 4 likewise). Two rigor caveats, both minor and non-fatal:
- The Derivation writes the block table only for orientation `e` and extends to `o,f,a`
  tersely ("by symmetry", "shares e's parity class"). The coloring is genuinely D4-covariant so
  the extension is valid, but a fully formal "for all n" proof would spell out the block tables
  per orientation (rot180 `f` does occur at depth, per run 3).
- Sufficiency of the parity condition (that AEP *realizes* the corner path when parity allows)
  is carried by the induction's base cases + junction identities; the domino base cases'
  corner-exit behavior in each orientation is not fully written out. Since square validity holds
  with zero failures on `n=1..40`, this is a write-up gap, not a defect.

None of these overturn the result. No counterexample exists on `n=1..40`; the full `9^4` rule
space was searched and yields exactly the reported 81 rules. **Verified over n=1..40** (validity
+ exhaustive search); **"for all n"** is a well-structured induction, corroborated on the tested
range and by family-closure, with the terse-symmetry and domino-base-case details noted above as
tightenings.
