"""Shared engine for the arbitrary-size (Hilbert*) generalization study.

This is the single source of truth every research agent uses.  It generalizes
Wu & Chang's approximately-even-partition Hilbert* construction (IET Image Process.
6(6) 2012) from the standard Hilbert curve to ALL forty hilbertplot curves, driven by
hilbertplot's catalog quadrant rules and the full dihedral group D4.

Terminology (fixed across all reports)
--------------------------------------
* A curve `index` (0..39) has four quadrant rules ``(base, morphism, reverse)`` for
  quadrants LL, UL, UR, LR (lower-left, upper-left, upper-right, lower-right), visited
  in that order (the paper's Fig 6 case A == hilbertplot's rules: e=A, delta_o=B, delta_f=C,
  delta_a=D).
* An ORIENTATION is a D4 element (one of 8), stored as a 2x2 integer matrix.
* A region is an axis-aligned rectangle (x0, y0, width w, height h).
* APPROXIMATELY-EVEN PARTITION of a length d: ``d1 = d//2, d2 = d-d1`` (|d1-d2|<=1).
* SWAP RULE: when a side is odd, which half is made even.  Encoded per axis as one of
  ``"first"`` (make d1 even), ``"second"`` (make d2 even), ``"none"`` (no swap).  The
  central research object is: for each curve and orientation, which swap rule (if any)
  yields a single connected space-filling path.

The recursion works in the curve's CANONICAL frame (orientation = identity) and applies
the orientation matrix M to place cells; sub-curve orientation = M . morphism_i.
"""

from __future__ import annotations

import itertools

import numpy as np

import hilbertplot
from hilbertplot._core.catalog import SPECS
from hilbertplot._core.symmetry import MORPHISMS

# ---- D4 matrices (act on column (x, y): new = M @ (x, y)) -------------------
MAT = {code: (tuple(s.matrix[0]), tuple(s.matrix[1])) for code, s in MORPHISMS.items()}
IDENT = MAT["e"]
D4 = list({m for m in MAT.values()})  # the 8 distinct matrices

# ---- catalog rules: index -> [(base, morphism-matrix, reverse) for LL,UL,UR,LR] ----
RULES = {s.index: [(q.base, MAT[q.morphism], q.reverse) for q in s.quadrants] for s in SPECS}
NAME = {s.index: s.name for s in SPECS}


def matmul(A, B):
    return ((A[0][0]*B[0][0]+A[0][1]*B[1][0], A[0][0]*B[0][1]+A[0][1]*B[1][1]),
            (A[1][0]*B[0][0]+A[1][1]*B[1][0], A[1][0]*B[0][1]+A[1][1]*B[1][1]))


def apply_pt(M, x, y):
    return (M[0][0]*x + M[0][1]*y, M[1][0]*x + M[1][1]*y)


# ---- base primitives (canonical order for a Wc x Hc box, Wc,Hc in {1,2}) ----
def base_cells(Wc, Hc):
    if (Wc, Hc) == (1, 1): return [(0, 0)]
    if (Wc, Hc) == (2, 1): return [(0, 0), (1, 0)]                 # wide domino
    if (Wc, Hc) == (1, 2): return [(0, 0), (0, 1)]                 # tall domino
    if (Wc, Hc) == (2, 2): return [(0, 0), (0, 1), (1, 1), (1, 0)] # canonical U (orientation A)
    raise ValueError((Wc, Hc))


def _mapper(M, Wc, Hc, x0, y0):
    corners = [apply_pt(M, cx, cy) for cx in (0, Wc-1) for cy in (0, Hc-1)]
    mnx = min(c[0] for c in corners); mny = min(c[1] for c in corners)
    return lambda cx, cy: (x0 + apply_pt(M, cx, cy)[0] - mnx, y0 + apply_pt(M, cx, cy)[1] - mny)


def _split(dim, mode):
    d1 = dim // 2; d2 = dim - d1
    if mode == "first" and d1 % 2 == 1: d1, d2 = d2, d1
    elif mode == "second" and d2 % 2 == 1: d1, d2 = d2, d1
    return d1, d2


def fill(index, x0, y0, w, h, M, rev, swap):
    """Return the ordered list of (x,y) cells for curve `index` on region
    (x0,y0,w,h) with orientation matrix M (reversed if `rev`).

    `swap` is a callable ``swap(index, M) -> (sw, sh)`` giving the swap rule for the
    canonical width- and height-split when partitioning this curve at this orientation.
    """
    transpose = (M[0][0] == 0)
    Wc, Hc = (h, w) if transpose else (w, h)
    if w <= 2 and h <= 2:
        f = _mapper(M, Wc, Hc, x0, y0)
        cells = [f(cx, cy) for (cx, cy) in base_cells(Wc, Hc)]
        return cells[::-1] if rev else cells
    sw, sh = swap(index, M)
    Wc1, Wc2 = _split(Wc, sw)
    Hc1, Hc2 = _split(Hc, sh)
    boxes = [(0, 0, Wc1, Hc1), (0, Hc1, Wc1, Hc2), (Wc1, Hc1, Wc2, Hc2), (Wc1, 0, Wc2, Hc1)]
    f = _mapper(M, Wc, Hc, x0, y0)
    order = [0, 1, 2, 3] if not rev else [3, 2, 1, 0]
    out = []
    for i in order:
        base_i, morph_i, revi = RULES[index][i]
        cx0, cy0, cw, ch = boxes[i]
        pts = [f(cx0, cy0), f(cx0+cw-1, cy0), f(cx0, cy0+ch-1), f(cx0+cw-1, cy0+ch-1)]
        axs = [p[0] for p in pts]; ays = [p[1] for p in pts]
        ax0, ay0 = min(axs), min(ays)
        aw, ah = max(axs)-ax0+1, max(ays)-ay0+1
        out += fill(base_i, ax0, ay0, aw, ah, matmul(M, morph_i), revi ^ rev, swap)
    return out


