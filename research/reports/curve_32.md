# Curve 32 — Moore+Liu4 #1

- **kernels / quadrant rules** (visited LL, UL, UR, LR):
  | quadrant | base kernel | morphism `M` | reverse |
  |----------|-------------|--------------|---------|
  | LL | 1 (Moore) | `((-1,0),(0,-1))` = 180° | False |
  | UL | 5 (Liu4)  | `((-1,0),(0,1))`  = x-mirror | True |
  | UR | 5 (Liu4)  | `((1,0),(0,1))`   = identity | False |
  | LR | 1 (Moore) | `((-1,0),(0,-1))` = 180° | False |

  Kernels bottom out through Moore (1) and Liu4 (5), which in turn are built from
  Hilbert (0). The full set of `(curve, orientation)` partition nodes that ever need a
  swap rule while drawing curve 32 on `n×n`, `n=1..40`, is **12 nodes**: all 8
  orientations of curve 0, curve 1 at 180°, curve 5 at `((-1,0),(0,1))` and
  `((1,0),(0,1))`, and curve 32 at identity. (`orientations_used(32)` samples only
  odd `n≤11` and reports 10; instrumenting `fill` over `n=1..40` gives the complete 12.)

- **entry/exit type:** `(interior, interior)` — both global endpoints lie in the interior
  (curve 32 is a Moore-family, near-cyclic construction).

## Result

- **squares: INFEASIBLE.** No swap rule — orientation-independent or per-orientation —
  makes `fill(32,·)` a Hamiltonian path on every `n×n` square. The obstruction already
  appears at **n = 5**, which is *exhaustively* infeasible.
- **swap rule:** none exists.
- **verified:**
  - `n = 5` : exhaustively infeasible — all `9⁴ = 6561` assignments of the 4 active nodes
    give a **disconnected** path (never a coverage/count failure).
  - odd `n ∈ {5, 11, 13, 15, 17, 19}` : infeasible by a rigorous block-obstruction
    (every top-level partition contains an unfillable quadrant; the `fillable` test is
    itself exhaustive over swaps).
  - `n = 7` : infeasible by exhaustive DFS (full search of the active-node tree).
  - `n = 9` : no valid rule found under a bounded exhaustive search (cap 2×10⁵ nodes);
    strong evidence, not a closed proof.
  - even `n ∈ {2,4,6,8}` : feasible (a valid rule exists for each individually).
  - **matches hilbertplot at `2^k`:** yes (`k=1..4`, `canonical_form` equality) — at powers of
    two no side is ever odd, no swap fires, and the construction reproduces hilbertplot's
    curve 32 exactly.
- **quasi-squares (`|w−h|=1`):**
  - Non-transposing orientations `{A(id), C(180°), x-mirror, y-mirror}` (those with
    `M[0][0]≠0`) connect **only for WIDE** quasi-squares (`w=h+1`: 3×2, 4×3, 5×4).
  - Transposing orientations `{B(main-diag), D(anti-diag), rot90, rot270}` (`M[0][0]=0`)
    connect **only for TALL** quasi-squares (`h=w+1`: 2×3, 3×4, 4×5).
  - No orientation connects both aspects. This is exactly the 1×2 / 2×1 primitive
    dichotomy propagated to the top level: curve 32 in a non-transposing frame lays its
    long axis horizontally, so it tolerates one extra column but not one extra row.

## Derivation / proof

### Lemma 1 (kernel unfillability of the wide 3×2 block).
The Moore and Liu4 kernels, in the *non-transposing* orientations in which curve 32
places them, cannot fill a 3×2 rectangle under **any** swap rule:

```
Moore(1)@180        3×2: X (unfillable)     2×3: Y (fillable)
Liu4(5)@((1,0),(0,1))    3×2: X              2×3: Y
Liu4(5)@((-1,0),(0,1)),rev 3×2: X            2×3: Y
```

