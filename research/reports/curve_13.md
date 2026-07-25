# Curve 13 — Liu2+Liu4 #2

- **kernels / quadrant rules** (visited order LL, UL, UR, LR):
  | quadrant | base | morphism `M` | reverse |
  |----------|------|--------------|---------|
  | LL | 3 (Liu2) | `((0,-1),(1,0))` = **rot90** | False |
  | UL | 5 (Liu4) | `((0,-1),(1,0))` = **rot90** | False |
  | UR | 5 (Liu4) | `((0,1),(1,0))`  = **transpose** | **True** |
  | LR | 3 (Liu2) | `((0,1),(-1,0))` = **rot270** | False |

  Curve 13 is a **composite** kernel: it recurses into **curve 3 (Liu2)** and
  **curve 5 (Liu4)**, each of which in turn recurses into **curve 0 (Hilbert)**. The
  dependency DAG is `13 → {3, 5} → 0`, so the problem is solved **bottom-up**: the swap
  rules of the kernels 0, 3, 5 are fixed first (established in `curve_0.md`,
  `curve_3.md`, `curve_5.md`), then curve 13 is analysed on top. Curve 13 itself appears
  in the recursion **only at the identity orientation** (it is never re-oriented by its
  own rules); all re-orientation happens on the kernels.

- **entry/exit type:** `entry_exit(13) = ('edge','edge')`. Like its parents 3 and 5 it is
  an edge→edge curve.

- **partition nodes** — the union of `(curve, orientation)` pairs that a swap rule must
  cover. Because the swap choice itself changes which orientations get recursed into, the
  true node universe is larger than `orientations_used` (which uses a single fixed split).
  Over `n = 3..39` the reachable nodes are: **curve 13** (1 orientation, identity),
  **curve 3** (2 orientations), **curve 5** (2 orientations), **curve 0** (8 orientations).

## Result

- **squares: INFEASIBLE.** No swap rule — orientation-independent **or** fully
  per-orientation — makes `fill(13,·)` a valid Hamiltonian path on every `n × n` square.
  The minimal witness is **n = 5**: the `5 × 5` square admits **no** valid fill under
  **any** swap assignment whatsoever.

- **swap rule:** none exists.

- **verified:**
  - Orientation-independent `(sw,sh)` for curve 13 (kernels at their established rules):
    all **9** options fail on `n = 1..40`.
  - Per-**index** rule for all four curves `{0,3,5,13}`: exhaustive **9⁴ = 6561**
    combinations, **0 valid** on `n = 1..40`.
  - Full **per-orientation** rule over the complete `n = 5` node universe (5 nodes):
    exhaustive **9⁵ = 59049** assignments, **0 valid**. Since a global swap function
    `swap(index,M)` assigns a fixed `(sw,sh)` to each node independent of region size,
    this enumerates *every* restriction any global function can have at `n = 5`; hence no
    global rule can validate the `5 × 5`, and a fortiori none validates all squares.
  - Per-orientation intersection search across `n = 3,5,…`: the surviving-assignment set
    is non-empty at `n = 3` (4 assignments) and collapses to **∅ at n = 5**.

- **quasi-squares:** see below — curve 13 *does* connect on many `|w−h| = 1` quasi-squares
  (the square obstruction is specific to the odd-square split), with an
  orientation-class-dependent pattern.

## Derivation / proof of impossibility

### Obstruction: a forced 2×3 block whose endpoints are colour-locked (parity)

**Setup.** For odd `n`, the approximately-even partition splits each side into
`{n//2, n−n//2}`. For `n = 5` this is `{2,3}` on both axes, and the swap rule only chooses
*which* half is the even one (`2`) — it cannot change the multiset `{2,3}`. Whatever the
choice, the four quadrants of the top split realise exactly one `2×2`, one `3×3`, and two
`6`-cell blocks, and — crucially — **exactly one block is `2`-wide × `3`-tall (a `2×3`
block)**, carried by base 3 or base 5 in one of curve 13's fixed orientations
(computationally: in all 9 top-split choices the four block sizes always include such a
`2×3` block).

