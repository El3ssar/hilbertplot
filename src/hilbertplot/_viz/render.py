"""Matplotlib rendering, kept behind the :class:`~hilbertplot._core.curve.Curve` methods.

Nothing else in the package imports matplotlib, and it is imported lazily only when a
plot is actually drawn, so the maths runs with numpy alone.  Users never call into
this module directly -- they use ``curve.show(order)`` / ``curve.save(order, path)`` /
``curve.plot(order)`` and :func:`gallery`.

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

import numpy as np

# At/above this order individual strokes are sub-pixel: switch to the fill image.
_AUTO_FILL_ORDER = 8
# Per-stroke gradient colouring (LineCollection) is only practical up to this order.
_GRADIENT_MAX_ORDER = 7
_DEFAULT_COLOR = "#1f4e79"


def pyplot():
    """Return ``matplotlib.pyplot`` with a friendly error if matplotlib is missing."""
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError as exc:  # pragma: no cover - environment dependent
        raise ModuleNotFoundError(
            "Plotting needs matplotlib. Install it with "
            "'uv pip install hilbertplot[plot]' (or 'pip install matplotlib')."
        ) from exc
    return plt


def _draw_fill(ax, pts, side, cmap):
    img = np.empty((side, side), dtype=np.float32)
    img[pts[:, 1], pts[:, 0]] = np.linspace(0.0, 1.0, len(pts), dtype=np.float32)
    ax.imshow(
        img,
        cmap=cmap,
        origin="lower",
        interpolation="nearest",
        extent=(-0.5, side - 0.5, -0.5, side - 0.5),
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
    curve,
    order: int,
    ax=None,
    *,
    mode: str = "auto",
    color: str | None = None,
    cmap: str = "viridis",
    linewidth: float | None = None,
    endpoints: bool = True,
    title: str | None = None,
):
    """Draw one curve at ``order`` onto ``ax`` (created if ``None``); return the axes."""
    plt = pyplot()
    pts = curve.points(order)
    side = 2**order
    if ax is None:
        _, ax = plt.subplots(figsize=(5, 5))
    if mode == "auto":
        mode = "fill" if order >= _AUTO_FILL_ORDER else "line"

    if mode == "fill":
        _draw_fill(ax, pts, side, cmap)
    elif mode == "line":
        _draw_line(ax, pts, order, color, cmap, linewidth)
        if endpoints:
            ms = max(2.0, 6.0 - 0.5 * order)
            ax.plot(*pts[0], "o", color="black", markersize=ms, zorder=3)  # entry
            ax.plot(*pts[-1], "s", color="black", markersize=ms, zorder=3)  # exit
    else:
        raise ValueError(f"mode must be 'auto', 'line' or 'fill', got {mode!r}")

    ax.set_xlim(-0.75, side - 0.25)
    ax.set_ylim(-0.75, side - 0.25)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    if title is None:
        title = f"{curve.symbol} ({curve.name}), order {order}"
    ax.set_title(title, fontsize=9)
    return ax


def gallery(
    curves,
    order=3,
    *,
    ncols=None,
    save=None,
    mode="auto",
    cmap="viridis",
    color=None,
    title=None,
    dpi=140,
):
    """Draw a grid of curves; show it, or save it if ``save=`` is given.

    Parameters
    ----------
    curves : iterable of Curve
        The curves to draw, e.g. ``hilbertplot.homogeneous()`` or ``hilbertplot.by_kernels(3, 5)``.
    order : int, default 3
        Order at which to draw every curve.
    ncols : int, optional
        Number of columns; chosen automatically when ``None``.
    save : str, optional
        If given, save the figure to this path and close it; otherwise open a window.
    mode : {"auto", "line", "fill"}, default "auto"
        Render mode passed to each panel (see :meth:`hilbertplot.curve.Curve.plot`).
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

    Examples
    --------
    >>> import hilbertplot
    >>> hilbertplot.gallery(hilbertplot.improper(), order=3, save="improper.png")   # doctest: +SKIP
    """
    plt = pyplot()
    curves = list(curves)
    if not curves:
        raise ValueError("no curves to plot")
    if ncols is None:
        ncols = min(6, len(curves))
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
        fig.savefig(save, dpi=dpi, bbox_inches="tight")
        plt.close(fig)
    else:
        plt.show()
    return fig
