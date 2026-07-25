"""Declarative specification of the forty two-dimensional Hilbert curves.

This module is pure data plus the small dataclasses that give it structure.  It is
the single source of truth for the whole library and maps one-to-one onto the tag
systems of Estevez-Rams *et al.*, "Hilbert curves in two dimensions",
*Rev. Cub. Fis.* **34**, 9 (2017).

The construction
----------------
Every order ``k`` curve is assembled from four sub-curves of order ``k - 1`` -- one
per quadrant -- joined by the fixed connectors ``u``, ``r``, ``d``::

    word_k(nu) = Q0 . 'u' . Q1 . 'r' . Q2 . 'd' . Q3

The quadrants are numbered as in Fig. 1 of the paper, clockwise from the lower
left: ``0`` = bottom-left, ``1`` = top-left, ``2`` = top-right, ``3`` =
bottom-right.  The connectors therefore trace ``0 -(up)-> 1 -(right)-> 2 -(down)->
3``.

Each quadrant ``Qi`` is obtained from a *kernel* curve ``base`` (also of order
``k - 1``) by applying a morphism and, optionally, a reversion:

    Qi = [reversion?] ( morphism ( word_{k-1}(base) ) )

The classification the paper draws -- and that the user asked us to reflect -- falls
straight out of the kernels:

* **homogeneous** curves use a single kernel type in all four quadrants
  (Definition III.1: "built from one and only one Hilbert curve of order k-1");
* **inhomogeneous** curves mix at least two kernel types (Definition VI.1).

Homogeneous curves split further into *proper* (kernel = the Hilbert curve ``0H``)
and *improper* (kernel = the Liu-4 curve ``5H``).
"""

from __future__ import annotations

import enum
from collections.abc import Mapping
from dataclasses import dataclass, field, replace

from .symmetry import MORPHISMS

__all__ = [
    "QUADRANT_MATRICES",
    "SPECS",
    "CurveSpec",
    "Family",
    "Matrix",
    "QuadrantRule",
    "spec_by_index",
]

#: An element of :math:`D_4` as a plain nested tuple -- hashable, and cheap to multiply.
Matrix = tuple[tuple[int, int], tuple[int, int]]


class Family(enum.Enum):
    """The three families the forty curves fall into."""

    HOMOGENEOUS_PROPER = "homogeneous-proper"
    HOMOGENEOUS_IMPROPER = "homogeneous-improper"
    INHOMOGENEOUS = "inhomogeneous"

    @property
    def is_homogeneous(self) -> bool:
        return self is not Family.INHOMOGENEOUS


@dataclass(frozen=True)
class QuadrantRule:
    """How one quadrant of an order ``k`` curve is built from an order ``k-1`` curve.

    Parameters
    ----------
    base:
        Index of the *kernel* curve supplying this quadrant's sub-curve.  Only the
        homogeneous building blocks ``{0, 1, 3, 4, 5}`` (and never ``2``) ever
        appear here, exactly as proved in the paper.
    morphism:
        Single-letter morphism code (see :data:`hilbertplot._core.symmetry.MORPHISMS`).
    reverse:
        Whether the reversion :math:`\\bar p` is applied after the morphism.
    """

    base: int
    morphism: str
    reverse: bool = False

    def __str__(self) -> str:
        inner = f"{self.base}H"
        if self.morphism != "e":
            inner = f"d_{self.morphism}({inner})"
        return f"rev({inner})" if self.reverse else inner


