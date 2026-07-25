# Curve 3 — Liu2

- **kernels / quadrant rules** (visited order LL, UL, UR, LR):
  | quadrant | base | morphism `M` | reverse |
  |----------|------|--------------|---------|
  | LL | 0 (Hilbert) | `((1,0),(0,-1))` = **vflip** | False |
  | UL | 0 (Hilbert) | `((0,-1),(1,0))` = **rot90** | False |
  | UR | 0 (Hilbert) | `((0,1),(-1,0))` = **rot270** | False |
  | LR | 0 (Hilbert) | `((1,0),(0,-1))` = **vflip** | False |

  Every quadrant recurses into **kernel curve 0 (Hilbert)**. Curve 3 uses no other
  kernel, so the problem is solvable bottom-up: fix curve 0 first, then curve 3.
- **entry/exit type:** `entry_exit(3) = ('edge','edge')`. On the `2^k` grid the global
  entry/exit are the two mid-points of the bottom-vs... concretely on order 4 (16×16):
  entry `(0,7)` (left edge, mid-height), exit `(15,7)` (right edge, mid-height). This is an
  **edge→edge, left-to-right** curve.
- **partition nodes** (`orientations_used(3)`), the `(curve, orientation)` pairs that need a
  swap rule — exactly **5 nodes**, a closed set:
  - `(3, A)` — curve 3 at identity;
  - `(0, hflip)`, `(0, rot90)`, `(0, rot270)`, `(0, vflip)` — curve 0 at four orientations.
  Curve 0 never appears at the identity/`{A,B,C,D}` coset inside curve 3; the four
  orientations above are closed under the recursion.

## Result

- **squares: FEASIBLE.**
- **swap rule** (orientation-*independent* — same rule at every orientation of a given
  curve; note curve 3 and its kernel take *different* pairs, so no single global `(sw,sh)`
  works):
  - **curve 3 node:** `(sw, sh) = (·, second)` — the canonical **height**-split must make
    the *high* half even; the width-split `sw` is arbitrary.
  - **curve 0 kernel nodes** (all four orientations): `(sw, sh) = (·, first)` — the
    canonical height-split makes the *low* half even; `sw` arbitrary.
  - The published compact form `const_swap({3:("first","second")})` is one instance:
    curve 3 → `(first,second)`, kernel curve 0 → default `(first,first)`. Both have
    `sh` pinned as above and `sw = first` (a free choice).
- **verified:** valid Hamiltonian path on `n × n` for **n = 1..40** (all OK); **matches
  hilbertplot at `2^k`** (k=1,2,3): **yes** (`square_valid(3, rule, sizes=range(1,41)) = True`).
- **quasi-squares** (`|w−h| = 1`, under the square rule): a quasi-square connects **iff its
  canonical width `Wc` is even**, i.e. the odd side must be the *canonical height*.
  Equivalently, non-transposing orientations `{A, C, hflip, vflip}` connect iff `w` is
  even; transposing orientations `{B, D, rot90, rot270}` connect iff `h` is even.
  (Verified for base 5..39, all 8 orientations; sizes ≤ 4 are all-valid boundary cases.)
  No swap rule makes any single orientation connect *all* quasi-squares — a genuine
  parity obstruction (search returned empty, below).

## Derivation / proof

### Search space and structure of the solution set

The full per-node rule space has `3 × 3 = 9` choices of `(sw,sh)` at each of the 5 nodes,
so `9^5 = 59049` candidate rules. Exhaustive test (prune on odd `n∈{3,5,7,9,11,13}`,
confirm survivors on `n=1..40`) yields **exactly 243 = 3^5 valid rules**, and the valid set
is *exactly* the Cartesian product of independent per-axis constraints:

| node | `sw` (canonical width-split) | `sh` (canonical height-split) |
|------|------------------------------|-------------------------------|
| `(0,hflip)`  | free `{first,second,none}` | **pinned `first`** |
| `(0,rot90)`  | free | **pinned `first`** |
| `(0,rot270)` | free | **pinned `first`** |
| `(0,vflip)`  | free | **pinned `first`** |
| `(3,A)`      | free | **pinned `second`** |

So: **`sw` is irrelevant everywhere; only the height-split parity matters**, and it must be
`second` at curve 3 but `first` at the kernel. This asymmetry is exactly why no single
global `(sw,sh)` works (Level‑1 search over 9 options: all fail).

### Lemma 1 (Junction invariance — closed form, all n ≥ 4)

Work in the canonical frame (top level: identity, no transpose, `Wc = Hc = n`). Split
`Wc = Wc1 + Wc2`, `Hc = Hc1 + Hc2`. The four boxes and the Hilbert sub-curve on each
(with its designated entry/exit corners) are:

| box | region | orient | entry | exit |
|-----|--------|--------|-------|------|
| LL | `[0,Wc1)×[0,Hc1)` | vflip | `TL=(0,Hc1−1)` | `TR=(Wc1−1,Hc1−1)` |
| UL | `[0,Wc1)×[Hc1,n)` | rot90 | `BR=(Wc1−1,Hc1)` | `TR=(Wc1−1,n−1)` |
| UR | `[Wc1,n)×[Hc1,n)` | rot270 | `TL=(Wc1,n−1)` | `BL=(Wc1,Hc1)` |
| LR | `[Wc1,n)×[0,Hc1)` | vflip | `TL=(Wc1,Hc1−1)` | `TR=(n−1,Hc1−1)` |

The three junctions along the traversal LL→UL→UR→LR are then

- **J1** `LL.exit (Wc1−1,Hc1−1) — UL.entry (Wc1−1,Hc1)` : displacement `(0,1)`, distance 1;
- **J2** `UL.exit (Wc1−1,n−1) — UR.entry (Wc1,n−1)` : displacement `(1,0)`, distance 1;
- **J3** `UR.exit (Wc1,Hc1) — LR.entry (Wc1,Hc1−1)` : displacement `(0,1)`, distance 1.

**All three are 4-adjacent for every `Wc1, Hc1`.** The junction connectivity is therefore
*completely independent of the split parities*. This proves the two facts the search found:
`sw` is free (J2 always lands on the top row `y=n−1` regardless of `Wc1`), and — at the
top level — even `sh` is unconstrained. Verified: the four top-level sub-curves hit exactly
these designated corners for all `n = 4..40`; `n = 1,2,3` are validated directly. ∎

### Lemma 2 (Reduction to the kernel)

By Lemma 1 the parent junctions cost nothing. Hence curve 3 on `n×n` is a valid path **iff**
each of its four sub-boxes is a valid Hilbert path terminating at the designated corners of
that box. The sub-boxes are rectangles `Wc1×Hc1, Wc1×Hc2, Wc2×Hc2, Wc2×Hc1` filled by
**curve 0** at the four orientations. Thus *all* remaining parity constraints come from the
**kernel corner-termination requirement**, not from curve 3's own geometry.

### Why `sh` is pinned (the kernel parity condition)

Curve 0 (Hilbert) under AEP is a corner-to-corner Hamiltonian path on a rectangle only when
the swap makes the correct half even — for the four orientations here this is the *canonical
height* condition `sh = first`. Curve 3's own `sh = second` forces `Hc2` even, which is the
parity that lets the vflip/rot90/rot270 kernels on the resulting sub-rectangles corner-
terminate (feeding Lemma 2). `sw` never enters either condition, matching the free column of
the table. This is the mechanism; it is verified over `n=1..40` and rests on curve 0's
established arbitrary-rectangle (Wu–Chang) corner-to-corner property as the kernel lemma.

### Quasi-squares (parity law)

For `|w−h|=1` the aspect ratio is *forced*: one side is longer by 1, so unlike a square the
construction cannot absorb the odd length on a free axis. Since the pinned axis is the
*height*, the odd side must be the canonical height for the kernels to corner-terminate;
equivalently **`Wc` (canonical width) must be even**. This is verified exactly for base
5..39 across all 8 orientations. It ties to the terminal `1×2`/`2×1` primitive: the AEP
recursion bottoms out on dominoes whose orientation is fixed by `Wc` parity — non-
transposing orientations `{A,C,hflip,vflip}` (`Wc=w`) need `w` even; transposing
`{B,D,rot90,rot270}` (`Wc=h`) need `h` even. All 8 orientations correctly fill both the
`1×2` and `2×1` primitives, so the obstruction is purely the parity of the *odd* dimension's
axis, not the primitive itself.

## Evidence

Commands (run as `cd /home/elessar/Projects/HilbertPlots && .venv/bin/python …`; scratch
scripts under `research/`).

**Feasibility + hilbertplot match (`research/scratch_c3.py`, `scratch_search.py`):**
```
curve 3 const (first,second), n=1..40:  bad: NONE — all OK
matches hilbertplot at 2^k: True
Level 1 (single global (sw,sh), 9 options): all 9 FAIL (n=3 or n=5)
Per-node search: space = 9^5 = 59049 ; valid = 243 = 3^5
```

**Product structure of the 243 valid rules (`research/scratch_analyze.py`):**
```
c0 @ hflip  sw FREE {first,none,second}   sh PINNED = first
c0 @ rot90  sw FREE                        sh PINNED = first
c0 @ rot270 sw FREE                        sh PINNED = first
c0 @ vflip  sw FREE                        sh PINNED = first
c3 @ A      sw FREE                        sh PINNED = second
product of per-axis freedoms = 243  (== |valid set|)
```

**Junction invariance (`research/scratch_quasi.py`, `scratch_mech.py`):**
```
Top-level junction distances = [1,1,1] for every n = 3..40
n=5 example: Wc1,Wc2=2,3  Hc1,Hc2=3,2
  LL exit (1,2) — UL entry (1,3) dist 1
  UL exit (1,4) — UR entry (2,4) dist 1
  UR exit (2,3) — LR entry (2,2) dist 1
Top-level sub-curves hit designated corners for all n = 4..40 (n≤3 direct).
```