(Each entry is an exhaustive search over the block's own swap sub-tree.) All three
forced orientations are *non-transposing* (`M[0][0]≠0`), so a 3×2 region is filled in the
kernel's canonical frame as *width 3 (odd) × height 2 (even)*. Moore and Liu4 are
edge→edge, near-cyclic curves: on a wide-odd × even canonical block their approximately-
even recursion cannot route the two forced endpoints into 4-adjacency with the demanded
sides. The transposed shape 2×3 (tall-odd) is fine — this asymmetry is the same one that
governs the quasi-square table.

### Lemma 2 (every 5×5 partition forces a wide 3×2 quadrant onto a kernel that cannot fill it).
The top-level split of `5` (identity, no transpose) yields halves `{Wc1,Wc2}` with one
even (2) and one odd (3), and likewise `{Hc1,Hc2}={2,3}`; the swap rule only chooses
*which* half is even, so there are exactly **4 distinct top partitions**. In each, the
quadrant that receives the shape 3×2 (width 3, height 2) is a Moore@180 or Liu4 quadrant,
i.e. a block that Lemma 1 proves unfillable:

```
(Wc1,Hc1)   LL M1@180     UL M5@a,rev    UR M5@b     LR M1@180
(2,2)        2x2:Y         2x3:Y         3x3:Y       3x2:X   <- LR dead
(2,3)        2x3:Y         2x2:Y         3x2:X       3x3:Y   <- UR dead
(3,2)        3x2:X         3x3:Y         2x3:Y       2x2:Y   <- LL dead
(3,3)        3x3:Y         3x2:X         2x2:Y       2x3:Y   <- UL dead
```

Since every partition contains a quadrant whose sub-region admits **no** valid filling,
`fill(32,0,0,5,5,·)` is disconnected for every choice of swap rule at every node. ∎

### Theorem (curve 32 does not generalize to squares).
A square generalization must be valid on *every* `n×n`. By Lemma 2 it fails on the 5×5.
Therefore no swap rule (orientation-independent or per-orientation) generalizes curve 32
to arbitrary squares. The exhaustive count confirms the mechanism: over all `9⁴ = 6561`
rule assignments at `n=5` the failure reason is always `disconnected` — the four
sub-regions always tile the grid and are internally consistent, but a junction (the entry
of the 3×2 quadrant) is never reachable. This is a **junction/boundary-vector
incompatibility**, not a global parity obstruction: the checkerboard color chain
`e_LL=B → x_LL=W → e_UL=B → x_UL=W → e_UR=B → (UR odd) x_UR=B → e_LR=W → x_LR=B` is
internally consistent, so global 2-coloring does *not* forbid the 5×5 — the obstruction is
the concrete unfillability of the wide-odd kernel block.

### Extent of the obstruction.
For odd `n ∈ {5,11,13,15,17,19}` the same block-obstruction is rigorous: every top
partition still contains an unfillable quadrant (verified with the exhaustive `fillable`
test). For `n=7,9` some partition is entirely block-fillable, so those sizes are killed at
the *junction* level instead — `n=7` was confirmed infeasible by a full DFS of its
active-node tree, and `n=9` by a bounded exhaustive search (no valid rule within 2×10⁵
explored nodes). The 5×5 result alone is a complete proof of non-generalizability; the
larger odd sizes corroborate that infeasibility persists.

## Evidence

Search-space accounting (`{first,second,none}²` = 9 options per node):

| search | space size | valid hits |
|--------|-----------|-----------|
| single global `(sw,sh)` for all nodes | `3² = 9` | 0 |
| const per-curve `{0,1,5,32}` | `9⁴ = 6561` | 0 |
| full per-orientation, 12 active nodes, `n=1..40` | `9¹² ≈ 2.82×10¹¹` | 0 |
| **decisive slice** `n=5`, 4 active nodes | `9⁴ = 6561` | **0 (all `disconnected`)** |

```
# nodes / structure
orientations_used(32)  -> 10 nodes (odd n<=11 sample); full n=1..40 -> 12 nodes
RULES[32] = LL:(1,180,F)  UL:(5,x-mirror,T)  UR:(5,id,F)  LR:(1,180,F)
entry_exit(32) = ('interior','interior')

# Search 1 (single global (sw,sh), 9 options): 0 hits; first failure n=3 or n=5
# Search 2 (const per-curve, 9^4=6561): 0 hits

# n=5 exhaustive (4 active nodes: (1,180),(5,x-mirror),(5,id),(32,id)):
active nodes at n=5: [(1,((-1,0),(0,-1))),(5,((-1,0),(0,1))),(5,((1,0),(0,1))),(32,((1,0),(0,1)))]
total combos: 6561   valid at n=5: 0   (every failure reason == 'disconnected')

# Lemma 1 (exhaustive per-block):
Moore@180        3x2: False   2x3: True
Liu4@((1,0),(0,1))    3x2: False   2x3: True
Liu4@((-1,0),(0,1)),rev 3x2: False   2x3: True

# Lemma 2 table (n=5, X = unfillable quadrant): see Derivation.

# 2^k reproduction:
matches hilbertplot at 2^k (k=1..4): True

# per-n feasibility (exhaustive unless noted):
n:  1 T | 2 T | 3 T | 4 T | 5 F(exh,6561) | 6 T | 7 F(exh) | 8 T | 9 F(bounded)
    | 11,13,15,17,19 F(block-obstruction) ; even 2,4,6,8 T

# quasi-squares (exists-a-rule per single shape):
orientation           2x3  3x2  3x4  4x3  4x5  5x4
A(id) / C(180) / x-mir / y-mir   .    Y    .    Y    Y    .     (WIDE only)
B(maindiag)/D(antidiag)/rot90/rot270  Y    .    Y    .    .    Y   (TALL only)
```

All runs: `cd /home/elessar/Projects/HilbertPlots/research && ../.venv/bin/python …`
using `aep.fill`, `aep.validate`, `aep.orientations_used`, `aep.entry_exit`, and
exhaustive DFS over the swap options at each active `(index, orientation)` node.

## Open questions

- Close the `n=9` case with a full (uncapped) exhaustive search or fold it into a uniform
  junction-parity argument covering the odd `n` where no single block is unfillable
  (`n≡1,3 mod 8`? — 7 and 9 are the small representatives).
- Prove Lemma 1 structurally from the Moore/Liu4 boundary vectors (endpoints on a common
  edge ⇒ wide-odd × even canonical block cannot present the two required junction sides),
  rather than by exhaustive block search.
- Characterize the even-`n` feasible rule explicitly (a valid rule exists for `n=2,4,6,8`);
  is there one rule valid on *all* even squares? This would give a "half-generalization."
- Situate curve 32 in the classification: it is the first studied curve that is
  **infeasible** for squares, driven by two 180°/mirror kernel quadrants (Moore) that
  cannot absorb the odd-side remainder — a structural predictor for infeasibility.

## Verification

**Verdict: CONFIRMED.** Independent adversarial re-check reproduces the report's central
result and, per the brief, actively tried to *refute* the impossibility claim by searching
the full swap-rule space; no valid rule exists.

**What I re-ran** (scripts in scratchpad, `.venv/bin/python`, importing `aep` from
`research/`):

1. **Decisive n=5 exhaustive search — reproduced, and gap closed.** The active nodes at
   `n=5` are exactly `(32,id), (5,x-mirror), (5,id), (1,180°)`. I did *not* trust the
   all-`first` node set: since different swap choices change split sizes and could route
   the recursion through *different* `(index,M)` nodes, I computed the **closure** of all
   nodes reachable at `n=5` under *any* of the 9 options at every node. The closure is
   **exactly those 4 nodes** — no additional node ever appears. Brute-forcing all
   `9⁴ = 6561` assignments: **0 valid, all 6561 `disconnected`** (never count/distinct/bbox).
   Because a swap rule is a pure function of `(index,M)`, and every assignment of the
   complete reachable-node set fails at `n=5`, **no swap rule can validate the 5×5** — this
   is a complete, rigorous proof of non-generalizability, independent of Lemmas 1–2.

2. **Supporting claims all hold:**
   - `2^k` match (k=1..4, `canonical_form` equality): **True**.
   - Lemma 1 (exhaustive over each block's own swap closure): Moore@180, Liu4@id,
     Liu4@x-mirror each **fail 3×2, succeed 2×3** — confirmed exactly as tabled.
   - Even-`n` feasibility: a valid rule exists individually for `n = 2,4,6,8` — **confirmed**.
   - `n = 3` feasible; `n = 5` infeasible; `n = 7` infeasible. Note: my closure method
     finds `n=7` has only 4 reachable nodes, so it is **exhaustively** infeasible over 6561
     combos — slightly *stronger* than the report's "confirmed by full DFS" phrasing.

**Assessment of the argument.** The load-bearing proof is the `n=5` exhaustive search, which
is sound and now watertight (closure verified). Lemmas 1–2, the checkerboard color-chain,
and the larger-odd-`n` block-obstruction are *explanatory corroboration*, not required for
the theorem; the report correctly flags `n=9` as bounded/non-closed evidence and does not
overclaim it. No logical gap found. The INFEASIBLE verdict stands.

*(Verified computationally over the stated ranges; the n=5 result is a proof for all n
since validity on every square is required and the 5×5 admits no rule.)*
