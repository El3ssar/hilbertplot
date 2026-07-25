# Curve 28 — Hilbert+Liu3 #11

- **kernels / quadrant rules** (visited order LL, UL, UR, LR; each `(base, morphism, reverse)`):
  | quadrant | base | morphism `M` | reverse |
  |----------|------|--------------|---------|
  | LL | 0 (Hilbert) | `f = ((-1,0),(0,-1))` = **rot180** | False |
  | UL | 0 (Hilbert) | `e = ((1,0),(0,1))` = **identity** | False |
  | UR | 0 (Hilbert) | `e = ((1,0),(0,1))` = **identity** | False |
  | LR | **4 (Liu3)** | `a = ((0,-1),(-1,0))` = **anti-diagonal reflection** | False |

  Three quadrants recurse into **kernel curve 0 (Hilbert)**; the LR quadrant recurses into
  **kernel curve 4 (Liu3)**, whose own four quadrants are all curve 0. Kernel dependency
  chain `28 → {0, 4}`, `4 → {0}`, solvable **bottom-up**. Curve 28 never appears inside
  itself; it occurs only as the top-level node. This is the same kernel skeleton as curve 24
  (`{0,0,0,4}`), but with a **different morphism assignment** `(f,e,e,a)` instead of curve
  24's `(m,g,x,x)` — and that difference is exactly what makes curve 28 **infeasible** where
  curve 24 is feasible.
- **entry/exit type:** `entry_exit(28) = ('interior','interior')` — both global endpoints in
  the interior.
- **partition nodes** (`orientations_used(28)`), the `(curve, orientation)` pairs that need a
  swap rule — exactly **6 nodes**, a closed set (stable over `sizes = 3..41`):
  - `(28, e)` — curve 28 at identity (the only curve-28 node);
  - `(4, a)` — curve 4 at anti-diagonal (the only curve-4 node, the LR quadrant);
  - `(0, e)`, `(0, f)`, `(0, o)`, `(0, a)` — curve 0 at identity / rot180 / main-diag / anti-diag.
  At the top level LL uses `(0,f)`, UL and UR **share** `(0,e)`; `(0,o)` and `(0,a)` appear
  only deeper inside the LR curve-4 block.

## Result

- **squares: INFEASIBLE.** No swap rule — orientation-independent **or** per-orientation over
  the full node set — makes `fill(28, ·)` a connected Hamiltonian path on every `n × n`.
- **swap rule:** none exists. The obstruction is a **forced unfillable sub-block** (below).
- **verified:**
  - Orientation-independent single `(sw,sh)` (9 options, kernels at their own square rules):
    **0 survivors** (n = 1..40).
  - Full per-node exhaustive over all **6 nodes**, each over `{first,second,none}²`: search
    space `9^6 = 531441`; screened on odd n ∈ {3,5,7,9,11,13,15}: **0 survivors**.
  - **Sharpest obstruction — n = 13 is _individually_ infeasible**: exhausting the entire
    `9^6 = 531441` rule space, **no** assignment yields a valid `13 × 13` path (full
    exhaustion, 273 s). Hence infeasibility is not merely "no single rule for all n" — a
    specific square admits **no** rule at all.
  - Individually-feasible squares (some rule works for that n alone): n = 3, 5, 7, 9, 11.
    Individually-**infeasible** squares verified in range: **n = 13, 19, 27, 29, 35, 37**
    (and 13 fully brute-forced; the rest via the exact reduction below, which matches the
    brute force for all n ≤ 13).
  - `matches hilbertplot at 2^k`: **yes** (k = 1,2,3,4) — at powers of two the partition is exactly
    even, the swap is inert, and the recursion reduces to hilbertplot's; infeasibility is purely an
    **odd-size** phenomenon.
- **quasi-squares** (`|w−h| = 1`): **FEASIBLE**. At every quasi-square size exactly **4 of 8**
  orientations connect, forming one full D4 transpose-coset, selected by size mod 4 (see
  §Quasi-squares). This is a sharp contrast: curve 28 fills all quasi-squares but not all
  squares.

## Derivation / proof

Work in the canonical top-level frame (`M = e`, no transpose, `Wc = Hc = n`). For odd
`n = 2s+1` the approximately-even split gives halves `{n//2, n−n//2} = {s, s+1}`, which have
**opposite parity**; the swap only chooses *which* half is even, i.e. it only reorders the
two halves. Writing `{Wc1,Wc2} = {s,s+1}` and `{Hc1,Hc2} = {s,s+1}`, the four sub-boxes
visited LL → UL → UR → LR are

