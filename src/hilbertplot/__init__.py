"""Plot numeric sequences on any of forty two-dimensional Hilbert-type curves.

Plot data or a curve directly; every plotting call returns a matplotlib Figure:

>>> import hilbertplot as hp
>>> fig = hp.plot(range(100), curve=12)                 # doctest: +SKIP
>>> fig = hp.plot(range(100), fourier=True)             # doctest: +SKIP
>>> fig = hp.plot(range(100), difference=True)          # doctest: +SKIP
>>> fig = hp.plot_curve("Moore", order=4)               # doctest: +SKIP

Use ``fig.savefig(path)`` to save and ``plt.show()`` in scripts. Fourier and
difference maps are mutually exclusive, single-image transformations.

``curves`` holds the catalog and geometry, ``data`` the numeric operations,
and ``config`` the optional resource controls. Numeric operations do not initialize
the plotting backend.
Metadata uses ordinary dicts/lists;
all custom curve and plot classes are implementation details.

>>> hp.data.to_grid(range(100)).shape
(16, 16)
>>> hp.curves.info("Moore")["index"]
1
>>> hp.curves.xy_to_index(*hp.curves.index_to_xy(5, 2), 2)
5
"""

from . import config, curves, data
from ._api import gallery, plot, plot_curve

__version__ = "1.0.3"

__all__ = ["__version__", "config", "curves", "data", "gallery", "plot", "plot_curve"]


def __dir__() -> list[str]:
    """Keep completion focused on the function-based public API."""
    return sorted(__all__)
