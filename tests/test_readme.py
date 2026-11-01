"""Execute every Python snippet in README.md, so the front page cannot rot.

The README's examples are plain fenced ``python`` blocks rather than doctests, which keeps
them readable -- but nothing then checks that they still run.  This module extracts and
executes them in order, sharing one namespace the way a reader following along would, with
``show()`` stubbed out so nothing tries to open a window.
"""

from __future__ import annotations

import re
from pathlib import Path

import matplotlib
import pytest

matplotlib.use("Agg")

README = Path(__file__).resolve().parent.parent / "README.md"

# ```python ... ``` blocks only; ```bash install lines are not executable here.
_PYTHON_BLOCK = re.compile(r"^```python\n(.*?)^```", re.MULTILINE | re.DOTALL)


def _python_blocks(text: str) -> list[str]:
    return [block for block in _PYTHON_BLOCK.findall(text) if block.strip()]


@pytest.fixture(scope="module")
def readme_text() -> str:
    if not README.is_file():
        pytest.skip(f"README.md not found at {README} (not running from a source checkout)")
    return README.read_text(encoding="utf-8")


def test_readme_has_python_examples(readme_text: str):
    """Guard the guard: if the extraction regex ever stops matching, fail loudly."""
    assert len(_python_blocks(readme_text)) >= 3


def test_every_readme_python_block_runs(
    readme_text: str, monkeypatch: pytest.MonkeyPatch, tmp_path
):
    import matplotlib.pyplot as plt

    # The README legitimately calls .show(); make it a no-op that also frees the figure.
    monkeypatch.setattr(plt, "show", lambda *a, **k: None)
    monkeypatch.chdir(tmp_path)
    shared: dict[str, object] = {}
    for number, block in enumerate(_python_blocks(readme_text), start=1):
        _run_block(block, number, shared)
        plt.close("all")


def _run_block(block: str, number: int, namespace: dict[str, object]) -> None:
    """Execute one README block, turning any failure into a readable test failure."""
    try:
        exec(compile(block, f"README.md[block {number}]", "exec"), namespace)
    except Exception as exc:  # pragma: no cover - only on a broken README
        pytest.fail(
            f"README.md python block {number} failed with {type(exc).__name__}: {exc}\n\n{block}"
        )
