"""Documentation configuration; public API signatures come from the installed package."""

from pathlib import Path

import hilbertplot

project = "hilbertplot"
author = "Daniel Estevez"
copyright = "2026, Daniel Estevez"
release = hilbertplot.__version__
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    "sphinx_copybutton",
]
source_suffix = {".md": "markdown", ".rst": "restructuredtext"}
root_doc = "index"
exclude_patterns = ["_build", ".DS_Store"]
html_theme = "furo"
html_title = "hilbertplot"
html_favicon = "_static/favicon.svg"
html_last_updated_fmt = "%b %d, %Y"
html_static_path = ["_static"]
templates_path = ["_templates"]
html_css_files = ["custom.css"]
html_js_files = ["theme-plots.js"]
html_theme_options = {
    "source_repository": "https://github.com/El3ssar/hilbertplot/",
    "source_branch": "main",
    "source_directory": "docs/",
    "light_css_variables": {
        "color-brand-primary": "#285f86",
        "color-brand-content": "#285f86",
        "color-background-primary": "#fbfaf7",
        "color-background-secondary": "#f1f1eb",
        "color-foreground-primary": "#202725",
    },
    "dark_css_variables": {
        "color-brand-primary": "#92bede",
        "color-brand-content": "#92bede",
        "color-background-primary": "#171d1d",
        "color-background-secondary": "#202928",
        "color-foreground-primary": "#e8ece5",
    },
}
myst_heading_anchors = 4
myst_enable_extensions = ["colon_fence", "dollarmath"]
autodoc_typehints = "description"
autodoc_member_order = "bysource"
napoleon_numpy_docstring = True
napoleon_google_docstring = False
copybutton_prompt_text = r">>> |\.\.\. "
copybutton_prompt_is_regexp = True
html_baseurl = "https://el3ssar.github.io/hilbertplot/"


def generate_gallery(app):
    """Build figures from the same public functions that users call."""
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
    from docs_gallery import build

    build(Path(app.srcdir) / "_static" / "generated")


def social_context(app, pagename, templatename, context, doctree):
    """Emit crawler-readable sharing metadata for every generated page."""
    from docutils import nodes

    descriptions = {
        "index": (
            "Plot one-dimensional arrays along Hilbert curves. Convert images to sequences "
            "and reconstruct them with NumPy and Matplotlib. Forty curve constructions, "
            "Fourier maps and granularity."
        ),
        "guides/curves": (
            "Understand proper and improper Hilbert-type curves, homogeneous and "
            "inhomogeneous kernels, rotations, reflections and traversal reversal through "
            "worked constructions."
        ),
        "catalog": (
            "Compare all forty Hilbert-type curve paths, their entry and exit cells, "
            "construction families and kernels. Select curves by index, label or paper "
            "symbol."
        ),
        "quickstart": (
            "Plot numeric data along a selected Hilbert-type curve. Set colormaps and "
            "normalization, handle missing values, draw curve paths and save Matplotlib "
            "figures."
        ),
        "guides/conversion": (
            "Convert arrays and color images to one-dimensional sequences along a curve, "
            "reconstruct exact values, or rearrange data with a different curve."
        ),
        "guides/fourier": (
            "Compute two-dimensional Fourier maps of data arranged along Hilbert curves. "
            "Reproduce the Thue-Morse example and understand Hann windowing, scaling and "
            "curve dependence."
        ),
        "guides/granularity": (
            "Average consecutive sequence blocks before curve mapping. Compare periodic "
            "regions, choose granularity and understand length preservation and missing- "
            "value behavior."
        ),
        "guides/locality": (
            "Understand difference maps as mean visit-index distances between spatial "
            "neighbors. Compare curve locality using shared color scales and grid sizes."
        ),
    }
    description = descriptions.get(pagename)
    if description is None and doctree is not None:
        paragraph = next(iter(doctree.findall(nodes.paragraph)), None)
        if paragraph is not None:
            description = " ".join(paragraph.astext().split())
            if len(description) > 190:
                description = description[:187].rsplit(" ", 1)[0] + "…"
    context["social_description"] = (
        description
        or "hilbertplot documentation: plotting arrays, converting images and exploring "
        "Hilbert-type curves with Python."
    )
    context["social_title"] = (
        "hilbertplot — Python documentation"
        if pagename == "index"
        else f"{context.get('title', 'Documentation')} — hilbertplot"
    )
    context["social_url"] = app.config.html_baseurl + app.builder.get_target_uri(pagename)
    context["social_image"] = app.config.html_baseurl + "_static/social-preview.png"


def setup(app):
    app.connect("builder-inited", generate_gallery)
    app.connect("html-page-context", social_context)
