"""The :class:`HilbertPlot` object -- data laid on a curve, rendered on demand.

A :class:`HilbertPlot` just holds a curve and a data vector; it draws nothing until
you ask.  Get one from :meth:`hilbertplot.curve.Curve.plot_data` or the
:func:`hilbert_plot` shortcut, then render with :meth:`HilbertPlot.show` /
:meth:`~HilbertPlot.save` / :meth:`~HilbertPlot.draw`, choosing the colormap,
granularity and power-of-four fit at that point (not at construction).

Colormaps
---------
``cmap`` accepts either a matplotlib colormap **name** (``"viridis"``, ``"gray"`` ...)
or a **list of colours** to interpolate smoothly between and spread across the data's
min-max range, e.g. ``["red", "green", "tab:blue"]`` sweeps red -> green -> blue.
"""

from __future__ import annotations

import numpy as np

from .._core.curve import Curve
from .._core.curve import curve as _lookup_curve
from .._data.mapping import granulate, resolve_order, scatter, square_side

__all__ = ["HilbertPlot", "hilbert_plot"]


def _resolve_cmap(cmap):
    """Turn ``cmap`` (a name or a list of colours) into a matplotlib Colormap.

    NaN-filled (unmapped) cells are made transparent so padding never shows.
    """
    from matplotlib import colormaps
    from matplotlib.colors import Colormap, LinearSegmentedColormap

    if isinstance(cmap, Colormap):
        resolved = cmap
    elif isinstance(cmap, str):
        resolved = colormaps[cmap]
    else:  # a sequence of colour specs to interpolate through
        colors = list(cmap)
        if not colors:
            raise ValueError("colormap colour list is empty")
        if len(colors) == 1:
            colors = colors * 2
        resolved = LinearSegmentedColormap.from_list("hilbertplot", colors)
    # Make NaN-filled (unmapped) cells transparent so padding never shows.
    return resolved.with_extremes(bad=(0.0, 0.0, 0.0, 0.0))


def _overlay_difference(ax, dmap, side, threshold, color):
    """Paint the strong-locality barrier of a difference map onto ``ax``.

    The barrier is the set of cells whose value exceeds ``mean + threshold * std``;
    all other cells stay transparent.
    """
    from matplotlib.colors import to_rgba

    barrier = dmap > dmap.mean() + threshold * dmap.std()
    overlay = np.zeros((side, side, 4))
    overlay[barrier] = to_rgba(color)
    ax.imshow(
        overlay,
        origin="lower",
        interpolation="nearest",
        extent=(-0.5, side - 0.5, -0.5, side - 0.5),
        zorder=2,
    )


