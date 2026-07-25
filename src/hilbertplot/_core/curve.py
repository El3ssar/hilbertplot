"""The public :class:`Curve` object, the :class:`CurveList` container, and lookups.

Everything a user touches starts here.  A :class:`Curve` is a light, hashable handle
onto one of the forty curves; :func:`curve` fetches one and the group functions
(:func:`catalog`, :func:`homogeneous`, ...) return a :class:`CurveList` that prints as a
tidy table.
"""

from __future__ import annotations

import numpy as np

from .catalog import SPECS, CurveSpec, Family, spec_by_index
from .generation import curve_word

__all__ = [
    "Curve",
    "CurveList",
    "curve",
    "catalog",
    "homogeneous",
    "inhomogeneous",
    "proper",
    "improper",
    "closed",
    "generalizing",
    "by_kernels",
]

_KIND = {
    Family.HOMOGENEOUS_PROPER: "proper",
    Family.HOMOGENEOUS_IMPROPER: "improper",
    Family.INHOMOGENEOUS: "inhomogeneous",
}


class Curve:
    """One of the forty two-dimensional Hilbert curves.

    A :class:`Curve` carries no per-order state; fetch one with :func:`curve` and then
    ask it for a word, points, a plot, or a data mapping at whatever order you need.

    Parameters
    ----------
    spec : CurveSpec
        The immutable specification backing this curve.  You normally never build a
        :class:`Curve` yourself -- use :func:`curve`.

    Attributes
    ----------
    index : int
        The curve number, ``0``..``39``.
    name : str
        Human-readable name, e.g. ``"Hilbert"``, ``"Moore"``, ``"Improper1"`` or
        ``"Liu2+Liu4 #1"``.
    kind : str
        ``"proper"``, ``"improper"`` or ``"inhomogeneous"``.

    Examples
    --------
    >>> import hilbertplot
    >>> c = hilbertplot.curve("Moore")
    >>> c.name
    'Moore'
    >>> c.word(2)
    'lurulurrrdldrdl'
    >>> c.points(3).shape
    (64, 2)
    """

    __slots__ = ("_spec",)

    def __init__(self, spec: CurveSpec) -> None:
        self._spec = spec

    # -- identity ------------------------------------------------------------
    @property
    def index(self) -> int:
        """int: The curve number in ``0``..``39``."""
        return self._spec.index

    @property
    def name(self) -> str:
        """str: Human-readable name (``"Hilbert"``, ``"Moore"``, ``"Liu2+Liu4 #1"``, ...)."""
        return self._spec.name

    @property
    def symbol(self) -> str:
        """str: The paper's ``{}_nu H`` symbol as ``"<index>H"`` (e.g. ``"0H"``)."""
        return f"{self._spec.index}H"

    @property
    def kind(self) -> str:
        """str: One of ``"proper"``, ``"improper"`` or ``"inhomogeneous"``."""
        return _KIND[self._spec.family]

    @property
    def is_homogeneous(self) -> bool:
        """bool: ``True`` for the twelve homogeneous curves (a single kernel type)."""
        return self._spec.is_homogeneous

    @property
    def is_closed(self) -> bool:
        """bool: ``True`` if the curve closes into a loop (Moore, Liu1, Improper1, Improper4)."""
        return self._spec.closed

    @property
    def generalizes(self) -> bool:
        """bool: ``True`` if the curve tiles an arbitrary ``n x n`` square (see :meth:`grid`).

        Only eight of the forty curves do (proved in ``research/quasisquares/``); the rest
        exist only on ``2**k`` grids.  Use :func:`hilbertplot.generalizing` for the whole group.
        """
        from .arbitrary import FEASIBLE

        return self._spec.index in FEASIBLE

    @property
    def kernels(self) -> frozenset[int]:
        """frozenset[int]: Indices of the building-block curves used in the four quadrants."""
        return self._spec.kernels

    @property
    def combination(self) -> str:
        """str: Kernel mix in paper symbols, e.g. ``"0H"``, ``"5H"``, ``"3H+5H"``."""
        return self._spec.combination

    @property
    def rule(self) -> str:
        """str: The construction rule in the paper's tag-system notation."""
        return self._spec.rule_str()

    # -- construction --------------------------------------------------------
    def word(self, order: int) -> str:
        """Return the curve word at ``order``.

        Parameters
        ----------
        order : int
            Recursion depth ``>= 0``.

        Returns
        -------
        str
            A string of ``4**order - 1`` letters over ``{'u', 'd', 'l', 'r'}``
            (up/down/left/right unit strokes).

        Examples
        --------
        >>> import hilbertplot
        >>> hilbertplot.curve(0).word(2)
        'ruluurdrurddldr'
        """
        return curve_word(self._spec.index, order)

    def points(self, order: int) -> np.ndarray:
        """Return the ordered lattice points the curve visits at ``order``.

        Parameters
        ----------
        order : int
            Recursion depth ``>= 0``.

        Returns
        -------
        numpy.ndarray
            An ``(4**order, 2)`` integer array of ``(x, y)`` cells in visit order,
            shifted so the minimum corner is ``(0, 0)`` (spanning ``0``..``2**order - 1``
            on each axis).

        Examples
        --------
        >>> import hilbertplot
        >>> hilbertplot.curve(0).points(1).tolist()
        [[0, 0], [0, 1], [1, 1], [1, 0]]
        """
        from .generation import curve_codes
        from .geometry import codes_to_points

        return codes_to_points(curve_codes(self._spec.index, order))

    def grid(self, n: int) -> np.ndarray:
        """Return the curve on an arbitrary ``n x n`` square: ``(n*n, 2)`` cells, in order.

        Unlike :meth:`points` (which only reaches ``2**k`` grids), ``grid`` fills any
        square side ``n`` using the approximately-even-partition construction.  It agrees
        with :meth:`points` exactly at ``n = 2**k``.

        Parameters
        ----------
        n : int
            Grid side, any integer ``>= 1``.

        Returns
        -------
        numpy.ndarray
            An ``(n*n, 2)`` integer array of ``(x, y)`` cells in visit order.

        Raises
        ------
        ValueError
            If this curve does not generalize to arbitrary squares
            (:attr:`generalizes` is ``False``), or ``n < 1``.

        Examples
        --------
        >>> import hilbertplot
        >>> hilbertplot.curve(0).grid(100).shape
        (10000, 2)
        """
        from .arbitrary import FEASIBLE, WITNESS, square_points

        idx = self._spec.index
        if idx not in FEASIBLE:
            raise ValueError(
                f"{self.name} does not tile arbitrary squares (it fails at "
                f"n={WITNESS.get(idx, '?')}); use points(order) for a 2**order grid, "
                f"or pick a curve from hilbertplot.generalizing()."
            )
        if n < 1:
            raise ValueError(f"n must be >= 1, got {n}")
        return square_points(idx, n)

    def unroll(self, array) -> np.ndarray:
        """Read a 2-D array along this curve's path, returning a 1-D vector.

        The inverse of laying data onto the plane (:func:`hilbertplot.hilbert_plot`): it walks
        the curve over a square array and reads the values in visit order, so neighbouring
        entries of the result are neighbours along the curve.

        The array side may be **any** integer when the curve :attr:`generalizes`
        (arbitrary squares via :meth:`grid`); otherwise it must be a power of two.  At
        ``2**k`` the two paths coincide, so a round trip with :func:`hilbertplot.hilbert_plot`
        is exact either way.

        Parameters
        ----------
        array : array_like
            A square 2-D array indexed ``array[y, x]`` (row ``y``, column ``x``).

        Returns
        -------
        numpy.ndarray
            A 1-D array of length ``side * side`` in curve order.

        Raises
        ------
        ValueError
            If ``array`` is not square, or its side is not a power of two and this curve
            does not generalize to arbitrary squares.

        Examples
        --------
        >>> import numpy as np, hilbertplot
        >>> data = np.arange(100)                         # not a power of four
        >>> img = hilbertplot.hilbert_plot(0, data).image()     # 10x10 (Hilbert generalizes)
        >>> np.array_equal(hilbertplot.curve(0).unroll(img), data)   # ...and read it back
        True
        """
        from .._data.mapping import gather

        array = np.asarray(array)
        if array.ndim != 2 or array.shape[0] != array.shape[1]:
            raise ValueError(f"expected a square 2-D array, got shape {array.shape!r}")
        side = array.shape[0]
        if side < 1:
            raise ValueError("array must have side >= 1")
        order = side.bit_length() - 1
        if (1 << order) == side:
            points = self.points(order)  # power of two: fast path
        elif self.generalizes:
            points = self.grid(side)  # arbitrary square
        else:
            raise ValueError(
                f"array side {side} is not a power of two, and {self.name} does not "
                f"generalize to arbitrary squares (see hilbertplot.generalizing())"
            )
        return gather(points, array)

    def difference_map(self, order: int) -> np.ndarray:
        """Return the curve's *difference map* at ``order`` (a locality-loss field).

        At each cell the value is the mean of ``|label - neighbour_label|`` over its
        up-to-8 nearest neighbours, where ``label`` is the step at which the curve
        reaches a cell.  Large values mark where cells that are neighbours on the plane
        are far apart along the curve -- i.e. where the curve breaks locality (there is
        always such a barrier between quadrants 1 and 4).  Depends only on the curve, not
        on any data.

        Parameters
        ----------
        order : int
            Recursion depth; the map is ``2**order`` by ``2**order``.

        Returns
        -------
        numpy.ndarray
            An ``(2**order, 2**order)`` float array, indexed ``[y, x]``.

        See Also
        --------
        HilbertPlot.show : overlay the strong-locality barrier on a data plot with
            ``difference=True``.

        Examples
        --------
        >>> import hilbertplot
        >>> hilbertplot.curve(0).difference_map(3).shape
        (8, 8)
        """
        from .._data.mapping import difference_map

        return difference_map(self.points(order), 2**order)

    # -- data plotting -------------------------------------------------------
    def plot_data(self, data) -> HilbertPlot:  # noqa: F821 (forward ref)
        """Bind a 1-D ``data`` vector to this curve, returning a :class:`HilbertPlot`.

        Nothing is drawn.  The returned object renders on demand -- choose the colormap,
        granularity and power-of-four fit when you call its ``show``/``save`` methods.

        Parameters
        ----------
        data : array_like
            The 1-D sequence to visualise.

        Returns
        -------
        HilbertPlot

        Examples
        --------
        >>> import hilbertplot
        >>> plot = hilbertplot.curve(0).plot_data(range(1024))
        >>> plot.show(["red", "green", "tab:blue"])   # doctest: +SKIP
        """
        from .._viz.hilbert_plot import HilbertPlot

        return HilbertPlot(self, data)

    # -- curve plotting ------------------------------------------------------
    def plot(self, order: int, ax=None, **style):
        """Draw the curve at ``order`` and return the matplotlib ``Axes``.

        Parameters
        ----------
        order : int
            Recursion depth to render.
        ax : matplotlib.axes.Axes, optional
            Axes to draw on; a new figure is created when ``None``.
        **style
            Forwarded to the renderer (``mode``, ``color``, ``cmap``, ``linewidth``, ...).

        Returns
        -------
        matplotlib.axes.Axes
        """
        from .._viz.render import draw

        return draw(self, order, ax=ax, **style)

    def show(self, order: int, **style) -> None:
        """Draw the curve at ``order`` and open a window.

        Parameters
        ----------
        order : int
            Recursion depth to render.
        **style
            Forwarded to :meth:`plot`.
        """
        from .._viz.render import draw, pyplot

        draw(self, order, ax=None, **style)
        pyplot().show()

    def save(self, order: int, path: str, *, dpi: int = 140, **style) -> str:
        """Draw the curve at ``order``, save it to ``path`` and return ``path``.

        Parameters
        ----------
        order : int
            Recursion depth to render.
        path : str
            Output file path (format inferred from the extension).
        dpi : int, default 140
            Output resolution.
        **style
            Forwarded to :meth:`plot`.

        Returns
        -------
        str
            ``path``.
        """
        from .._viz.render import draw, pyplot

        ax = draw(self, order, ax=None, **style)
        ax.figure.savefig(path, dpi=dpi, bbox_inches="tight")
        pyplot().close(ax.figure)
        return path

    # -- dunders -------------------------------------------------------------
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Curve) and other._spec.index == self._spec.index

    def __hash__(self) -> int:
        return hash(self._spec.index)

    def __repr__(self) -> str:
        return self._spec.name

    __str__ = __repr__


