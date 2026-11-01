"""Internal curve handles, curve lists, and lookups used by the function-based API.

The public functions delegate here. A :class:`Curve` is a light, hashable handle
onto one of the forty curves; :func:`curve` fetches one and the group functions
(:func:`catalog`, :func:`homogeneous`, ...) return a :class:`CurveList` that prints as a
tidy table.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

import numpy as np

from .catalog import SPECS, CurveSpec, Family, spec_by_index
from .generation import curve_word

if TYPE_CHECKING:
    # Annotation-only imports: matplotlib is an optional extra and must stay out of the
    # import path, and HilbertPlot would be a cycle.
    from matplotlib.axes import Axes

    from .._viz.hilbert_plot import HilbertPlot
else:
    # ...but `from __future__ import annotations` makes every annotation a string, and
    # `typing.get_type_hints()` evaluates those strings in the *module* namespace.  Without
    # runtime stand-ins it raises NameError, which breaks Sphinx autodoc, pydantic and
    # anything else that introspects a py.typed package.  `Any` is the honest runtime
    # answer; type checkers still see the real classes above.
    Axes = Any
    HilbertPlot = Any

__all__ = [
    "Curve",
    "CurveList",
    "by_kernels",
    "catalog",
    "closed",
    "curve",
    "generalizing",
    "homogeneous",
    "improper",
    "inhomogeneous",
    "proper",
]

_KIND = {
    Family.HOMOGENEOUS_PROPER: "proper",
    Family.HOMOGENEOUS_IMPROPER: "improper",
    Family.INHOMOGENEOUS: "inhomogeneous",
}


#: Order used for the inline notebook preview: fine enough to show the curve's character,
#: coarse enough that a cell renders instantly.
_REPR_ORDER = 5


def _check_int(value: int, name: str) -> int:
    """Return ``value`` as an ``int``, rejecting ``bool`` and non-integers.

    ``bool`` is a subclass of ``int``, so without this ``curve(True)`` would quietly mean
    ``curve(1)``; and ``3.0`` would index as ``3`` while ``3.5`` silently truncated.
    """
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    return int(value)


def _check_index_order(order: int) -> int:
    """Validate an ``order`` for the ``O(order)`` index maths, which materialises nothing.

    Unlike :func:`hilbertplot._core.generation.check_order` there is no memory ceiling
    here -- :meth:`Curve.encode` at order 200 is perfectly reasonable.
    """
    order = _check_int(order, "order")
    if order < 0:
        raise ValueError(f"order must be non-negative, got {order}")
    return order


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
    >>> from hilbertplot._core import curve as curves
    >>> c = curves.curve("Moore")
    >>> c.name
    'Moore'
    >>> c.word(2)
    'lurulurrrdldrdl'
    >>> c.points(3).shape
    (64, 2)
    """

    __slots__ = ("_spec",)

    def __init__(self, spec: CurveSpec) -> None:
        if not isinstance(spec, CurveSpec):
            raise TypeError(
                f"Curve() takes a CurveSpec, got {type(spec).__name__}; "
                "Curve is internal; use the private curve() factory for internal lookups."
            )
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
        exist only on ``2**k`` grids. Use :func:`hilbertplot.curves.generalizing`
        for the whole group.
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
        >>> from hilbertplot._core import curve as curves
        >>> curves.curve(0).word(2)
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
        >>> from hilbertplot._core import curve as curves
        >>> curves.curve(0).points(1).tolist()
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
            (:attr:`generalizes` is ``False``), ``n < 1``, or the square would exceed
            :func:`hilbertplot.config.cell_limit`.
        TypeError
            If ``n`` is not an integer.

        Examples
        --------
        >>> from hilbertplot._core import curve as curves
        >>> curves.curve(0).grid(100).shape
        (10000, 2)
        """
        from .arbitrary import FEASIBLE, SMALLEST_FAILURE, square_points
        from .limits import check_cells

        # Argument shape first, curve capability second -- otherwise `grid(-2)` on an
        # infeasible curve blames the curve and quotes a size the caller never asked for.
        n = _check_int(n, "n")
        if n < 1:
            raise ValueError(f"n must be >= 1, got {n}")
        idx = self._spec.index
        if idx not in FEASIBLE:
            raise ValueError(
                f"{self.name} does not tile arbitrary squares (the construction already "
                f"breaks at n={SMALLEST_FAILURE[idx]}); use points(order) for a 2**order "
                f"grid, or pick a curve from hilbertplot.curves.generalizing()."
            )
        check_cells(n * n, f"a {n}x{n} square")
        return square_points(idx, n)

    def encode(self, i: int, order: int) -> tuple[int, int]:
        """Return the ``(x, y)`` cell this curve visits at step ``i``, without building it.

        Where :meth:`points` materialises all ``4**order`` cells, ``encode`` answers for a
        single step in ``O(order)`` arithmetic -- so it works at orders whose curve could
        never fit in memory.

        Parameters
        ----------
        i : int
            Step along the curve, ``0 <= i < 4**order``.
        order : int
            Recursion depth ``>= 0``.

        Returns
        -------
        tuple of int
            The cell ``(x, y)``, each coordinate in ``0``..``2**order - 1``.

        See Also
        --------
        decode : the inverse.

        Examples
        --------
        >>> from hilbertplot._core import curve as curves
        >>> curves.curve(0).encode(5, 2)
        (0, 3)
        >>> curves.curve(0).encode(10**18, 40)     # 2**80 cells: unbuildable
        (751054336, 346100736)
        """
        from .indexing import encode

        order = _check_index_order(order)
        i = _check_int(i, "i")
        if not 0 <= i < 4**order:
            raise ValueError(f"i must be in 0..{4**order - 1} for order {order}, got {i}")
        return encode(self._spec.index, i, order)

    def decode(self, x: int, y: int, order: int) -> int:
        """Return the step at which this curve reaches cell ``(x, y)``, without building it.

        The inverse of :meth:`encode`, also ``O(order)``.

        Parameters
        ----------
        x, y : int
            Cell coordinates, each in ``0``..``2**order - 1``.
        order : int
            Recursion depth ``>= 0``.

        Returns
        -------
        int
            The step ``i`` with ``encode(i, order) == (x, y)``.

        See Also
        --------
        encode : the inverse.

        Examples
        --------
        >>> from hilbertplot._core import curve as curves
        >>> curves.curve(0).decode(0, 3, 2)
        5
        """
        from .indexing import decode

        order = _check_index_order(order)
        side = 1 << order
        x, y = _check_int(x, "x"), _check_int(y, "y")
        if not (0 <= x < side and 0 <= y < side):
            raise ValueError(f"(x, y) must lie in 0..{side - 1} for order {order}, got {(x, y)}")
        return decode(self._spec.index, x, y, order)

    def label_map(self, order: int) -> np.ndarray:
        """Return the ``(2**order, 2**order)`` grid of visit-order indices.

        ``label_map(order)[y, x]`` is the step at which the curve reaches cell ``(x, y)``
        -- the inverse of :meth:`points`, as an image.

        Parameters
        ----------
        order : int
            Recursion depth ``>= 0``.

        Returns
        -------
        numpy.ndarray
            An integer array indexed ``[y, x]``.

        Examples
        --------
        >>> from hilbertplot._core import curve as curves
        >>> curves.curve(0).label_map(1).tolist()
        [[0, 3], [1, 2]]
        """
        from .._data.mapping import label_map

        return label_map(self.points(order), 2**order)

    def unroll(self, array) -> np.ndarray:
        """Read a 2-D array along this curve's path, returning a 1-D vector.

        The inverse of laying data onto the plane: it walks
        the curve over a square array and reads the values in visit order, so neighbouring
        entries of the result are neighbours along the curve.

        The array side may be **any** integer when the curve :attr:`generalizes`
        (arbitrary squares via :meth:`grid`); otherwise it must be a power of two.  At
        ``2**k`` the two paths coincide, so the data mapping round trip is exact either way.

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
        >>> from hilbertplot._core import curve as curves
        >>> data = np.arange(100)                         # not a power of four
        >>> img = hilbertplot.data.to_grid(data, fit="square")     # 10x10 (Hilbert generalizes)
        >>> np.array_equal(curves.curve(0).unroll(img), data)   # ...and read it back
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
                f"generalize to arbitrary squares (see hilbertplot.curves.generalizing())"
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
        HilbertPlot.draw : render the full difference map with ``difference=True``.

        Examples
        --------
        >>> from hilbertplot._core import curve as curves
        >>> curves.curve(0).difference_map(3).shape
        (8, 8)
        """
        from .._data.mapping import difference_map

        return difference_map(self.points(order), 2**order)

    # -- data plotting -------------------------------------------------------
    def plot_data(self, data) -> HilbertPlot:
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
        >>> from hilbertplot._core import curve as curves
        >>> plot = curves.curve(0).plot_data(range(1024))
        >>> plot.show(["red", "green", "tab:blue"])   # doctest: +SKIP
        """
        from .._viz.hilbert_plot import HilbertPlot

        return HilbertPlot(self, data)

    # -- curve plotting ------------------------------------------------------
    def draw(self, order: int, ax: Axes | None = None, **style) -> Axes:
        """Draw the curve at ``order`` onto ``ax`` and return it -- no window.

        Parameters
        ----------
        order : int
            Recursion depth to render.
        ax : matplotlib.axes.Axes, optional
            Axes to draw on; a new figure is created when ``None``.
        **style
            Forwarded to the renderer:

            ``mode`` : {"auto", "line", "fill"}
                ``"line"`` draws the polyline (colour-graded by traversal order below
                order 8), ``"fill"`` paints one pixel per cell.  ``"auto"`` picks ``line``
                below order 8 and ``fill`` at or above it.
            ``color`` : color
                A solid line colour; overrides the traversal gradient.
            ``cmap`` : str, default "viridis"
                Colormap for the gradient and fill modes.
            ``linewidth`` : float
                Line width; scaled from ``order`` when omitted.
            ``endpoints`` : bool, default True
                Mark the entry (circle) and exit (square) cells.
            ``title`` : str
                Axes title; names the curve and order when omitted.

        Returns
        -------
        matplotlib.axes.Axes

        Examples
        --------
        >>> from hilbertplot._core import curve as curves
        >>> ax = curves.curve(0).draw(4)                        # doctest: +SKIP
        >>> ax = curves.curve("Moore").draw(8, mode="fill")     # doctest: +SKIP
        """
        from .._viz.render import draw

        return draw(self, order, ax=ax, **style)

    def show(self, order: int, **style) -> Axes:
        """Draw the curve at ``order``, open a window, and return the axes.

        Parameters
        ----------
        order : int
            Recursion depth to render.
        **style
            Forwarded to :meth:`draw`.

        Returns
        -------
        matplotlib.axes.Axes
        """
        from .._viz.render import pyplot

        ax = self.draw(order, **style)
        pyplot().show()
        return ax

    def save(self, path: str, order: int, *, dpi: int = 140, **style) -> str:
        """Draw the curve at ``order``, save it to ``path`` and return ``path``.

        Parameters
        ----------
        path : str
            Output file path (format inferred from the extension).
        order : int
            Recursion depth to render.
        dpi : int, default 140
            Output resolution.
        **style
            Forwarded to :meth:`draw`.

        Returns
        -------
        str
            ``path``.

        Examples
        --------
        >>> from hilbertplot._core import curve as curves
        >>> curves.curve(0).save("hilbert.png", 6)       # doctest: +SKIP
        'hilbert.png'
        """
        from .._viz.render import save_figure

        if isinstance(path, (int, np.integer)) and isinstance(order, (str, os.PathLike)):
            # 0.1.0 spelled this save(order, path); fail loudly rather than confusingly.
            raise TypeError(
                "Curve.save() now takes (path, order) so it matches HilbertPlot.save(); "
                f"call save({order!r}, {path!r}) instead."
            )
        return save_figure(self.draw(order, **style), path, dpi=dpi)

    # -- dunders -------------------------------------------------------------
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Curve) and other._spec.index == self._spec.index

    def __hash__(self) -> int:
        return hash(self._spec.index)

    def __lt__(self, other: object) -> bool:
        """Order by index, so ``sorted``/``min``/``max`` work over a :class:`CurveList`."""
        if not isinstance(other, Curve):
            return NotImplemented
        return self._spec.index < other._spec.index

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Curve):
            return NotImplemented
        return self._spec.index <= other._spec.index

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Curve):
            return NotImplemented
        return self._spec.index > other._spec.index

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Curve):
            return NotImplemented
        return self._spec.index >= other._spec.index

    def __index__(self) -> int:
        """Allow a ``Curve`` to be used wherever its index is expected."""
        return self._spec.index

    def __repr__(self) -> str:
        return f"<Curve {self.symbol} {self._spec.name} ({self.kind})>"

    def __str__(self) -> str:
        return self._spec.name

    def _repr_png_(self) -> bytes | None:
        """Render inline in Jupyter, so ``hilbertplot.curves.info(0)`` in a cell shows the curve.

        Returns ``None`` when matplotlib is not installed, which makes the notebook fall
        back to :meth:`__repr__` instead of raising -- matplotlib is an optional extra.
        """
        try:
            from .._viz.render import figure_png
        except ModuleNotFoundError:  # pragma: no cover - matplotlib is a test dependency
            return None
        try:
            return figure_png(self.draw(_REPR_ORDER, ax=None))
        except ModuleNotFoundError:  # pragma: no cover - matplotlib absent
            return None