**Lemma (colour-lock).** Let a sub-region be the `2×3` block of curve 13's top split,
filled by base 3 (in orientation `rot90` / `rot270`) or base 5 (in orientation `rot90` /
`transpose,rev`). Then for **every** swap assignment the sub-curve's entry and exit cells
are the two corners of a single vertical (short) edge of the block:

| block | entry | exit |
|-------|-------|------|
| base 5 @ UL (`rot90`) | `(1,0)` | `(1,2)` |
| base 5 @ UR (`transpose,rev`) | `(0,2)` | `(0,0)` |
| base 3 @ LL (`rot90`) | `(1,0)` | `(1,2)` |
| base 3 @ LR (`rot270`) | `(0,2)` | `(0,0)` |

These endpoints are **swap-invariant** (verified over all 9 swaps per block) and always lie
on the same column, separated in the `y`-direction by `2`.

**Parity contradiction.** Colour the grid `χ(x,y) = (x+y) mod 2`. Two cells on the same
column separated by `Δy = 2` have the **same** colour. A `2×3` block has `6` cells,
`3` of each colour; a Hamiltonian path on `6` cells alternates colour and therefore must
have endpoints of **opposite** colour. But the Lemma forces both endpoints to the same
colour. **Hence the `2×3` block has no Hamiltonian path** — for any swap rule.

**Conclusion.** In every top-split of the `5×5`, one quadrant is a `2×3` block on base 3 or
base 5 whose sub-path cannot exist. Therefore the concatenated `5×5` path cannot exist
under any swap rule, so **curve 13 is square-infeasible.** ∎

### Why the endpoints are colour-locked (structural reason)

Curves 3 and 5 are **edge→edge** curves whose global entry/exit lie on opposite ends of the
curve. Under the `rot90`/`rot270`/`transpose` morphisms curve 13 assigns to the quadrants
that receive the odd (`3`) canonical dimension, those two edge endpoints are mapped onto the
two corners of the block's **short (`2`-wide) side**. On a `2`-wide side the two corners
differ by `Δy = 2` (even) → identical colour. The swap rule reroutes the *interior* of the
sub-path but can never move its two global endpoints off those corners, so the colour
mismatch is unavoidable. This is the boundary-vector face of the `1×2`(A,C)/`2×1`(B,D)
primitive constraint: the odd side lands on the axis where the curve's dominoes cannot
reconcile the endpoint colours.

### Contrast: why 3×2 is fine

The transposed block `3`-wide × `2`-tall *does* admit a valid fill (e.g. base 5 @ `rot90`
on `3×2` is OK for 6 of 9 swaps, entry `(2,0)` exit `(2,1)` — opposite colours). The `3×3`
and `2×2` quadrants are also always fillable. The obstruction is **exclusively** the `2×3`
orientation, which the odd-square split cannot avoid.

### Independent confirmation via the top-split junction/parity chain

The colour argument at the *junction* level (start colour free ⇒ satisfiable) does **not**
forbid the split — the obstruction is strictly one level lower, inside the `2×3` block. This
was confirmed computationally: over the complete `n=5` space, **no** assignment even makes
all four sub-blocks *internally* valid simultaneously (the `2×3` block always fails
internally), so the failure is never a junction that could be repaired by a colour choice.

## Quasi-squares (`|w − h| = 1`)

The `2×3` square-split obstruction is specific to odd *squares*; quasi-squares split
differently and curve 13 connects on many of them. Testing existence of a per-index
(`9⁴`) swap rule per region, over smaller-dimension `s = 1..6` and all 8 top orientations,
gives a clean **transpose vs non-transpose** class split (`Y` = a valid rule exists):

