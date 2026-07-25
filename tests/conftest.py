"""Shared test setup: a headless backend, and no figure leaks between tests.

Matplotlib keeps every open figure alive in a global registry, so a suite that draws
without closing slowly accumulates them and eventually warns about too many open figures.
Selecting ``Agg`` before anything imports ``pyplot`` also guarantees no test can block on
an interactive window in CI.

matplotlib is an optional extra, and CI has a job that installs the package *without* it to
exercise the numpy-only path -- so everything here degrades to a no-op when it is absent
rather than failing collection.
"""

from __future__ import annotations

import pytest

try:
    import matplotlib

    matplotlib.use("Agg")
    HAVE_MATPLOTLIB = True
except ModuleNotFoundError:  # numpy-only environment
    HAVE_MATPLOTLIB = False

#: Modules that import matplotlib at module scope.  ``collect_ignore`` is consulted before
#: pytest imports a file, so this prevents a collection error rather than merely skipping
#: the tests after the fact -- which a marker could not do.
_NEEDS_MATPLOTLIB = ("test_plotting.py", "test_readme.py")

collect_ignore = [] if HAVE_MATPLOTLIB else list(_NEEDS_MATPLOTLIB)


@pytest.fixture(autouse=True)
def _close_figures():
    """Close any figures a test leaves open, whether it passed or failed."""
    yield
    if HAVE_MATPLOTLIB:
        import matplotlib.pyplot as plt

        plt.close("all")