class CurveList(list):
    """A ``list`` of :class:`Curve` objects that prints as a readable table.

    Behaves exactly like a list (indexing, iteration, ``len``); only its text
    representation is prettier.

    Examples
    --------
    >>> import hilbertplot
    >>> print(hilbertplot.proper())          # doctest: +NORMALIZE_WHITESPACE
    #  name     kind    closed
    -  -------  ------  ------
    0  Hilbert  proper
    1  Moore    proper  yes
    2  Liu1     proper  yes
    3  Liu2     proper
    4  Liu3     proper
    5  Liu4     proper
    """

    def __repr__(self) -> str:
        if not self:
            return "CurveList([])"
        header = ("#", "name", "kind", "closed")
        rows = [header]
        rows += [(str(c.index), c.name, c.kind, "yes" if c.is_closed else "") for c in self]
        widths = [max(len(row[i]) for row in rows) for i in range(len(header))]
        out = []
        for i, row in enumerate(rows):
            out.append("  ".join(cell.ljust(widths[j]) for j, cell in enumerate(row)).rstrip())
            if i == 0:
                out.append("  ".join("-" * w for w in widths))
        return "\n".join(out)

    __str__ = __repr__


# The forty curves, built once.
_CATALOG: tuple[Curve, ...] = tuple(Curve(spec) for spec in SPECS)