```
wide (w=s+1, h=s)                 tall (w=s, h=s+1)
 non-transpose {e,rot180,          non-transpose : YYY..Y
   vflip,hflip} : Y..YYY           transpose {transpose,
 transpose {transpose,rot90,         rot90,antidiag,
   antidiag,rot270} : YYY..Y         rot270} : Y..YYY
                                   (cols s=1..6)
```

- The two D4 cosets are **mirror images**: what a non-transpose orientation achieves on
  *wide* quasi-squares, a transpose orientation achieves on *tall* ones, and vice-versa —
  exactly the `1×2`(orientations A,C) / `2×1`(orientations B,D) primitive duality.
- `s = 1` (the `2×1`/`1×2` domino) connects in **every** orientation (base primitive).
- Connectivity is **not** monotone in `s` (e.g. non-transpose wide fails at `s = 2,3`
  i.e. `3×2, 4×3`, then succeeds at `s ≥ 4`); a single uniform quasi-square rule is *not*
  claimed. (Caveat: the `.` entries are for the **per-index** `9⁴` space; a full
  per-orientation rule might connect a few more — the square result, by contrast, is proved
  over the **full per-orientation** space and is unconditional.)

## Evidence

Commands (run from `/home/elessar/Projects/HilbertPlots`, engine `research/aep.py`):

```
# quadrant rules / nodes
aep.RULES[13] = [(3, rot90, F), (5, rot90, F), (5, transpose, T), (3, rot270, F)]
aep.entry_exit(13) = ('edge','edge')

# orientation-independent (9) and per-index (9^4) searches over n=1..40:
9   options for curve 13  (kernels fixed) -> 0 valid
6561 = 9^4 per-index combos {0,3,5,13}    -> 0 valid

# n=5 admissible top rules, allowing ALL kernel per-orientation freedom:
n=3 : {(second,second),(second,none),(none,second),(none,none)}   (4 rules OK)
n=5 : {}                                                           (NONE)
n=7 : {(first,first),(none,first),(second,first)}                 (note: disjoint from n=3)

# n=5 EXHAUSTIVE over complete node universe (5 nodes):
space size = 9^5 = 59049 ; valid = 0 ; every failure reason = "disconnected"

# per-block fillability at the n=5 top split (all 9 split choices):
each choice -> exactly one 2x3 block on base 3 or 5 is UN-fillable (0/9 swaps),
              all 2x2, 3x2, 3x3 blocks fillable.

# colour-lock (swap-invariant endpoints of the 2x3 block):
base5@UL 2x3: entry (1,0) exit (1,2)   [colours 1,1  -> SAME]
base5@UR 2x3: entry (0,2) exit (0,0)   [colours 0,0  -> SAME]
base3@LL 2x3: entry (1,0) exit (1,2)   [colours 1,1  -> SAME]
base3@LR 2x3: entry (0,2) exit (0,0)   [colours 0,0  -> SAME]
2x3 grid = 6 cells (3+3) -> Hamiltonian path needs OPPOSITE-colour endpoints.
```

**Total search space explored for the impossibility:** `9` (orientation-independent) `+`
`6561` (`9⁴` per-index) `+` `59049` (`9⁵` full per-orientation over the complete `n=5`
node universe) `= 65619` assignments, plus the `n=3..39` intersection search — all empty
except `n=3`. The `9⁵` `n=5` enumeration is the decisive exhaustive proof.

## Open questions

- **General theorem.** Curve 13 fails because two edge→edge kernels (3, 5) are placed by
  `rot90`/`rot270`/`transpose` so the odd split-dimension lands on their short (`2`) side,
  colour-locking a `2×3` block. Conjecture: **a composite curve is square-infeasible iff
  some quadrant morphism maps an edge→edge kernel's endpoint-edge onto the axis that
  receives the odd half at odd sizes**, forcing a same-colour `2×(odd)` block. This should
  be checked against the feasible composites and folded into the section-7 classification.
- **Rectangles.** A full `w × h` characterisation of curve 13's connectivity (beyond the
  quasi-square class table) is left open; the non-monotone quasi-square pattern suggests a
  size-parity condition worth pinning down.
