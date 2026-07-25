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
   - updates `CHANGELOG.md`, commits, tags `vX.Y.Z`, and creates a GitHub Release.
3. If a release was cut, the **publish** job builds the sdist + wheel from the
   new tag and uploads them to [PyPI](https://pypi.org/p/hilbertplot) via Trusted
   Publishing (OIDC — no API tokens involved).

You never edit the version by hand and you never publish manually.

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

Open a PR against `main` with a Conventional-Commit title, make sure CI is green,
and you're done — the release machinery takes it from there.