def _norm(name: str) -> str:
    """Normalise a name/symbol for tolerant lookup (drop case, spaces and ``#``)."""
    return name.lower().replace(" ", "").replace("#", "")


# Look up by friendly name ("Liu2+Liu4 #1") or paper symbol ("12H"), both tolerant.
_BY_NAME: dict[str, Curve] = {}
for _c in _CATALOG:
    _BY_NAME[_norm(_c.name)] = _c
    _BY_NAME[_norm(_c.symbol)] = _c


def curve(which: int | str) -> Curve:
    """Fetch a curve by index, friendly name, or paper symbol.

    Parameters
    ----------
    which : int or str
        A curve index (``0``..``39``), a friendly name (``"Moore"``,
        ``"Liu2+Liu4 #1"``), or a paper symbol (``"12H"``).  Name/symbol lookup is
        case-insensitive and ignores spaces and ``#``, so ``"Liu2+Liu4 #1"``,
        ``"liu2+liu4 1"`` and ``"12H"`` all resolve to curve 12.

    Returns
    -------
    Curve

    Raises
    ------
    KeyError
        If no curve matches ``which``.

    Examples
    --------
    >>> import hilbertplot
    >>> hilbertplot.curve(0).name
    'Hilbert'
    >>> hilbertplot.curve("moore").index
    1
    """
    if isinstance(which, str):
        try:
            return _BY_NAME[_norm(which)]
        except KeyError:
            raise KeyError(f"no curve named {which!r}") from None
    return _CATALOG[spec_by_index(which).index]


