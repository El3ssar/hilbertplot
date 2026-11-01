"""The :class:`HilbertPlot` object -- data laid on a curve, rendered on demand.

A :class:`HilbertPlot` just holds a curve and a data vector; it draws nothing until
you ask.  Get one from :meth:`hilbertplot._core.curve.Curve.plot_data` or the
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

from typing import TYPE_CHECKING, Any

import numpy as np

from .._core.curve import Curve
from .._core.curve import curve as _lookup_curve
from .._data.mapping import (
    check_fit,
    check_granularity,
    granulate,
    resolve_order,
    scatter,
    square_side,
)

if TYPE_CHECKING:
    from matplotlib.axes import Axes
else:
    # Runtime stand-in so `get_type_hints()` resolves without importing matplotlib --
    # see the note in `_core/curve.py`.
    Axes = Any

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


#: ``draw``'s own parameters.  Anything else in ``**imshow_kw`` is meant for matplotlib --
#: but a *near miss* of one of these is a typo, and passing it on produces an opaque
#: ``AxesImage.set() got an unexpected keyword argument`` from deep inside matplotlib.
_DRAW_PARAMETERS = frozenset(
    {
        "cmap", "granularity", "order", "fit", "fill", "ax", "vmin", "vmax", "title",
        "difference", "fourier", "window",
        "log", "remove_dc", "colorbar",
    }
)  # fmt: skip


def _imshow_properties() -> frozenset[str]:
    """Every keyword matplotlib's ``imshow`` legitimately accepts, from matplotlib itself.

    Hard-coding a list would go stale and would misjudge real arguments -- ``zorder``, for
    instance, is a perfectly good imshow keyword that happens to look like ``order``.
    """
    from matplotlib.artist import ArtistInspector
    from matplotlib.image import AxesImage

    return frozenset(ArtistInspector(AxesImage).get_setters()) | {
        "norm", "aspect", "interpolation", "alpha", "vmin", "vmax", "origin", "extent",
        "interpolation_stage", "filternorm", "filterrad", "resample", "url", "data",
    }  # fmt: skip


def _reject_unknown_kwargs(imshow_kw: dict) -> None:
    """Raise for a keyword that is a near-miss of one of ``draw``'s own parameters.

    Anything matplotlib actually understands is passed straight through; only a name that
    matplotlib does *not* accept and that closely resembles a ``draw`` parameter is treated
    as a typo, so the user gets ``did you mean 'granularity'?`` instead of an opaque
    ``AxesImage.set() got an unexpected keyword argument`` from inside matplotlib.
    """
    from difflib import get_close_matches

    unknown = [name for name in imshow_kw if name not in _DRAW_PARAMETERS]
    if not unknown:
        return
    accepted = _imshow_properties()
    for name in unknown:
        if name in accepted:
            continue
        close = get_close_matches(name, sorted(_DRAW_PARAMETERS), n=1, cutoff=0.8)
        if close:
            raise TypeError(
                f"draw() got an unexpected keyword argument {name!r}; did you mean "
                f"{close[0]!r}? (Unrecognised keywords are forwarded to matplotlib's imshow.)"
            )


def _check_transforms(fourier, difference):
    """Select at most one transformation; boolean flags also accept integer 0/1."""
    for name, value in (("fourier", fourier), ("difference", difference)):
        if not isinstance(value, (bool, np.bool_, int, np.integer)) or value not in (0, 1):
            raise TypeError(f"{name} must be a boolean (False/True or 0/1)")
    if fourier and difference:
        raise ValueError("fourier and difference are mutually exclusive; choose only one")


class HilbertPlot:
    """A 1-D data vector bound to a curve, ready to be rendered as a Hilbert plot.

    Holds only the curve and the data and draws nothing on construction; the colormap,
    granularity and power-of-four fit are all chosen at render time, so one object gives
    you every variant.  Construct via :meth:`hilbertplot._core.curve.Curve.plot_data` or
    :func:`hilbert_plot`.

    Parameters
    ----------
    curve : Curve
        The curve whose path lays out the data.
    data : array_like
        The 1-D sequence to visualise.

    Examples
    --------
    >>> import numpy as np; from hilbertplot._viz.hilbert_plot import hilbert_plot
    >>> plot = hilbert_plot(0, np.arange(1, 101))
    >>> plot.show(["red", "green", "tab:blue"])   # doctest: +SKIP
    >>> plot.image().shape          # 100 values -> tight 10x10 square (Hilbert generalizes)
    (10, 10)
    """

    __slots__ = ("_curve", "_data")

    def __init__(self, curve: Curve, data) -> None:
        if not isinstance(curve, Curve):
            raise TypeError(f"curve must be a Curve, got {type(curve).__name__}")
        self._curve = curve
        # own a private, immutable copy so the plot never aliases the caller's array
        if np.ma.isMaskedArray(data):
            # Masked entries are missing, not zero; NaN is what the renderer draws as blank.
            data = np.ma.filled(data, np.nan)
        try:
            owner = np.ascontiguousarray(np.array(data, dtype=float))
        except (TypeError, ValueError) as exc:
            raise TypeError(
                f"data must be numeric and convertible to a float array; got "
                f"{type(data).__name__} ({exc})"
            ) from exc
        if owner.size == 0:
            raise ValueError("data is empty; need at least one value to plot")
        # View the buffer through a read-only memoryview.  Simply clearing the writeable
        # flag is not enough: an array that *owns* its data may always turn its own flag
        # back on, so `plot.data.base.flags.writeable = True` -- a routine numpy idiom --
        # would re-arm the private copy and let the plot be corrupted.  Going through a
        # read-only memoryview makes `plot.data` and its base un-re-armable at no extra
        # allocation.  (Copying to `bytes` would also hide `owner`, but at 3x peak memory
        # instead of 2x, which for a multi-gigabyte vector is the worse failure.)
        self._data = np.frombuffer(memoryview(owner.reshape(-1)).toreadonly(), dtype=np.float64)

    @property
    def curve(self) -> Curve:
        """The curve the data is mapped through."""
        return self._curve

    @property
    def data(self) -> np.ndarray:
        """numpy.ndarray: The 1-D data, as a read-only view of a private copy.

        A fresh view is handed out each time, over a read-only buffer, so neither the array
        you get back nor its ``.base`` can be written to or made writable again -- a plot
        cannot be corrupted by accident.  A masked array's masked entries arrive as ``NaN``.
        """
        return self._data.view()

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
            :attr:`~hilbertplot._core.curve.Curve.generalizes` (a tight ``ceil(sqrt(N))`` square, no
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
        >>> import numpy as np; from hilbertplot._viz.hilbert_plot import hilbert_plot
        >>> hilbert_plot(0, np.arange(10000)).image().shape   # tight square
        (100, 100)
        >>> hilbert_plot(0, np.arange(64)).image(order=3).shape
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
        remove_dc: bool = True,
    ) -> np.ndarray:
        """Return the 2-D Fourier map -- the centred FFT magnitude of the image.

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
        remove_dc : bool, default True
            Subtract the mean before transforming, so the huge DC spike at the centre does
            not wash out the pattern.  Pass ``False`` to keep it.

        Returns
        -------
        numpy.ndarray
            The centred 2-D spectrum, same shape as :meth:`image`.

        Examples
        --------
        >>> import numpy as np; from hilbertplot._viz.hilbert_plot import hilbert_plot
        >>> spec = hilbert_plot(0, np.tile([1, 0], 512)).fourier()   # ·10· pattern
        >>> spec.shape
        (32, 32)
        """
        from .._data.mapping import fourier_spectrum

        img = self.image(granularity=granularity, order=order, fit=fit, fill=np.nan)
        return fourier_spectrum(img, log=log, window=window, remove_dc=remove_dc)

    def difference_map(
        self, *, granularity: int = 1, order: int | None = None, fit: str = "auto"
    ) -> np.ndarray:
        """Return the locality-loss field for **this plot's own grid**.

        The curve-level difference map takes an order, so it describes a ``2**k`` grid.
        This one uses whatever grid the plot actually renders on -- including
        the tight ``ceil(sqrt(N))`` square that ``fit="auto"`` picks for a generalizing
        curve -- so it matches the field ``draw(difference=True)`` renders.

        Parameters
        ----------
        granularity, order, fit
            Resolved exactly as in :meth:`image`, so the grid matches cell for cell.

        Returns
        -------
        numpy.ndarray
            A ``side`` by ``side`` float array of mean 8-neighbour label distances, ``[y, x]``.

        Examples
        --------
        >>> import numpy as np; from hilbertplot._viz.hilbert_plot import hilbert_plot
        >>> hilbert_plot(0, np.arange(100)).difference_map().shape
        (10, 10)
        """
        from .._data.mapping import difference_map

        _, points, side = self._layout(granularity, order, fit)
        return difference_map(points, side)

    def label_map(
        self, *, granularity: int = 1, order: int | None = None, fit: str = "auto"
    ) -> np.ndarray:
        """Return the visit-order index of every cell of this plot's grid.

        ``label_map()[y, x]`` is the step at which the curve reaches cell ``(x, y)``.  Like
        :meth:`difference_map`, it follows the plot's actual grid rather than a power of two.

        Returns
        -------
        numpy.ndarray
            A ``side`` by ``side`` integer array, indexed ``[y, x]``.

        Examples
        --------
        >>> import numpy as np; from hilbertplot._viz.hilbert_plot import hilbert_plot
        >>> hilbert_plot(0, np.arange(100)).label_map().shape
        (10, 10)
        """
        from .._data.mapping import label_map

        _, points, side = self._layout(granularity, order, fit)
        return label_map(points, side)

    def _layout(self, granularity, order, fit):
        """Resolve (values, curve points, grid side) for a given granularity/order/fit.

        ``fit`` is validated up front, even when an explicit ``order`` makes it moot --
        otherwise a typo like ``fit="squre"`` would pass silently.
        """
        check_fit(fit)
        # Validate unconditionally -- `granularity=True` must not slip past as "no
        # coarsening" -- but only pay for the transform when it does something.  At 1 it is
        # the identity, and every render path comes through here, so copying the whole
        # vector each time would cost a full allocation per call for nothing.
        granularity = check_granularity(granularity)
        values = self._data if granularity == 1 else granulate(self._data, granularity)
        n = values.size
        effective = fit
        if order is None and fit == "auto":
            effective = "square" if self._curve.generalizes else "pad"
        if order is None and effective == "square":
            if not self._curve.generalizes:
                raise ValueError(
                    f"fit='square' needs a generalizing curve; {self._curve.name} is not "
                    f"one (see hilbertplot.curves.generalizing()). Use fit='pad' or 'truncate'."
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
        fourier: bool = False,
        window: bool = False,
        log: bool = True,
        remove_dc: bool = True,
        colorbar: bool = False,
        **imshow_kw,
    ) -> Axes:
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
            Render the full locality-loss field instead of the data. This describes
            geometry, independently of measurement values. Cannot be combined with fourier.
        fourier : bool, default False
            Render the **2-D Fourier map** (centred FFT magnitude) instead of the data
            image. Cannot be combined with difference.
        window : bool, default False
            (Fourier mode) apply a Hann window first to suppress edge artifacts.
        log, remove_dc : bool
            (Fourier mode) as on :meth:`fourier` -- compress the dynamic range, and drop the
            central DC spike.  Both default to ``True``.
        colorbar : bool, default False
            Attach a colourbar to the axes. The single image is ``ax.images[0]``.
        **imshow_kw
            Extra keyword arguments forwarded to ``matplotlib``'s ``imshow`` -- e.g.
            ``norm=matplotlib.colors.LogNorm()`` for heavy-tailed data.

        Returns
        -------
        matplotlib.axes.Axes

        Examples
        --------
        >>> import numpy as np; from hilbertplot._viz.hilbert_plot import hilbert_plot
        >>> plot = hilbert_plot(0, np.arange(4096))
        >>> ax = plot.draw("gray", difference=True)                  # doctest: +SKIP
        >>> ax = plot.draw("magma", fourier=True)                    # doctest: +SKIP
        >>> ax = plot.draw(colorbar=True)                            # doctest: +SKIP
        """
        from .._data.mapping import difference_map, fourier_spectrum
        from .render import bare_axes, pyplot

        plt = pyplot()
        # Every argument-only check happens before a figure exists, so a rejected call
        # cannot leak one -- matplotlib keeps open figures alive globally, and a loop that
        # sweeps normalisations catching ValueError would otherwise grow without bound.
        _check_transforms(fourier, difference)
        _reject_unknown_kwargs(imshow_kw)
        # A caller-supplied `norm` carries its own limits, and matplotlib refuses to accept
        # both; so once a norm is given we must not fill in our default vmin/vmax.
        caller_norm = imshow_kw.get("norm") is not None
        if caller_norm and (vmin is not None or vmax is not None):
            raise ValueError(
                "pass either norm= or vmin=/vmax=, not both -- set the limits on the norm "
                "itself, e.g. LogNorm(vmin=1, vmax=1000)"
            )
        values, points, side = self._layout(granularity, order, fit)
        if difference:
            image = difference_map(points, side)
        else:
            image = scatter(points, values, side, fill)
            if fourier:
                image = fourier_spectrum(image, log=log, window=window, remove_dc=remove_dc)
        if not np.isfinite(image).any():
            raise ValueError("plot needs at least one finite value")
        resolved_cmap = _resolve_cmap(cmap)
        if ax is None:
            _, ax = plt.subplots(figsize=(5, 5))
        if fourier and not caller_norm and (vmin is None or vmax is None):
            # percentile contrast so faint spectral structure is visible by default
            lo, hi = np.percentile(image, [50.0, 99.8])
            vmin = lo if vmin is None else vmin
            vmax = (hi if hi > lo else image.max()) if vmax is None else vmax
        if not caller_norm:
            if vmin is None:
                vmin = np.nanmin(image)
            if vmax is None:
                vmax = np.nanmax(image)
            imshow_kw["vmin"] = vmin
            imshow_kw["vmax"] = vmax
        imshow_kw.setdefault("origin", "lower")
        imshow_kw.setdefault("interpolation", "nearest")
        imshow_kw.setdefault("extent", (-0.5, side - 0.5, -0.5, side - 0.5))
        mappable = ax.imshow(image, cmap=resolved_cmap, **imshow_kw)
        bare_axes(ax)
        if colorbar:
            ax.get_figure().colorbar(mappable, ax=ax, fraction=0.046, pad=0.04)
        if title is None:
            gran = "" if granularity == 1 else f", {granularity}-granularity"
            kind = "Fourier map" if fourier else "Difference map" if difference else "Hilbert plot"
            title = f"{self._curve.name}  {kind} ({side}x{side}{gran})"
        ax.set_title(title, fontsize=9)
        return ax

    def show(self, cmap="viridis", **kwargs) -> Axes:
        """Draw the plot, open a window, and return the axes.

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
        >>> import numpy as np; from hilbertplot._viz.hilbert_plot import hilbert_plot
        >>> hilbert_plot(0, np.arange(1, 101)).save(
        ...     "out.png", ["red", "green", "tab:blue"])          # doctest: +SKIP
        'out.png'
        """
        from .render import save_figure

        return save_figure(self.draw(cmap, **kwargs), path, dpi=dpi)

    def __repr__(self) -> str:
        return f"<HilbertPlot: {len(self)} values on {self._curve.name}>"

    def _repr_png_(self) -> bytes | None:
        """Render inline in Jupyter, so a bare ``plot`` in a cell shows the image.

        Returns ``None`` when matplotlib is not installed, so the notebook falls back to
        :meth:`__repr__` rather than raising -- matplotlib is an optional extra.
        """
        try:
            from .render import figure_png

            return figure_png(self.draw())
        except ModuleNotFoundError:  # pragma: no cover - matplotlib is a test dependency
            return None


def hilbert_plot(curve: Curve | int | str, data) -> HilbertPlot:
    """Make a :class:`HilbertPlot` straight from a curve and data.

    A shortcut for ``hilbertplot.curves.info(which).plot_data(data)`` that skips the intermediate
    curve object.

    Parameters
    ----------
    curve : Curve or int or str
        A :class:`Curve`, or an index, name or paper symbol.
    data : array_like
        The 1-D sequence to visualise.

    Returns
    -------
    HilbertPlot

    Examples
    --------
    >>> from hilbertplot._viz.hilbert_plot import hilbert_plot
    >>> plot = hilbert_plot(0, range(1024))    # curve 0 (Hilbert)
    >>> plot.show(["red", "green", "tab:blue"])      # doctest: +SKIP
    """
    c = curve if isinstance(curve, Curve) else _lookup_curve(curve)
    return HilbertPlot(c, data)
