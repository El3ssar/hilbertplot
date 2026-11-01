"""Shared test setup: a headless backend, and no figure leaks between tests.

Matplotlib keeps every open figure alive in a global registry, so a suite that draws
without closing slowly accumulates them and eventually warns about too many open figures.
Selecting ``Agg`` before anything imports ``pyplot`` also guarantees no test can block on
an interactive window in CI.

NumPy and Matplotlib are standard runtime dependencies. Missing Matplotlib should
fail test collection rather than silently skipping plotting coverage.
"""

from __future__ import annotations

import matplotlib
import pytest

matplotlib.use("Agg")


@pytest.fixture(autouse=True)
def _close_figures():
    """Close any figures a test leaves open, whether it passed or failed."""
    yield
    import matplotlib.pyplot as plt

    plt.close("all")