def catalog() -> CurveList:
    """Return all forty curves, ordered by index.

    Returns
    -------
    CurveList

    Examples
    --------
    >>> import hilbertplot
    >>> len(hilbertplot.catalog())
    40
    """
    return CurveList(_CATALOG)


def homogeneous() -> CurveList:
    """Return the twelve homogeneous curves (a single kernel type): indices 0-11.

    Returns
    -------
    CurveList
    """
    return CurveList(c for c in _CATALOG if c.is_homogeneous)


def inhomogeneous() -> CurveList:
    """Return the twenty-eight inhomogeneous curves (mixed kernels): indices 12-39.

    Returns
    -------
    CurveList
    """
    return CurveList(c for c in _CATALOG if not c.is_homogeneous)


def proper() -> CurveList:
    """Return the six proper curves (kernel Hilbert): Hilbert, Moore, Liu1-4.

    Returns
    -------
    CurveList
    """
    return CurveList(c for c in _CATALOG if c.kind == "proper")


def improper() -> CurveList:
    """Return the six improper curves (kernel Liu4): Improper1-6.

    Returns
    -------
    CurveList
    """
    return CurveList(c for c in _CATALOG if c.kind == "improper")


def closed() -> CurveList:
    """Return the curves that close into a loop: Moore, Liu1, Improper1, Improper4.

    Returns
    -------
    CurveList
    """
    return CurveList(c for c in _CATALOG if c.is_closed)


def generalizing() -> CurveList:
    """Return the curves that tile an arbitrary ``n x n`` square (see :meth:`Curve.grid`).

    Exactly eight of the forty: Hilbert, Liu2, Liu3, Liu4, and the four composites
    Hilbert+Liu3 #7/#12/#13/#14.  The other thirty-two exist only on ``2**k`` grids
    (proved in ``research/quasisquares/``).

    Returns
    -------
    CurveList
    """
    return CurveList(c for c in _CATALOG if c.generalizes)


def by_kernels(*indices: int) -> CurveList:
    """Return curves whose kernel set is exactly ``indices``.

    Parameters
    ----------
    *indices : int
        Kernel curve indices, e.g. ``by_kernels(3, 5)`` for the six Liu2+Liu4 curves.

    Returns
    -------
    CurveList

    Examples
    --------
    >>> import hilbertplot
    >>> [c.index for c in hilbertplot.by_kernels(3, 5)]
    [12, 13, 14, 15, 16, 17]
    """
    target = frozenset(indices)
    return CurveList(c for c in _CATALOG if c.kernels == target)