class CurveList(list):
    """A ``list`` of :class:`Curve` objects that prints as a readable table.

    Behaves exactly like a list (indexing, iteration, ``len``), and slicing, ``+`` and
    ``copy()`` give back a ``CurveList`` rather than degrading to a plain ``list``, so
    groups stay composable and keep printing as a table.

    Examples
    --------
    >>> from hilbertplot._core import curve as curves
    >>> print(curves.proper())          # doctest: +NORMALIZE_WHITESPACE
    #  name     kind    closed
    -  -------  ------  ------
    0  Hilbert  proper
    1  Moore    proper  yes
    2  Liu1     proper  yes
    3  Liu2     proper
    4  Liu3     proper
    5  Liu4     proper
    >>> curves.proper()[:2].names
    ['Hilbert', 'Moore']
    >>> curves.catalog().closed().names
    ['Moore', 'Liu1', 'Improper1', 'Improper4']
    """

    # -- keep the type through the usual list operations ---------------------
    def __getitem__(self, item):
        result = list.__getitem__(self, item)
        return CurveList(result) if isinstance(item, slice) else result

    def __add__(self, other):
        return CurveList(list.__add__(self, other))

    def __mul__(self, count):
        return CurveList(list.__mul__(self, count))

    __rmul__ = __mul__

    def copy(self) -> CurveList:
        return CurveList(self)

    # -- convenience ---------------------------------------------------------
    @property
    def indices(self) -> list[int]:
        """list[int]: The index of every curve in this list."""
        return [c.index for c in self]

    @property
    def names(self) -> list[str]:
        """list[str]: The name of every curve in this list."""
        return [c.name for c in self]

    def closed(self) -> CurveList:
        """Return just the curves in this list that close into a loop."""
        return CurveList(c for c in self if c.is_closed)

    def generalizing(self) -> CurveList:
        """Return just the curves in this list that tile arbitrary ``n x n`` squares."""
        return CurveList(c for c in self if c.generalizes)

    def gallery(self, order: int = 3, **kwargs):
        """Draw this list as a grid of panels -- see :func:`hilbertplot.gallery`."""
        from .._viz.render import gallery

        return gallery(self, order=order, **kwargs)

    # -- presentation --------------------------------------------------------
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


