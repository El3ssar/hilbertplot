"""Optional cache and allocation controls. Ordinary plotting needs no configuration."""

from ._core.generation import cache_info, clear_cache
from ._core.limits import cell_limit, set_cell_limit

__all__ = ["cache_info", "cell_limit", "clear_cache", "set_cell_limit"]


def __dir__() -> list[str]:
    return sorted(__all__)