class HilbertPlot:
    """A 1-D data vector bound to a curve, ready to be rendered as a Hilbert plot.

    Holds only the curve and the data and draws nothing on construction; the colormap,
    granularity and power-of-four fit are all chosen at render time, so one object gives
    you every variant.  Construct via :meth:`hilbertplot.curve.Curve.plot_data` or
    :func:`hilbert_plot`.

    Parameters
    ----------
    curve : Curve
        The curve whose path lays out the data.
    data : array_like
        The 1-D sequence to visualise.

    Examples
    --------
    >>> import numpy as np, hilbertplot
    >>> plot = hilbertplot.hilbert_plot(0, np.arange(1, 101))
    >>> plot.show(["red", "green", "tab:blue"])   # doctest: +SKIP
    >>> plot.image().shape          # 100 values -> tight 10x10 square (Hilbert generalizes)
    (10, 10)
    """

    __slots__ = ("_curve", "_data")

    def __init__(self, curve: Curve, data) -> None:
        if not isinstance(curve, Curve):
            raise TypeError(f"curve must be a Curve, got {type(curve).__name__}")
        self._curve = curve
        # own a private, read-only copy so the plot never aliases the caller's array
        self._data = np.array(data, dtype=float).ravel()
        self._data.flags.writeable = False

    @property
    def curve(self) -> Curve:
        """The curve the data is mapped through."""
        return self._curve

    @property
    def data(self) -> np.ndarray:
        """The 1-D data vector, as a read-only array (a private copy of the input)."""
        return self._data

    def __len__(self) -> int:
        return self._data.size

    # -- the mapping ---------------------------------------------------------
    def image(
        self,
        *,
        granularity: int = 1,
        order: int | None = None,
        fit: str = "auto",
        fill: float = np.nan,
    ) -> np.ndarray:
        """Return the 2-D image of the data mapped through the curve.

        Parameters
        ----------
        granularity : int, default 1
            Coarsen the data with the ``l``-granularity transform first (``1`` = none).
        order : int, optional
            Force a ``2**order`` grid (implies a power-of-two fit).
        fit : {"auto", "square", "pad", "truncate"}, default "auto"
            How to size the grid.  ``"auto"`` uses ``"square"`` when the curve
            :attr:`~hilbertplot.Curve.generalizes` (a tight ``ceil(sqrt(N))`` square, no
            power-of-two waste) and ``"pad"`` otherwise.  ``"square"`` forces the tight
            square (only for generalizing curves).  ``"pad"`` uses the smallest enclosing
            ``2**k`` grid; ``"truncate"`` the largest ``2**k`` grid that fits inside the
            data.
        fill : float, default numpy.nan
            Value for unmapped cells (``NaN`` renders transparent).

        Returns
        -------
        numpy.ndarray
            A ``side`` by ``side`` float image, indexed ``[y, x]``.

        Examples
        --------
        >>> import numpy as np, hilbertplot
        >>> hilbertplot.hilbert_plot(0, np.arange(10000)).image().shape   # tight square
        (100, 100)
        >>> hilbertplot.hilbert_plot(0, np.arange(64)).image(order=3).shape
        (8, 8)
        """
        values, points, side = self._layout(granularity, order, fit)
        return scatter(points, values, side, fill)

    def fourier(
        self,
        *,
        granularity: int = 1,
        order: int | None = None,
        fit: str = "auto",
        log: bool = True,
        window: bool = False,
    ) -> np.ndarray:
        """Return the 2-D Fourier map of this plot -- the centred power spectrum of the image.

        Periodic and self-similar structure in the data appears as bright peaks and
        symmetric patterns (the "Fourier map" of Estevez-Rams et al., 2015).

        Parameters
        ----------
        granularity, order, fit
            Passed to :meth:`image` to build the data image that is transformed.
        log : bool, default True
            Return ``log(1 + |F|)`` so faint structure is visible.
        window : bool, default False
            Apply a Hann window first to suppress edge artifacts.

        Returns
        -------
        numpy.ndarray
            The centred 2-D spectrum, same shape as :meth:`image`.

        Examples
        --------
        >>> import numpy as np, hilbertplot
        >>> spec = hilbertplot.hilbert_plot(0, np.tile([1, 0], 512)).fourier()   # ·10· pattern
        >>> spec.shape
        (32, 32)
        """
        from .._data.mapping import fourier_spectrum

        img = self.image(granularity=granularity, order=order, fit=fit, fill=np.nan)
        return fourier_spectrum(img, log=log, window=window)

    def _layout(self, granularity, order, fit):
        """Resolve (values, curve points, grid side) for a given granularity/order/fit."""
        values = self._data
        if granularity != 1:
            values = granulate(values, granularity)
        n = values.size
        effective = fit
        if order is None and fit == "auto":
            effective = "square" if self._curve.generalizes else "pad"
        if order is None and effective == "square":
            if not self._curve.generalizes:
                raise ValueError(
                    f"fit='square' needs a generalizing curve; {self._curve.name} is not "
                    f"one (see hilbertplot.generalizing()). Use fit='pad' or 'truncate'."
                )
            side = square_side(n)
            return values, self._curve.grid(side), side
        pot_fit = "pad" if effective in ("auto", "square") else effective
        order = resolve_order(n, order, pot_fit)
        return values, self._curve.points(order), 2**order

    # -- rendering -----------------------------------------------------------
    def draw(
        self,
        cmap="viridis",
        *,
        granularity: int = 1,
        order: int | None = None,
        fit: str = "auto",
        fill: float = np.nan,
        ax=None,
        vmin=None,
        vmax=None,
        title: str | None = None,
        difference: bool = False,
        difference_threshold: float = 1.0,
        difference_color="#2b6cff",
        fourier: bool = False,
        window: bool = False,
        **imshow_kw,
    ):
        """Render onto ``ax`` (created if ``None``) and return the axes -- no window.

        Parameters
        ----------
        cmap : str or list of color, default "viridis"
            A matplotlib colormap **name**, or a **list of colours** to interpolate
            smoothly between (e.g. ``["red", "green", "tab:blue"]`` sweeps red to blue).
        granularity, order, fit, fill
            Passed to :meth:`image`.
        ax : matplotlib.axes.Axes, optional
            Axes to draw on; a new figure is created when ``None``.
        vmin, vmax : float, optional
            Colour limits; default to the data's min/max so the colours span the full
            value range.
        title : str, optional
            Axes title; a default naming the curve and grid size is used when ``None``.
        difference : bool, default False
            Overlay the curve's strong-locality barrier -- the cells of the difference
            map above ``mean + difference_threshold * std`` -- marking where the curve
            breaks locality (see :meth:`hilbertplot.curve.Curve.difference_map`).
        difference_threshold : float, default 1.0
            Std multiplier for the barrier: **higher marks fewer, worse sites**; lower
            marks more.
        difference_color : color, default "#2b6cff"
            Colour of the barrier overlay.
        fourier : bool, default False
            Render the **2-D Fourier map** (centred power spectrum) instead of the data
            image, revealing periodic/self-similar structure as bright peaks.  The
            ``difference`` overlay is ignored in this mode.
        window : bool, default False
            (Fourier mode) apply a Hann window first to suppress edge artifacts.
        **imshow_kw
            Extra keyword arguments forwarded to ``matplotlib``'s ``imshow``.

        Returns
        -------
        matplotlib.axes.Axes

        Examples
        --------
        >>> import numpy as np, hilbertplot
        >>> plot = hilbertplot.hilbert_plot(0, np.arange(4096))
        >>> ax = plot.draw("gray", difference=True)                  # doctest: +SKIP
        >>> ax = plot.draw("magma", fourier=True)                    # doctest: +SKIP
        """
        from .._data.mapping import difference_map, fourier_spectrum
        from .render import pyplot

        plt = pyplot()
        values, points, side = self._layout(granularity, order, fit)
        image = scatter(points, values, side, fill)
        if fourier:
            image = fourier_spectrum(image, log=True, window=window)
            difference = False  # not meaningful on a spectrum
        if ax is None:
            _, ax = plt.subplots(figsize=(5, 5))
        if fourier and (vmin is None or vmax is None):
            # percentile contrast so faint spectral structure is visible by default
            lo, hi = np.percentile(image, [50.0, 99.8])
            vmin = lo if vmin is None else vmin
            vmax = (hi if hi > lo else image.max()) if vmax is None else vmax
        if vmin is None:
            vmin = np.nanmin(image)
        if vmax is None:
            vmax = np.nanmax(image)
        ax.imshow(
            image,
            origin="lower",
            interpolation="nearest",
            cmap=_resolve_cmap(cmap),
            vmin=vmin,
            vmax=vmax,
            extent=(-0.5, side - 0.5, -0.5, side - 0.5),
            **imshow_kw,
        )
        if difference:
            _overlay_difference(
                ax, difference_map(points, side), side, difference_threshold, difference_color
            )
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        if title is None:
            gran = "" if granularity == 1 else f", {granularity}-granularity"
            kind = "Fourier map" if fourier else "Hilbert plot"
            title = f"{self._curve.name}  {kind} ({side}x{side}{gran})"
        ax.set_title(title, fontsize=9)
        return ax

    def show(self, cmap="viridis", **kwargs):
        """Draw the plot and open a window.

        Parameters
        ----------
        cmap : str or list of color, default "viridis"
            See :meth:`draw`.
        **kwargs
            Every :meth:`draw` option (``granularity``, ``fit``, ``vmin``, ...).

        Returns
        -------
        matplotlib.axes.Axes
        """
        from .render import pyplot

        ax = self.draw(cmap, **kwargs)
        pyplot().show()
        return ax

    def save(self, path: str, cmap="viridis", *, dpi: int = 140, **kwargs) -> str:
        """Draw the plot, save it to ``path`` and return ``path``.

        Parameters
        ----------
        path : str
            Output file path (format inferred from the extension).
        cmap : str or list of color, default "viridis"
            See :meth:`draw`.
        dpi : int, default 140
            Output resolution.
        **kwargs
            Every :meth:`draw` option.

        Returns
        -------
        str
            ``path``.

        Examples
        --------
        >>> import numpy as np, hilbertplot
        >>> hilbertplot.hilbert_plot(0, np.arange(1, 101)).save(
        ...     "out.png", ["red", "green", "tab:blue"])          # doctest: +SKIP
        'out.png'
        """
        from .render import pyplot

        ax = self.draw(cmap, **kwargs)
        ax.figure.savefig(path, dpi=dpi, bbox_inches="tight")
        pyplot().close(ax.figure)
        return path

    def __repr__(self) -> str:
        return f"<HilbertPlot: {len(self)} values on {self._curve.name}>"


def hilbert_plot(curve: Curve | int | str, data) -> HilbertPlot:
    """Make a :class:`HilbertPlot` straight from a curve and data.

    A shortcut for ``hilbertplot.curve(which).plot_data(data)`` that skips the intermediate
    curve object.

    Parameters
    ----------
    curve : Curve or int or str
        A :class:`Curve`, or anything :func:`hilbertplot.curve` accepts (index, name or symbol).
    data : array_like
        The 1-D sequence to visualise.

    Returns
    -------
    HilbertPlot

    Examples
    --------
    >>> import hilbertplot
    >>> plot = hilbertplot.hilbert_plot(0, range(1024))    # curve 0 (Hilbert)
    >>> plot.show(["red", "green", "tab:blue"])      # doctest: +SKIP
    """
    c = curve if isinstance(curve, Curve) else _lookup_curve(curve)
    return HilbertPlot(c, data)