def _suggest(name: str, limit: int = 3) -> list[str]:
    """Return the closest real curve names to a misspelling, or an empty list if none are."""
    from difflib import get_close_matches

    candidates = {c.name for c in _CATALOG} | {c.symbol for c in _CATALOG}
    return get_close_matches(name, sorted(candidates), n=limit, cutoff=0.6)


def curve(which: int | str | Curve) -> Curve:
    """Fetch a curve by index, friendly name, paper symbol -- or pass one straight through.

    Parameters
    ----------
    which : int or str or Curve
        A curve index (``0``..``39``), a friendly name (``"Moore"``,
        ``"Liu2+Liu4 #1"``), or a paper symbol (``"12H"``).  Name/symbol lookup is
        case-insensitive and ignores spaces and ``#``, so ``"Liu2+Liu4 #1"``,
        ``"liu2+liu4 1"`` and ``"12H"`` all resolve to curve 12.  An existing
        :class:`Curve` is returned unchanged, so this is safe to call on any input.

    Returns
    -------
    Curve

    Raises
    ------
    IndexError
        If ``which`` is an integer outside ``0``..``39``.
    KeyError
        If ``which`` is a string that names no curve.  The message suggests near matches.
    TypeError
        If ``which`` is not an integer, string or :class:`Curve`.  ``bool`` and ``float``
        are rejected on purpose: ``curve(True)`` silently meant ``curve(1)`` before, and
        ``curve(3.5)`` truncated.

    Examples
    --------
    >>> from hilbertplot._core import curve as curves
    >>> curves.curve(0).name
    'Hilbert'
    >>> curves.curve("moore").index
    1
    >>> curves.curve(curves.curve(7)).index      # idempotent
    7
    """
    if isinstance(which, Curve):
        return which
    if isinstance(which, str):
        try:
            return _BY_NAME[_norm(which)]
        except KeyError:
            close = _suggest(which)
            hint = (
                f"did you mean one of {', '.join(repr(n) for n in close)}?"
                if close
                else "see hilbertplot.curves.catalog() for the forty names, or use an index 0..39"
            )
            raise KeyError(f"no curve named {which!r}; {hint}") from None
    index = _check_int(which, "curve index")
    if not 0 <= index < len(_CATALOG):
        raise IndexError(f"curve index {index} out of range; expected 0..{len(_CATALOG) - 1}")
    return _CATALOG[spec_by_index(index).index]


def catalog() -> CurveList:
    """Return all forty curves, ordered by index.

    Returns
    -------
    CurveList

    Examples
    --------
    >>> from hilbertplot._core import curve as curves
    >>> len(curves.catalog())
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
    >>> from hilbertplot._core import curve as curves
    >>> [c.index for c in curves.by_kernels(3, 5)]
    [12, 13, 14, 15, 16, 17]
    """
    target = frozenset(indices)
    return CurveList(c for c in _CATALOG if c.kernels == target)