@dataclass(frozen=True)
class CurveSpec:
    """Immutable description of one of the forty curves.

    Attributes
    ----------
    index:
        The curve number ``nu`` in ``0..39`` (the paper's :math:`{}_\\nu H`).
    name:
        Human-readable name (``"Hilbert"``, ``"Moore"``, ``"Liu1"``, ..., ``"I1"``,
        ``"IH12"`` ...).
    family:
        Which :class:`Family` the curve belongs to.
    quadrants:
        The four :class:`QuadrantRule` s, in quadrant order ``0, 1, 2, 3``.
    combination:
        Short label of the kernel mix (e.g. ``"0H"``, ``"5H"``, ``"3H+5H"``), matching
        the paper's grouping of the inhomogeneous curves.
    closed:
        ``True`` if the curve's entry and exit lie in adjacent sub-squares so that the
        infinite curve closes into a loop (Moore, Liu1, I1, I4; Table 3 of the paper).
    """

    index: int
    name: str
    family: Family
    quadrants: tuple[QuadrantRule, QuadrantRule, QuadrantRule, QuadrantRule]
    combination: str
    closed: bool = False
    #: Optional free-form geometric notes lifted from Table 3 of the paper.
    notes: str = field(default="", compare=False)

    @property
    def kernels(self) -> frozenset[int]:
        """The set of distinct kernel curve indices used across the four quadrants."""
        return frozenset(q.base for q in self.quadrants)

    @property
    def is_homogeneous(self) -> bool:
        return self.family.is_homogeneous

    def rule_str(self) -> str:
        """Reconstruct the paper's tag-system line for this curve."""
        q0, q1, q2, q3 = self.quadrants
        return f"{self.index}h(k) = {q0} u {q1} r {q2} d {q3}"


def _q(base: int, morphism: str = "e", reverse: bool = False) -> QuadrantRule:
    return QuadrantRule(base, morphism, reverse)


# ---------------------------------------------------------------------------
# The forty curves.
#
# Transcribed directly from the tag systems in sections V and VII of the paper.
# Homogeneous proper curves are built over the Hilbert kernel 0H; improper curves
# over the Liu-4 kernel 5H; inhomogeneous curves mix kernels.  A bar over a term in
# the paper (reversion) is recorded as ``reverse=True``.
# ---------------------------------------------------------------------------

_PROPER: tuple[CurveSpec, ...] = (
    CurveSpec(
        0,
        "Hilbert",
        Family.HOMOGENEOUS_PROPER,
        (_q(0, "o"), _q(0), _q(0), _q(0, "a")),
        "0H",
        notes="corner-corner; the original Hilbert curve",
    ),
    CurveSpec(
        1,
        "Moore",
        Family.HOMOGENEOUS_PROPER,
        (_q(0, "g"), _q(0, "g"), _q(0, "x"), _q(0, "x")),
        "0H",
        closed=True,
        notes="edge-edge shared; Moore's closed curve",
    ),
    CurveSpec(
        2,
        "Liu1",
        Family.HOMOGENEOUS_PROPER,
        (_q(0, "f"), _q(0), _q(0), _q(0, "f")),
        "0H",
        closed=True,
        notes="interior-interior; cannot serve as a building block",
    ),
    CurveSpec(
        3,
        "Liu2",
        Family.HOMOGENEOUS_PROPER,
        (_q(0, "m"), _q(0, "g"), _q(0, "x"), _q(0, "m")),
        "0H",
        notes="edge-edge opposed",
    ),
    CurveSpec(
        4,
        "Liu3",
        Family.HOMOGENEOUS_PROPER,
        (_q(0, "o"), _q(0), _q(0), _q(0, "f")),
        "0H",
        notes="corner-interior",
    ),
    CurveSpec(
        5,
        "Liu4",
        Family.HOMOGENEOUS_PROPER,
        (_q(0, "m"), _q(0, "g"), _q(0, "x"), _q(0, "x")),
        "0H",
        notes="edge-edge adjacent; kernel of every improper curve",
    ),
)

