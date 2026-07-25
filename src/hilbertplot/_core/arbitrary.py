"""Arbitrary-size (non-power-of-two) square generation for the curves that support it.

Only eight of the forty curves can be laid on an arbitrary ``n x n`` square as a single
connected space-filling path (the rest are provably obstructed -- see
``research/quasisquares/``).  This module implements the approximately-even-partition
(AEP) construction of Wu & Chang, generalized to those eight curves via the catalog
quadrant rules and the full dihedral group ``D4``, with a per-curve *swap rule* that
keeps the path connected at odd sizes.

Public surface is the :meth:`hilbertplot.Curve.grid` method and the
:func:`hilbertplot.generalizing` group; this module is the engine behind them.
``grid(2**k)`` reproduces the standard ``points(k)`` curve exactly for all eight, so the
two are interchangeable.

How the construction works
--------------------------
Filling a region is a recursion over *oriented* regions.  A region is described by its
absolute origin ``(x0, y0)``, its width and height, an orientation ``M`` (an element of
``D4``, as a 2x2 signed permutation matrix) and a reversal flag:

1. **Canonical extent.** The curve is defined in its own frame; ``M`` maps that frame
   onto the region.  If ``M`` swaps the axes the canonical extent is ``(h, w)``,
   otherwise ``(w, h)`` -- see :func:`_canonical_extent`.
2. **Canonical origin.** ``M`` sends the canonical box onto the region, but a rotation
   or reflection moves the minimum corner, so the canonical origin has to be offset to
   put the image's minimum corner back at ``(x0, y0)`` -- see :func:`_canonical_origin`.
3. **Base case.** A region of at most ``2 x 2`` cells is emitted directly from the
   canonical visit orders in :data:`_BASE_TILES`.
4. **Split.** Otherwise the canonical extent is cut into four sub-boxes, each side split
   as evenly as possible.  When a half would come out odd, the curve's *swap rule*
   decides which half absorbs the odd cell; this is what keeps the path connected at
   odd sizes.  The four sub-boxes are laid out as quadrants ``0``=bottom-left,
   ``1``=top-left, ``2``=top-right, ``3``=bottom-right *in the canonical frame*, matching
   the quadrant numbering of the catalog.
5. **Recurse.** Each quadrant recurses into its catalog rule's kernel curve, with the
   morphism composed onto ``M`` and the reversal flag xor-ed in.  Quadrants are visited
   in order ``0, 1, 2, 3``, or in reverse when the region itself is reversed.

Performance
-----------
A naive recursion bottoms out once per cell, which costs a Python frame per cell and is
what made ``grid(1024)`` take the better part of a second.  Instead, :func:`_emit`
recurses only until a region is small enough (:data:`_BLOCK_CELLS`) and then copies a
*memoised block* into a preallocated output array.

The memo works because a sub-region's cell pattern depends only on
``(index, width, height, M, reversed)`` -- never on its absolute position, which enters
solely as a translation.  Since the AEP split produces only a handful of distinct
extents, one ``grid(n)`` call solves a couple of dozen distinct blocks and then does
pure numpy adds, making the whole thing roughly a hundred times faster than the
per-cell recursion while producing bit-identical output.
"""

from __future__ import annotations

import numpy as np

from .catalog import SPECS
from .symmetry import MORPHISMS

__all__ = ["FEASIBLE", "SMALLEST_FAILURE", "square_points"]

#: The eight curves that tile arbitrary squares (proved in research/quasisquares/).
FEASIBLE: frozenset[int] = frozenset({0, 3, 4, 5, 24, 29, 30, 31})

#: The size-independent swap rule for each feasible curve: ``(width-split, height-split)``.
#: ``"first"`` forces the low half even, ``"second"`` the high half even.
_SWAP: dict[int, tuple[str, str]] = {
    0: ("first", "first"),
    3: ("first", "second"),
    4: ("second", "first"),
    5: ("first", "second"),
    24: ("first", "second"),
    29: ("second", "first"),
    30: ("second", "first"),
    31: ("first", "second"),
}

#: Swap rule used for kernel curves that are not themselves feasible.
_DEFAULT_SWAP: tuple[str, str] = ("first", "first")

#: For each infeasible curve, the **smallest** square side at which the construction
#: actually breaks -- the number :meth:`hilbertplot.Curve.grid` quotes when it refuses.
#:
#: Every entry is verified by ``tests/test_arbitrary.py`` to be exactly the smallest ``n``
#: for which the path is not Hamiltonian, so the error message cannot drift into a
#: falsehood.  Note this is a weaker statement than the *impossibility witnesses* in
#: ``research/RESULTS.md``, which record the size at which an exhaustive search over swap
#: rules proves no rule can work; several of those sizes are individually fillable.
SMALLEST_FAILURE: dict[int, int] = {
    1: 3, 2: 5, 6: 3, 7: 7, 8: 7, 9: 3, 10: 3, 11: 3,
    12: 7, 13: 3, 14: 7, 15: 3, 16: 3, 17: 3, 18: 11, 19: 7,
    20: 7, 21: 3, 22: 3, 23: 3, 25: 3, 26: 3, 27: 7, 28: 11,
    32: 5, 33: 3, 34: 5, 35: 3, 36: 5, 37: 3, 38: 5, 39: 3,
}  # fmt: skip