```
LL = (0,   0,   Wc1, Hc1) @ f   (Hilbert)
UL = (0,   Hc1, Wc1, Hc2) @ e   (Hilbert)
UR = (Wc1, Hc1, Wc2, Hc2) @ e   (Hilbert)
LR = (Wc1, 0,   Wc2, Hc1) @ a   (CURVE 4)
```

### Lemma 1 (Junction auto-adjacency — joins are parity-free)

For every split the three internal junctions LL→UL, UL→UR, UR→LR are 4-adjacent, independent
of parity. Verified for odd n = 5..41 under the natural rule: `all junctions adjacent = True`.
So, exactly as for curves 4 and 24, the morphism assignment makes consecutive blocks meet at
the internal cross with unit-adjacent corner cells, and the joins impose **no** constraint.
Feasibility therefore reduces entirely to the four sub-blocks being internally fillable.

### Lemma 2 (The four block shapes are a fixed multiset; the swap only permutes them)

Because `{Wc1,Wc2} = {s,s+1}` and `{Hc1,Hc2} = {s,s+1}`, the four blocks
`(Wc1,Hc1),(Wc1,Hc2),(Wc2,Hc2),(Wc2,Hc1)` realize **all four** width×height combinations of
`{s,s+1}²`. Thus at every odd n the block-shape multiset is **always**

```
{ s×s ,  s×(s+1) ,  (s+1)×s ,  (s+1)×(s+1) }
```

— two squares and the two "mixed" near-squares — and the swap rule can only change *which
block* carries which shape, never the multiset. In particular the shape `(s+1)×s` and the
shape `s×(s+1)` **each appear exactly once**, no matter the swap.

### Lemma 3 (Hilbert kernel fills a near-square only with even width)

Curve 0 (at orientations `e` and `f`, which give identical fillability) on a near-square
`w × h`, `|w−h| ≤ 1`, over **all** its own swap rules:
- `w × w` (square): fillable, always;
- `w × (w±1)`: fillable **iff `w` is even** (for `w ≥ 2`), with only the sporadic exceptions
  `w = 3, 11` for the `w×(w−1)` shape.

(Verified `best_fill`, full kernel freedom, w,h ≤ 19; `@e` and `@f` agree everywhere.)

### Lemma 4 (The odd-width mixed shape `M(s)` — the culprit)

Of the two mixed shapes, exactly one has **odd width**:
`M(s) = (s+1)×s` when `s` is even (width `s+1` odd), and `M(s) = s×(s+1)` when `s` is odd
(width `s` odd). By Lemma 3, `M(s)` is **not curve-0-fillable** (odd width; and at the
infeasible `s` below, `s+1 ∉ {3,11}`, so no sporadic rescue). The only block that carries a
**non**-Hilbert kernel is LR (curve 4 at `a`). Therefore:

> A valid `n × n` path requires `M(s)` to sit on the LR block **and** curve 4 at `a` to fill
> `M(s)`; on any of the three Hilbert blocks `M(s)` is unfillable.

Equivalently, **curve 28 on `(2s+1)×(2s+1)` is feasible for some swap rule ⟺ curve 4@`a`
fills `M(s)`.** (This exact reduction matches the full-`9^6` brute force for all n ≤ 13:
feasible n = 3,5,7,9,11 ↔ curve 4 fills M(s); infeasible n = 13 ↔ curve 4 does not.)

### Theorem (Impossibility)

Curve 28 does **not** admit a connected arbitrary-square generalization. Concretely, take
`n = 13` (`s = 6`, even). The forced mixed shape is `M(6) = 7 × 6`. Then:
- `7 × 6 @ curve0/e` : **unfillable** (odd width 7) — verified;
- `7 × 6 @ curve0/f` : **unfillable** — verified;
- `7 × 6 @ curve4/a` : **unfillable** (curve 4 fills odd×odd squares and some near-squares,
  but not `7×6`) — verified with full curve-4 rule freedom.

By Lemma 2 the shape `7×6` occupies exactly one of the four blocks; by Lemma 1 the block must
be internally filled; but whichever of the four positions (three Hilbert, one curve-4) it
lands in, that block is unfillable. Hence **no** swap rule yields a valid `13×13` path —
confirmed independently by exhausting the entire `9^6 = 531441` rule space (0 valid).
A single infeasible square suffices: curve 28 is **INFEASIBLE** for squares.

**Mechanism in one line.** Curve 28 shares curve 24's kernel skeleton `{0,0,0,4}` but its
morphism assignment `(f,e,e,a)` forces the LR curve-4 quadrant to be an odd-width **near-square
rectangle** `M(s)` rather than the odd×odd **square** that curve 24's `(m,g,x,x)` produces;
curve 4 fills squares but not these rectangles, and no Hilbert block can absorb an odd-width
near-square either, so the shape has nowhere to go.

### Recurrence of the obstruction