# ---- validation ------------------------------------------------------------
def validate(cells, w, h):
    """Return "OK" if `cells` is a Hamiltonian path over the w x h grid, else a reason."""
    if len(cells) != w * h: return f"count {len(cells)}!={w*h}"
    if len(set(cells)) != w * h: return "not distinct"
    xs = [c[0] for c in cells]; ys = [c[1] for c in cells]
    if (min(xs), min(ys), max(xs), max(ys)) != (0, 0, w-1, h-1): return "bbox"
    for a, b in zip(cells, cells[1:]):
        if abs(a[0]-b[0]) + abs(a[1]-b[1]) != 1: return "disconnected"
    return "OK"


# ---- swap-rule helpers -----------------------------------------------------
def const_swap(rules):
    """rules: dict index -> (sw, sh). A swap function independent of orientation."""
    return lambda index, M: rules.get(index, ("first", "first"))


def per_orientation_swap(rules):
    """rules: dict (index, M) -> (sw, sh); falls back to ('first','first')."""
    return lambda index, M: rules.get((index, M), ("first", "first"))


def square_valid(index, swap, sizes=range(1, 14), check_2k=True):
    """True iff curve `index` is a valid Hamiltonian path on every n x n in `sizes`
    (and matches hilbertplot's 2^k curve up to symmetry when check_2k)."""
    from hilbertplot._core.geometry import canonical_form
    for n in sizes:
        if validate(fill(index, 0, 0, n, n, IDENT, False, swap), n, n) != "OK":
            return False
    if check_2k:
        for k in (1, 2, 3):
            a = canonical_form(np.array(fill(index, 0, 0, 2**k, 2**k, IDENT, False, swap)))
            if a != canonical_form(hilbertplot.curves.points(index, k)):
                return False
    return True


def search_const_square_swap(index, swap, sizes=range(1, 14)):
    """Search a single orientation-independent (sw, sh) for `index` (kernels via `swap`).
    Returns (sw, sh) or None. Mutates nothing; caller installs the result."""
    from copy import copy
    for sw, sh in itertools.product(["first", "second", "none"], repeat=2):
        base = swap  # closure captures rules dict; build a trial
        trial_rules = dict(getattr(swap, "_rules", {}))
        # Rebuild as const on top of existing kernel rules is caller's job; here we
        # just test a const rule for this index layered over `swap` for other indices.
        def trial(i, M, _sw=sw, _sh=sh, _idx=index, _base=swap):
            return (_sw, _sh) if i == _idx else _base(i, M)
        if square_valid(index, trial, sizes):
            return (sw, sh)
    return None


# ---- entry/exit structure (the key to feasibility proofs) ------------------
def endpoint_type(cell, side):
    x, y = int(cell[0]), int(cell[1])
    on = (x in (0, side-1)) + (y in (0, side-1))
    return ("interior", "edge", "corner")[on]


def entry_exit(index, order=5):
    """(entry_type, exit_type) of curve `index` on its 2^order grid: corner/edge/interior."""
    pts = hilbertplot.curves.points(index, order)
    side = 2**order
    return endpoint_type(pts[0], side), endpoint_type(pts[-1], side)


def orientations_used(index, sizes=range(3, 12, 2)):
    """Set of (curve, orientation-matrix) partition nodes encountered when drawing
    `index` on odd squares -- i.e. which (curve, orientation) pairs need a swap rule."""
    seen = set()
    def rec(idx, w, h, M):
        transpose = (M[0][0] == 0)
        Wc, Hc = (h, w) if transpose else (w, h)
        if w <= 2 and h <= 2:
            return
        seen.add((idx, M))
        Wc1, Wc2 = Wc // 2, Wc - Wc // 2
        Hc1, Hc2 = Hc // 2, Hc - Hc // 2
        boxes = [(Wc1, Hc1), (Wc1, Hc2), (Wc2, Hc2), (Wc2, Hc1)]
        for i, (cw, ch) in enumerate(boxes):
            base_i, morph_i, _ = RULES[idx][i]
            # sub width/height in absolute frame depends on transpose of M.morph
            subM = matmul(M, morph_i)
            st = (subM[0][0] == 0)
            aw, ah = (ch, cw) if st else (cw, ch)
            rec(base_i, aw, ah, subM)
    for n in sizes:
        rec(index, n, n, IDENT)
    return seen


if __name__ == "__main__":
    # self-check: curve 0 with the paper's rule, and the 8 known-good curves
    swap0 = const_swap({0: ("first", "first")})
    print("curve 0 squares valid:", square_valid(0, swap0))
    known = {0: ("first", "first"), 3: ("first", "second"), 5: ("first", "second"),
             24: ("first", "second"), 31: ("first", "second"),
             4: ("second", "first"), 29: ("second", "first"), 30: ("second", "first")}
    sw = const_swap(known)
    for i in sorted(known):
        print(f"  curve {i:2} ({NAME[i]:14}) const-swap {known[i]}: valid={square_valid(i, sw)}")
    print("entry/exit types:")
    for i in range(40):
        print(f"  {i:2} {NAME[i]:18} {entry_exit(i)}")