**Quasi-square parity law (`research/scratch_quasi2.py` + verification):**
```
WIDE  (w=h+1): {A,C,hflip,vflip} valid at odd h (w even); {B,D,rot90,rot270} valid at even h (w odd)
TALL  (h=w+1): mirror image
Unified: valid  ⇔  canonical width Wc even   — holds for all 8 orients, base 5..39 (0 exceptions)
Per-node search for a rule connecting ALL wide quasi-squares at a fixed orientation: 0 found
```

## Open questions

- **Full all-`n` proof of the kernel lemma.** The reduction (Lemmas 1–2) is closed form; the
  remaining step — curve 0 at `{vflip,rot90,rot270,hflip}` corner-terminates on every
  sub-rectangle under `sh=first` — is verified over `n=1..40` and follows the Wu–Chang
  arbitrary-rectangle Hilbert result, but is not re-proven here for all `n` by induction.
  Closing it would upgrade the square result from *verified n=1..40* to *proved for all n*.
- **Rectangles** (`|w−h|>1`): the `Wc`-even parity law suggests a per-aspect swap rule;
  not yet mapped.
- Whether the `sw`-free / `sh`-pinned dichotomy generalizes to the other kernel-0 curves
  (5, 24, 31 share the `(first,second)` const rule) — a candidate structural theorem:
  *a curve whose four kernels are Hilbert at the `{vflip,rot90,rot270,hflip}` coset
  generalizes to squares with the height-axis carrying the odd length.*

## Verification

Adversarial re-check performed independently with the shared engine (`research/aep.py`);
scratch scripts `research/scratch_verify_c3.py`, `scratch_search_c3.py`,
`scratch_level1_c3.py`, `scratch_quasi_c3.py`, `scratch_quasi_c3b.py`,
`scratch_struct_c3.py`. **Verdict: CONFIRMED.**

**Computational claims — all reproduced exactly:**

- Compact rule `const_swap({3:("first","second")})`: `validate == "OK"` on every `n × n`,
  **n = 1..40** (bad set empty); `square_valid(3, rule, sizes=range(1,41)) = True`
  (so hilbertplot `2^k` match holds for k=1,2,3). I additionally ran **n = 41..80** — still all
  OK, so the rule is not silently failing just past the reported range.
- Partition nodes: exactly **5**, matching the report — curve 0 at
  `hflip, rot90, rot270, vflip` and curve 3 at identity.
- Exhaustive per-node search: space `9^5 = 59049`; **exactly 243 = 3^5** rules survive the
  odd-`n` prune AND re-confirm on n=1..40. The valid set **equals the full Cartesian
  product** of per-node freedoms: at every node `sw ∈ {first,second,none}` is free; `sh` is
  **pinned `first`** at all four kernel-0 nodes and **pinned `second`** at the curve-3 node.
  Reproduces the report's table cell-for-cell.
- Level-1 (single global `(sw,sh)` for all nodes): **0 of 9 work** — confirms no orientation-
  independent global rule exists, hence the kernel/curve-3 `sh` asymmetry is genuine.
- Junction invariance (Lemma 1): top-level junction distances `= [1,1,1]` for **all
  n = 3..40**, confirming the three parent junctions are 4-adjacent independent of split
  parity.
- Quadrant rules table, `entry_exit(3) = ('edge','edge')`, and the `sh=second ⇒ Hc2 even`
  mechanics all verified directly.

**Quasi-square law:** `valid ⇔ canonical width Wc even` holds with **0 mismatches** over
base(min side) `5..39`, all 8 orientations (560 cases). The 8 apparent mismatches at
`3×4 / 4×3` are exactly the `sizes ≤ 4` boundary cases the report already excludes.
Per-node search for a rule connecting **all** wide quasi-squares at a fixed orientation:
**0 found** — the parity obstruction is real.

**Proof scrutiny.** The reduction is sound: Lemma 1 (junction invariance) is a closed-form
displacement argument corroborated by the `[1,1,1]` measurement; Lemma 2 (curve 3 valid iff
each of the four sub-boxes is a corner-terminating Hilbert path) follows validly from it,
since the four boxes tile the square and the parent junctions cost nothing. The `sh`-pinning
mechanism is consistent — top-level junction connectivity is independent of `sh` (Lemma 1),
while `sh=second` is forced one level down to give the kernels the `Hc2`-even parity they
need to corner-terminate; these act at different levels and do not conflict. Lemma 1's phrase
"even `sh` is unconstrained" is terse but not wrong (it refers only to the top-level
junctions, not the kernel-feeding requirement).

**Scope / honesty.** The square result is correctly stated as **verified over n = 1..40**,
not proved for all n. The single genuine gap — that curve 0 at `{vflip,rot90,rot270,hflip}`
corner-terminates on every sub-rectangle under `sh=first`, the base kernel lemma — is
**verified, not inductively proved for all n**, and the report explicitly discloses this in
Open Questions. No overclaim was found; the "FEASIBLE" verdict is appropriately scoped.
