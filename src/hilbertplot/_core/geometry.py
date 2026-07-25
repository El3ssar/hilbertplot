"""From curve words to grid coordinates, plus validation and canonicalisation.

The functions here turn a word of ``u/d/l/r`` strokes into the ordered array of
integer lattice points the curve visits, and provide the tools we use to *prove*
the constructions are correct:

* :func:`is_space_filling` checks that an order ``k`` curve visits every cell of the
  ``2**k`` by ``2**k`` grid exactly once (a Hamiltonian path on the grid);
* :func:`canonical_form` reduces a point sequence modulo the sixteen square
  symmetries and reversion, so that two curves can be compared "up to rotation,
  reflection or reversion" -- the equivalence under which the paper's forty curves
  are distinct.

Coordinates are produced with a vectorised cumulative sum, so building the
``4**k`` points is linear in the output size with essentially no Python-level loop.
"""

from __future__ import annotations

import numpy as np

from .symmetry import (
    ANTIDIAGONAL,
    DIAGONAL,
    FLIP_HORIZONTAL,
    FLIP_VERTICAL,
    IDENTITY,
    ROT90,
    ROT180,
    ROT270,
    Symmetry,
)

__all__ = [
    "D4_ELEMENTS",
    "canonical_form",
    "codes_to_points",
    "is_space_filling",
    "word_to_codes",
    "word_to_points",
    "word_to_steps",
]

#: The eight elements of D4, used for canonicalisation and (later) generalisation.
D4_ELEMENTS: tuple[Symmetry, ...] = (
    IDENTITY,
    ROT90,
    ROT180,
    ROT270,
    FLIP_VERTICAL,
    FLIP_HORIZONTAL,
    DIAGONAL,
    ANTIDIAGONAL,
)

# Stroke codes u=0, d=1, l=2, r=3, indexed into unit (dx, dy) steps.
_LETTER_TO_CODE = bytes.maketrans(b"udlr", bytes((0, 1, 2, 3)))
_STEP_LOOKUP = np.array([(0, 1), (0, -1), (-1, 0), (1, 0)], dtype=np.int64)
# The same steps split per axis as ``int8``: gathering two 1-byte columns and accumulating
# each straight into the output is markedly cheaper than building an (N, 2) ``int64``
# intermediate and running a strided 2-D cumsum over it.
_DX_LOOKUP = np.array([0, 0, -1, 1], dtype=np.int8)
_DY_LOOKUP = np.array([1, -1, 0, 0], dtype=np.int8)


def word_to_codes(word: str) -> np.ndarray:
    """Return the ``uint8`` stroke-code array for a ``u/d/l/r`` word."""
    if not word:
        return np.empty(0, dtype=np.uint8)
    return np.frombuffer(word.encode("ascii").translate(_LETTER_TO_CODE), dtype=np.uint8)


def codes_to_points(codes: np.ndarray, *, normalize: bool = True) -> np.ndarray:
    """Return the ordered ``(len(codes) + 1, 2)`` integer points for a stroke-code array.

    The walk starts at the origin and accumulates unit steps with one vectorised ``cumsum``
    per axis, written directly into the output.  With ``normalize=True`` (the default) the
    points are shifted so the minimum corner is ``(0, 0)``; for a valid order ``k`` curve
    they then tile ``{0, ..., 2**k - 1}`` on each axis.
    """
    points = np.empty((len(codes) + 1, 2), dtype=np.int64)
    points[0] = 0
    if len(codes):
        np.cumsum(_DX_LOOKUP[codes], dtype=np.int64, out=points[1:, 0])
        np.cumsum(_DY_LOOKUP[codes], dtype=np.int64, out=points[1:, 1])
    if normalize:
        points -= points.min(axis=0)
    return points


def word_to_steps(word: str) -> np.ndarray:
    """Return the ``(len(word), 2)`` array of unit ``(dx, dy)`` steps for ``word``."""
    return _STEP_LOOKUP[word_to_codes(word)]


def word_to_points(word: str, *, normalize: bool = True) -> np.ndarray:
    """Return the ordered ``(len(word) + 1, 2)`` integer points a curve word visits."""
    return codes_to_points(word_to_codes(word), normalize=normalize)


def is_space_filling(points: np.ndarray, side: int, *, connected: bool = True) -> bool:
    """Check that ``points`` is a Hamiltonian path over a ``side`` by ``side`` grid.

    Verifies at once that there is one point per cell, that all of them are distinct, and
    that the bounding box is exactly ``side`` by ``side`` -- together, that the path visits
    every cell of the square precisely once.  With ``connected=True`` (the default) it also
    checks that consecutive points are 4-adjacent, which is what makes the sequence a
    *path* rather than merely a permutation of the cells.

    Takes a **side**, not an order, so it applies equally to :meth:`~hilbertplot.Curve.points`
    (where the side is ``2**order``) and to :meth:`~hilbertplot.Curve.grid` on an arbitrary
    square.

    Parameters
    ----------
    points : numpy.ndarray
        An ``(N, 2)`` integer array of ``(x, y)`` cells in visit order.
    side : int
        The grid side the path should fill.
    connected : bool, default True
        Also require each consecutive pair to differ by a single unit step.

    Returns
    -------
    bool

    Examples
    --------
    >>> import hilbertplot
    >>> c = hilbertplot.curve(0)
    >>> hilbertplot.is_space_filling(c.points(3), 8)
    True
    >>> hilbertplot.is_space_filling(c.grid(10), 10)      # arbitrary squares too
    True
    >>> hilbertplot.is_space_filling(c.points(3), 16)     # wrong side
    False
    """
    if side < 1 or points.shape != (side * side, 2):
        return False
    lo = points.min(axis=0)
    hi = points.max(axis=0)
    if not (np.array_equal(lo, (0, 0)) and np.array_equal(hi, (side - 1, side - 1))):
        return False
    # Distinctness: pack each (x, y) into a single integer key and count uniques.
    keys = points[:, 0].astype(np.int64) * side + points[:, 1]
    if np.unique(keys).size != side * side:
        return False
    if connected and points.shape[0] > 1:
        return bool((np.abs(np.diff(points, axis=0)).sum(axis=1) == 1).all())
    return True


def _transform_points(points: np.ndarray, sym: Symmetry, *, reverse: bool) -> np.ndarray:
    (a, b), (c, d) = sym.matrix
    x = points[:, 0]
    y = points[:, 1]
    out = np.empty_like(points)
    out[:, 0] = a * x + b * y
    out[:, 1] = c * x + d * y
    if reverse:
        out = out[::-1]
    out -= out.min(axis=0)
    return np.ascontiguousarray(out)


def canonical_form(points: np.ndarray) -> bytes:
    """Return a canonical byte key for ``points`` modulo symmetry and reversion.

    Two point sequences share a canonical form iff one can be mapped onto the other
    by a square symmetry (rotation/reflection) and/or reversion (traversal reversal).
    This is exactly the equivalence under which the paper's forty curves are counted
    as distinct, so equal canonical forms mean "the same curve".
    """
    best: bytes | None = None
    for sym in D4_ELEMENTS:
        for reverse in (False, True):
            key = _transform_points(points, sym, reverse=reverse).tobytes()
            if best is None or key < best:
                best = key
    assert best is not None
    return best
