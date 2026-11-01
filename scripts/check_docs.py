"""Execute documentation examples and check coverage of the public API reference."""

from __future__ import annotations

import ast
import contextlib
import inspect
import io
import os
import re
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import hilbertplot as hp


def check_html():
    """Check generated local links, anchors, images, API signatures and favicon geometry."""
    from bs4 import BeautifulSoup

    root = Path(__file__).resolve().parents[1] / "docs" / "_build" / "html"
    pages = {p.resolve(): BeautifulSoup(p.read_text(), "html.parser") for p in root.rglob("*.html")}
    if not pages:
        raise AssertionError("Build HTML before running --html")
    for path, page in pages.items():
        required = {
            "description": page.select_one('meta[name="description"]'),
            "og:title": page.select_one('meta[property="og:title"]'),
            "og:description": page.select_one('meta[property="og:description"]'),
            "og:url": page.select_one('meta[property="og:url"]'),
            "og:image": page.select_one('meta[property="og:image"]'),
            "og:image:alt": page.select_one('meta[property="og:image:alt"]'),
            "twitter:title": page.select_one('meta[name="twitter:title"]'),
            "twitter:description": page.select_one('meta[name="twitter:description"]'),
            "twitter:image": page.select_one('meta[name="twitter:image"]'),
            "twitter:image:alt": page.select_one('meta[name="twitter:image:alt"]'),
        }
        for name, node in required.items():
            if node is None or not node.get("content", "").strip():
                raise AssertionError(f"Missing sharing metadata: {path.name}: {name}")
        canonical = page.select_one('link[rel="canonical"]')
        if canonical is None or canonical.get("href") != required["og:url"]["content"]:
            raise AssertionError(f"Canonical and social URLs disagree: {path.name}")
        for name in ("og:url", "og:image", "twitter:image"):
            if not required[name]["content"].startswith("https://el3ssar.github.io/hilbertplot/"):
                raise AssertionError(f"Sharing URL must be absolute: {path.name}: {name}")
        if required["og:image"]["content"] != required["twitter:image"]["content"]:
            raise AssertionError(f"Sharing images disagree: {path.name}")
        card = page.select_one('meta[name="twitter:card"]')
        if card is None or card.get("content") != "summary_large_image":
            raise AssertionError(f"Missing large social card: {path.name}")
        for dimension, expected in (("width", "1200"), ("height", "630")):
            node = page.select_one(f'meta[property="og:image:{dimension}"]')
            if node is None or node.get("content") != expected:
                raise AssertionError(f"Wrong sharing image {dimension}: {path.name}")
        for node in page.select("a[href], link[href], img[src], script[src]"):
            address = urlsplit(node.get("href", node.get("src", "")))
            if address.scheme or address.netloc:
                continue
            target = (path.parent / unquote(address.path)).resolve() if address.path else path
            if target.is_dir():
                target /= "index.html"
            if not target.exists():
                raise AssertionError(f"Missing local target: {path.name} -> {target}")
            if node.name == "img" and "generated" in target.parts and target.suffix == ".png":
                alternate = target.with_name(target.stem + "-dark.png")
                if not alternate.exists():
                    raise AssertionError(f"Missing dark-theme figure: {alternate}")
            if (
                address.fragment
                and target in pages
                and not pages[target].find(id=unquote(address.fragment))
            ):
                raise AssertionError(f"Missing anchor: {target}#{address.fragment}")
        if page.select_one("article p") and ".. py:function::" in page.get_text():
            raise AssertionError(f"Unrendered API markup: {path}")
    from PIL import Image

    with Image.open(root / "_static" / "social-preview.png") as poster:
        if poster.size != (1200, 630) or poster.format != "PNG":
            raise AssertionError("Sharing poster must be a 1200 by 630 PNG")
    svg = ElementTree.parse(root / "_static" / "favicon.svg")
    polyline = svg.find("{http://www.w3.org/2000/svg}polyline")
    vertices = np.array(
        [tuple(map(float, p.split(","))) for p in polyline.attrib["points"].split()]
    )
    expected = hp.curves.points(0, order=3)
    np.testing.assert_array_equal(vertices[:, 0], 10 + 6 * expected[:, 0])
    np.testing.assert_array_equal(vertices[:, 1], 54 - 6 * expected[:, 1])
    print(
        f"Checked {len(pages)} HTML pages: sharing metadata, local links, anchors, "
        "assets and exact order-3 favicon."
    )


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
    # Keep REPL help as complete as the rendered reference, without adding public objects.
    audited = 0
    for module in (hp, hp.curves, hp.data, hp.config):
        for name in module.__all__:
            func = getattr(module, name)
            if not inspect.isfunction(func):
                continue
            text = inspect.getdoc(func) or ""
            if "\nReturns\n-------" not in text:
                raise AssertionError(f"Missing NumPy Returns section: {module.__name__}.{name}")
            signature = inspect.signature(func)
            if signature.parameters:
                if "\nParameters\n----------" not in text:
                    raise AssertionError(f"Missing Parameters section: {module.__name__}.{name}")
                section = text.split("\nParameters\n----------\n", 1)[1]
                section = re.split(r"\n[A-Z][A-Za-z ]+\n-+\n", section)[0]
                documented = set()
                for declaration in re.findall(r"^([\w*, ]+) : ", section, re.MULTILINE):
                    documented.update(n.strip().lstrip("*") for n in declaration.split(","))
                absent = set(signature.parameters) - documented
                if absent:
                    raise AssertionError(f"Undocumented parameters on {name}: {sorted(absent)}")
            audited += 1
    for source in (root / "src" / "hilbertplot").rglob("*.py"):
        tree = ast.parse(source.read_text())
        for node in ast.walk(tree):
            if isinstance(
                node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
            ) and not ast.get_docstring(node):
                raise AssertionError(f"Missing source docstring: {source}:{node.lineno}")
    count = 0
    original = Path.cwd()
    plt.show = lambda: None
    try:
        with tempfile.TemporaryDirectory(prefix="hilbertplot-doc-examples-") as temporary:
            os.chdir(temporary)
            for page in sorted(docs.rglob("*.md")):
                if "_build" in page.parts:
                    continue
                namespace = {}
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
        f"{audited} public functions have typed NumPy sections and reference entries"
    )


if __name__ == "__main__":
    import sys

    if sys.argv[1:] == ["--html"]:
        check_html()
    elif sys.argv[1:]:
        raise SystemExit("Usage: python scripts/check_docs.py [--html]")
    else:
        main()
