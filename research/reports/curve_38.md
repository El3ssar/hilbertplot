# Curve 38 — Moore+Liu2+Liu4 #1

- **kernels / quadrant rules** (order LL, UL, UR, LR; each `(base, morphism, reverse)`,
  from `aep.RULES[38]`; D4 codes `e=id, f=rot180, y=reflect-vertical-axis ((-1,0),(0,1)),
  o=main-diagonal ((0,1),(1,0)), a=anti-diagonal, g=rot+90, x=rot−90, m=reflect-horizontal`):
  - LL: `(3, o, False)`   — **Liu2** on the main-diagonal reflection
  - UL: `(5, y, True)`    — **Liu4** on the vertical-axis reflection, traversal reversed
  - UR: `(5, e, False)`   — **Liu4** upright
  - LR: `(1, f, False)`   — **Moore** rotated 180°

  The curve grafts three different kernels: two copies of **Liu4 (curve 5)** in the upper
  band, **Liu2 (curve 3)** in the lower-left, and the **cyclic Moore curve (curve 1)** in the
  lower-right, visited **last**. All three kernels recurse (through their own quadrant rules)
  down to the **Hilbert curve (curve 0)**. Curve 38 never appears as any other curve's kernel,
  so its only top-level responsibility is the identity orientation `e`, but its feasibility is
  bound up with the swap behaviour of curves 1, 3, 5 and 0 at the orientations it induces.

- **partition nodes** — the true set of `(curve, orientation)` pairs that ever require a swap
  rule, computed by expanding the recursion at **both** split parities across `n = 1..40`
  (`aep.orientations_used` under-reports because it only follows the default even split):
  **13 nodes** —
  - `(38, e)`
  - `(1, f)`                          (Moore, one orientation)
  - `(3, o)`                          (Liu2, one orientation)
  - `(5, y)`, `(5, e)`                (Liu4, two orientations)
  - `(0, e), (0, f), (0, y), (0, m), (0, o), (0, a), (0, g), (0, x)`   (Hilbert, all 8)

  **Key structural fact:** curve 0 (Hilbert) only surfaces at sizes `n ≥ 9`; at the decisive
  size `n = 7` the recursion bottoms out inside the kernels before reaching Hilbert, so the
  nodes live there are exactly the **5 nodes** `(1,f), (3,o), (5,y), (5,e), (38,e)`.

- **entry/exit type** (`aep.entry_exit(38)`): `('edge', 'interior')`. The global exit lands in
  the **interior** — it is the exit of the Moore (curve 1) block in the LR quadrant.

## Result

- **squares: INFEASIBLE.** No swap rule — orientation-independent **or** per-orientation over
  the **full** node space — makes `fill(38, ·)` a valid Hamiltonian path on every `n×n`
  square. The first obstruction is **n = 7**, where the failure is proven by *complete*
  exhaustion (curve 0 is absent, so the 5-node `9⁵` sweep is the entire rule space).
- **swap rule: none exists.** For reference, the best fixed rule `38:(second,first)` with the
  kernels at their good square rules (`3:(first,second), 5:(first,second), 0:(first,first),
  1:(first,first)`) is valid on `n ∈ {1,2,3,4,5,8,11,12,13,16,19,20,21,24,27,28,29,32,35,36,
  37,40}` and fails at `n = 6,7,9,10,14,15,17,18,…` — it can never be repaired at `n = 7`.
- **verified:**
  - orientation-independent per-curve search over `{0,1,3,5,38}` (each one `(sw,sh)`):
    **9⁵ = 59049** combos → **0** valid on `n = 1..15` (fails because Hilbert provably needs a
    per-orientation rule; not the decisive argument).
  - **per-size full per-node freedom** at `n = 7` (5 nodes, each `{first,second,none}²`):
    **9⁵ = 59049** combos → **0** valid (all `disconnected`). This is the impossibility proof.
  - per-size feasibility "does *any* rule connect?": `n=3:✓ 4:✓ 5:✓ 6:✓ 7:✗ 8:✓`.
  - matches hilbertplot at `2^k`: **yes** (`k = 1..5`, exact after `canonical_form`; swaps are inert
    at powers of two since no split is odd).
  - full per-orientation universe size (for the record): **13 nodes ⇒ 9¹³ ≈ 2.5×10¹²**;
    not enumerated — a single impossible size (`n = 7`) already refutes every point of it.
- **quasi-squares** (`|w−h| = 1`): connectivity is orientation-dependent and splits the 8
  orientations into the **non-transposing class** `{e,f,m,y}` and the **transposing class**
  `{a,g,o,x}`. Dominoes and near-dominoes (`2×1, 1×2, 3×2, 2×3`) connect at **all 8**; from
  side ≥ 3 exactly one class (occasionally both) connects, and transposing the region swaps
  the two classes (wide↔tall are exact transposes). Data below.

