"""Execute documentation examples and check coverage of the public API reference."""

from __future__ import annotations

import contextlib
import inspect
import io
import os
import re
import tempfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import hilbertplot as hp


def main():
    root = Path(__file__).resolve().parents[1]
    docs = root / "docs"
    pattern = re.compile(r"^```python\n(.*?)^```", re.MULTILINE | re.DOTALL)
    reference = "\n".join(p.read_text() for p in (docs / "reference").glob("*.md"))
    missing = []
    for module in (hp, hp.curves, hp.data, hp.config):
        for name in module.__all__:
            if inspect.isfunction(getattr(module, name)):
                target = f"{module.__name__}.{name}"
                if f".. autofunction:: {target}" not in reference:
                    missing.append(target)
    if missing:
        raise AssertionError(f"Public functions missing from reference: {missing}")
    count = 0
    original = Path.cwd()
    plt.show = lambda: None
    try:
        with tempfile.TemporaryDirectory(prefix="hilbertplot-doc-examples-") as temporary:
            os.chdir(temporary)
            for page in sorted(docs.rglob("*.md")):
                if "_build" in page.parts:
                    continue
                namespace = {
                    "hp": hp,
                    "np": np,
                    "plt": plt,
                    "t": np.arange(4096),
                    "values": np.sin(np.arange(900) / 15),
                    "image": np.arange(256).reshape(16, 16),
                }
                for number, code in enumerate(pattern.findall(page.read_text()), start=1):
                    try:
                        with contextlib.redirect_stdout(io.StringIO()):
                            exec(
                                compile(code, f"{page.relative_to(root)}[block {number}]", "exec"),
                                namespace,
                            )
                    except Exception as exc:
                        raise RuntimeError(
                            f"{page.relative_to(root)} block {number} failed"
                        ) from exc
                    finally:
                        plt.close("all")
                    count += 1
    finally:
        os.chdir(original)
    print(
        f"Executed {count} Python documentation examples; "
        "all public functions have reference entries"
    )


if __name__ == "__main__":
    main()
