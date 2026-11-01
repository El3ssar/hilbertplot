"""Matplotlib rendering, kept behind the :class:`~hilbertplot._core.curve.Curve` methods.

Nothing else in the package imports matplotlib, and it is imported lazily only when a
plot is actually drawn, so the maths runs with numpy alone.  Users never call into
this module directly -- they use ``curve.draw(order)`` / ``curve.show(order)`` /
``curve.save(path, order)`` and :func:`gallery`.

Two render modes, chosen automatically by order:

* ``"line"`` draws the actual polyline.  At low orders this is colour-graded along the
  curve (via a ``LineCollection``) so the traversal order is visible; that technique
  is one path per stroke, so it is only used up to order 7.
* ``"fill"`` paints a ``2**order`` by ``2**order`` image whose pixels are coloured by
  visit order and shows it with ``imshow``.  This is O(cells) and stays fast for
  millions of points -- and at high orders, where individual strokes are sub-pixel,
  it is also the *only* legible view.

``mode="auto"`` (the default) uses ``line`` below order 8 and ``fill`` at or above it.
Passing an explicit ``color=`` always draws a single fast solid polyline.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING, Any

import numpy as np

from .._core.curve import Curve

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure
else:
    # Runtime stand-ins so `get_type_hints()` can evaluate the stringified annotations
    # without importing matplotlib -- see the note in `_core/curve.py`.
    Axes = Any
    Figure = Any

__all__ = ["bare_axes", "draw", "figure_png", "gallery", "pyplot", "save_figure"]

# At/above this order individual strokes are sub-pixel: switch to the fill image.
_AUTO_FILL_ORDER = 8
# Per-stroke gradient colouring (LineCollection) is only practical up to this order.
_GRADIENT_MAX_ORDER = 7
_DEFAULT_COLOR = "#1f4e79"
_MODES = ("auto", "line", "fill")


def pyplot():
    """Return ``matplotlib.pyplot`` with a friendly error if matplotlib is missing."""
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "Plotting needs matplotlib. Install it with "
            "'uv pip install hilbertplot[plot]' (or 'pip install matplotlib')."
        ) from exc
    return plt


def bare_axes(ax: Axes, side: int | None = None) -> Axes:
    """Strip an axes down to the image: equal aspect, no ticks, no spines.

    Shared by the curve renderer and :meth:`hilbertplot.HilbertPlot.draw` so both look
    the same.  When ``side`` is given the limits are set to frame a ``side x side`` grid.
    """
    if side is not None:
        ax.set_xlim(-0.75, side - 0.25)
        ax.set_ylim(-0.75, side - 0.25)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    return ax


def save_figure(ax: Axes, path: str, *, dpi: int = 140) -> str:
    """Save ``ax``'s figure to ``path``, always closing it, and return ``path``.

    The close is in a ``finally`` so a failed write (bad extension, unwritable directory)
    cannot leak the figure -- matplotlib keeps every open figure alive globally, so a loop
    of failing saves would otherwise grow without bound.
    """
    plt = pyplot()
    figure = ax.get_figure()
    try:
        figure.savefig(path, dpi=dpi, bbox_inches="tight")
    finally:
        plt.close(figure)
    return path


def figure_png(ax: Axes) -> bytes:
    """Render ``ax``'s figure to PNG bytes and close it -- for notebook ``_repr_png_``."""
    import io

    plt = pyplot()
    figure = ax.get_figure()
    buffer = io.BytesIO()
    try:
        figure.savefig(buffer, format="png", dpi=110, bbox_inches="tight")
    finally:
        plt.close(figure)
    return buffer.getvalue()


def _draw_fill(ax, pts, rows, columns, cmap):
    img = np.empty((rows, columns), dtype=np.float32)
    img[pts[:, 1], pts[:, 0]] = np.linspace(0.0, 1.0, len(pts), dtype=np.float32)
    ax.imshow(
        img,
        cmap=cmap,
        origin="lower",
        interpolation="nearest",
        extent=(-0.5, columns - 0.5, -0.5, rows - 0.5),
    )


def _draw_line(ax, pts, order, color, cmap, linewidth):
    if linewidth is None:
        linewidth = max(0.15, 3.0 - 0.35 * order)
    if color is None and order <= _GRADIENT_MAX_ORDER:
        from matplotlib.collections import LineCollection

        segs = np.stack([pts[:-1], pts[1:]], axis=1)
        lc = LineCollection(
            segs, cmap=cmap, linewidth=linewidth, capstyle="round", joinstyle="round"
        )
        lc.set_array(np.linspace(0.0, 1.0, len(segs)))
        ax.add_collection(lc)
        ax.autoscale_view()
    else:
        ax.plot(
            pts[:, 0],
            pts[:, 1],
            color=color or _DEFAULT_COLOR,
            linewidth=linewidth,
            solid_capstyle="round",
            solid_joinstyle="round",
        )


