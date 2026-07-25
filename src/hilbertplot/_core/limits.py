"""A soft ceiling on how many cells one call may materialise.

An order ``k`` curve has ``4**k`` cells and each cell costs 16 bytes as an ``(x, y)``
``int64`` pair, so the cost climbs by 4x per order: order 12 is 0.25 GiB, order 14 is
4 GiB, order 16 is 64 GiB.  Without a guard, a typo like ``points(20)`` does not fail
fast -- it asks for 16 TiB, and the machine spends minutes thrashing swap before the
allocator gives up.  Worse, :mod:`hilbertplot._core.generation` memoises results, so a
single bad order stays resident.

So every entry point that materialises a whole curve checks its cell count against
:func:`cell_limit` first and raises a :class:`ValueError` naming the actual memory
required.  The default is deliberately generous -- larger than any curve a plot could
usefully show -- so it only ever catches mistakes.  Raise it with :func:`set_cell_limit`
if you have the memory and mean it.
"""

from __future__ import annotations

__all__ = ["BYTES_PER_CELL", "cell_limit", "check_cells", "set_cell_limit"]

#: Bytes one cell occupies in the returned array: an ``(x, y)`` pair of ``int64``.
BYTES_PER_CELL = 16

#: Default ceiling: 2**28 cells = 268 million = 4 GiB of coordinates (order 14, or a
#: 16384 x 16384 square).  Generous for any real plot, small enough to catch a typo.
_DEFAULT_MAX_CELLS = 1 << 28

_max_cells = _DEFAULT_MAX_CELLS


def cell_limit() -> int:
    """Return the current ceiling, in cells, on a single materialised curve."""
    return _max_cells


def set_cell_limit(cells: int | None) -> int:
    """Set the ceiling on a single materialised curve and return the previous value.

    Parameters
    ----------
    cells : int or None
        The new limit in cells.  ``None`` restores the default; a limit of ``0`` or less
        is rejected.  Pass a very large number to effectively disable the check.

    Returns
    -------
    int
        The limit that was in force before this call, so it can be restored.

    Examples
    --------
    >>> import hilbertplot
    >>> previous = hilbertplot.set_cell_limit(4 ** 10)
    >>> hilbertplot.cell_limit()
    1048576
    >>> _ = hilbertplot.set_cell_limit(previous)
    """
    global _max_cells
    if cells is None:
        cells = _DEFAULT_MAX_CELLS
    elif not isinstance(cells, int) or isinstance(cells, bool):
        raise TypeError(f"cell limit must be an int or None, got {type(cells).__name__}")
    elif cells < 1:
        raise ValueError(f"cell limit must be >= 1, got {cells}")
    previous, _max_cells = _max_cells, cells
    return previous


def _gib(cells: int, bytes_per_cell: int) -> str:
    """Format a byte count as GiB, in integer arithmetic so huge sizes cannot overflow.

    ``cells`` is an unbounded Python int: at order 525 the true division ``cells * b / 2**30``
    raises ``OverflowError`` instead of producing the helpful message this module exists to
    give.  Above a petabyte the fractional part is meaningless anyway.
    """
    total = cells * bytes_per_cell
    if total >= 2**60:  # >= 1 EiB: print exactly, no float involved
        return f"{total // 2**30:,} GiB"
    return f"{total / 2**30:,.1f} GiB"


def check_cells(cells: int, what: str, *, bytes_per_cell: int = BYTES_PER_CELL) -> None:
    """Raise if materialising ``cells`` cells would exceed :func:`cell_limit`.

    ``what`` describes the request in the user's own terms (e.g. ``"order 20"``) so the
    message says which argument to change.  ``bytes_per_cell`` is the size of the array the
    caller is about to build -- 16 for an ``(x, y)`` pair, 1 for a stroke of a word.

    The quoted size is that array alone.  Peak memory runs higher, because building it takes
    intermediates: expect roughly 1.5x for :meth:`~hilbertplot.Curve.points` and several
    times that for the map builders, which is why the default ceiling sits well below what
    a machine could actually hold.
    """
    if cells > _max_cells:
        raise ValueError(
            f"{what} needs {cells:,} cells ({_gib(cells, bytes_per_cell)}), over the "
            f"{_max_cells:,}-cell limit ({_gib(_max_cells, bytes_per_cell)}). Use a smaller "
            f"size, or raise the ceiling with hilbertplot.set_cell_limit() if you have the "
            f"memory."
        )
