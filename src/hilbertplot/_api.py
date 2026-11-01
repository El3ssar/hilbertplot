"""Function-based public API. Curve and plot objects stay inside the implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from ._core import curve as _curves
from ._core.generation import check_order as _check_order
from ._viz.hilbert_plot import HilbertPlot as _HilbertPlot

if TYPE_CHECKING:
    from matplotlib.figure import Figure as _Figure
else:
    _Figure = Any


def _data_plot(data, curve):
    values = np.asanyarray(data)
    if values.ndim != 1:
        raise ValueError(
            f"data must be a 1-D sequence, got shape {values.shape}; "
            "flatten explicitly with .ravel(), or use hp.data.from_grid(image, curve=...)."
        )
    if np.iscomplexobj(values):
        raise TypeError("data must be real; choose np.abs(data), np.angle(data), .real or .imag")
    if np.ma.isMaskedArray(values):
        values = values.astype(float).filled(np.nan)
    result = _HilbertPlot(_curves.curve(curve), values)
    if np.isinf(result.data).any():
        raise ValueError("data contains infinity; replace infinite values before plotting")
    return result


def _check_size(plot, order, fit):
    # Explicit truncation is the only way to drop values in the new interface.
    if order is not None:
        order = _check_order(order)
        if len(plot) > 4**order and fit != "truncate":
            raise ValueError(
                f"{len(plot)} values do not fit in order {order} ({4**order} cells). "
                "Use a larger order, omit order, or choose fit='truncate' explicitly."
            )


def plot(
    data,
    *,
    curve: int | str = 0,
    fourier: bool = False,
    difference: bool = False,
    granularity: int = 1,
    cmap="viridis",
    fit: str = "pad",
    order: int | None = None,
    colorbar: bool = True,
    ax=None,
    **style,
) -> _Figure:
    """Plot a numeric sequence on a curve and return its matplotlib Figure.

    ``curve`` accepts an index 0..39, a label such as ``"Moore"``, or a paper
    symbol such as ``"12H"``. Omit it for the standard Hilbert curve.

    Each call draws one image: data by default, the 2-D Fourier magnitude when
    ``fourier=True``, or the full locality-loss field when ``difference=True``.
    The two flags default to False (0) and cannot both be enabled. The difference
    map describes the curve's geometry, independently of the measurement values.

    ``granularity`` averages consecutive blocks while preserving sequence length.
    ``fit='pad'`` works on all forty curves; ``'auto'`` selects a compact square
    where supported, ``'square'`` requires that support, and ``'truncate'``
    explicitly allows dropping the tail. ``order`` fixes a 2**order square.

    Pass ``ax=`` to draw on existing axes. No window opens automatically; use
    ``plt.show()`` in scripts, or ``figure.savefig(path)`` to save. Extra style
    keywords include ``title``, ``vmin``, ``vmax``, ``norm`` and ``alpha``. Fourier
    options are ``window`` (Hann, default False), ``log`` (default True), and
    ``remove_dc`` (default True). NaN cells are transparent.

    Examples
    --------
    >>> import hilbertplot as hp
    >>> fig = hp.plot([1, 2, 3, 4], curve="Moore")  # doctest: +SKIP
    >>> fig = hp.plot(range(100), fourier=True)      # doctest: +SKIP
    """
    from ._viz.hilbert_plot import _check_transforms

    _check_transforms(fourier, difference)
    for name in ("view", "panels", "overlay", "difference_threshold", "difference_color"):
        if name in style:
            raise TypeError(
                f"plot() does not accept {name!r}; use fourier=True or difference=True "
                "for a single transformed image"
            )
    result = _data_plot(data, curve)
    _check_size(result, order, fit)
    axes = result.draw(
        cmap,
        fourier=fourier,
        difference=difference,
        granularity=granularity,
        fit=fit,
        order=order,
        colorbar=colorbar,
        ax=ax,
        **style,
    )
    return axes.get_figure()


def plot_curve(
    curve: int | str = 0,
    order: int | None = None,
    *,
    shape: tuple[int, int] | None = None,
    ax=None,
    mode: str = "auto",
    color=None,
    cmap="viridis",
    linewidth: float | None = None,
    endpoints: bool = True,
    title: str | None = None,
) -> _Figure:
    """Draw a curve (index or label) and return its matplotlib Figure.

    Use ``shape=(rows, columns)`` for an explicit square or quasisquare. Arbitrary
    sizes require a generalizing curve (0, 3, 4, 5, 24, 29, 30, 31); a quasisquare
    has sides differing by one. Its orientation is chosen to keep the path connected.
    Alternatively use ``order`` for a power-of-two square. Omit both for order 4.
    Supplying both ``shape`` and ``order`` is an error.

    ``mode`` is ``'line'``, ``'fill'``, or ``'auto'`` (line below order 8, fill
    otherwise). ``color`` selects a solid line; ``cmap`` colours visit order.
    Use ``fig.savefig(path)`` to save or ``plt.show()`` to display in a script.
    """
    from ._viz.render import draw

    axes = draw(
        _curves.curve(curve),
        order,
        shape=shape,
        ax=ax,
        mode=mode,
        color=color,
        cmap=cmap,
        linewidth=linewidth,
        endpoints=endpoints,
        title=title,
    )
    return axes.get_figure()


def to_grid(
    data,
    *,
    curve: int | str = 0,
    shape: tuple[int, ...] | None = None,
    granularity: int = 1,
    fit: str = "pad",
    order: int | None = None,
    fill: float | complex = np.nan,
) -> np.ndarray:
    """Place samples on a curve, preserving their dtype and trailing channel axes.

    Scalars (N,) become a grid (rows, columns); pixel samples (N, C) become
    (rows, columns, C). A flat colour sequence can be reconstructed by passing
    its original ``shape=(rows, columns, C)``. Shape and order are mutually exclusive.
    Without shape, sizing matches plot(). Granularity > 1 explicitly averages
    blocks and may change the dtype.

    Explicit spatial shapes must be supported squares or quasisquares, using
    the same connected path as plot_curve(shape=...). General rectangles and
    shapes unsupported by the selected curve raise an error, without a fallback.

    With no padding, the input dtype is retained exactly, including complex and
    large-integer values. Default NaN padding uses the input floating/complex dtype;
    integer/bool padding uses a numpy masked array to avoid lossy float conversion.
    An explicit representable fill (e.g. fill=0) retains ordinary integer arrays.
    Input masks are preserved. Plotting remains restricted to real scalar sequences.

    >>> import hilbertplot as hp
    >>> hp.data.to_grid(range(100)).shape
    (16, 16)
    >>> hp.data.to_grid(range(100), fit="square").shape
    (10, 10)
    """
    from ._data.conversion import to_grid as convert

    return convert(
        data, curve=curve, shape=shape, order=order, fit=fit, fill=fill, granularity=granularity
    )


def fourier(
    data,
    *,
    curve: int | str = 0,
    granularity: int = 1,
    fit: str = "pad",
    order: int | None = None,
    log: bool = True,
    window: bool = False,
    remove_dc: bool = True,
) -> np.ndarray:
    """Return the centred 2-D FFT magnitude of the data image, without rendering.

    Defaults match ``plot(data, fourier=True)``: ``log1p`` magnitude and mean
    subtraction, without a Hann window. This is not squared power or a 1-D FFT.
    Missing cells are filled with the mean of valid values for the transform.
    """
    result = _data_plot(data, curve)
    _check_size(result, order, fit)
    return result.fourier(
        granularity=granularity,
        fit=fit,
        order=order,
        log=log,
        window=window,
        remove_dc=remove_dc,
    )


def curve(which: int | str = 0) -> dict:
    """Return plain metadata for a curve index, label or paper symbol.

    >>> import hilbertplot as hp
    >>> hp.curves.info("Moore")["index"]
    1
    """
    c = _curves.curve(which)
    return {
        "index": c.index,
        "name": c.name,
        "symbol": c.symbol,
        "kind": c.kind,
        "homogeneous": c.is_homogeneous,
        "closed": c.is_closed,
        "generalizes": c.generalizes,
        "kernels": sorted(c.kernels),
        "combination": c.combination,
        "rule": c.rule,
    }


def catalog() -> list[dict]:
    """Return metadata dictionaries for all forty curves, in index order."""
    return [curve(i) for i in range(40)]


def proper() -> list[dict]:
    """Return metadata for the six proper curves."""
    return [curve(c.index) for c in _curves.proper()]


def improper() -> list[dict]:
    """Return metadata for the six improper curves."""
    return [curve(c.index) for c in _curves.improper()]


def homogeneous() -> list[dict]:
    """Return metadata for the twelve homogeneous curves."""
    return [curve(c.index) for c in _curves.homogeneous()]


def inhomogeneous() -> list[dict]:
    """Return metadata for the twenty-eight inhomogeneous curves."""
    return [curve(c.index) for c in _curves.inhomogeneous()]


def closed() -> list[dict]:
    """Return metadata for the four closed curves."""
    return [curve(c.index) for c in _curves.closed()]


def generalizing() -> list[dict]:
    """Return metadata for the eight curves that support arbitrary square sizes."""
    return [curve(c.index) for c in _curves.generalizing()]


def by_kernels(*indices: int) -> list[dict]:
    """Return metadata for curves whose kernel set is exactly ``indices``."""
    return [curve(c.index) for c in _curves.by_kernels(*indices)]


def points(curve: int | str = 0, order: int = 4) -> np.ndarray:
    """Return the (4**order, 2) array of (x, y) cells in visit order."""
    return _curves.curve(curve).points(order)


def grid(n: int | tuple[int, int], *, curve: int | str = 0) -> np.ndarray:
    """Return ordered (x, y) cells on a square or quasisquare.

    ``n`` is a square side or a ``(rows, columns)`` pair, as on plot_curve(shape=...).
    Arbitrary sizes require a generalizing curve. A shape with two power-of-two,
    equal sides works on every curve.
    """
    if isinstance(n, (tuple, list)):
        from ._core.arbitrary import shape_points

        return shape_points(_curves.curve(curve).index, n)
    return _curves.curve(curve).grid(n)


def word(curve: int | str = 0, order: int = 4) -> str:
    """Return the curve's u/d/l/r direction word at this order."""
    return _curves.curve(curve).word(order)


