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
>>> print(hilbertplot.proper())                        # doctest: +SKIP
 #  name     kind    closed
 ...

Data plots
----------
``plot_data`` / ``hilbert_plot`` return a ``HilbertPlot`` that holds the data and draws
nothing until you call ``.show`` / ``.save`` -- where you pick the colormap (a name or a
list of colours to interpolate), the granularity, and how to fit a length that is not a
power of four:

>>> plot = hilbertplot.hilbert_plot(0, range(1024))    # curve 0, the Hilbert curve
>>> plot.show(["red", "green", "tab:blue"])      # doctest: +SKIP
>>> plot.show("viridis", granularity=4)          # doctest: +SKIP

Round trip
----------
``curve.unroll(image)`` reads a ``2**k`` by ``2**k`` array back into a 1-D vector in
curve order -- the inverse of the data mapping.

The public API is exactly the names in ``hilbertplot.__all__``; everything else is internal.
"""

from __future__ import annotations

from ._core.curve import (
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
from ._viz.hilbert_plot import hilbert_plot
from ._viz.render import gallery

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "curve",
    "catalog",
    "homogeneous",
    "inhomogeneous",
    "proper",
    "improper",
    "closed",
    "generalizing",
    "by_kernels",
    "hilbert_plot",
    "gallery",
]