## Derivation / proof

### Setup — the top-level split and its junctions.
At orientation `e`, `fill(38, n, n)` splits the canonical `n×n` into
`Wc = Wc1+Wc2`, `Hc = Hc1+Hc2` (`|Wc1−Wc2| ≤ 1`, `|Hc1−Hc2| ≤ 1`) and lays the four kernels
in visiting order

```
LL = (0,0,   Wc1,Hc1)  Liu2      →  UL = (0,Hc1, Wc1,Hc2)  Liu4(rev)
                                     ↓                          ↓ junction UL→UR
LR = (Wc1,0, Wc2,Hc1)  Moore  ←  UR = (Wc1,Hc1, Wc2,Hc2) Liu4
```

visited `LL → UL → UR → LR`. The global entry is `LL`'s entry (bottom edge), the global exit
is `LR`'s exit (interior, inside the Moore block). Connectivity requires the three internal
junctions `LL→UL`, `UL→UR`, `UR→LR` each to have exit/entry cells at Manhattan distance 1,
**and** each kernel block to be internally a Hamiltonian path.

### Lemma 1 (the width swap is forced to `second`).
At `n = 5` the full per-node sweep (`9⁵`, all 5 nodes free) admits `3888` valid rules, and the
top node `(38,e)` takes a value in **`{(second,first),(second,none)}` in every one of them**
(projection of the solution set). Geometrically: with `sw = first` the low columns `{LL,UL}`
get the even width and `{UR,LR}` the odd width, which places `UR`'s exit and `LR`'s (Moore)
entry two cells apart — the `UR→LR` junction breaks (Manhattan distance 2). Only `sw = second`
(make the **high**/right column-pair even) brings that junction to distance 1. So **`sw` must
be `second`** at the top for any hope of connectivity.

### Proposition (impossibility at n = 7 — the two-horn conflict).
At `n = 7` the touched nodes are exactly `(1,f),(3,o),(5,y),(5,e),(38,e)` — **Hilbert is not
yet present** — so the rule space is the finite set of `9⁵ = 59049` assignments and can be
enumerated completely. The result:

> **Over all 59049 rules, `fill(38,7,7)` is `disconnected` in every case.**

The mechanism is a contradiction between the `UR→LR` junction and the internal validity of the
Moore (LR) block. Classifying the 59049 rules by the pair
`(all three junctions connect?, all four blocks internally valid?)`:

```
(junctions_ok, internals_ok)  →  count
   (False, False)                36045
   (False, True )                 7452     # blocks fine, but a junction breaks
   (True , False)                15552     # junctions fine, but a block is disconnected
   (True , True )                    0     # never
```

The pair `(True, True)` — the only one that could give a valid path — **never occurs**. The
two horns:
- **Making the junctions connect** forces (Lemma 1) `sw = second`; at `n = 7` this hands the
  Moore block the odd-height rectangle `4×3` (or `3×4`), on which *no* Moore swap rule
  (`3.\text{–}` of the 9) yields a Hamiltonian path with the entry the junction demands — the
  dominant internal failure (13 284 of 15 552 rules) is precisely the **Moore LR block**.
- **Making the Moore block internally valid** (e.g. `sw = second, sh = none/second` gives a
  `4×3` Moore) throws the `UR→LR` junction to distance ≥ 2, or breaks a `Liu` block.

No swap assignment satisfies both simultaneously. A single impossible size refutes the
existence of a universal rule, so **curve 38 does not generalize to arbitrary squares.** ∎

### Why this is *not* the Moore (curve 1) parity obstruction.
Curve 1 is infeasible for a clean 2-colouring reason: on an odd square both path endpoints
must be the majority (black) colour, but Moore's opened-cycle endpoints are 4-adjacent hence
opposite colours. Curve 38 is different. Colour `χ(x,y)=(x+y)\bmod 2`; sweeping all 59049
rules at `n = 7` the reachable endpoint-colour pairs are

```
(χ_entry, χ_exit) counts:  (0,0):5832  (0,1):20412  (1,0):17496  (1,1):15309
```

The legal black–black pair `(0,0)` **is** reachable (5832 rules) — the global parity
condition can be met — yet none of those rules connect. Curve 38's obstruction is therefore a
genuinely combinatorial **junction/interior incompatibility on the odd split**, one level
deeper than a colouring invariant. This is why the proof is by complete finite exhaustion of
the (small) `n = 7` rule space rather than by a counting lemma.