def index_to_xy(index: int, order: int, *, curve: int | str = 0) -> tuple[int, int]:
    """Return the cell (x, y) at a sequence index in O(order), without building the grid."""
    return _curves.curve(curve).encode(index, order)


def xy_to_index(x: int, y: int, order: int, *, curve: int | str = 0) -> int:
    """Return the step visiting cell (x, y) in O(order), inverse of index_to_xy."""
    return _curves.curve(curve).decode(x, y, order)


def from_grid(array, *, curve: int | str = 0, length: int | None = None) -> np.ndarray:
    """Read an image/array in curve order, preserving dtype, masks and pixel channels.

    Always returns one flat array. A colour pixel's channels stay consecutive,
    in their original order. Pass length= to retain an explicit number of values,
    including legitimate NaNs or masked values. Padding is never stripped automatically.

    Spatial dimensions must form a supported square or quasisquare. General
    rectangles and shapes unsupported by the selected curve raise an error.
    Reconstruct with to_grid(samples, shape=array.shape, curve=the_same_curve).
    A different read curve reorders samples and can move padding into the sequence.
    """
    from ._data.conversion import from_grid as convert

    return convert(array, curve=curve, length=length)


def _grid_points(curve, order, side):
    c = _curves.curve(curve)
    if side is None:
        order = 4 if order is None else order
        return c.points(order), 2**order
    if order is not None:
        raise ValueError("choose either order or side, not both")
    side = _curves._check_int(side, "side")
    if side < 1:
        raise ValueError("side must be >= 1")
    if side & (side - 1) == 0:
        return c.points(side.bit_length() - 1), side
    return c.grid(side), side


