# Contributing to hilbertplot

Thanks for helping improve **hilbertplot**! This project ships continuously:
every merge to `main` is analyzed, and if it warrants a release, the version is
bumped, tagged, changelogged, and published to PyPI **automatically**. That only
works if commit history speaks [Conventional Commits](https://www.conventionalcommits.org/),
so please read the short section below before opening a PR.

## Conventional Commits and version bumps

Pull requests are **squash-merged**, and the **PR title becomes the commit that
lands on `main`**. A CI check (`Lint PR title`) enforces that the title is a valid
Conventional Commit, so the title is what matters — not your individual commits.

Format:

```
<type>[optional (scope)][optional !]: <subject>
```

How the type maps to the next version (via python-semantic-release):

| PR title example                                  | Release effect            |
| ------------------------------------------------- | ------------------------- |
| `fix: correct off-by-one in unroll`               | **patch** (0.1.0 → 0.1.1) |
| `feat: add Moore-curve gallery layout`            | **minor** (0.1.0 → 0.2.0) |
| `feat!: rename plot_data to hilbert_plot`         | **major** (0.1.0 → 1.0.0) |
| `refactor: ...` `perf: ...` `docs: ...` `chore: ...` `test: ...` `build: ...` `ci: ...` `style: ...` | no release |

A breaking change is signalled **either** by a `!` after the type/scope
(`feat!:` / `feat(core)!:`) **or** by a `BREAKING CHANGE:` footer in the PR body.

Allowed types: `feat`, `fix`, `docs`, `chore`, `refactor`, `perf`, `test`,
`build`, `ci`, `style`, `revert`. Scope is optional. The subject must not start
with an uppercase letter (`feat: add ...`, not `feat: Add ...`).

> While the project is on `0.x`, a plain `feat:` stays within `0.x` (e.g.
> `0.2.0 → 0.3.0`); a breaking change moves the leading `0` and cuts `1.0.0`.

## What happens on merge

1. Your PR is squash-merged to `main` with its Conventional-Commit title.
2. The **Release** workflow runs python-semantic-release, which:
   - computes the next version from the commits since the last tag,
   - stamps it into `pyproject.toml` and `src/hilbertplot/__init__.py`,
   - runs `scripts/build_release.sh` to regenerate `uv.lock` with uv and build
     the candidate distributions, then includes the lock in its release commit,
   - updates `CHANGELOG.md`, commits, tags `vX.Y.Z`, and creates a GitHub Release.
3. If a release was cut, the **publish** job builds the sdist + wheel from the
   new tag and uploads them to [PyPI](https://pypi.org/p/hilbertplot) via Trusted
   Publishing (OIDC — no API tokens involved).

You never edit the version by hand and you never publish manually.

The version is determined by the squash commit/PR title. `uv.lock` is generated;
do not edit its version entry manually. The release build hook runs after version
stamping and before the release commit/tag. For development dependency changes,
`uv lock` updates the generated lock against the current project metadata.

CI exercises `fix:`, `feat:`, and `feat!:` releases in disposable repositories,
checking that metadata, the source version, the committed lockfile, tags and built
artifacts agree. This check never pushes or publishes:

```bash
uv run --no-project --with python-semantic-release==10.6.1 python scripts/check_release.py
```

## Local development

```bash
# One-time: create the environment and install the project with dev extras.
uv venv
uv sync --extra dev

# Run the full test suite (unit tests + doctests).
uv run pytest
uv run pytest --doctest-modules src/hilbertplot

# Lint and formatting (must be clean for CI to pass).
uv run ruff check .
uv run ruff format --check .

# Auto-fix what can be fixed.
uv run ruff check --fix .
uv run ruff format .
```

CI runs three more jobs you can reproduce locally when you touch the relevant area:

```bash
# matplotlib is an optional extra; the numpy-only path must keep working.
uv venv /tmp/nomp && VIRTUAL_ENV=/tmp/nomp uv pip install . pytest
VIRTUAL_ENV=/tmp/nomp uv run --no-project pytest

# `python -O` strips asserts, so shipped-data validation must use `raise`.
uv run python -O -m pytest

# The built artifacts must contain the package and nothing else.
uv build && uvx twine check dist/*
```

## Documentation

Build the guides, API reference and generated gallery locally:

```bash
uv sync --inexact --extra dev --extra docs
uv run --no-sync python scripts/check_docs.py
uv run --no-sync sphinx-build -W --keep-going -b html docs docs/_build/html
python -m http.server 8000 --directory docs/_build/html
```

Open `http://localhost:8000`. The documentation check executes Python examples and
checks coverage of public functions. The strict Sphinx build rejects warnings.
Generated HTML and gallery images are ignored by Git.

The Documentation workflow validates pull requests and deploys `main` after the
Release workflow completes. Before the first deployment, a repository maintainer
must select **GitHub Actions** under **Settings → Pages → Build and deployment**.
The intended URL is `https://el3ssar.github.io/hilbertplot/`.

## What the tests are protecting

Beyond the usual unit tests, a few suites encode invariants that have actually been
broken before — read these before changing the code they cover:

- `tests/test_performance.py` asserts *ratios*, not wall-clock, so it means the same on a
  laptop and a throttled runner. It exists because `grid()` once bottomed out its recursion
  once per cell, making the default render path ~17× slower than the power-of-two path.
- `tests/test_arbitrary.py` checks that every entry of `SMALLEST_FAILURE` really is the
  smallest square at which that curve's construction breaks. The number goes straight into
  a user-facing error, and three entries were wrong before the test existed.
- `tests/test_indexing.py` checks `encode`/`decode` against the materialised curve for all
  forty curves, exhaustively at small orders.
- `tests/test_readme.py` executes every `python` block in `README.md`, so the front page
  cannot drift from the API.
- `-W error::RuntimeWarning` is on by default: a numpy warning during ordinary use is a
  defect, not noise.

Open a PR against `main` with a Conventional-Commit title, make sure CI is green,
and you're done — the release machinery takes it from there.
