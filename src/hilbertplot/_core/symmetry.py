"""Symmetries of the square (the dihedral group :math:`D_4`) acting on directions.

Every construction rule in Estevez-Rams *et al.* (2017) is expressed with a small
set of *morphisms* :math:`\\delta_\\bullet` that rewrite the direction letters of a
curve word.  Each such morphism is nothing more than an element of the symmetry
group of the square applied to unit direction vectors.  Making that explicit here
(rather than hard-coding opaque letter tables) keeps the code principled and gives
us the group machinery we will need later when generalising the curves to squares
of arbitrary side.

Directions
----------
A curve is encoded as a word over the alphabet ``{'u', 'd', 'l', 'r'}`` where each
letter is a unit pencil stroke:

======  ==========
letter  vector
======  ==========
``u``   ``(0, +1)``
``d``   ``(0, -1)``
``l``   ``(-1, 0)``
``r``   ``(+1, 0)``
======  ==========

The eight elements of :math:`D_4` are exposed both as named constants and through
:data:`MORPHISMS`, keyed by the single-letter codes used throughout the paper
(``e o a g x f m y``).
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from typing import Iterable, Mapping

__all__ = [
    "Direction",
    "DIRECTIONS",
    "DIRECTION_VECTORS",
    "Symmetry",
    "MORPHISMS",
    "IDENTITY",
    "ROT90",
    "ROT180",
    "ROT270",
    "FLIP_VERTICAL",
    "FLIP_HORIZONTAL",
    "DIAGONAL",
    "ANTIDIAGONAL",
    "reverse_word",
    "apply_morphism",
]

#: The four direction letters, in a fixed canonical order.
DIRECTIONS: tuple[str, ...] = ("u", "d", "l", "r")

#: Mapping from each direction letter to its integer unit vector ``(dx, dy)``.
DIRECTION_VECTORS: Mapping[str, tuple[int, int]] = {
    "u": (0, 1),
    "d": (0, -1),
    "l": (-1, 0),
    "r": (1, 0),
}

# Reverse lookup: unit vector -> letter.
_VECTOR_TO_LETTER: Mapping[tuple[int, int], str] = {
    v: k for k, v in DIRECTION_VECTORS.items()
}

# A lightweight alias; a "Direction" is just one of the letters above.
Direction = str


@dataclass(frozen=True)
class Symmetry:
    """An element of the dihedral group :math:`D_4` (symmetries of the square).

    The element is stored as a 2x2 integer matrix ``((a, b), (c, d))`` acting on a
    column vector ``(x, y)`` as ``(a*x + b*y, c*x + d*y)``.  Only the eight
    orthogonal integer matrices with determinant :math:`\\pm 1` are valid, but the
    class does not police this -- the named constants below are the canonical set.

    Instances are immutable and hashable, so they compose cleanly and can be used
    as dictionary keys or catalog entries.
    """

    matrix: tuple[tuple[int, int], tuple[int, int]]
    name: str = ""

    # -- action on geometry -------------------------------------------------
    def apply_vector(self, vector: tuple[int, int]) -> tuple[int, int]:
        """Return ``self`` applied to an integer ``(x, y)`` vector."""
        (a, b), (c, d) = self.matrix
        x, y = vector
        return (a * x + b * y, c * x + d * y)

    def apply_letter(self, letter: Direction) -> Direction:
        """Return the direction letter obtained by transforming ``letter``."""
        return self._letter_map[letter]

    @cached_property
    def _letter_map(self) -> Mapping[str, str]:
        return {
            letter: _VECTOR_TO_LETTER[self.apply_vector(DIRECTION_VECTORS[letter])]
            for letter in DIRECTIONS
        }

    def apply_word(self, word: str) -> str:
        """Rewrite every letter of ``word`` under this symmetry (a morphism)."""
        table = self._letter_map
        return "".join(table[letter] for letter in word)

    # -- group structure ----------------------------------------------------
    def compose(self, other: "Symmetry") -> "Symmetry":
        """Return the symmetry ``self`` followed by ``other`` (``other after self``).

        ``s.compose(t).apply_vector(v) == t.apply_vector(s.apply_vector(v))``.
        """
        (a, b), (c, d) = other.matrix
        (e, f), (g, h) = self.matrix
        return Symmetry(
            (
                (a * e + b * g, a * f + b * h),
                (c * e + d * g, c * f + d * h),
            )
        )

    def __matmul__(self, other: "Symmetry") -> "Symmetry":
        return self.compose(other)

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return f"Symmetry({self.name or self.matrix})"


# The eight elements of D4.  Matrices act on (x, y) column vectors.
IDENTITY = Symmetry(((1, 0), (0, 1)), "e")          # identity
ROT90 = Symmetry(((0, -1), (1, 0)), "g")            # +90 deg (counter-clockwise)
ROT180 = Symmetry(((-1, 0), (0, -1)), "f")          # 180 deg
ROT270 = Symmetry(((0, 1), (-1, 0)), "x")           # -90 deg (clockwise)
FLIP_VERTICAL = Symmetry(((1, 0), (0, -1)), "m")    # reflect across x-axis (y -> -y)
FLIP_HORIZONTAL = Symmetry(((-1, 0), (0, 1)), "y")  # reflect across y-axis (x -> -x)
DIAGONAL = Symmetry(((0, 1), (1, 0)), "o")          # reflect across line y = x
ANTIDIAGONAL = Symmetry(((0, -1), (-1, 0)), "a")    # reflect across line y = -x

#: The paper's morphisms, keyed by their single-letter codes.
#:
#: ``e`` identity, ``g`` = :math:`\\delta_g`, ``x`` = :math:`\\delta_x`,
#: ``f`` = :math:`\\delta_f`, ``m`` = :math:`\\delta_m`, ``y`` = :math:`\\delta_y`,
#: ``o`` = :math:`\\delta_o`, ``a`` = :math:`\\delta_a` (written :math:`\\delta_d`
#: in section V of the paper).
MORPHISMS: Mapping[str, Symmetry] = {
    "e": IDENTITY,
    "g": ROT90,
    "x": ROT270,
    "f": ROT180,
    "m": FLIP_VERTICAL,
    "y": FLIP_HORIZONTAL,
    "o": DIAGONAL,
    "a": ANTIDIAGONAL,
}


def apply_morphism(code: str, word: str) -> str:
    """Apply the morphism named ``code`` (one of :data:`MORPHISMS`) to ``word``."""
    return MORPHISMS[code].apply_word(word)


def reverse_word(word: str) -> str:
    """Return the *reversion* :math:`\\bar p` of a curve word.

    Reversion swaps the entry and exit point of a curve: it reverses the order of
    the strokes and negates each one (``u`` <-> ``d`` and ``l`` <-> ``r``).  This is
    exactly walking the curve backwards, i.e. reversing the word and applying the
    180-degree rotation :data:`ROT180` to every letter.

    >>> reverse_word("ruluurdrurddldr")
    'luruuldlulddrdl'
    """
    flip = ROT180._letter_map
    return "".join(flip[letter] for letter in reversed(word))


def compose_all(symmetries: Iterable[Symmetry]) -> Symmetry:
    """Compose a sequence of symmetries left to right, returning their product."""
    result = IDENTITY
    for sym in symmetries:
        result = result.compose(sym)
    return result