_IMPROPER: tuple[CurveSpec, ...] = (
    CurveSpec(
        6,
        "I1",
        Family.HOMOGENEOUS_IMPROPER,
        (_q(5, "f"), _q(5, "y", True), _q(5), _q(5, "m", True)),
        "5H",
        closed=True,
        notes="interior-interior",
    ),
    CurveSpec(
        7,
        "I2",
        Family.HOMOGENEOUS_IMPROPER,
        (_q(5, "f"), _q(5, "y", True), _q(5), _q(5, "a")),
        "5H",
        notes="interior-edge",
    ),
    CurveSpec(
        8,
        "I3",
        Family.HOMOGENEOUS_IMPROPER,
        (_q(5, "x", True), _q(5, "y", True), _q(5), _q(5, "a")),
        "5H",
        notes="edge-edge opposed",
    ),
    CurveSpec(
        9,
        "I4",
        Family.HOMOGENEOUS_IMPROPER,
        (_q(5, "a", True), _q(5, "g"), _q(5, "o", True), _q(5, "x")),
        "5H",
        closed=True,
        notes="interior-interior",
    ),
    CurveSpec(
        10,
        "I5",
        Family.HOMOGENEOUS_IMPROPER,
        (_q(5, "m"), _q(5, "g"), _q(5, "o", True), _q(5, "f", True)),
        "5H",
        notes="edge-edge opposed",
    ),
    CurveSpec(
        11,
        "I6",
        Family.HOMOGENEOUS_IMPROPER,
        (_q(5, "m"), _q(5, "g"), _q(5, "o", True), _q(5, "x")),
        "5H",
        notes="edge-interior",
    ),
)

