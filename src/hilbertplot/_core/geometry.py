"""From curve words to grid coordinates, plus validation and canonicalisation.

The functions here turn a word of ``u/d/l/r`` strokes into the ordered array of
integer lattice points the curve visits, and provide the tools we use to *prove*
the constructions are correct:

* :func:`is_space_filling` checks that a path visits every cell of a ``side`` by ``side``
  grid exactly once and (by default) that consecutive cells are 4-adjacent -- a Hamiltonian
  path on the grid, for ``2**k`` and arbitrary squares alike;
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
    """Return the ``uint8`` stroke-code array for a ``u/d/l/r`` word.

    Parameters
    ----------
    word : str
        Unit direction word over u, d, l and r.

    Returns
    -------
    numpy.ndarray of uint8
        One code per direction letter.
    """
    if not word:
        return np.empty(0, dtype=np.uint8)
    return np.frombuffer(word.encode("ascii").translate(_LETTER_TO_CODE), dtype=np.uint8)


def codes_to_points(codes: np.ndarray, *, normalize: bool = True) -> np.ndarray:
    """Return the ordered ``(len(codes) + 1, 2)`` integer points for a stroke-code array.

    The walk starts at the origin and accumulates unit steps with one vectorised ``cumsum``
    per axis, written directly into the output.  With ``normalize=True`` (the default) the
    points are shifted so the minimum corner is ``(0, 0)``; for a valid order ``k`` curve
    they then tile ``{0, ..., 2**k - 1}`` on each axis.

    Parameters
    ----------
    codes : numpy.ndarray of uint8
        Stroke codes u=0, d=1, l=2, r=3.
    normalize : bool
        Translate the minimum path coordinate to (0, 0) when True.

    Returns
    -------
    numpy.ndarray of int64
        Shape (len(codes) + 1, 2) containing (x, y) cells in visit order.
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
    """Return the ``(len(word), 2)`` array of unit ``(dx, dy)`` steps for ``word``.

    Parameters
    ----------
    word : str
        Unit direction word over u, d, l and r.

    Returns
    -------
    numpy.ndarray of int64
        Shape (len(word), 2) containing each (dx, dy) unit step.
    """
    return _STEP_LOOKUP[word_to_codes(word)]


def word_to_points(word: str, *, normalize: bool = True) -> np.ndarray:
    """Return the ordered ``(len(word) + 1, 2)`` integer points a curve word visits.

    Parameters
    ----------
    word : str
        Unit direction word over u, d, l and r.
    normalize : bool
        Translate the minimum path coordinate to (0, 0) when True.

    Returns
    -------
    numpy.ndarray of int64
        Shape (len(word) + 1, 2) containing the visited (x, y) cells.
    """
    return codes_to_points(word_to_codes(word), normalize=normalize)


def is_space_filling(points: np.ndarray, side: int, *, connected: bool = True) -> bool:
    """Check coverage and optional connectivity of a discrete square-grid path.

    Parameters
    ----------
    points : array_like, shape (N, 2)
        Integer (x, y) cells in visit order. A valid square path has N=side**2.
    side : int
        Positive square side length, not a recursion order.
    connected : bool, default True
        Also require unit horizontal/vertical steps between successive cells.
        False checks coverage, uniqueness and bounds only.

    Returns
    -------
    valid : bool
        Whether the path visits every cell of the given square once, with
        connectivity when requested. General rectangles are not checked.

    See Also
    --------
    hilbertplot.curves.points : Generate a power-of-two path.
    hilbertplot.curves.grid : Generate other supported path sizes.

    Examples
    --------
    >>> import hilbertplot as hp
    >>> hp.curves.is_space_filling(hp.curves.points(0, order=3), side=8)
    True
    >>> hp.curves.is_space_filling(hp.curves.points(0, order=3), side=16)
    False
    """
    points = np.asarray(points)
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
    """Transform and optionally reverse a path, then translate its minimum to zero.

    Parameters
    ----------
    points : numpy.ndarray
        Ordered integer (x, y) cells with shape (N, 2).
    sym : Symmetry
        Square symmetry applied to coordinates or stroke directions.
    reverse : bool
        Whether to traverse the construction in the opposite order.

    Returns
    -------
    numpy.ndarray
        Contiguous transformed coordinates with the original shape and dtype.
    """
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
    """Build a byte key invariant to square symmetries and traversal reversal.

    Parameters
    ----------
    points : numpy.ndarray, shape (N, 2)
        Nonempty integer (x, y) coordinates. Compare arrays with compatible
        dtype and byte order; the key uses their native byte representation.

    Returns
    -------
    key : bytes
        Lexicographically smallest translated path representation among
        eight square symmetries and both traversal directions.

    See Also
    --------
    hilbertplot.curves.is_space_filling : Check square coverage and connectivity.

    Notes
    -----
    Coordinates are shifted so their minimum is (0, 0). Equal keys identify
    paths related by these operations when dtype/representation agree. The
    key is not a portable serialization or a validation of space filling.

    Examples
    --------
    >>> import hilbertplot as hp
    >>> points = hp.curves.points(0, order=3)
    >>> hp.curves.canonical_form(points) == hp.curves.canonical_form(points[::-1])
    True
    """
    best: bytes | None = None
    for sym in D4_ELEMENTS:
        for reverse in (False, True):
            key = _transform_points(points, sym, reverse=reverse).tobytes()
            if best is None or key < best:
                best = key
    assert best is not None
    return best
