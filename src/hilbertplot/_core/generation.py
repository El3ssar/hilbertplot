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
from .symmetry import DIRECTIONS, MORPHISMS, ROT180

__all__ = ["curve_codes", "curve_word", "word_length", "clear_cache"]

# Stroke codes follow the canonical direction order: u=0, d=1, l=2, r=3.
_CODE = {letter: i for i, letter in enumerate(DIRECTIONS)}
_U, _D, _L, _R = _CODE["u"], _CODE["d"], _CODE["l"], _CODE["r"]

# Bytes translation for turning a code array back into a u/d/l/r string (C speed).
_CODE_TO_LETTER = bytes.maketrans(bytes(range(len(DIRECTIONS))), "".join(DIRECTIONS).encode())


def _code_table(sym) -> np.ndarray:
    """A 4-entry lookup ``new_code = table[old_code]`` for a symmetry/morphism."""
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
    """Number of strokes in an order ``order`` curve: ``4**order - 1``."""
    if order < 0:
        raise ValueError(f"order must be non-negative, got {order}")
    return 4**order - 1


@cache
def _codes(index: int, order: int) -> np.ndarray:
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


def curve_codes(index: int, order: int) -> np.ndarray:
    """Return the order ``order`` stroke codes for curve ``index`` as a ``uint8`` array.

    The array is read-only (it is shared from the memo cache); copy it if you need to
    mutate it.
    """
    if order < 0:
        raise ValueError(f"order must be non-negative, got {order}")
    return _codes(index, order)


def curve_word(index: int, order: int) -> str:
    """Return the order ``order`` word for curve ``index`` (0..39) as a ``u/d/l/r`` string.

    >>> curve_word(0, 2)          # the classic Hilbert curve
    'ruluurdrurddldr'
    """
    return curve_codes(index, order).tobytes().translate(_CODE_TO_LETTER).decode("ascii")


def clear_cache() -> None:
    """Drop all memoised curves (frees memory after generating high-order curves)."""
    _codes.cache_clear()
