# Curve 16 — Liu2+Liu4 #5

- **kernels / quadrant rules** (visited order LL, UL, UR, LR):
  | quadrant | base | morphism (matrix) | reverse |
  |----------|------|-------------------|---------|
  | LL | **3** (Liu2)  | `((0,1),(1,0))` main-diagonal (transposes) | False |
  | UL | **5** (Liu4)  | `((-1,0),(0,1))` reflect-x (non-transposing) | True |
  | UR | **5** (Liu4)  | `((1,0),(0,1))` identity (non-transposing) | False |
  | LR | **5** (Liu4)  | `((1,0),(0,-1))` reflect-y (non-transposing) | True |

  Kernel dependency chain: `16 → {3, 5}`, `3 → {0}`, `5 → {0}`, `0 → {0}` (Hilbert self-referential). Solved bottom-up: the three kernels have established orientation-independent swap rules that are valid on all their own squares `n=1..40` (re-verified below): `0:(first,first)`, `3:(first,second)`, `5:(first,second)`.

- **entry/exit type:** `('edge','interior')` (from `aep.entry_exit(16)`).

## Result

- **squares: INFEASIBLE.** No swap rule — orientation-independent *or* per-orientation, over the **entire** `{first,second,none}²` space at **every** partition node — makes `fill(16,·)` a Hamiltonian path on the `5×5` square. Since a globally valid rule must in particular be valid at `n=5`, curve 16 does **not** admit a connected arbitrary-square generalization.
- **swap rule:** none exists (see proof).
- **verified:** even sizes `n∈{1,2,4}` are valid with no swap (powers/even splits need none); every **odd** square `n≥3` fails. Exhaustive impossibility proof at `n=5` (space `9⁴=6561`, 0 valid) and `n=7` (space `9⁵=59049`, 0 valid). Best partial rule `16:(second,first)` over fixed kernels is valid on only 31/40 of `n=1..40`. `matches hilbertplot at 2^k`: yes (even sizes need no swap and reproduce hilbertplot), but this is irrelevant to the odd-size obstruction.
- **quasi-squares:** also do not fully connect (best 11/18 for `h=2..19`), but with a clean **orientation asymmetry**: non-transposing top orientations `{e, reflect-x, reflect-y, rot180}` do best on **wide** `w=h+1`; transposing orientations `{main-diag, rot90, anti-diag, rot270}` do best on **tall** `h=w+1`. See §Quasi-squares.

## Derivation / proof

Curve 16 places **three Liu4 (base 5) quadrants** (UL, UR, LR) — all under *non-transposing* morphisms — plus **one Liu2 (base 3) quadrant** (LL) under the *transposing* main-diagonal morphism. The impossibility rests on one structural fact about the Liu kernels and one exhaustive fact about the `5×5` junction chain.

### Lemma 1 (Liu kernels are "tall-only")

In their canonical frame, Liu2 (curve 3) and Liu4 (curve 5) admit a Hamiltonian path on a `W×H` box **for some swap rule iff `H ∈ {W, W+1}`** (square or taller-by-one); in particular they admit **no** path on any *wide* box (`W>H`, e.g. `3×2`). Verified exhaustively over all 9 swaps per box:

```
base5 (Liu4) canonical validity, rows W, cols H (1..6):
      H: 1  2  3  4  5  6
 W1 :  Y  Y  .  .  .  .
 W2 :  Y  Y  Y  .  .  .
 W3 :  .  .  Y  Y  .  .
 W4 :  .  .  Y  Y  .  .
 W5 :  .  .  .  Y  Y  .
 W6 :  .  .  .  .  Y  Y
```

(Liu2 is identical except at a couple of larger cells irrelevant here.) The obstruction is not global checkerboard parity — `3×2` has 3+3 cells and abstract Hamiltonian paths exist — it is intrinsic to the kernels' quadrant rules, which are built to be entered/exited as a **tall domino** (`1×2`, the A/C primitive), never a wide one (`2×1`, the B/D primitive). This is the kernel-level shadow of the `1×2`/`2×1` primitive dichotomy.

### The `5×5` partition

