"""hilbertplot -- the complete set of 40 two-dimensional Hilbert curves, and data plots on them.

``hilbertplot`` implements every two-dimensional Hilbert-type space-filling curve proved to
exist by Estevez-Rams *et al.*, "Hilbert curves in two dimensions", *Rev. Cub. Fis.*
**34**, 9 (2017): twelve homogeneous (six proper, six improper) and twenty-eight
inhomogeneous -- forty in all -- and uses them to lay long 1-D data vectors onto 2-D
images (Estevez-Rams *et al.*, *Comput. Phys. Commun.* **197** (2015) 118).

Curves
------
>>> import hilbertplot
>>> hilbertplot.curve("Moore").show(6)                 # doctest: +SKIP
>>> hilbertplot.curve(0).points(3).shape
(64, 2)
>>> hilbertplot.proper().names
['Hilbert', 'Moore', 'Liu1', 'Liu2', 'Liu3', 'Liu4']

Group functions (:func:`catalog`, :func:`homogeneous`, :func:`generalizing`, ...) return a
:class:`CurveList` that prints as a table and composes -- ``catalog().closed()``.

Data plots
----------
:meth:`Curve.plot_data` / :func:`hilbert_plot` return a :class:`HilbertPlot` that holds the
data and draws nothing until you call ``.draw`` / ``.show`` / ``.save`` -- where you pick
the colormap (a name or a list of colours to interpolate), the granularity, and how to fit
a length that is not a power of four:

>>> plot = hilbertplot.hilbert_plot(0, range(1024))    # curve 0, the Hilbert curve
>>> plot.show(["red", "green", "tab:blue"])      # doctest: +SKIP
>>> plot.show("viridis", granularity=4)          # doctest: +SKIP

One cell at a time
------------------
:meth:`Curve.encode` and :meth:`Curve.decode` convert between a step along the curve and a
cell, in ``O(order)`` and without materialising anything -- so they work at orders whose
curve could never fit in memory, for all forty curves:

>>> hilbertplot.curve(0).encode(5, 2)
(0, 3)
>>> hilbertplot.curve(0).decode(0, 3, 2)
5

Round trip
----------
``curve.unroll(image)`` reads a square array back into a 1-D vector in curve order -- the
inverse of the data mapping.  It accepts any side for the eight :func:`generalizing`
curves, and ``2**k`` for the rest.

Rendering needs the optional ``[plot]`` extra (matplotlib); everything above -- generation,
the data mapping, ``unroll``, the difference and Fourier maps -- runs on numpy alone.

The public API is exactly the names in ``hilbertplot.__all__``; everything else is internal.
"""

from __future__ import annotations

from ._core.curve import (
    Curve,
    CurveList,
    by_kernels,
    catalog,
    closed,
    curve,
    generalizing,
    homogeneous,
    improper,
    inhomogeneous,
    proper,
)
from ._core.generation import cache_info, clear_cache
from ._core.geometry import canonical_form, is_space_filling
from ._core.limits import cell_limit, set_cell_limit
from ._data.mapping import granulate
from ._viz.hilbert_plot import HilbertPlot, hilbert_plot
from ._viz.render import gallery

__version__ = "0.2.0"

__all__ = [
    "Curve",
    "CurveList",
    "HilbertPlot",
    "__version__",
    "by_kernels",
    "cache_info",
    "canonical_form",
    "catalog",
    "cell_limit",
    "clear_cache",
    "closed",
    "curve",
    "gallery",
    "generalizing",
    "granulate",
    "hilbert_plot",
    "homogeneous",
    "improper",
    "inhomogeneous",
    "is_space_filling",
    "proper",
    "set_cell_limit",
]
