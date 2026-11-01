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
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
]
source_suffix = {".md": "markdown", ".rst": "restructuredtext"}
root_doc = "index"
exclude_patterns = ["_build", ".DS_Store"]
html_theme = "furo"
html_title = "hilbertplot"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_theme_options = {
    "source_repository": "https://github.com/El3ssar/hilbertplot/",
    "source_branch": "main",
    "source_directory": "docs/",
    "light_css_variables": {"color-brand-primary": "#146d78", "color-brand-content": "#126571"},
    "dark_css_variables": {"color-brand-primary": "#67ced4", "color-brand-content": "#83dce0"},
}
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


def setup(app):
    app.connect("builder-inited", generate_gallery)