- Whether allowing a *size-dependent* swap rule (outside the paper's size-independent model)
  could rescue curve 13 on squares — the `2×3` block has no Hamiltonian path at all, so
  **no**: the obstruction is intrinsic to the block, not to the rule model.

## Verification

**Verdict: CONFIRMED.** An independent adversarial re-check reproduced every computational
claim and found the impossibility proof sound. No working swap rule exists.

**What was re-run** (engine `research/aep.py`, `.venv/bin/python`):

1. **`RULES[13]` matches the report table** exactly: LL=(3, rot90, F), UL=(5, rot90, F),
   UR=(5, transpose, **T**), LR=(3, rot270, F). `entry_exit(13)=('edge','edge')`.

2. **Orientation-independent search (9 options), n=1..40, kernels fixed:** 0 valid.
   Reproduced.

3. **n=5 node universe rebuilt independently** by recursively exploring *all* 9 swap
   branches at each node (not a single fixed split): exactly **5** nodes —
   curve 13 @ identity, curve 3 @ {rot90, rot270}, curve 5 @ {rot90, transpose}. Curve 0
   does **not** appear at n=5 (it first appears at n≥7), so the n=5 space is genuinely 9⁵.
   Matches the report's node count.

4. **Exhaustive 9⁵ = 59049 over the complete n=5 node universe:** **0 valid**, and every
   single failure reason is `disconnected` (59049/59049). This is the decisive check: a
   global `swap(index,M)` assigns one fixed `(sw,sh)` per node, so enumerating all 9⁵
   assignments over exactly the 5 reachable nodes covers *every* restriction any global
   function can have at n=5. None validate ⇒ no global rule validates the 5×5 ⇒ (by the
   definition requiring validity on *every* square) curve 13 is square-infeasible.

5. **Per-index 9⁴ = 6561 over {0,3,5,13}, n=1..40:** 0 valid; moreover **0** even pass the
   n=5 gate. Reproduced.

6. **Colour-lock lemma verified two ways.** (a) An independent brute-force DFS confirms a
   2-wide × 3-tall grid with same-column, Δy=2 endpoints has **no** Hamiltonian path
   (`(1,0)→(1,2)`: False; `(0,0)→(0,2)`: False), while opposite-colour controls
   (`(0,0)→(1,2)` on 2×3, `(2,0)→(2,1)` on 3×2) **do** (True). (b) Extracting the actual
   2×3 sub-block for all 9 top-split choices: **every** choice yields exactly one 2×3 block
   (on base 3 or base 5), each **0/9 internally fillable**, with swap-invariant endpoints
   matching the report's table verbatim (base3@rot90 & base5@rot90 → `(1,0)/(1,2)`;
   base3@rot270 & base5@transpose,rev → `(0,2)/(0,0)`), both endpoints same colour.

**Refutation attempts (all failed to refute):** the orientation-independent (9), per-index
(9⁴), and full per-orientation (9⁵ at n=5) searches were re-run from scratch; none produced
a valid rule. The split multiset at n=5 is always `{2,3}` (the swap only relabels which half
is even), so a 2×3 block is unavoidable — confirmed across all 9 choices.

**Proof audit — no gaps found.** The parity argument is correct (6-cell bipartite path
alternates colour ⇒ opposite-colour endpoints required; the forced endpoints are same
colour). The obstruction is *internal* to the 2×3 block (stronger than a repairable
junction), so it also rules out any size-*dependent* rule. A single failing square (n=5)
correctly suffices to deny an all-squares rule. The 9⁵ enumeration is genuinely complete
over the independently-reconstructed node set.

*Minor, non-substantive note:* the report's "n=3 : 4 rules OK" counts admissible top-level
`(sw,sh)` choices, whereas an independent recount over the full 5-node tuple space gives
26244 surviving 5-tuples at n=3 — different counting bases, not a discrepancy; both agree
the survivor set is **empty at n=5**, which is the load-bearing result.
