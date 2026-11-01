"""Single-cell index <-> coordinate conversion, without building the whole curve.

:meth:`hilbertplot._core.curve.Curve.points` materialises all ``4**order`` cells, which is the right
thing when you want the whole path but hopeless when you only want to know *where step
i lands* -- at order 30 the path has 10^18 cells and cannot be built at all.

The two functions here answer that question in ``O(order)`` arithmetic for **all forty**
curves, working straight off the catalog's quadrant rules:

* :func:`encode` -- step index ``i`` to the cell ``(x, y)`` the curve reaches at that step;
* :func:`decode` -- cell ``(x, y)`` to the step index at which the curve reaches it.

They are exact inverses of each other and agree with ``points(order)`` cell for cell.
Because they are pure Python integer arithmetic they work at any order the machine can
hold coordinates for, far beyond what :meth:`~hilbertplot._core.curve.Curve.points` can materialise.

How it works
------------
An order ``k`` curve visits its four quadrants in the order ``0, 1, 2, 3`` (bottom-left,
top-left, top-right, bottom-right), spending ``4**(k-1)`` consecutive steps in each.  So
the leading base-4 digit of ``i`` picks the quadrant and the rest is the step index
*within* that quadrant's sub-curve.  Each quadrant is a kernel curve with a morphism and
possibly a reversion applied (see :mod:`hilbertplot._core.catalog`), so descending one
level means: pick the digit, undo the reversion on the remaining index, and remember the
morphism to apply to the coordinates on the way back up.

Reversion needs care when decoding.  A reversed quadrant complements its local index,
``i_local = 4**(k-1) - 1 - j``, and complementing distributes over the base-4 digits:
``4**k - 1 - (q * 4**(k-1) + inner) == (3 - q) * 4**(k-1) + (4**(k-1) - 1 - inner)``.
So a reversal at one level flips the digit written there *and* propagates a complement
to everything below it.  :func:`decode` therefore carries a single ``flipped`` parity
bit instead of recursing.
"""

from __future__ import annotations

from .catalog import QUADRANT_MATRICES, Matrix

__all__ = ["decode", "encode"]

#: Quadrant offsets in units of the half-side: 0 bottom-left, 1 top-left, 2 top-right,
#: 3 bottom-right -- the catalog's quadrant numbering.
_QUADRANT_OFFSET: tuple[tuple[int, int], ...] = ((0, 0), (0, 1), (1, 1), (1, 0))
_OFFSET_TO_QUADRANT: dict[tuple[int, int], int] = {
    offset: q for q, offset in enumerate(_QUADRANT_OFFSET)
}


def _origin_shift(matrix: Matrix, side: int) -> tuple[int, int]:
    """Return the translation that keeps ``matrix`` mapping a ``side`` box onto itself.

    A rotation or reflection moves the box's minimum corner off the origin; since
    ``matrix`` is a signed permutation the minimum of each row is reached at the extreme
    of whichever coordinate has a negative coefficient.

    Parameters
    ----------
    matrix : tuple of tuple of int
        Two-by-two integer orientation matrix.
    side : int or None
        Square side in cells, or None when an order determines it.

    Returns
    -------
    tuple of int
        Translation keeping transformed coordinates inside the same square.
    """
    (a, b), (c, d) = matrix
    dx = (a * (side - 1) if a < 0 else 0) + (b * (side - 1) if b < 0 else 0)
    dy = (c * (side - 1) if c < 0 else 0) + (d * (side - 1) if d < 0 else 0)
    return -dx, -dy


def encode(index: int, i: int, order: int) -> tuple[int, int]:
    """Return the ``(x, y)`` cell that curve ``index`` visits at step ``i``.

    Runs in ``O(order)`` without materialising the curve.

    Parameters
    ----------
    index : int
        Curve number, ``0``..``39``.
    i : int
        Step along the curve, ``0 <= i < 4**order``.
    order : int
        Recursion depth ``>= 0``.

    Returns
    -------
    tuple of int
        The cell ``(x, y)``, with both coordinates in ``0``..``2**order - 1``.
    """
    # Descend, recording which quadrant each level lands in, then rebuild coordinates
    # from the innermost level outwards.
    descent: list[tuple[int, Matrix, int]] = []
    curve_index, remaining, level = index, i, order
    while level > 0:
        span = 1 << (2 * (level - 1))  # 4**(level-1) steps per quadrant
        quadrant, local = divmod(remaining, span)
        kernel, morphism, reverse = QUADRANT_MATRICES[curve_index][quadrant]
        if reverse:
            local = span - 1 - local
        descent.append((quadrant, morphism, level))
        curve_index, remaining, level = kernel, local, level - 1

    x = y = 0
    for quadrant, morphism, level in reversed(descent):
        half = 1 << (level - 1)
        (a, b), (c, d) = morphism
        shift_x, shift_y = _origin_shift(morphism, half)
        x, y = shift_x + a * x + b * y, shift_y + c * x + d * y
        offset_x, offset_y = _QUADRANT_OFFSET[quadrant]
        x += offset_x * half
        y += offset_y * half
    return x, y


def decode(index: int, x: int, y: int, order: int) -> int:
    """Return the step at which curve ``index`` reaches cell ``(x, y)``.

    The exact inverse of :func:`encode`, also ``O(order)``.

    Parameters
    ----------
    index : int
        Curve number, ``0``..``39``.
    x, y : int
        Cell coordinates, each in ``0``..``2**order - 1``.
    order : int
        Recursion depth ``>= 0``.

    Returns
    -------
    int
        The step ``i`` in ``0``..``4**order - 1`` with ``encode(index, i, order) == (x, y)``.
    """
    step = 0
    curve_index, flipped = index, False
    for level in range(order, 0, -1):
        half = 1 << (level - 1)
        span = 1 << (2 * (level - 1))
        offset_x, offset_y = int(x >= half), int(y >= half)
        quadrant = _OFFSET_TO_QUADRANT[offset_x, offset_y]
        x -= offset_x * half
        y -= offset_y * half
        kernel, morphism, reverse = QUADRANT_MATRICES[curve_index][quadrant]
        # A pending complement flips this digit and keeps propagating downwards.
        step += ((3 - quadrant) if flipped else quadrant) * span
        flipped ^= reverse
        # Undo the morphism: D4 matrices are integer-invertible (determinant +-1).
        (a, b), (c, d) = morphism
        shift_x, shift_y = _origin_shift(morphism, half)
        px, py = x - shift_x, y - shift_y
        determinant = a * d - b * c
        x = (d * px - b * py) // determinant
        y = (a * py - c * px) // determinant
        curve_index = kernel
    return step
