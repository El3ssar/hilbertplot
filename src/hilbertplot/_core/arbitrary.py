"""Arbitrary-size (non-power-of-two) square generation for the curves that support it.

Only eight of the forty curves can be laid on an arbitrary ``n x n`` square as a single
connected space-filling path (the rest are provably obstructed -- see
``research/quasisquares/``). This module implements the approximately-even-partition
(AEP) construction of Wu & Chang, generalized to those eight curves via the catalog
quadrant rules and the full dihedral group ``D4``, with a per-curve *swap rule* that
keeps the path connected at odd sizes.

Public surface is the :meth:`hilbertplot.Curve.grid` method and the :func:`hilbertplot.generalizing`
group; this module is the engine behind them.  ``grid(2**k)`` reproduces the standard
``points(k)`` curve exactly for all eight, so the two are interchangeable.
"""

from __future__ import annotations

import numpy as np

from .catalog import SPECS
from .symmetry import MORPHISMS

#: The eight curves that tile arbitrary squares (proved in research/quasisquares/).
FEASIBLE: frozenset[int] = frozenset({0, 3, 4, 5, 24, 29, 30, 31})

#: The size-independent swap rule for each feasible curve: (width-split, height-split),
#: each in {"first" = force low half even, "second" = high half even, "none"}.
_SWAP: dict[int, tuple[str, str]] = {
    0: ("first", "first"), 3: ("first", "second"), 4: ("second", "first"),
    5: ("first", "second"), 24: ("first", "second"), 29: ("second", "first"),
    30: ("second", "first"), 31: ("first", "second"),
}

#: For each infeasible curve, a small square size at which it provably fails (for messages).
WITNESS: dict[int, int] = {
    1: 7, 2: 7, 6: 3, 7: 9, 8: 3, 9: 5, 10: 5, 11: 5, 12: 3, 13: 5, 14: 3, 15: 5,
    16: 7, 17: 5, 18: 13, 19: 7, 20: 7, 21: 13, 22: 7, 23: 9, 25: 13, 26: 7, 27: 7,
    28: 13, 32: 5, 33: 5, 34: 5, 35: 5, 36: 5, 37: 3, 38: 7, 39: 14,
}

# D4 matrices (act on column (x, y): new = M @ (x, y)) and catalog rules.
_MAT = {code: (tuple(s.matrix[0]), tuple(s.matrix[1])) for code, s in MORPHISMS.items()}
_IDENT = _MAT["e"]
_RULES = {s.index: [(q.base, _MAT[q.morphism], q.reverse) for q in s.quadrants] for s in SPECS}


def _matmul(A, B):
    return ((A[0][0]*B[0][0]+A[0][1]*B[1][0], A[0][0]*B[0][1]+A[0][1]*B[1][1]),
            (A[1][0]*B[0][0]+A[1][1]*B[1][0], A[1][0]*B[0][1]+A[1][1]*B[1][1]))


# Canonical base-tile visit orders (Wc, Hc) -> cells; the 2x2 is orientation A's U.
_BASE = {(1, 1): ((0, 0),), (2, 1): ((0, 0), (1, 0)), (1, 2): ((0, 0), (0, 1)),
         (2, 2): ((0, 0), (0, 1), (1, 1), (1, 0))}
_ORDER = (0, 1, 2, 3)
_ORDER_REV = (3, 2, 1, 0)


def _fill(index, x0, y0, w, h, M, rev, out):
    """Append the (x, y) cells of curve `index` on region (x0,y0,w,h), orientation `M`,
    to the list `out` (reversed if `rev`).  Hot path -- all affine maths is inlined."""
    (a, b), (c, d) = M
    Wc, Hc = (h, w) if a == 0 else (w, h)
    # translate so the canonical box maps into the region's own frame (D4 matrices only)
    ox = x0 - ((a * (Wc - 1) if a < 0 else 0) + (b * (Hc - 1) if b < 0 else 0))
    oy = y0 - ((c * (Wc - 1) if c < 0 else 0) + (d * (Hc - 1) if d < 0 else 0))
    if w <= 2 and h <= 2:
        cells = _BASE[(Wc, Hc)]
        mapped = [(ox + a * cx + b * cy, oy + c * cx + d * cy) for (cx, cy) in cells]
        out.extend(reversed(mapped) if rev else mapped)
        return
    sw, sh = _SWAP.get(index, ("first", "first"))
    Wc1 = Wc // 2; Wc2 = Wc - Wc1
    if sw == "first" and Wc1 & 1: Wc1, Wc2 = Wc2, Wc1
    elif sw == "second" and Wc2 & 1: Wc1, Wc2 = Wc2, Wc1
    Hc1 = Hc // 2; Hc2 = Hc - Hc1
    if sh == "first" and Hc1 & 1: Hc1, Hc2 = Hc2, Hc1
    elif sh == "second" and Hc2 & 1: Hc1, Hc2 = Hc2, Hc1
    boxes = ((0, 0, Wc1, Hc1), (0, Hc1, Wc1, Hc2), (Wc1, Hc1, Wc2, Hc2), (Wc1, 0, Wc2, Hc1))
    rules = _RULES[index]
    for i in (_ORDER_REV if rev else _ORDER):
        base_i, morph_i, revi = rules[i]
        cx0, cy0, cw, ch = boxes[i]
        x1 = cx0 + cw - 1; y1 = cy0 + ch - 1
        # absolute bounding box of the four transformed sub-box corners
        u0 = ox + a * cx0 + b * cy0; u1 = ox + a * x1 + b * cy0
        u2 = ox + a * cx0 + b * y1; u3 = ox + a * x1 + b * y1
        v0 = oy + c * cx0 + d * cy0; v1 = oy + c * x1 + d * cy0
        v2 = oy + c * cx0 + d * y1; v3 = oy + c * x1 + d * y1
        axmin = u0 if u0 < u1 else u1
        if u2 < axmin: axmin = u2
        if u3 < axmin: axmin = u3
        axmax = u0 if u0 > u1 else u1
        if u2 > axmax: axmax = u2
        if u3 > axmax: axmax = u3
        aymin = v0 if v0 < v1 else v1
        if v2 < aymin: aymin = v2
        if v3 < aymin: aymin = v3
        aymax = v0 if v0 > v1 else v1
        if v2 > aymax: aymax = v2
        if v3 > aymax: aymax = v3
        _fill(base_i, axmin, aymin, axmax - axmin + 1, aymax - aymin + 1,
              _matmul(M, morph_i), revi ^ rev, out)


def square_points(index: int, n: int) -> np.ndarray:
    """Return the ``(n*n, 2)`` cell path of feasible curve ``index`` on an ``n x n`` grid.

    The caller is responsible for checking ``index in FEASIBLE`` and ``n >= 1``.
    """
    if n == 1:
        return np.zeros((1, 2), dtype=np.int64)
    out: list = []
    _fill(index, 0, 0, n, n, _IDENT, False, out)
    return np.array(out, dtype=np.int64)