def draw(
    curve: Curve,
    order: int | None = None,
    ax: Axes | None = None,
    *,
    shape: tuple[int, int] | None = None,
    mode: str = "auto",
    color: str | None = None,
    cmap: str = "viridis",
    linewidth: float | None = None,
    endpoints: bool = True,
    title: str | None = None,
) -> Axes:
    """Draw one curve at ``order`` onto ``ax`` (created if ``None``); return the axes."""
    if mode not in _MODES:
        legal = ", ".join(repr(name) for name in _MODES)
        raise ValueError(f"mode must be one of {legal}, got {mode!r}")
    if shape is not None:
        from .._core.arbitrary import check_shape, shape_points

        if order is not None:
            raise ValueError("choose either order or shape, not both")
        rows, columns = check_shape(shape)
        pts = shape_points(curve.index, (rows, columns))
        order = (max(rows, columns) - 1).bit_length()
        size_title = f"{rows}x{columns}"
    else:
        order = 4 if order is None else order
        pts = curve.points(order)
        rows = columns = 2**order
        size_title = f"order {order}"
    plt = pyplot()
    if ax is None:
        _, ax = plt.subplots(figsize=(5, 5))
    if mode == "auto":
        mode = "fill" if order >= _AUTO_FILL_ORDER else "line"

    if mode == "fill":
        _draw_fill(ax, pts, rows, columns, cmap)
    else:
        _draw_line(ax, pts, order, color, cmap, linewidth)
        if endpoints:
            ms = max(2.0, 6.0 - 0.5 * order)
            ax.plot(*pts[0], "o", color="black", markersize=ms, zorder=3)  # entry
            ax.plot(*pts[-1], "s", color="black", markersize=ms, zorder=3)  # exit

    bare_axes(ax)
    ax.set_xlim(-0.75, columns - 0.25)
    ax.set_ylim(-0.75, rows - 0.25)
    if title is None:
        title = f"{curve.symbol} ({curve.name}), {size_title}"
    ax.set_title(title, fontsize=9)
    return ax


def gallery(
    curves: Iterable[Curve],
    order: int = 3,
    *,
    ncols: int | None = None,
    save: str | None = None,
    mode: str = "auto",
    cmap: str = "viridis",
    color: str | None = None,
    title: str | None = None,
    dpi: int = 140,
    show: bool = True,
) -> Figure:
    """Draw a grid of curves; show it, or save it if ``save=`` is given.

    Parameters
    ----------
    curves : iterable of Curve
        The curves to draw, e.g. ``hilbertplot.curves.homogeneous()`` or
        Any iterable of internal Curve handles works; it is consumed once.
    order : int, default 3
        Order at which to draw every curve.
    ncols : int, optional
        Number of columns; chosen automatically when ``None``.
    save : str, optional
        If given, save the figure to this path and close it; otherwise open a window.
    mode : {"auto", "line", "fill"}, default "auto"
        Render mode passed to each panel (see :meth:`hilbertplot._core.curve.Curve.draw`).
    cmap : str, default "viridis"
        Colormap for the gradient/fill rendering.
    color : str, optional
        Solid line colour (overrides the gradient) for every panel.
    title : str, optional
        Overall figure title.
    dpi : int, default 140
        Resolution used when ``save`` is given.

    Returns
    -------
    matplotlib.figure.Figure

    Raises
    ------
    ValueError
        If ``curves`` is empty, or ``ncols`` is not at least 1.

    Examples
    --------
    >>> import hilbertplot
    >>> figure = hilbertplot.gallery(hilbertplot.curves.proper(), order=3)      # doctest: +SKIP
    >>> hilbertplot.gallery(hilbertplot.curves.improper(), save="improper.png")  # doctest: +SKIP
    """
    plt = pyplot()
    curves = list(curves)
    if not curves:
        raise ValueError("no curves to plot; pass a non-empty iterable of Curve")
    if ncols is None:
        ncols = min(6, len(curves))
    elif not isinstance(ncols, int) or isinstance(ncols, bool) or ncols < 1:
        raise ValueError(f"ncols must be an int >= 1, got {ncols!r}")
    nrows = -(-len(curves) // ncols)

    fig, axes = plt.subplots(nrows, ncols, figsize=(2.2 * ncols, 2.2 * nrows), squeeze=False)
    flat = axes.ravel()
    for ax, c in zip(flat, curves, strict=False):
        draw(c, order, ax=ax, mode=mode, cmap=cmap, color=color, endpoints=False)
    for ax in flat[len(curves) :]:
        ax.set_visible(False)
    if title:
        fig.suptitle(title, fontsize=12)
    fig.tight_layout()

    if save is not None:
        try:
            fig.savefig(save, dpi=dpi, bbox_inches="tight")
        finally:
            plt.close(fig)
    elif show:
        plt.show()
    return fig