# Inhomogeneous curves 12-39.  Grouped exactly as in the paper (Figures 6-9).
_INHOMOGENEOUS: tuple[CurveSpec, ...] = (
    # 3H + 5H  (Figure 6): two 3H + two 5H, then one 3H + three 5H.
    CurveSpec(
        12, "IH12", Family.INHOMOGENEOUS, (_q(3, "o"), _q(5, "y", True), _q(5), _q(3, "a")), "3H+5H"
    ),
    CurveSpec(
        13,
        "IH13",
        Family.INHOMOGENEOUS,
        (_q(3, "g"), _q(5, "g"), _q(5, "o", True), _q(3, "x")),
        "3H+5H",
    ),
    CurveSpec(
        14, "IH14", Family.INHOMOGENEOUS, (_q(3, "o"), _q(5, "y", True), _q(5), _q(5, "a")), "3H+5H"
    ),
    CurveSpec(
        15,
        "IH15",
        Family.INHOMOGENEOUS,
        (_q(3, "g"), _q(5, "g"), _q(5, "o", True), _q(5, "f", True)),
        "3H+5H",
    ),
    CurveSpec(
        16,
        "IH16",
        Family.INHOMOGENEOUS,
        (_q(3, "o"), _q(5, "y", True), _q(5), _q(5, "m", True)),
        "3H+5H",
    ),
    CurveSpec(
        17,
        "IH17",
        Family.INHOMOGENEOUS,
        (_q(3, "g"), _q(5, "g"), _q(5, "o", True), _q(5, "x")),
        "3H+5H",
    ),
    # 0H + 4H  (Figure 7): fourteen curves.
    CurveSpec(
        18, "IH18", Family.INHOMOGENEOUS, (_q(4, "x", True), _q(0), _q(0), _q(4, "a")), "0H+4H"
    ),
    CurveSpec(
        19, "IH19", Family.INHOMOGENEOUS, (_q(4, "m", True), _q(0), _q(0), _q(4, "f")), "0H+4H"
    ),
    CurveSpec(
        20, "IH20", Family.INHOMOGENEOUS, (_q(4, "x", True), _q(0), _q(0), _q(4, "f")), "0H+4H"
    ),
    CurveSpec(
        21,
        "IH21",
        Family.INHOMOGENEOUS,
        (_q(4, "f", True), _q(0, "g"), _q(0, "x"), _q(4, "m")),
        "0H+4H",
    ),
    CurveSpec(
        22,
        "IH22",
        Family.INHOMOGENEOUS,
        (_q(4, "a", True), _q(0, "g"), _q(0, "x"), _q(4, "x")),
        "0H+4H",
    ),
    CurveSpec(
        23,
        "IH23",
        Family.INHOMOGENEOUS,
        (_q(4, "a", True), _q(0, "g"), _q(0, "x"), _q(4, "m")),
        "0H+4H",
    ),
    CurveSpec(
        24, "IH24", Family.INHOMOGENEOUS, (_q(0, "m"), _q(0, "g"), _q(0, "x"), _q(4, "x")), "0H+4H"
    ),
    CurveSpec(
        25, "IH25", Family.INHOMOGENEOUS, (_q(0, "g"), _q(0, "g"), _q(0, "x"), _q(4, "m")), "0H+4H"
    ),
    CurveSpec(
        26, "IH26", Family.INHOMOGENEOUS, (_q(0, "g"), _q(0, "g"), _q(0, "x"), _q(4, "x")), "0H+4H"
    ),
    CurveSpec(27, "IH27", Family.INHOMOGENEOUS, (_q(0, "f"), _q(0), _q(0), _q(4, "f")), "0H+4H"),
    CurveSpec(28, "IH28", Family.INHOMOGENEOUS, (_q(0, "f"), _q(0), _q(0), _q(4, "a")), "0H+4H"),
    CurveSpec(29, "IH29", Family.INHOMOGENEOUS, (_q(0, "o"), _q(0), _q(0), _q(4, "f")), "0H+4H"),
    CurveSpec(30, "IH30", Family.INHOMOGENEOUS, (_q(0, "o"), _q(0), _q(0), _q(4, "a")), "0H+4H"),
    CurveSpec(
        31, "IH31", Family.INHOMOGENEOUS, (_q(0, "m"), _q(0, "g"), _q(0, "x"), _q(4, "m")), "0H+4H"
    ),
    # 1H + 5H  (Figure 8): two 1H + two 5H, then one 1H + three 5H.
    CurveSpec(
        32, "IH32", Family.INHOMOGENEOUS, (_q(1, "f"), _q(5, "y", True), _q(5), _q(1, "f")), "1H+5H"
    ),
    CurveSpec(
        33,
        "IH33",
        Family.INHOMOGENEOUS,
        (_q(1, "m"), _q(5, "g"), _q(5, "o", True), _q(1, "m")),
        "1H+5H",
    ),
    CurveSpec(
        34, "IH34", Family.INHOMOGENEOUS, (_q(5, "f"), _q(5, "y", True), _q(5), _q(1, "f")), "1H+5H"
    ),
    CurveSpec(
        35,
        "IH35",
        Family.INHOMOGENEOUS,
        (_q(5, "a", True), _q(5, "g"), _q(5, "o", True), _q(1, "m")),
        "1H+5H",
    ),
    CurveSpec(
        36,
        "IH36",
        Family.INHOMOGENEOUS,
        (_q(5, "x", True), _q(5, "y", True), _q(5), _q(1, "f")),
        "1H+5H",
    ),
    CurveSpec(
        37,
        "IH37",
        Family.INHOMOGENEOUS,
        (_q(5, "m"), _q(5, "g"), _q(5, "o", True), _q(1, "m")),
        "1H+5H",
    ),
    # 1H + 3H + 5H  (Figure 9): two curves.
    CurveSpec(
        38,
        "IH38",
        Family.INHOMOGENEOUS,
        (_q(3, "o"), _q(5, "y", True), _q(5), _q(1, "f")),
        "1H+3H+5H",
    ),
    CurveSpec(
        39,
        "IH39",
        Family.INHOMOGENEOUS,
        (_q(3, "g"), _q(5, "g"), _q(5, "o", True), _q(1, "m")),
        "1H+3H+5H",
    ),
)