The infeasible sizes are exactly the odd `n = 2s+1` for which curve 4@`a` cannot fill `M(s)`.
Verified over `s = 1..20`: curve 4 fails at `s = 6, 9, 13, 14, 17, 18`, i.e.
`n = 13, 19, 27, 29, 35, 37`. These recur throughout the tested range; the pattern is
inherited from curve 4's **irregular rectangle fillability** (curve 4 generalizes to squares
only). That infinitely many infeasible n exist is therefore **verified over n ≤ 41**, not
proved in closed form — but a *single* infeasible n (n = 13) already proves the theorem.

## Quasi-squares (`|w − h| = 1`)

Unlike squares, quasi-squares are **feasible**: at every size a connected path exists. With
the natural rule, exactly **4 of 8** top-level orientations connect at each size, always a
complete D4 transpose-coset — the non-transposing class `{e,f,m,y}` or the transposing class
`{a,g,o,x}` — selected by size mod 4:

| aspect | `{e,f,m,y}` connects | `{a,g,o,x}` connects |
|--------|----------------------|----------------------|
| wide `w = h+1` | `h ≡ 2, 3 (mod 4)` | `h ≡ 0, 1 (mod 4)` |
| tall `h = w+1` | `w ≡ 0, 1 (mod 4)` | `w ≡ 2, 3 (mod 4)` |

(Verified for sizes up to 20; the tall table is the wide table with axes swapped, since
`{a,g,o,x}` are the transposes of `{e,f,m,y}`.) The two connecting classes are exactly the
domino-primitive classes the AEP recursion bottoms out on: a `1×2` (tall-domino) region admits
`{e,f,m,y}`, a `2×1` (wide-domino) region admits `{a,g,o,x}`. At `|w−h| = 1` the aspect is
*not* square, so the recursion never forces the fatal odd-width near-square onto the curve-4
quadrant — a connected path always exists, with the orientation chosen by size class. There is
no orientation-independent quasi-square rule. This is a **verified-over-range** (mod-4) result.

## Evidence

Engine `research/aep.py`; scratch scripts under the session scratchpad, run via `.venv/bin/python`.

**Partition nodes** — `orientations_used(28)` = 6 nodes
`{(28,e),(4,a),(0,e),(0,f),(0,o),(0,a)}`, closed over sizes 3..41.

**Search passes (kernels 0:(first,first), 4:(second,first) where fixed):**
```
Pass 1  orientation-independent single (sw,sh) for node 28, 9 options, n=1..40:
        survivors = []   (28:(first,first) survives longest, first bad n = 11)
Pass 2  full per-node exhaustive, 6 nodes × {first,second,none}^2 = 9^6 = 531441,
        screened odd n∈{3,5,7,9,11,13,15}:  survivors = 0
```

**Individual-n feasibility over the full 9^6 space:**
```
n= 3,5,7,9,11 : individually feasible = True
n=13          : individually feasible = FALSE   (full 9^6 exhaustion, 273 s)  <-- proof
```

**n = 13 pinpoint (forced shape 7×6, full kernel freedom):**
```
7x6 @ curve0/e = False    7x6 @ curve0/f = False    7x6 @ curve4/a = False
(6x7 @ curve0/e = True,    6x7 @ curve4/a = True  — the *other* mixed shape is fine)
```

**Exact reduction  curve28(2s+1) feasible ⇔ curve4@a fills M(s)** (best_fill, s=1..20):
```
s : 1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20
n :  3  5  7  9 11 13 15 17 19 21 23 25 27 29 31 33 35 37 39 41
c4:  T  T  T  T  T  F  T  T  F  T  T  T  F  F  T  T  F  F  T  T
  INFEASIBLE squares: n = 13, 19, 27, 29, 35, 37   (s = 6,9,13,14,17,18)
```

**Junctions / 2^k:**
```
junctions adjacent, odd n = 5..41 (natural rule): True
2^k match (k=1..4): valid=OK, matches hilbertplot=True  (even sizes fill; obstruction is odd-only)
```

**Curve-0 near-square fillability law (full freedom, w,h ≤ 19), @e ≡ @f:**
square always fillable; `w×(w±1)` fillable iff `w` even (sporadic odd exceptions w=3,11 for
`w×(w−1)` only) — this is Lemma 3.

Search-space totals reported: orientation-independent pass = 9; full per-node exhaustive =
`9^6 = 531441` (0 valid); plus a complete `9^6` exhaustion at the single size n = 13 (0 valid).

## Open questions

- **All-n impossibility.** The theorem is proved (n = 13 is individually infeasible). The
  *density* of infeasible squares rests on curve 4's rectangle-fillability being irregular and
  failing infinitely often, which is here **verified to n ≤ 41**, not closed-form. Closing it
  requires a lemma on exactly which near-square rectangles curve 4@`a` fills — the same open
  input flagged in `curve_4.md`.