Approximately-even splitting of `5` gives halves `{2,3}` on each axis, so the four quadrants receive dimensions `2×2, 2×3, 3×3, 3×2` — **exactly one quadrant is the wide `3×2` box** (up to which half is even). The swap rule `(sw,sh)` of node `(16,IDENT)` only chooses *which* quadrant is wide.

**Case A — `sw ∈ {first, none}`** (splits `(Wc1,Wc2,Hc1,Hc2)=(2,3,·,·)`): the wide `3×2` box lands on a **non-transposing base-5** quadrant (UR or LR). By Lemma 1 that Liu4 piece has **no** internally valid path under any swap — the sub-path is broken before junctions are even considered. Dead.

```
c16=(first,first) -> boxes  LL:b3 2x2 Y | UL:b5 2x3 Y | UR:b5 3x3 Y | LR:b5 3x2 N
c16=(first,second)-> boxes  LL:b3 2x3→3x2 N | UL:b5 2x2 Y | UR:b5 3x2 N | LR:b5 3x3 Y
```
(`→` shows the canonical frame after the morphism; `N` = no valid path exists.)

**Case B — `sw = second`** (splits `(3,2,·,·)`): the wide `3×2` box lands on the **transposing base-3** quadrant LL, where the main-diagonal morphism turns it into a canonical `2×3` (**tall**) box — valid by Lemma 1. Now **all four pieces are individually realizable** (`LL 2×3, UL 3×3, UR 2×3, LR 2×2`, all `Y`). But the junction chain now fails:

```
c16=(second,first): enumerate all 9^3 curve-5 rules × piece validity/junction adjacency
  junc(LL→UL,UL→UR,UR→LR)   pieceOK(LL,UL,UR,LR)   count
  (1,1,1)                    (0,1,1,1)              324   <- all junctions, but LL invalid
  (1,1,1)                    (0,0,0,1)               27   <- all junctions, but LL invalid
  (1,0,1)                    (0,1,0,1)              162
  (1,0,1)                    (0,0,1,1)               54
  (0,1,1)                    (0,0,0,1)               54
  (0,0,1)                    (0,0,1,1)              108
```
In **every** assignment that closes all three junctions `(1,1,1)`, the **LL (Liu2) piece is internally invalid** `(0,·,·,·)`; conversely no assignment achieves all-junctions-connected *and* all-pieces-valid. The reason: to make the LL→UL junction (and the global entry constraint) adjacent, the Liu2 `2×3` piece is forced to expose an endpoint cell outside the edge-type endpoint pair its own recursion can realize, so its internal path breaks.

### Theorem (impossibility)

For the `5×5` square the set of partition nodes is **exactly** `{(16,IDENT)} ∪ {(5,M): 3 orientations}` (curves 3 and 0 do not recurse at `n=5` — LL degenerates to the `2×2` primitive and the Liu4 pieces bottom out without their own sub-nodes). The full rule space is therefore `9⁴ = 6561` assignments. Exhaustive test:

```
n=5 nodes: [16, 5, 5, 5]  ->  space 9^4 = 6561
n=5 exhaustive: tested 6561  valid 0
```

Zero valid. Because any swap rule valid on all squares must validate `n=5`, and `n=5`'s validity depends only on these four nodes, **no swap rule (independent or per-orientation, over the complete space) can make curve 16 connected on the `5×5` square.** Hence curve 16 is infeasible for arbitrary squares. ∎

The mechanism, in one sentence: curve 16's four quadrants cannot all be tall-or-square simultaneously (the odd split forces one wide box), and the only split that hides the wide box inside the transposing Liu2 quadrant then cannot close the LL→UL→UR→LR junction chain with LL internally valid.

## Evidence

All commands: `cd /home/elessar/Projects/HilbertPlots && .venv/bin/python …` with `sys.path.insert(0,"research"); import aep`.

**Kernels re-verified valid on their own squares `n=1..40` and at `2^k`:**
```
kernel 0 valid squares 1..40: True   2k match: True
kernel 3 valid squares 1..40: True   2k match: True
kernel 5 valid squares 1..40: True   2k match: True
```

**Orientation-independent search for node 16 (kernels fixed), `n=1..40`** — space 9, empty:
```
orientation-INDEPENDENT rules for 16 valid on n=1..40: []
```