# Friendly, human-readable names.  Proper curves keep their established names
# (Hilbert, Moore, Liu1-4); improper curves become Improper1-6; and each
# inhomogeneous curve is named by the curves it mixes plus an index within the
# group, e.g. "Liu2+Liu4 #1" -- so the name states the recipe.
_PROPER_NAME = {0: "Hilbert", 1: "Moore", 2: "Liu1", 3: "Liu2", 4: "Liu3", 5: "Liu4"}


def _with_friendly_names(specs: tuple[CurveSpec, ...]) -> tuple[CurveSpec, ...]:
    counters: dict[str, int] = {}
    out = []
    for s in specs:
        if s.family is Family.HOMOGENEOUS_IMPROPER:
            s = replace(s, name=f"Improper{s.index - 5}")
        elif s.family is Family.INHOMOGENEOUS:
            recipe = "+".join(_PROPER_NAME[k] for k in sorted(s.kernels))
            counters[recipe] = counters.get(recipe, 0) + 1
            s = replace(s, name=f"{recipe} #{counters[recipe]}")
        out.append(s)
    return tuple(out)


#: All forty specifications, ordered by index.
SPECS: tuple[CurveSpec, ...] = _with_friendly_names(_PROPER + _IMPROPER + _INHOMOGENEOUS)

#: Per curve, the four quadrant rules as ``(kernel index, D4 matrix, reverse)``.
#:
#: The same information as :attr:`CurveSpec.quadrants`, with each morphism resolved to its
#: matrix -- the form the geometric constructions in :mod:`hilbertplot._core.arbitrary` and
#: :mod:`hilbertplot._core.indexing` consume.  Built once, at import.
QUADRANT_MATRICES: Mapping[int, tuple[tuple[int, Matrix, bool], ...]] = {
    spec.index: tuple(
        (
            rule.base,
            (
                tuple(MORPHISMS[rule.morphism].matrix[0]),
                tuple(MORPHISMS[rule.morphism].matrix[1]),
            ),
            rule.reverse,
        )
        for rule in spec.quadrants
    )
    for spec in SPECS
}

_BY_INDEX: Mapping[int, CurveSpec] = {s.index: s for s in SPECS}


def spec_by_index(index: int) -> CurveSpec:
    """Return the :class:`CurveSpec` for curve number ``index`` (0..39)."""
    try:
        return _BY_INDEX[index]
    except KeyError:
        raise KeyError(
            f"curve index {index!r} out of range; expected an integer in 0..39"
        ) from None


# --- internal consistency checks (cheap, run once at import) ----------------
# These guard against typos in the table above: the declared family must agree
# with what the kernels imply, and only valid building blocks may appear.
#
# Deliberately `raise` rather than `assert`: these validate the shipped table, so they
# must still run under `python -O`, where assertions are stripped out entirely.
def _self_check() -> None:
    def require(condition: bool, message: str) -> None:
        if not condition:
            raise RuntimeError(f"hilbertplot catalog is inconsistent: {message}")

    require(len(SPECS) == 40, f"expected 40 curves, found {len(SPECS)}")
    require([s.index for s in SPECS] == list(range(40)), "curve indices must be 0..39")
    valid_kernels = {0, 1, 3, 4, 5}  # never 2 (Liu1 cannot connect quadrants)
    for s in SPECS:
        require(len(s.quadrants) == 4, f"curve {s.index} needs four quadrants")
        require(
            s.kernels <= valid_kernels,
            f"curve {s.index} uses invalid kernel(s) {set(s.kernels - valid_kernels)}",
        )
        require(
            (len(s.kernels) == 1) == s.is_homogeneous,
            f"curve {s.index}: family {s.family} disagrees with kernels {set(s.kernels)}",
        )
        if s.family is Family.HOMOGENEOUS_PROPER:
            require(s.kernels == {0}, f"proper curve {s.index} must use kernel 0H")
        elif s.family is Family.HOMOGENEOUS_IMPROPER:
            require(s.kernels == {5}, f"improper curve {s.index} must use kernel 5H")


_self_check()
