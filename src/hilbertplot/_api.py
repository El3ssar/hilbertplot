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
    """Validate a real scalar sequence and bind a private floating-point copy.

    Parameters
    ----------
    data : array_like
        Numeric sample sequence supplied by the caller.
    curve : Curve or int or str
        Internal curve instance, or selector resolved by the caller.

    Returns
    -------
    HilbertPlot
        Validated private data binding used by the public wrappers.
    """
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
    """Reject data exceeding an explicit grid capacity unless truncation is requested.

    Parameters
    ----------
    plot : HilbertPlot
        Internal data binding whose sequence length is checked.
    order : int or None
        Recursion depth for a side of 2**order; None requests automatic sizing when supported.
    fit : str
        Sizing policy already selected by the caller: pad, truncate, square or auto.

    Returns
    -------
    None
        Raise ValueError if explicit capacity would silently drop samples.
    """
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
    """Plot a real one-dimensional sequence along a selected curve.

    Parameters
    ----------
    data : array_like, shape (N,)
        Nonempty real numeric sequence. NaNs and masked samples mark missing
        values; infinities and complex values are rejected. Values are copied
        to floating point for display, so large integers may lose precision.
    curve : int or str, default 0
        Curve index in 0..39, friendly label (for example, "Moore"), or paper
        symbol (for example, "12H"). The default is the standard Hilbert curve.
    fourier : bool, default False
        Render the centred 2-D Fourier magnitude of the mapped image.
        Incompatible with difference=True. Accepts integer 0 or 1.
    difference : bool, default False
        Render mean 8-neighbour visit-index distances for the complete grid.
        This is a property of curve geometry, independent of data values.
        Incompatible with fourier=True. Accepts integer 0 or 1.
    granularity : int, default 1
        Positive block length. Replace consecutive blocks with their means,
        repeated to preserve sequence length. A final short block uses its
        own mean. One leaves samples unchanged; averaging is lossy.
    cmap : str, matplotlib.colors.Colormap or sequence of colors, default 'viridis'
        Matplotlib colormap, or color stops interpolated into one continuous
        gradient (for example, ['#132b43', 'white', '#c44e52']).
    fit : {'pad', 'square', 'truncate', 'auto'}, default 'pad'
        'pad' uses the smallest enclosing power-of-two square. 'square' uses
        a side of ceil(sqrt(N)) and requires a generalizing curve. 'truncate'
        uses the largest power-of-two square fitting inside the sequence and
        discards the tail. 'auto' chooses 'square' when supported, else 'pad'.
    order : int or None, optional
        Fix the grid side to 2**order, with order >= 0. Without an explicit
        order, use fit to determine the size. Too much data raises unless
        fit='truncate'.
    colorbar : bool, default True
        Attach a color scale to the drawing.
    ax : matplotlib.axes.Axes or None, optional
        Draw on these axes; otherwise create a new figure and axes.
    **style : dict, optional
        Drawing keywords: title (str), vmin/vmax (float color limits), fill
        (padding value, default NaN), and Matplotlib imshow properties such
        as norm, alpha and interpolation. Fourier keywords are window (Hann,
        default False), log (log1p magnitude, default True), and remove_dc
        (subtract the image mean, default True).

    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure containing the drawing. Call fig.savefig(...) to export,
        matplotlib.pyplot.show() to display, or pyplot.close(fig) to release it.

    Raises
    ------
    TypeError
        Nonreal/non-numeric input, invalid boolean flags, or unknown keywords.
    ValueError
        Empty/non-1-D data, infinity, incompatible transformations, unsupported
        fitting, insufficient grid capacity, or a request over the cell limit.

    See Also
    --------
    hilbertplot.plot_curve : Draw the path itself.
    hilbertplot.data.to_grid : Convert values without display normalization.
    hilbertplot.data.fourier : Compute a spectrum without plotting.

    Notes
    -----
    Each call draws one image and does not open a window. NaNs are transparent
    in the data image. Fourier color limits default to the 50th and 99.8th
    percentiles; this affects display only. Use data.to_grid for lossless
    numeric conversion and data.fourier to obtain the transformed array.

    Examples
    --------
    >>> import hilbertplot as hp
    >>> fig = hp.plot([1, 2, 3, 4], curve="Moore")  # doctest: +SKIP
    >>> fig = hp.plot(range(100), fourier=True)  # doctest: +SKIP
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
    """Draw a curve path on a square or quasisquare.

    Parameters
    ----------
    curve : int or str, default 0
        Curve index in 0..39, friendly label (for example, "Moore"), or paper
        symbol (for example, "12H"). The default is the standard Hilbert curve.
    order : int or None, optional
        Nonnegative recursion depth; the side is 2**order. Defaults to 4 when
        neither order nor shape is supplied. Mutually exclusive with shape.
    shape : tuple of int or None, optional
        Explicit (rows, columns) of a supported square or quasisquare. Arbitrary
        sizes require one of curves 0, 3, 4, 5, 24, 29, 30, 31. The orientation
        is chosen to keep the quasisquare path connected.
    ax : matplotlib.axes.Axes or None, optional
        Draw on these axes, or create a new figure.
    mode : {'auto', 'line', 'fill'}, default 'auto'
        Draw connected segments, or color cells by visit order. Auto uses
        lines below effective order 8 and filled cells otherwise.
    color : color-like or None, optional
        Solid line color. With None, color the path using cmap.
    cmap : str or matplotlib.colors.Colormap, default 'viridis'
        Color path segments or filled cells by visit order.
    linewidth : float or None, optional
        Line width in points; None selects a width for the grid size.
    endpoints : bool, default True
        Mark the entry with a circle and exit with a square in line mode.
    title : str or None, optional
        Axes title; None uses the curve label and grid size.

    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure containing the drawing. Call fig.savefig(...) to export,
        matplotlib.pyplot.show() to display, or pyplot.close(fig) to release it.

    Raises
    ------
    ValueError
        Both order and shape are given, shape is unsupported, mode is invalid,
        or the requested allocation exceeds the cell limit.

    See Also
    --------
    hilbertplot.curves.points : Get power-of-two path coordinates.
    hilbertplot.curves.grid : Get arbitrary square/quasisquare coordinates.

    Examples
    --------
    >>> import hilbertplot as hp
    >>> fig = hp.plot_curve(0, order=3)  # doctest: +SKIP
    >>> fig = hp.plot_curve(3, shape=(15, 16), mode="line")  # doctest: +SKIP
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
    """Arrange numeric samples into a grid along a curve, preserving dtype.

    Parameters
    ----------
    data : array_like, shape (N, ...) or (N,)
        Nonempty numeric samples, including boolean, integer, float and complex
        arrays. Trailing sample axes are retained as pixel component axes.
        A flat color sequence can be reconstructed using its full original shape.
    curve : int or str, default 0
        Curve index in 0..39, friendly label (for example, "Moore"), or paper
        symbol (for example, "12H"). The default is the standard Hilbert curve.
    shape : tuple of int or None, optional
        Explicit (rows, columns), optionally followed by channel dimensions.
        Spatial dimensions must form a supported square or quasisquare (sides
        differing by one). Mutually exclusive with order.
    granularity : int, default 1
        Positive block length. Replace consecutive blocks with their means,
        repeated to preserve sequence length. A final short block uses its
        own mean. One leaves samples unchanged; averaging is lossy.
    fit : {'pad', 'square', 'truncate', 'auto'}, default 'pad'
        'pad' uses the smallest enclosing power-of-two square. 'square' uses
        a side of ceil(sqrt(N)) and requires a generalizing curve. 'truncate'
        uses the largest power-of-two square fitting inside the sequence and
        discards the tail. 'auto' chooses 'square' when supported, else 'pad'.
    order : int or None, optional
        Fix the grid side to 2**order, with order >= 0. Without an explicit
        order, use fit to determine the size. Too much data raises unless
        fit='truncate'.
    fill : numeric scalar, default numpy.nan
        Padding value. Default NaN padding preserves floating/complex dtype;
        integer/bool inputs use masked padding to preserve exact values. An
        explicit representable fill, such as 0, retains an ordinary integer
        array. An unrepresentable fill raises when padding is required.

    Returns
    -------
    grid : numpy.ndarray or numpy.ma.MaskedArray
        Shape (rows, columns, ...) with sample i at grid[y_i, x_i, ...].
        Input masks are preserved. With granularity=1 the input dtype is
        retained exactly, including large integers and complex values.

    Raises
    ------
    TypeError
        Non-numeric data, non-integer dimensions, or a nonscalar fill.
    ValueError
        Empty/scalar data, unsupported shape, incompatible channel axes, both
        shape and order, unrepresentable padding, or insufficient capacity.

    See Also
    --------
    hilbertplot.data.from_grid : Read values along a curve.
    hilbertplot.plot : Display real scalar samples.

    Notes
    -----
    Square/quasisquare paths agree with plot_curve(shape=...). General
    rectangles are unsupported. Conversion performs no color normalization.
    Padding is retained by from_grid; pass the known original length to remove
    only the tail. Averaging and explicit truncation prevent an exact round trip.

    Examples
    --------
    >>> import numpy as np
    >>> import hilbertplot as hp
    >>> values = np.arange(10, dtype=np.uint64)
    >>> grid = hp.data.to_grid(values, curve=12)
    >>> hp.data.from_grid(grid, curve=12, length=10).tolist()
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
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
    """Compute the centred 2-D FFT magnitude of a mapped sequence.

    Parameters
    ----------
    data : array_like, shape (N,)
        Nonempty real numeric sequence. NaNs and masked samples denote missing
        values. Infinities and complex inputs are rejected.
    curve : int or str, default 0
        Curve index in 0..39, friendly label (for example, "Moore"), or paper
        symbol (for example, "12H"). The default is the standard Hilbert curve.
    granularity : int, default 1
        Positive block length. Replace consecutive blocks with their means,
        repeated to preserve sequence length. A final short block uses its
        own mean. One leaves samples unchanged; averaging is lossy.
    fit : {'pad', 'square', 'truncate', 'auto'}, default 'pad'
        'pad' uses the smallest enclosing power-of-two square. 'square' uses
        a side of ceil(sqrt(N)) and requires a generalizing curve. 'truncate'
        uses the largest power-of-two square fitting inside the sequence and
        discards the tail. 'auto' chooses 'square' when supported, else 'pad'.
    order : int or None, optional
        Fix the grid side to 2**order, with order >= 0. Without an explicit
        order, use fit to determine the size. Too much data raises unless
        fit='truncate'.
    log : bool, default True
        Return log1p(abs(F)) instead of abs(F).
    window : bool, default False
        Multiply the mapped image by separable Hann weights before the FFT.
        This tapers edges; it is not a moving window on the sequence.
    remove_dc : bool, default True
        Subtract the image mean before optional windowing and transformation.

    Returns
    -------
    spectrum : numpy.ndarray, shape (side, side)
        Real nonnegative FFT magnitude, with zero frequency at the centre.
        This is not squared power, a normalized density, or a 1-D FFT.

    Raises
    ------
    ValueError
        No finite samples, invalid fitting, incompatible size, or infinity.

    See Also
    --------
    hilbertplot.plot : Pass fourier=True to render the spectrum.

    Notes
    -----
    First map the data and replace missing cells by the finite image mean.
    Optionally subtract the mean, then multiply by
    outer(numpy.hanning(rows), numpy.hanning(columns)) when window=True.
    Compute abs(fftshift(fft2(image))) and optionally apply log1p.
    The Hann window changes sample weights and amplitudes; there is no gain
    correction. At sides 1 or 2 its special/degenerate weights matter.

    Examples
    --------
    >>> import hilbertplot as hp
    >>> hp.data.fourier(range(100), curve=12).shape
    (16, 16)
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
    """Return plain metadata for a curve selected by index or label.

    Parameters
    ----------
    which : int or str, default 0
        Index 0..39, friendly label such as 'Moore', or paper symbol such as
        '12H'. Name matching ignores case, whitespace and '#'.

    Returns
    -------
    info : dict
        Keys: index (int), name/symbol/kind (str), homogeneous/closed/generalizes
        (bool), kernels (sorted list of int), combination (str), and rule (str).
        kind is 'proper', 'improper' or 'inhomogeneous'; generalizes means
        arbitrary square sizes are supported. Kernels identify building blocks.

    Raises
    ------
    TypeError
        Invalid selector type, including bool.
    ValueError
        Unknown index, label or symbol.

    Examples
    --------
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
    """Return metadata for all forty curves, in index order.

    Returns
    -------
    curves : list of dict
        Metadata in index order, using the same keys as curves.info. Safe to
        pass directly to gallery; no library-defined objects are returned.

    See Also
    --------
    hilbertplot.curves.info : Metadata keys and curve selection.
    hilbertplot.gallery : Render a selection of curves.
    """
    return [curve(i) for i in range(40)]


def proper() -> list[dict]:
    """Return metadata for the six proper homogeneous curves.

    Returns
    -------
    curves : list of dict
        Metadata in index order, using the same keys as curves.info. Safe to
        pass directly to gallery; no library-defined objects are returned.

    See Also
    --------
    hilbertplot.curves.info : Metadata keys and curve selection.
    hilbertplot.gallery : Render a selection of curves.
    """
    return [curve(c.index) for c in _curves.proper()]


def improper() -> list[dict]:
    """Return metadata for the six improper homogeneous curves.

    Returns
    -------
    curves : list of dict
        Metadata in index order, using the same keys as curves.info. Safe to
        pass directly to gallery; no library-defined objects are returned.

    See Also
    --------
    hilbertplot.curves.info : Metadata keys and curve selection.
    hilbertplot.gallery : Render a selection of curves.
    """
    return [curve(c.index) for c in _curves.improper()]


def homogeneous() -> list[dict]:
    """Return metadata for the twelve homogeneous curves.

    Returns
    -------
    curves : list of dict
        Metadata in index order, using the same keys as curves.info. Safe to
        pass directly to gallery; no library-defined objects are returned.

    See Also
    --------
    hilbertplot.curves.info : Metadata keys and curve selection.
    hilbertplot.gallery : Render a selection of curves.
    """
    return [curve(c.index) for c in _curves.homogeneous()]


def inhomogeneous() -> list[dict]:
    """Return metadata for the twenty-eight inhomogeneous curves.

    Returns
    -------
    curves : list of dict
        Metadata in index order, using the same keys as curves.info. Safe to
        pass directly to gallery; no library-defined objects are returned.

    See Also
    --------
    hilbertplot.curves.info : Metadata keys and curve selection.
    hilbertplot.gallery : Render a selection of curves.
    """
    return [curve(c.index) for c in _curves.inhomogeneous()]


def closed() -> list[dict]:
    """Return metadata for the four curves with adjacent entry and exit cells.

    Returns
    -------
    curves : list of dict
        Metadata in index order, using the same keys as curves.info. Safe to
        pass directly to gallery; no library-defined objects are returned.

    See Also
    --------
    hilbertplot.curves.info : Metadata keys and curve selection.
    hilbertplot.gallery : Render a selection of curves.
    """
    return [curve(c.index) for c in _curves.closed()]


def generalizing() -> list[dict]:
    """Return metadata for the eight curves supporting arbitrary squares and quasisquares.

    Returns
    -------
    curves : list of dict
        Metadata in index order, using the same keys as curves.info. Safe to
        pass directly to gallery; no library-defined objects are returned.

    See Also
    --------
    hilbertplot.curves.info : Metadata keys and curve selection.
    hilbertplot.gallery : Render a selection of curves.
    """
    return [curve(c.index) for c in _curves.generalizing()]


def by_kernels(*indices: int) -> list[dict]:
    """Select curves with exactly the requested set of quadrant kernels.

    Parameters
    ----------
    *indices : int
        Kernel curve indices. Set matching is exact, not a subset query;
        order and repetitions do not change the selection.

    Returns
    -------
    curves : list of dict
        Matching metadata in index order; empty if there is no match.

    See Also
    --------
    hilbertplot.curves.info : Inspect kernels and construction rules.

    Examples
    --------
    >>> import hilbertplot as hp
    >>> len(hp.curves.by_kernels(0))
    6
    """
    return [curve(c.index) for c in _curves.by_kernels(*indices)]


def points(curve: int | str = 0, order: int = 4) -> np.ndarray:
    """Return the ordered cells of a power-of-two curve.

    Parameters
    ----------
    curve : int or str, default 0
        Curve index in 0..39, friendly label (for example, "Moore"), or paper
        symbol (for example, "12H"). The default is the standard Hilbert curve.
    order : int, default 4
        Nonnegative recursion depth. Side length is 2**order and the path
        contains 4**order cells. Order zero contains just (0, 0).

    Returns
    -------
    points : numpy.ndarray, shape (4**order, 2)
        Integer (x, y) coordinates in visit order, normalized to the lower-left
        origin. Array indexing uses [y, x].

    Raises
    ------
    ValueError
        Negative order, invalid curve, or allocation over the cell limit.
    TypeError
        Order is not an integer or is bool.

    See Also
    --------
    hilbertplot.curves.index_to_xy : Access a single cell without materializing a path.
    hilbertplot.curves.grid : Coordinates for other supported square/quasisquare sizes.

    Examples
    --------
    >>> import hilbertplot as hp
    >>> hp.curves.points(0, order=1).tolist()
    [[0, 0], [0, 1], [1, 1], [1, 0]]
    """
    return _curves.curve(curve).points(order)


def grid(n: int | tuple[int, int], *, curve: int | str = 0) -> np.ndarray:
    """Return the ordered cells of a square or quasisquare.

    Parameters
    ----------
    n : int or tuple of int
        Square side, or (rows, columns). Dimensions must be positive; a
        quasisquare has sides differing by one. General rectangles are rejected.
    curve : int or str, default 0
        Curve index in 0..39, friendly label (for example, "Moore"), or paper
        symbol (for example, "12H"). The default is the standard Hilbert curve.

    Returns
    -------
    points : numpy.ndarray, shape (rows * columns, 2)
        Integer (x, y) coordinates in visit order. Quasisquare orientation is
        chosen automatically to retain a connected path.

    Raises
    ------
    ValueError
        Unsupported shape/curve combination, nonpositive dimensions, or an
        allocation over the cell limit.

    Notes
    -----
    Power-of-two squares work on all forty curves. Other sizes require a
    generalizing curve: 0, 3, 4, 5, 24, 29, 30 or 31. This function returns
    coordinates, not an image; use data.to_grid to arrange sample values.

    Examples
    --------
    >>> import hilbertplot as hp
    >>> hp.curves.grid((15, 16), curve=3).shape
    (240, 2)
    """
    if isinstance(n, (tuple, list)):
        from ._core.arbitrary import shape_points

        return shape_points(_curves.curve(curve).index, n)
    return _curves.curve(curve).grid(n)


def word(curve: int | str = 0, order: int = 4) -> str:
    """Return a power-of-two curve as unit direction letters.

    Parameters
    ----------
    curve : int or str, default 0
        Curve index in 0..39, friendly label (for example, "Moore"), or paper
        symbol (for example, "12H"). The default is the standard Hilbert curve.
    order : int, default 4
        Nonnegative recursion depth.

    Returns
    -------
    word : str
        String of length 4**order - 1 over 'u', 'd', 'l', 'r', for up, down,
        left and right. The order-zero word is empty.

    Examples
    --------
    >>> import hilbertplot as hp
    >>> hp.curves.word(0, order=1)
    'urd'
    """
    return _curves.curve(curve).word(order)


def index_to_xy(index: int, order: int, *, curve: int | str = 0) -> tuple[int, int]:
    """Locate one sequence index without building the full curve.

    Parameters
    ----------
    index : int
        Zero-based visit index in [0, 4**order).
    order : int
        Nonnegative recursion depth of a power-of-two square.
    curve : int or str, default 0
        Curve index in 0..39, friendly label (for example, "Moore"), or paper
        symbol (for example, "12H"). The default is the standard Hilbert curve.

    Returns
    -------
    xy : tuple of int
        Cell (x, y), each in [0, 2**order). Python integers retain exactness at
        very large orders.

    Raises
    ------
    TypeError
        A numeric index/order is not an integer, or is bool.
    ValueError
        Negative order or index outside the curve.

    See Also
    --------
    hilbertplot.curves.xy_to_index : Invert this mapping.

    Notes
    -----
    Time and auxiliary space grow with order, not the number of cells. This
    routine does not allocate a full grid and is independent of the materialized
    cell limit. Arbitrary square/quasisquare indexing is not supported here.

    Examples
    --------
    >>> import hilbertplot as hp
    >>> hp.curves.index_to_xy(2, 1)
    (1, 1)
    """
    return _curves.curve(curve).encode(index, order)


def xy_to_index(x: int, y: int, order: int, *, curve: int | str = 0) -> int:
    """Find the visit index of one cell without building the curve.

    Parameters
    ----------
    x, y : int
        Cell coordinates in [0, 2**order); x is column and y is row.
    order : int
        Nonnegative recursion depth of a power-of-two square.
    curve : int or str, default 0
        Curve index in 0..39, friendly label (for example, "Moore"), or paper
        symbol (for example, "12H"). The default is the standard Hilbert curve.

    Returns
    -------
    index : int
        Zero-based visit index in [0, 4**order). Uses exact Python integers.

    Raises
    ------
    TypeError
        Coordinates/order are not integers, or are bool.
    ValueError
        Negative order or coordinates outside the grid.

    See Also
    --------
    hilbertplot.curves.index_to_xy : Invert this mapping.

    Notes
    -----
    Uses O(order) traversal rather than materializing 4**order cells. Supports
    power-of-two squares only and is independent of the materialized cell limit.

    Examples
    --------
    >>> import hilbertplot as hp
    >>> hp.curves.xy_to_index(1, 1, 1)
    2
    """
    return _curves.curve(curve).decode(x, y, order)


def from_grid(array, *, curve: int | str = 0, length: int | None = None) -> np.ndarray:
    """Read a grid along a curve into one flat sequence.

    Parameters
    ----------
    array : array_like, shape (rows, columns, ...)
        At least two spatial dimensions, forming a supported square or
        quasisquare. Optional trailing axes contain pixel components.
    curve : int or str, default 0
        Curve index in 0..39, friendly label (for example, "Moore"), or paper
        symbol (for example, "12H"). The default is the standard Hilbert curve.
    length : int or None, optional
        Retain exactly this many flattened values, from 0 through array.size.
        Counts channels as individual values. None keeps every value,
        including NaNs, masks and padding; nothing is stripped automatically.

    Returns
    -------
    sequence : numpy.ndarray or numpy.ma.MaskedArray, shape (M,)
        Values in curve visit order, with each pixel's components consecutive.
        Dtype and masks are preserved. M is array.size unless length is given.

    Raises
    ------
    TypeError
        Non-integer length or dimensions.
    ValueError
        Fewer than two dimensions, empty component axes, unsupported spatial
        shape, or length outside the available range.

    See Also
    --------
    hilbertplot.data.to_grid : Inverse arrangement using the same curve and shape.

    Notes
    -----
    Reconstruct with to_grid(sequence, curve=the_same_curve, shape=array.shape).
    Reading with another curve reorders values and may move padding into the
    middle of the sequence. Keep every entry to invert such a permutation.

    Examples
    --------
    >>> import numpy as np
    >>> import hilbertplot as hp
    >>> image = np.arange(16).reshape(4, 4)
    >>> sequence = hp.data.from_grid(image, curve=12)
    >>> np.array_equal(hp.data.to_grid(sequence, curve=12, shape=image.shape), image)
    True
    """
    from ._data.conversion import from_grid as convert

    return convert(array, curve=curve, length=length)


def _grid_points(curve, order, side):
    """Resolve a square path and its side from mutually exclusive size selectors.

    Parameters
    ----------
    curve : Curve or int or str
        Internal curve instance, or selector resolved by the caller.
    order : int or None
        Recursion depth for a side of 2**order; None requests automatic sizing when supported.
    side : int or None
        Square side in cells, or None when an order determines it.

    Returns
    -------
    tuple
        Ordered (x, y) coordinates and square side.
    """
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
    """Return the visit index at every square-grid cell.

    Parameters
    ----------
    curve : int or str, default 0
        Curve index in 0..39, friendly label (for example, "Moore"), or paper
        symbol (for example, "12H"). The default is the standard Hilbert curve.
    order : int or None, optional
        Nonnegative recursion depth. Defaults to 4 if side is also omitted.
        Mutually exclusive with side.
    side : int or None, optional
        Explicit square side. Non-power-of-two sizes require a generalizing
        curve. Mutually exclusive with order.

    Returns
    -------
    labels : numpy.ndarray of int64, shape (side, side)
        labels[y, x] is the zero-based visit index of cell (x, y).

    Raises
    ------
    ValueError
        Both side and order, unsupported side/curve, or excessive allocation.

    Notes
    -----
    Coordinates are (x, y), while array access is [y, x].

    Examples
    --------
    >>> import hilbertplot as hp
    >>> hp.curves.label_map(order=1).tolist()
    [[0, 3], [1, 2]]
    """
    from ._data.mapping import label_map as build

    pts, side = _grid_points(curve, order, side)
    return build(pts, side)


def difference_map(
    curve: int | str = 0,
    order: int | None = None,
    *,
    side: int | None = None,
) -> np.ndarray:
    """Return mean neighbour visit-index distance at every cell.

    Parameters
    ----------
    curve : int or str, default 0
        Curve index in 0..39, friendly label (for example, "Moore"), or paper
        symbol (for example, "12H"). The default is the standard Hilbert curve.
    order : int or None, optional
        Nonnegative recursion depth. Defaults to 4 if side is also omitted.
        Mutually exclusive with side.
    side : int or None, optional
        Explicit square side. Non-power-of-two sizes require a generalizing
        curve. Mutually exclusive with order.

    Returns
    -------
    distances : numpy.ndarray of float64, shape (side, side)
        At each cell, average abs(label_here - label_neighbour) over all
        in-bounds horizontal, vertical and diagonal neighbours. Corners have
        three neighbours, edges five, interiors eight. A single cell gives 0.

    Raises
    ------
    ValueError
        Both side and order, unsupported side/curve, or excessive allocation.

    Notes
    -----
    This describes geometry, independently of measurement values. Large values
    mean spatial neighbours can be far apart along the sequence. To match a
    plot's grid, pass side=hp.data.to_grid(values, curve=...).shape[0].

    Examples
    --------
    >>> import hilbertplot as hp
    >>> hp.curves.difference_map(order=0).tolist()
    [[0.0]]
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
    """Draw a gallery of selected curves and return a Matplotlib figure.

    Parameters
    ----------
    curves : iterable of int, str or dict, optional
        Indices, labels, symbols or metadata dictionaries from curves.catalog
        or a group function. None selects all forty curves.
    order : int, default 3
        Nonnegative recursion depth for every curve.
    ncols : int or None, optional
        Number of columns. None chooses a layout for the number of curves.
    mode : {'auto', 'line', 'fill'}, default 'auto'
        Path segments or cells colored by visit order; see plot_curve.
    cmap : str or matplotlib.colors.Colormap, default 'viridis'
        Color path segments or cells by visit order.
    color : color-like or None, optional
        Solid line color; None uses cmap.
    title : str or None, optional
        Optional title for the whole figure.

    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure containing the drawing. Call fig.savefig(...) to export,
        matplotlib.pyplot.show() to display, or pyplot.close(fig) to release it.

    See Also
    --------
    hilbertplot.plot_curve : Draw one curve with more styling options.

    Examples
    --------
    >>> import hilbertplot as hp
    >>> fig = hp.gallery(hp.curves.generalizing(), order=3)  # doctest: +SKIP
    """
    from ._viz.render import gallery as draw

    selected = range(40) if curves is None else curves
    selected = [_curves.curve(c["index"] if isinstance(c, dict) else c) for c in selected]
    return draw(
        selected, order, ncols=ncols, show=False, mode=mode, cmap=cmap, color=color, title=title
    )