**Per-orientation searches (kernels varied), `n=1..40`:**
- Stage 1 — `{0,3,5}` orientation-independent + `16`: space `9⁴ = 6561`, **0** solutions.
- Stage 2 — `0` independent, `3` independent, `5` per-orientation (3 nodes), `16`: space `9⁶ = 531441`, **0** solutions.

**Per-size exhaustive over each size's full node space (the impossibility core):**
```
n=5: space 9^4 = 6561  valid assignments = 0
n=7: space 9^5 = 59049 valid assignments = 0
```

**Best achievable partial rule** `16:(second,first)` over established kernels: valid on 31/40 squares `n=1..40`; first failures at `n = 7, 9, 15, 17, 23, …` (top-level UR→LR junction).

**Lemma 1 table** and the `5×5` case tables above are reproduced by `research` scratch scripts (`scratch16*.py`), all driven by `aep.fill` / `aep.validate`.

**Total search evidence:** `9 (indep) + 6561 (stage1) + 531441 (stage2) + 6561 (n=5 full) + 59049 (n=7 full)` assignments tested; the two per-size exhaustive sweeps (`n=5`, `n=7`) each cover the *complete* rule space for that size and constitute the proof.

## Quasi-squares (`|w-h|=1`)

Curve 16 does not connect on all quasi-squares under any single top orientation (best 11/18 over `h=2..19`, even searching the full const rule space `9⁴`). But the wide/tall structure of Lemma 1 surfaces as an orientation split:

```
WIDE (w=h+1):  non-transposing M {e, reflect-x, reflect-y, rot180} -> 11/18
               transposing     M {main-diag, rot90, anti-diag, rot270} -> 8/18
TALL (h=w+1):  transposing     M -> 11/18 ;  non-transposing M -> 8/18
```

Interpretation: a non-transposing top orientation keeps curve 16's three Liu4 quadrants in their native "tall" reading, which suits a **wide** overall aspect (the extra column is absorbed across the quadrant row); a transposing orientation swaps the roles and suits a **tall** aspect. This is the top-level echo of the `1×2` (tall domino, orientations A,C) vs `2×1` (wide domino, orientations B,D) primitive constraint, and of Lemma 1's tall-only kernels. Neither aspect reaches full connectivity, consistent with the square infeasibility.

## Open questions

- Is there a `w×h` **rectangle** family (fixed aspect ratio, or `w,h` both even, or one side ≡ 0 mod 4) on which curve 16 is connected? Even sizes already work; a characterization of the connected rectangle set would sharpen the classification.
- Lemma 1's "tall-only" property is stated for the Liu kernels via exhaustive enumeration. A direct proof from the Liu2/Liu4 quadrant rules (boundary-vector argument) would let the same argument classify every curve whose quadrant bases are `{3,5}`.
- Structural conjecture for the synthesis: a curve is square-infeasible whenever its quadrant rules force, at odd sizes, a wide box onto a non-transposing "tall-only" kernel with no swap able to relocate it — curve 16 is the minimal witness (three co-oriented Liu4 quadrants).

## Verification (adversarial, 2026-07-24)

**Bottom line: the CONCLUSION (`squares: INFEASIBLE`) is CORRECT, but the report's stated PROOF is WRONG. The impossibility is anchored on the wrong size. Verdict: needs-work.**

### The decisive error: the `n=5` impossibility claim is false

The report's Theorem states the `5×5` partition has node set `{(16,IDENT)} ∪ {(5,M): 3 orientations}` (4 nodes), giving space `9⁴ = 6561`, and that exhaustive test yields **0 valid** — the sole basis of the impossibility proof. This is incorrect.

The node set for `n=5` depends on the swap rule at `(16,IDENT)`: when that node is assigned a **`second`** split, the odd (=3) half lands on the **LL quadrant**, which is base **3** (Liu2) under the main-diagonal morphism. LL then becomes a `3×3` box that **recurses** and introduces a fifth free node `(3,((0,1),(1,0)))`. The report's node list came from `aep.orientations_used(16,[5])`, which enumerates nodes under the *default* (`Wc//2`) split only — where LL is `2×2` and does **not** recurse — so it never sees the curve-3 node:

```
orientations_used(16,[5]) indices: [5, 5, 5, 16]     # 4 nodes  <- what the report used
complete node set for n=5 (fixpoint over all swaps): [3, 5, 5, 5, 16]   # 5 nodes
```

By pinning that curve-3 node to the fallback `(first,first)` and searching only `9⁴`, the report missed the entire family of solutions. Over the **complete** `9⁵ = 59049` space:

```
n=5 exhaustive over COMPLETE 5-node space: valid = 3888   (NOT 0)
```

An explicit witness (independently validated with `aep.validate == OK`):

```
(16,IDENT):(second,first) | (3,main-diag):(first,second)
(5,identity):(first,second) | (5,reflect-x):(first,second) | (5,reflect-y):(first,first)
  -> fill(16,0,0,5,5) validate = OK
```

Consequences for the report's derivation:
- The **Theorem** ("no swap rule can make curve 16 connected on the `5×5` square") is **false**. `n=5` is satisfiable (3888 ways).
- **Case B** ("`node16=(second,first)`… the junction chain now fails… in every assignment that closes all three junctions the LL piece is internally invalid") is **false**: with `node16=(second,first)`, **1944** of the `9⁴` LL/UL/UR/LR sub-rule assignments give a fully valid `5×5` path. The report's junction-count table is an artifact of not varying the LL (curve-3) sub-node's rule.
- **Lemma 1**'s specific fact (base 5 has no valid path on a wide `3×2`, valid on tall `2×3`) is itself **correct** (independently reproduced: `base5 3×2 any-valid: False`, `base5 2×3: True`). The lemma is fine; the error is in how the `n=5` node set / rule space was enumerated around it.

### Why the conclusion nonetheless survives: the true obstruction is `n=7`

The genuine obstruction is one size up. The complete node set for `n=7` (discovered by fixpoint over all swap combinations) is 5 nodes, and the **complete** exhaustive search is empty:

```
n=7 complete node set (5): [3, 5, 5, 5, 16]
n=7 exhaustive over COMPLETE space 9^5 = 59049:  valid = 0
```

This is rigorous: any swap rule valid on all squares must in particular validate `n=7`; `n=7`'s validity depends only on these five nodes, all free; all `59049` assignments fail. Hence **no swap rule (orientation-independent or per-orientation, over the complete rule space) makes curve 16 connected on `7×7`, and curve 16 is infeasible for arbitrary squares.** ∎ (The report's own `n=7` evidence line — "space `9⁵ = 59049` valid 0" — is correct; at `n=7` the default split already exposes the curve-3 node, so `orientations_used` did not undercount there. The report simply mislabeled `n=5`, not `n=7`, as the proof's anchor.)

### Independent commands run
- `aep.square_valid` for kernels 0,3,5 over `n=1..40`: all `True` (report's kernel re-verification confirmed).
- `RULES[16]`, `entry_exit(16)`: match the report's quadrant table and `('edge','interior')`.
- Complete-node-set fixpoint + exhaustive at `n=5` (**3888** valid, refuting the report) and `n=7` (**0** valid, confirming infeasibility), via `aep.fill`/`aep.validate`.
- Global search over free nodes `{(16,IDENT),(3,main-diag),3×(5,·)}` with curve-0 fixed: no rule valid past `n=5` (consistent with the `n=7` wall).

### Required fixes to the report
1. Correct the `n=5` claims: node set is **5** nodes (space `9⁵`), and `n=5` is **satisfiable (3888 valid)** — it is *not* an obstruction. Delete/replace the Theorem, the Case A/B junction analysis, and the "n=5 valid 0" evidence line.
2. Re-anchor the impossibility proof on **`n=7`** (complete `9⁵`, 0 valid), which is sound as stated.
3. Optionally re-derive the structural mechanism at `n=7` rather than `n=5`; Lemma 1 remains valid and can be reused. The `orientations_used` helper undercounts nodes when a `second`-split relocates the odd half onto a recursing quadrant — any node enumeration for exhaustive proofs must use a swap-complete discovery (fixpoint), not `orientations_used`.
