"""Generation of curves from the tag-system specifications.

A curve of order ``k`` is a sequence of ``4**k - 1`` unit strokes over the alphabet
``{u, d, l, r}``.  Internally each stroke is a small integer *code* (``u=0, d=1,
l=2, r=3``) so the whole construction runs on ``numpy`` arrays -- morphisms become a
4-entry lookup, reversion an array reversal, and quadrant assembly a
``concatenate``.  There is no Python-level loop over strokes, so an order-10 curve
(over a million strokes) is built in a few tens of milliseconds.

The recursion is the paper's rule

    codes_k(nu) = Q0 . [u] . Q1 . [r] . Q2 . [d] . Q3

where each quadrant recurses into its kernel curve at order ``k - 1`` and then has a
morphism and (optionally) a reversion applied.  Results are memoised on
``(index, order)`` so the shared Hilbert kernel is built once.
"""

from __future__ import annotations

from functools import cache

import numpy as np

from .catalog import spec_by_index
from .limits import check_cells
from .symmetry import DIRECTIONS, MORPHISMS, ROT180

__all__ = ["cache_info", "check_order", "clear_cache", "curve_codes", "curve_word", "word_length"]

# Stroke codes follow the canonical direction order: u=0, d=1, l=2, r=3.
_CODE = {letter: i for i, letter in enumerate(DIRECTIONS)}
_U, _D, _L, _R = _CODE["u"], _CODE["d"], _CODE["l"], _CODE["r"]

# Bytes translation for turning a code array back into a u/d/l/r string (C speed).
_CODE_TO_LETTER = bytes.maketrans(bytes(range(len(DIRECTIONS))), "".join(DIRECTIONS).encode())


def _code_table(sym) -> np.ndarray:
    """A 4-entry lookup ``new_code = table[old_code]`` for a symmetry/morphism.

    Parameters
    ----------
    sym : Symmetry
        Square symmetry applied to coordinates or stroke directions.

    Returns
    -------
    numpy.ndarray of uint8
        Four-entry lookup from original to transformed stroke codes.
    """
    return np.array([_CODE[sym.apply_letter(letter)] for letter in DIRECTIONS], dtype=np.uint8)


_MORPH_TABLES = {code: _code_table(sym) for code, sym in MORPHISMS.items()}
_REVERSION_TABLE = _code_table(ROT180)  # reversion negates each stroke: u<->d, l<->r

# Connector strokes between quadrants 0->1 (up), 1->2 (right), 2->3 (down).
_CONNECTORS = (
    np.array([_U], dtype=np.uint8),
    np.array([_R], dtype=np.uint8),
    np.array([_D], dtype=np.uint8),
)
_EMPTY = np.empty(0, dtype=np.uint8)


def word_length(order: int) -> int:
    """Number of strokes in an order ``order`` curve: ``4**order - 1``.

    Parameters
    ----------
    order : int or None
        Recursion depth for a side of 2**order; None requests automatic sizing when supported.

    Returns
    -------
    int
        Number of unit strokes, equal to 4**order - 1.
    """
    if order < 0:
        raise ValueError(f"order must be non-negative, got {order}")
    return 4**order - 1


def cache_info():
    """Return statistics for cached recursive curve construction.

    Returns
    -------
    info : namedtuple
        Standard functools cache statistics: hits, misses, maxsize, currsize.
        maxsize is None for this unbounded memo cache. currsize counts
        recursive construction entries, not cells or bytes.

    See Also
    --------
    hilbertplot.config.clear_cache : Release cached construction entries.

    Notes
    -----
    The cache stores recursive stroke arrays shared between curves. It does
    not report arrays owned by callers or open Matplotlib figures.

    Examples
    --------
    >>> import hilbertplot as hp
    >>> hp.config.cache_info().maxsize is None
    True
    """
    return _codes.cache_info()


@cache
def _codes(index: int, order: int) -> np.ndarray:
    """Recursively assemble and cache read-only stroke codes for one curve and order.

    Parameters
    ----------
    index : int
        Curve catalog index in 0..39.
    order : int or None
        Recursion depth for a side of 2**order; None requests automatic sizing when supported.

    Returns
    -------
    numpy.ndarray of uint8
        Read-only recursively assembled stroke codes.
    """
    if order == 0:
        return _EMPTY
    spec = spec_by_index(index)
    q = []
    for rule in spec.quadrants:
        sub = _codes(rule.base, order - 1)
        if rule.morphism != "e":
            sub = _MORPH_TABLES[rule.morphism][sub]
        if rule.reverse:
            sub = _REVERSION_TABLE[sub[::-1]]
        q.append(sub)
    out = np.concatenate((q[0], _CONNECTORS[0], q[1], _CONNECTORS[1], q[2], _CONNECTORS[2], q[3]))
    out.flags.writeable = False  # cached; never mutate in place
    return out


def check_order(order: int, *, bytes_per_cell: int = 16) -> int:
    """Return ``order`` if it is a usable recursion depth, else raise.

    Rejects non-integers (including ``bool``), negatives, and depths whose curve could not
    be held in memory -- see :mod:`hilbertplot._core.limits`.

    Parameters
    ----------
    order : int or None
        Recursion depth for a side of 2**order; None requests automatic sizing when supported.
    bytes_per_cell : int
        Bytes per output element used for the allocation estimate.

    Returns
    -------
    int
        Validated nonnegative recursion depth.
    """
    if isinstance(order, bool) or not isinstance(order, (int, np.integer)):
        raise TypeError(f"order must be an int, got {type(order).__name__}")
    order = int(order)
    if order < 0:
        raise ValueError(f"order must be non-negative, got {order}")
    check_cells(4**order, f"order {order}", bytes_per_cell=bytes_per_cell)
    return order


def curve_codes(index: int, order: int) -> np.ndarray:
    """Return the order ``order`` stroke codes for curve ``index`` as a ``uint8`` array.

    The array is read-only (it is shared from the memo cache); copy it if you need to
    mutate it.

    Parameters
    ----------
    index : int
        Curve catalog index in 0..39.
    order : int or None
        Recursion depth for a side of 2**order; None requests automatic sizing when supported.

    Returns
    -------
    numpy.ndarray of uint8
        Read-only cached stroke array; copy before mutation.
    """
    return _codes(index, check_order(order))


def curve_word(index: int, order: int) -> str:
    """Return the order ``order`` word for curve ``index`` (0..39) as a ``u/d/l/r`` string.

    >>> curve_word(0, 2)          # the classic Hilbert curve
    'ruluurdrurddldr'

    Parameters
    ----------
    index : int
        Curve catalog index in 0..39.
    order : int or None
        Recursion depth for a side of 2**order; None requests automatic sizing when supported.

    Returns
    -------
    str
        Direction word of length 4**order - 1.
    """
    # A word is one ASCII byte per stroke, not a 16-byte coordinate pair.
    check_order(order, bytes_per_cell=1)
    return curve_codes(index, order).tobytes().translate(_CODE_TO_LETTER).decode("ascii")


def clear_cache() -> None:
    """Clear memoized recursive stroke arrays and reset cache statistics.

    Returns
    -------
    None
        The generation cache is cleared in place.

    See Also
    --------
    hilbertplot.config.cache_info : Inspect cache entries and hit/miss counts.

    Notes
    -----
    Does not close figures or release arrays referenced elsewhere. A process's
    resident memory need not decrease immediately, because Python and NumPy
    allocators may retain freed memory for reuse.

    Examples
    --------
    >>> import hilbertplot as hp
    >>> hp.config.clear_cache()
    >>> hp.config.cache_info().currsize
    0
    """
    _codes.cache_clear()