def label_map(
    curve: int | str = 0,
    order: int | None = None,
    *,
    side: int | None = None,
) -> np.ndarray:
    """Return visit indices [y, x]; default order 4, or specify a square side."""
    from ._data.mapping import label_map as build

    pts, side = _grid_points(curve, order, side)
    return build(pts, side)


def difference_map(
    curve: int | str = 0,
    order: int | None = None,
    *,
    side: int | None = None,
) -> np.ndarray:
    """Return mean 8-neighbour visit-index distances; default order 4, or a side.

    To match a plot's grid, pass ``side=hp.data.to_grid(data, curve=...).shape[0]``.
    This field is a property of geometry, independent of measurement values.
    """
    from ._data.mapping import difference_map as build

    pts, side = _grid_points(curve, order, side)
    return build(pts, side)


def gallery(
    curves=None,
    order: int = 3,
    *,
    ncols: int | None = None,
    mode: str = "auto",
    cmap="viridis",
    color=None,
    title: str | None = None,
) -> _Figure:
    """Draw a curve gallery and return a Figure, without showing or saving it.

    Accepts curve indices, labels, or metadata dictionaries returned by the group
    functions. With no argument, draws all forty curves.
    """
    from ._viz.render import gallery as draw

    selected = range(40) if curves is None else curves
    selected = [_curves.curve(c["index"] if isinstance(c, dict) else c) for c in selected]
    return draw(
        selected, order, ncols=ncols, show=False, mode=mode, cmap=cmap, color=color, title=title
    )