- **Structural theorem candidate.** Curves 24 and 28 have identical kernel skeleton
  `{0,0,0,4}` but opposite verdicts. The discriminant is the morphism assignment's effect on
  the LR (curve-4) quadrant's shape at odd n: curve 24's `(m,g,x,x)` makes LR an odd×odd
  **square** (curve-4-fillable ⇒ feasible); curve 28's `(f,e,e,a)` makes LR an odd-width
  **near-square rectangle** (curve-4-**un**fillable for infinitely many sizes ⇒ infeasible).
  Conjecture: *a `{0,0,0,4}`-kernel curve generalizes to squares iff its morphisms send the
  curve-4 quadrant to an odd×odd square at every odd split.*
- **Quasi-square mod-4 law** verified to size 20, not yet proved for all sizes.
- **General rectangles** `|w−h| ≥ 2` not probed.

## Verification

**Verdict: CONFIRMED.** An independent, skeptical re-run of the engine reproduces every
load-bearing claim; a deliberate attempt to *refute* the impossibility (full brute-force search
for any working rule at n = 13) failed. Commands run via `.venv/bin/python`, engine
`research/aep.py` unchanged.

**Structural facts reproduced.** `orientations_used(28)` = 6 nodes
`{(28,e),(4,a),(0,e),(0,f),(0,o),(0,a)}`; `RULES[28]` = LL `(0,f)`, UL `(0,e)`, UR `(0,e)`,
LR `(4,a)`; `entry_exit(28) = ('interior','interior')`. All match the report.

**Refutation attempt — the crux (n = 13), FAILED.** I ran the full `9^6 = 531441` per-node
exhaustion over the 6 nodes, each `{first,second,none}²`, on the `13×13` square:
`n=13: NONE (274.1 s)` — no assignment yields `validate == OK`. This independently reproduces
the report's 273 s result and directly proves n = 13 admits no rule. A single infeasible
square suffices, so **squares are INFEASIBLE** — confirmed.

**Independent second proof of n = 13 (block necessity, cleaner than the report's).** For each
of the 9 top-level `(sw,sh)` splits I computed the four absolute block shapes and, granting each
block its *full independent* internal swap freedom, tested whether it is a Hamiltonian path.
Every split places the odd-width shape `7×6` on exactly one block, and `7×6` is unfillable in
all three positions it can occupy: `7×6 @ curve0/e = False`, `@ curve0/f = False`,
`@ curve4/a = False` (while the mirror shape `6×7` is fillable at both `curve0/e` and
`curve4/a`). Result: `ANY top-split with all-four-fillable = False`. Note this direction needs
only that an overall Hamiltonian path restricts to a Hamiltonian path on each contiguous block —
it does **not** rely on Lemma 1 (join adjacency), and it *over*-grants freedom (the real per-node
model forces the shared node `(0,e)` to use one swap across the UL/UR blocks, a strictly tighter
constraint). Since infeasibility survives even the looser check, the report's argument is sound
*a fortiori*; the shared-node subtlety only strengthens it.

**Infeasible set reproduced exactly.** The block-necessity test over odd `n = 3..41` flags
infeasible at **n = 13, 19, 27, 29, 35, 37** and nowhere else — identical to the report's set.
The reduction "curve28(2s+1) feasible ⇔ curve4@`a` fills `M(s)`" was reproduced independently for
s = 1..12 (curve4@`a` fails exactly at s = 6, 9 in that range; `M(6)=7×6`, `M(9)=9×10`), matching
the report's table.

**Other claims reproduced.** Orientation-independent single `(sw,sh)` pass, n = 1..40:
**0 survivors**; `(first,first)` survives longest with first failure at n = 11 — matches.
Individually feasible n = 3,5,7,9,11: confirmed. `matches hilbertplot at 2^k` (k = 1..4):
`validate = OK`, `matches_hilbertplot = True` — confirmed. Quasi-squares: exactly **4 of 8**
orientations connect at each tested size, forming a D4 transpose-coset selected by size mod 4
(`4×3→{e,f,m,y}`, `6×5→{a,g,o,x}`, `8×7→{e,f,m,y}`, `3×4→{a,g,o,x}`, `5×6→{e,f,m,y}`) — matches
the mod-4 table.

**Gaps / caveats (none fatal).** (i) The all-n impossibility remains verified-over-range
(n ≤ 41), not closed-form; the report states this honestly and the theorem needs only the single
proved size n = 13. (ii) Scope: the search space is the problem's defined swap alphabet
`{first,second,none}²` per node; infeasibility is a statement within that model, which is the
correct object of study. No error found.