# A D4 element as a plain nested tuple, so it is hashable and cheap to multiply.
Matrix = tuple[tuple[int, int], tuple[int, int]]

_MATRICES: dict[str, Matrix] = {
    code: (tuple(sym.matrix[0]), tuple(sym.matrix[1]))  # type: ignore[misc]
    for code, sym in MORPHISMS.items()
}
_IDENTITY: Matrix = _MATRICES["e"]

# Per curve, the four quadrant rules as (kernel index, morphism matrix, reverse).
_RULES: dict[int, tuple[tuple[int, Matrix, bool], ...]] = {
    spec.index: tuple((q.base, _MATRICES[q.morphism], q.reverse) for q in spec.quadrants)
    for spec in SPECS
}

#: Canonical visit orders for the degenerate tiles, keyed by canonical ``(width, height)``.
#: The ``2 x 2`` entry is the "U" traversal of orientation A.
_BASE_TILES: dict[tuple[int, int], tuple[tuple[int, int], ...]] = {
    (1, 1): ((0, 0),),
    (2, 1): ((0, 0), (1, 0)),
    (1, 2): ((0, 0), (0, 1)),
    (2, 2): ((0, 0), (0, 1), (1, 1), (1, 0)),
}

_FORWARD = (0, 1, 2, 3)
_REVERSED = (3, 2, 1, 0)

#: Recurse in Python down to regions of at most this many cells, then use a memoised
#: block.  Tuned empirically: smaller pays more Python frames, larger inflates the memo.
_BLOCK_CELLS = 4096


def _compose(left: Matrix, right: Matrix) -> Matrix:
    """Return the matrix product ``left @ right``."""
    (a, b), (c, d) = left
    (e, f), (g, h) = right
    return ((a * e + b * g, a * f + b * h), (c * e + d * g, c * f + d * h))


def _canonical_extent(matrix: Matrix, width: int, height: int) -> tuple[int, int]:
    """Return the region's extent in the curve's own frame.

    ``matrix`` is a signed permutation; when it swaps the axes (its top-left entry is
    zero) the canonical width is the region's height and vice versa.
    """
    return (height, width) if matrix[0][0] == 0 else (width, height)


def _canonical_origin(
    matrix: Matrix, x0: int, y0: int, canonical_width: int, canonical_height: int
) -> tuple[int, int]:
    """Return the absolute position of the canonical frame's origin.

    ``matrix`` maps the canonical box onto the region, but a rotation or reflection
    moves the minimum corner away from the origin.  Because ``matrix`` is a signed
    permutation, the minimum of ``a*cx + b*cy`` over the box is reached at the extreme
    of whichever coordinate has a negative coefficient; subtracting that minimum puts
    the image's lower-left corner back on ``(x0, y0)``.
    """
    (a, b), (c, d) = matrix
    dx = (a * (canonical_width - 1) if a < 0 else 0) + (b * (canonical_height - 1) if b < 0 else 0)
    dy = (c * (canonical_width - 1) if c < 0 else 0) + (d * (canonical_height - 1) if d < 0 else 0)
    return x0 - dx, y0 - dy


def _split(length: int, rule: str) -> tuple[int, int]:
    """Split ``length`` into two near-equal halves, honouring a swap ``rule``.

    The halves are ``length // 2`` and the remainder.  When ``length`` is **odd** the two
    halves differ in parity, and ``rule="first"`` makes the *low* half even while
    ``rule="second"`` makes the *high* half even, swapping them when needed; forcing that
    parity is what keeps the path connected.  When ``length`` is even both halves already
    share a parity, so the swap cannot change anything and the rule has no effect.
    """
    low = length // 2
    high = length - low
    if (rule == "first" and low & 1) or (rule == "second" and high & 1):
        return high, low
    return low, high