### Structural characterization.
Curve 38 places the **cyclic Moore kernel in its last-visited quadrant and exits in the
interior**. The approximately-even split of an odd side always produces one odd-length side on
the Moore block; the Moore curve — being an opened cycle — cannot present the interior exit
cell demanded by `entry_exit(38) = (edge, interior)` *and* the junction-entry cell demanded by
the preceding `UR` block, for any swap, once the block's odd side appears. Feasible curves in
this program either exit at a **corner** (e.g. Hilbert, curve 0) or keep their odd-side kernels
free of a forced interior endpoint; curve 38 violates both. The infeasibility is thus intrinsic
to the *Moore-in-final-quadrant + interior-exit* structure, independent of the kernel swap
rules.

### Quasi-squares.
For `|w−h| = 1` the connectable orientations split by the transpose classes
`{e,f,m,y}` (non-transposing) and `{a,g,o,x}` (transposing). Transposing the region composes
with the transposing group elements, which is exactly the observed **wide↔tall transpose
symmetry** (e.g. WIDE `4×3` connects on `{e,f,m,y}` ⇔ TALL `3×4` connects on `{a,g,o,x}`). At
the primitive level this is the `2×1` domino (kept by the non-transposing class) vs the `1×2`
domino (kept by the transposing class) constraint — the Wu–Chang `A,C`/`B,D` split. The
connectable class as a function of size is **not** a plain parity: it is all-8 for side ≤ 2,
then follows the same mod-4-flavoured pattern as the square obstruction (data below).

## Evidence

Engine: `research/aep.py`. All runs `cd /home/elessar/Projects/HilbertPlots`.

**Kernels, nodes, endpoints**
```
aep.RULES[38] = LL:(3,o,F)  UL:(5,y,T)  UR:(5,e,F)  LR:(1,f,F)
aep.entry_exit(38) = ('edge','interior')
true node universe (both split parities, n=1..40): 13 nodes
   (38,e); (1,f); (3,o); (5,y),(5,e); (0,e/f/y/m/o/a/g/x)
nodes actually live at n=7: {(1,f),(3,o),(5,y),(5,e),(38,e)}  -- curve 0 ABSENT
```

**Exhaustive swap searches**
```
(A) orientation-independent, curves {0,1,3,5,38} each one (sw,sh): 9^5 = 59049
    -> 0 valid on n=1..15    (Hilbert needs a per-orientation rule; not decisive)
(B) DECISIVE: per-node full freedom at n=7 (5 nodes x {first,second,none}^2): 9^5 = 59049
    -> 0 valid  (validate == 'disconnected' in all 59049)
full per-orientation universe (all 13 nodes): 9^13 ≈ 2.5e12  (not enumerated; n=7 suffices)
```

**Per-size feasibility (does ANY rule connect?), full per-node freedom**
```
n :  3   4    5     6    7    8
sat: 3   9  3888  7776   0   59049      # n=7 is the unique small-size zero
```

**The two-horn conflict at n = 7** (classification of all 59049 rules)
```
(junctions_ok, internals_ok):  (F,F) 36045 | (F,T) 7452 | (T,F) 15552 | (T,T) 0
when (T,F): dominant bad block = LR/Moore(base 1): 13284   (also LL/Liu2 9072, UL/UR/Liu4)
when (F,T): broken junction = UR->LR (4860) or LL->UL (3564)
```

**Not a colouring obstruction** (endpoint colours reachable at n=7 over all 59049 rules)
```
(χ_entry,χ_exit): (0,0):5832  (0,1):20412  (1,0):17496  (1,1):15309
=> black-black (0,0) IS reachable, yet no such rule connects  => combinatorial, not parity
```

**Matches hilbertplot at powers of two**
```
2^k = 2,4,8,16,32 :  canonical_form(fill(38,..)) == canonical_form(hilbertplot.curve(38).points(k))
                     -> True for k=1..5
```

**Quasi-squares** (`|w−h|=1`; some-rule connectivity; D4 codes; nonT = {e,f,m,y}, transp = {a,g,o,x})
```
WIDE w=h+1        nonT            transp
  2x1        {e,f,m,y}        {a,g,o,x}      (all 8)
  3x2        {e,f,m,y}        {a,g,o,x}      (all 8)
  4x3        {e,f,m,y}        --
  5x4        --               {a,g,o,x}
  6x5        --               {a,g,o,x}
  7x6        {e,f,m,y}        {a,g,o,x}      (all 8)
TALL h=w+1        nonT            transp
  1x2        {e,f,m,y}        {a,g,o,x}      (all 8)
  2x3        {e,f,m,y}        {a,g,o,x}      (all 8)
  3x4        --               {a,g,o,x}
  4x5        {e,f,m,y}        --
  5x6        {e,f,m,y}        --
  6x7        {e,f,m,y}        {a,g,o,x}      (all 8)
   => wide(size s) and tall(size s) are exact transposes: nonT<->transp swap.
```

## Open questions

