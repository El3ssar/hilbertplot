# Development and reproducibility

```bash
uv sync --extra dev --extra docs
uv run pytest
uv run pytest --doctest-modules src/hilbertplot
uv run ruff check .
uv run ruff format --check .
```

## Build this documentation

```bash
uv run sphinx-build -W --keep-going -b html docs docs/_build/html
uv run python scripts/check_docs.py --html
python -m http.server 8000 --directory docs/_build/html
```

Open `http://localhost:8000`. The documentation build generates gallery images from the
public API and reads function signatures/docstrings for the reference pages. Generated
images and HTML are ignored by Git. `scripts/check_docs.py` executes the narrative Python
examples and checks that every public function is represented in the reference.

## Release process

Conventional commit titles select the next version. On the main branch, semantic-release
stamps the version, refreshes `uv.lock` through `scripts/build_release.sh`, builds the
artifacts, and creates a release commit and tag. The publish job builds from that tag and
uploads to PyPI. No manual version or lockfile text edits are needed.

```bash
uv run --no-project --with python-semantic-release==10.6.1 python scripts/check_release.py
```

This exercises patch, minor and breaking releases in disposable repositories without pushing.

## Scientific scope

The catalog follows Estevez-Rams et al., *Hilbert curves in two dimensions*, Rev. Cub. Fís.
**34**, 9 (2017). The implementation uses the specified family of forty Hilbert-type curves;
it is not a catalog of every possible space-filling construction.

The repository's `research/` folder contains the arbitrary-square and quasisquare study.
The package exposes its supported constructions and verifies their coverage and connectivity
in tests. Research manuscripts and intermediate artifacts are excluded from package builds.

## Citation and archiving

Zenodo automatically archives new GitHub releases. The all-versions DOI is
[10.5281/zenodo.23858267](https://doi.org/10.5281/zenodo.23858267).
Version 1.0.1 is archived at
[10.5281/zenodo.23858268](https://doi.org/10.5281/zenodo.23858268).
Author, description, license and keywords come from `CITATION.cff`. Keep its
all-versions DOI stable; release-specific DOIs are assigned by Zenodo.

## Documentation conventions

Public functions use NumPy-style docstrings: a concise summary, typed Parameters,
named Returns, applicable Raises, and executable Examples. Explain array shapes,
coordinate conventions, dtype/mask behavior and information loss at the call site.
Keep implementation classes internal; expose only the function reference to users.

Run `python scripts/check_docs.py` to execute the narrative examples, verify every
public function has a reference entry, and audit public docstring sections and parameters.
CI also runs the source docstring examples. The strict Sphinx build generates the gallery
from the public API. The favicon is generated from curve 0 at order 3.
