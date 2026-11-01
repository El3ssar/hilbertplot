"""Array operations on numeric sequences, without rendering figures.

>>> from hilbertplot import data
>>> data.to_grid(range(100)).shape
(16, 16)
"""

from ._api import fourier, from_grid, to_grid
from ._data.mapping import granulate

__all__ = ["fourier", "from_grid", "granulate", "to_grid"]


def __dir__() -> list[str]:
    """Return only the supported public names for interactive completion."""
    return sorted(__all__)
