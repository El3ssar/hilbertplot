"""Curve catalog, metadata, coordinates and indexing; no custom objects are returned.

>>> from hilbertplot import curves
>>> curves.info("Moore")["index"]
1
>>> curves.points(12, order=3).shape
(64, 2)
"""

from ._api import (
    by_kernels,
    catalog,
    closed,
    difference_map,
    generalizing,
    grid,
    homogeneous,
    improper,
    index_to_xy,
    inhomogeneous,
    label_map,
    points,
    proper,
    word,
    xy_to_index,
)
from ._api import curve as info
from ._core.geometry import canonical_form, is_space_filling

__all__ = [
    "by_kernels",
    "canonical_form",
    "catalog",
    "closed",
    "difference_map",
    "generalizing",
    "grid",
    "homogeneous",
    "improper",
    "index_to_xy",
    "info",
    "inhomogeneous",
    "is_space_filling",
    "label_map",
    "points",
    "proper",
    "word",
    "xy_to_index",
]


def __dir__() -> list[str]:
    """Return only the supported public names for interactive completion."""
    return sorted(__all__)