- A closed-form proof that the `n = 7` junction/interior conflict recurs at every non-power-of-two
  odd scale (verified operationally: no fixed rule reaches `n = 40`; and `n = 7` is provably dead).
  Conjecture: the feasible sizes for curve 38 are exactly `{n : the odd-side descent never lands a
  Moore block on an odd side}`, i.e. the powers of two and small exceptions — to be characterized.
- The exact size-indexed law for which quasi-square orientation class connects (the mod-4 pattern),
  proven from the Moore mid-edge domino constraint rather than verified for side ≤ 7.
- Whether the criterion "**cyclic kernel in the final quadrant + interior global exit ⇒ infeasible
  on odd squares**" is the right structural invariant to quote in the 40-curve classification, with
  curve 38 as the canonical Moore-tail instance (contrast curve 1, the pure-Moore parity instance).
```

## Verification

**Adversarial re-check (independent).** Verdict: **CONFIRMED — squares INFEASIBLE.** All
computational claims reproduced exactly; the impossibility argument is logically sound.

**What I re-ran** (engine `research/aep.py`, `.venv/bin/python`, from project root):

1. *Node universe at n = 7, established independently.* I wrote my own branch-enumerator that,
   at every partition node, follows **all three** split parities (`first/second/none`) on each
   axis and records every `(index, M)` with a side > 2. Result: exactly
   `{(1,f), (3,o), (5,y), (5,e), (38,e)}` — 5 nodes, **curve 0 absent**. This confirms the
   report's central structural fact rather than trusting it.
2. *Airtight completeness of the 9⁵ sweep.* I instrumented the `swap` callback to log every node
   `fill(38,7,7,…)` actually queries, across all 59049 assignments. The logged union equals the
   5-node set exactly (`queried_union == set(nodes)` → `True`). Hence the swap function's behaviour
   at n = 7 is **fully** parametrized by those 5 nodes and 9⁵ is the complete rule space — no 6th
   node is ever silently taking the `('first','first')` default.
3. *Decisive exhaustion.* All 59049 per-node assignments at n = 7 →
   **`valid = 0`, every one `disconnected`** (reason breakdown `{'disconnected': 59049}`).
   Reproduced twice (independent scripts).
4. *Supporting evidence reproduced exactly.* Per-size "does any rule connect?" with full per-node
   freedom: `n=3:3, 4:9, 5:3888, 6:7776, 7:0, 8:59049` — matches the report digit-for-digit; n = 7
   is the unique small-size zero. Matches hilbertplot at 2^k for k = 1..5 (True, via `canonical_form`).
   Best fixed rule `38:(second,first)` (kernels `3:(first,second),5:(first,second),0:(first,first),
   1:(first,first)`) valid on exactly
   `{1,2,3,4,5,8,11,12,13,16,19,20,21,24,27,28,29,32,35,36,37,40}` over n = 1..40, failing at n = 7
   — matches the report.

**Attempt to refute (as instructed).** The report claims impossibility, so I actively searched for
*any* working rule. The n = 7 rule space is finite and small (9⁵) and I enumerated it completely
via two independent code paths (report's framing and my own node-collector); both return zero valid
rules. No rule escapes because a swap function's signature is `swap(index, M)` — it **cannot depend
on n** (confirmed against `aep.py` / `context.md`), so its restriction to the 5 live nodes at n = 7
is necessarily one of the 9⁵ assignments, all of which are disconnected.

**Logical soundness of the impossibility.** The verdict rests only on: (i) the swap rule cannot see
the size; (ii) at n = 7 exactly 5 nodes are live (independently verified, incl. instrumented
coverage); (iii) all 9⁵ assignments over those nodes fail. A universal square rule would have to
succeed at n = 7, which is impossible — one dead size refutes universality. This core argument is
**airtight** and does **not** depend on the report's finer heuristic claims (Lemma 1's "sw =
second", the two-horn (T,F)/(F,T) sub-counts, the colouring reachability table). Those are
plausible supporting colour but are not load-bearing for the verdict; I did not separately re-derive
the (36045/7452/15552/0) breakdown, though its only load-bearing entry, `(True,True)=0`, is
equivalent to the confirmed `valid = 0`.

**Caveats (unchanged from report, correctly scoped).** Infeasibility is *proved* only in the sense
that n = 7 admits no rule; the report's stronger conjecture — that the obstruction recurs at every
non-power-of-two odd scale — remains an open question, correctly flagged as such and not claimed as
proven. The "cyclic-kernel-in-final-quadrant + interior-exit" structural characterization is a
heuristic narrative, not a proof, and is presented that way. No overclaiming detected.

*Scripts:* `…/scratchpad/verify38.py` (node collector), `verify38b.py`/`verify38c.py` (9⁵ sweep +
coverage instrumentation), `verify38d.py` (per-size + 2^k).