def _child_regions(
    index: int, matrix: Matrix, width: int, height: int
) -> tuple[tuple[int, Matrix, bool, int, int, int, int], ...]:
    """Return the four child regions of an oriented region, in quadrant order.

    Each entry is ``(kernel index, child matrix, child reversal, dx, dy, width, height)``
    where ``dx, dy`` is the child's offset relative to this region's own minimum corner,
    so a caller adds its own absolute origin.
    """
    (a, b), (c, d) = matrix
    canonical_width, canonical_height = _canonical_extent(matrix, width, height)
    origin_x, origin_y = _canonical_origin(matrix, 0, 0, canonical_width, canonical_height)

    swap_width, swap_height = _SWAP.get(index, _DEFAULT_SWAP)
    low_w, high_w = _split(canonical_width, swap_width)
    low_h, high_h = _split(canonical_height, swap_height)
    # Quadrants in the canonical frame: 0 bottom-left, 1 top-left, 2 top-right, 3 bottom-right.
    boxes = (
        (0, 0, low_w, low_h),
        (0, low_h, low_w, high_h),
        (low_w, low_h, high_w, high_h),
        (low_w, 0, high_w, low_h),
    )

    children = []
    for (kernel, morphism, reverse), (cx, cy, cw, ch) in zip(_RULES[index], boxes, strict=True):
        # Transform the box's four corners and take the axis-aligned bounding box.
        x1, y1 = cx + cw - 1, cy + ch - 1
        xs = (
            origin_x + a * cx + b * cy,
            origin_x + a * x1 + b * cy,
            origin_x + a * cx + b * y1,
            origin_x + a * x1 + b * y1,
        )
        ys = (
            origin_y + c * cx + d * cy,
            origin_y + c * x1 + d * cy,
            origin_y + c * cx + d * y1,
            origin_y + c * x1 + d * y1,
        )
        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)
        children.append(
            (
                kernel,
                _compose(matrix, morphism),
                reverse,
                x_min,
                y_min,
                x_max - x_min + 1,
                y_max - y_min + 1,
            )
        )
    return tuple(children)


def _block(
    index: int,
    width: int,
    height: int,
    matrix: Matrix,
    reverse: bool,
    memo: dict[tuple[int, int, int, Matrix, bool], np.ndarray],
) -> np.ndarray:
    """Return the ``(width*height, 2)`` cells of an oriented region, relative to its corner.

    Memoised on the region's *shape* -- absolute position never enters, since it is a
    pure translation the caller adds.  The returned array is read-only and shared.
    """
    key = (index, width, height, matrix, reverse)
    cached = memo.get(key)
    if cached is not None:
        return cached

    if width <= 2 and height <= 2:
        (a, b), (c, d) = matrix
        canonical_width, canonical_height = _canonical_extent(matrix, width, height)
        origin_x, origin_y = _canonical_origin(matrix, 0, 0, canonical_width, canonical_height)
        cells = [
            (origin_x + a * cx + b * cy, origin_y + c * cx + d * cy)
            for cx, cy in _BASE_TILES[canonical_width, canonical_height]
        ]
        if reverse:
            cells.reverse()
        block = np.array(cells, dtype=np.int64)
    else:
        children = _child_regions(index, matrix, width, height)
        parts = []
        for i in _REVERSED if reverse else _FORWARD:
            kernel, child_matrix, child_reverse, dx, dy, cw, ch = children[i]
            sub = _block(kernel, cw, ch, child_matrix, child_reverse ^ reverse, memo)
            parts.append(sub + np.array((dx, dy), dtype=np.int64))
        block = np.concatenate(parts)

    block.flags.writeable = False  # memoised; never mutate in place
    memo[key] = block
    return block


def _emit(
    index: int,
    x0: int,
    y0: int,
    width: int,
    height: int,
    matrix: Matrix,
    reverse: bool,
    out: np.ndarray,
    cursor: list[int],
    memo: dict[tuple[int, int, int, Matrix, bool], np.ndarray],
) -> None:
    """Write the cells of an oriented region into ``out``, advancing ``cursor``.

    Recurses in Python only while the region is larger than :data:`_BLOCK_CELLS`; below
    that it translates a memoised block straight into the output slice.
    """
    if width * height <= _BLOCK_CELLS:
        block = _block(index, width, height, matrix, reverse, memo)
        start = cursor[0]
        stop = start + block.shape[0]
        np.add(block, np.array((x0, y0), dtype=np.int64), out=out[start:stop])
        cursor[0] = stop
        return

    children = _child_regions(index, matrix, width, height)
    for i in _REVERSED if reverse else _FORWARD:
        kernel, child_matrix, child_reverse, dx, dy, cw, ch = children[i]
        _emit(
            kernel,
            x0 + dx,
            y0 + dy,
            cw,
            ch,
            child_matrix,
            child_reverse ^ reverse,
            out,
            cursor,
            memo,
        )


def square_points(index: int, n: int) -> np.ndarray:
    """Return the ``(n*n, 2)`` cell path of feasible curve ``index`` on an ``n x n`` grid.

    The caller is responsible for checking ``index in FEASIBLE`` and ``n >= 1``.
    """
    if n == 1:
        return np.zeros((1, 2), dtype=np.int64)
    out = np.empty((n * n, 2), dtype=np.int64)
    _emit(index, 0, 0, n, n, _IDENTITY, False, out, [0], {})
    return out
