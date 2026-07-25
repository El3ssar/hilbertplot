# Packaging & Release Readiness Review — `hilbertplot`

Reviewer: senior packaging audit. Every claim below is backed by a command run or a
cited `file:line`. Commands were run from the project root
`/home/elessar/Projects/HilbertPlots` unless noted.

## Verdict

**Not release-ready.** The wheel is clean and well-formed, and `uv build` / `twine check`
both pass — but the **source distribution ships ~7 MB of junk, including five copyrighted
academic PDFs it must not redistribute**, and the project metadata still points at
placeholder URLs (`github.com/example/hilbertplot`) with a placeholder author. These are
blockers for a public PyPI upload. Fix the sdist file selection and the metadata, add a
CHANGELOG, and single-source the version, and the package is in good shape for a `0.1.0`
release.

Readiness (this dimension): **4 / 10.**

## Strengths

- **Build works out of the box.** `uv build` produces both artifacts with no config
  fiddling, and `twine check` PASSES on both:
  ```
  Successfully built hilbertplot-0.1.0.tar.gz
  Successfully built hilbertplot-0.1.0-py3-none-any.whl
  Checking hilbertplot-0.1.0-py3-none-any.whl: PASSED
  Checking hilbertplot-0.1.0.tar.gz: PASSED
  ```
- **The wheel is minimal and correct.** `unzip -l` shows only `hilbertplot/**` plus
  dist-info — no tests, no research, no PDFs (38 KB total). `packages = ["src/hilbertplot"]`
  in `[tool.hatch.build.targets.wheel]` (pyproject.toml:41-42) is doing its job.
- **`py.typed` ships in the wheel** (`hilbertplot/py.typed` present in `unzip -l`), so the
  `Typing :: Typed` classifier is truthful and downstream type-checkers will see the types.
- **LICENSE ships correctly** as `hilbertplot-0.1.0.dist-info/licenses/LICENSE` in the wheel
  and at sdist root; it is referenced via `license = { text = "MIT" }` (pyproject.toml:9).
- **Sensible core metadata:** good `description`, `readme = "README.md"`, curated `keywords`,
  a correct set of trove `classifiers`, `requires-python = ">=3.10"`, a minimal runtime dep
  (`numpy>=1.21`), and `[plot]`/`[dev]` extras (pyproject.toml:1-40).
- **Dependency floors are declared** rather than pinned, which is right for a library.

## Findings

### BLOCKER — sdist redistributes five copyrighted academic PDFs
- **Location:** sdist contents; source files at project root (`Approximately even
  partition.pdf`, `Complete set.pdf`, `Hilbert Curves in two dimensions.pdf`,
  `Locality preserving homogeneous Hilbert curves.pdf`, `Visualizing long vectors.pdf`).
- **Evidence:** `tar tzf hilbertplot-0.1.0.tar.gz` lists all five PDFs at the sdist root;
  `ls -la` on the build output shows the sdist is **7,216,560 bytes (~7 MB)** versus a
  **38 KB** wheel. These are published papers (Rev. Cub. Fís.; Comput. Phys. Commun.), not
  the project's own work.
- **Why blocker:** uploading these to PyPI redistributes third-party copyrighted material
  under the project's MIT license, which the project has no right to do. It is also a 190x
  size blow-up of the sdist for content that has no place in a distribution.
- **Recommendation:** never ship these. Move the PDFs out of the repo (or into a
  git-ignored `papers/` dir) and, regardless, add an explicit sdist include-list so only
  intended files ship (see next finding).

### BLOCKER — sdist has no include/exclude control and vacuums up the whole tree
- **Location:** pyproject.toml — there is a `[tool.hatch.build.targets.wheel]` section but
  **no `[tool.hatch.build.targets.sdist]`** section, and no `MANIFEST.in`
  (`ls MANIFEST.in` → "no MANIFEST.in").
- **Evidence:** `tar tzf` shows the sdist contains `.coverage`, `scratch_blocks.py/.out`,
  `scratch_n13.out`, `scratch_v28.py`, `uv.lock`, the entire `research/` tree (LaTeX build
  artifacts `quasisquares/*.aux/.log/.out`, 40 `research/reports/curve_*.md`, internal
  `research/review/*.md`, `scratch_*` scripts), plus the five PDFs. Because this directory
  **is not a git repo** ("Is directory a git repo: No"), hatchling cannot use VCS ignore
  rules and falls back to including nearly everything.
- **Why blocker:** the sdist is the canonical source PyPI stores and from which the wheel is
  rebuilt; shipping scratch files, coverage data, and internal review notes is unprofessional
  and, combined with the PDFs, makes the artifact unacceptable.
- **Recommendation:** add an explicit allow-list, e.g.
  ```toml
  [tool.hatch.build.targets.sdist]
  include = ["src/hilbertplot", "tests", "examples", "README.md", "LICENSE", "pyproject.toml", "CHANGELOG.md"]
  ```
  Re-run `uv build` and re-inspect with `tar tzf` to confirm only these ship.

### MAJOR — placeholder project URLs (`github.com/example/...`)
- **Location:** pyproject.toml:44-46 (`[project.urls]` Homepage/Source =
  `https://github.com/example/hilbertplot`).
- **Evidence:** both URLs use the `example` org, which is a dead placeholder; the README
  install section references only the package name, not a real repo.
- **Why major:** these links render on the PyPI project page as the primary "Homepage"/
  "Source" and would 404. Must be real before a public release.
- **Recommendation:** set the real repository URL and add `Issues` and (if applicable)
  `Documentation`/`Changelog` entries.

### MAJOR — placeholder / inconsistent author and copyright identity
- **Location:** pyproject.toml:10 (`authors = [{ name = "hilbertplot authors" }]`, no email);
  LICENSE:3 (`Copyright (c) 2026 HilbertPlots authors`).
- **Evidence:** author name is a placeholder with no contact; the LICENSE holder is spelled
  `HilbertPlots` while the package/author is `hilbertplot` — an inconsistent identity.
- **Why major:** PyPI shows the author; an anonymous placeholder with no email and a name
  that disagrees with the license holder is not acceptable for a 1.0 and looks abandoned.
- **Recommendation:** use a real author name + email and reconcile the copyright holder
  string in LICENSE with it.

### MAJOR — version is duplicated, not single-sourced
- **Location:** pyproject.toml:7 (`version = "0.1.0"`) **and**
  src/hilbertplot/__init__.py:54 (`__version__ = "0.1.0"`).
- **Evidence:** `grep -n __version__ src/hilbertplot/__init__.py` → line 54; the same literal
  appears independently in pyproject. They agree today but nothing enforces that; the next
  bump will silently drift.
- **Why major:** a mismatch between installed `__version__` and distribution metadata is a
  classic release bug.
- **Recommendation:** single-source it. Either use hatchling's dynamic version
  (`[project] dynamic = ["version"]` + `[tool.hatch.version] path = "src/hilbertplot/__init__.py"`),
  or drop `__version__` and expose it at runtime via
  `importlib.metadata.version("hilbertplot")`.

### MAJOR — no CHANGELOG
- **Location:** project root (`ls CHANGELOG*` → none).
- **Evidence:** no CHANGELOG/HISTORY/NEWS file exists.
- **Why major:** a released package should document what shipped; downstream users and your
  own future releases need it. Not a hard blocker for the very first `0.1.0`, but expected
  before 1.0.
- **Recommendation:** add `CHANGELOG.md` (Keep a Changelog format) with a `0.1.0` entry and
  link it from `[project.urls]`.

### MINOR — no CI configuration
- **Location:** repository root (`ls .github` → not present; no workflow yaml found).
- **Evidence:** `find . -name "*.yml" ...` matched nothing under a `.github`/workflow path.
- **Why minor:** the package builds and tests locally (`uv run pytest`), but there is no
  automated build/test/publish. For a public release you want at least a test matrix and a
  tag-triggered `uv build` + Trusted-Publishing upload.
- **Recommendation:** add `.github/workflows/ci.yml` (pytest on 3.10–3.13) and a
  `release.yml` that builds and publishes on tag via PyPI Trusted Publishing.

### MINOR — deprecated license metadata form / PEP 639
- **Location:** pyproject.toml:9 (`license = { text = "MIT" }`) plus the
  `License :: OSI Approved :: MIT License` classifier (pyproject.toml:22).
- **Evidence:** the table form is the legacy style; current packaging (PEP 639) prefers a
  SPDX string `license = "MIT"` with `license-files = ["LICENSE"]`, and deprecates the
  license *classifier*. `twine check` still passes, so this is polish, not breakage.
- **Recommendation:** move to `license = "MIT"` + `license-files = ["LICENSE"]` and drop the
  license classifier (requires a recent hatchling; verify the build still passes).

### MINOR — no per-minor Python version classifiers
- **Location:** pyproject.toml:19-25 (`classifiers` has only
  `Programming Language :: Python :: 3`).
- **Evidence:** no `Python :: 3.10 … 3.13` entries though `requires-python = ">=3.10"`.
- **Recommendation:** add explicit `3.10`–`3.13` classifiers so the PyPI sidebar advertises
  the supported range (keep them in sync with the CI matrix).

### MINOR — `dev` extra omits the linter it uses
- **Location:** pyproject.toml:38 (`dev = ["matplotlib>=3.5", "pytest>=7.0"]`).
- **Evidence:** a `.ruff_cache/` directory exists at the project root, so ruff is used in
  development, but it is not declared in the `dev` extra.
- **Recommendation:** add `ruff` (and `mypy`, if used) to the `dev` extra so
  `uv pip install -e ".[dev]"` reproduces the dev toolchain.

### NIT — `dev` extra restates the `plot` extra instead of composing it
- **Location:** pyproject.toml:37-38.
- **Evidence:** `dev` hard-codes `matplotlib>=3.5`, duplicating `plot`.
- **Recommendation:** reference the extra: `dev = ["hilbertplot[plot]", "pytest>=7.0", ...]`
  so the matplotlib floor lives in one place.

## Pre-release checklist

Blockers (must fix before any upload):
- [ ] Remove the five copyrighted PDFs from what ships; do not redistribute them.
- [ ] Add `[tool.hatch.build.targets.sdist] include = [...]` and verify `tar tzf` shows only
      `src/hilbertplot`, `tests`, `examples`, `README.md`, `LICENSE`, `pyproject.toml`,
      `CHANGELOG.md`.

Before 1.0:
- [ ] Replace `github.com/example/hilbertplot` URLs with the real repo; add `Issues`.
- [ ] Real author name + email; reconcile LICENSE copyright holder spelling.
- [ ] Single-source the version (dynamic hatchling version or `importlib.metadata`).
- [ ] Add `CHANGELOG.md` with a `0.1.0` entry and link it in `[project.urls]`.
- [ ] Add CI: pytest matrix + tag-triggered build & Trusted-Publishing upload.

Polish:
- [ ] PEP 639 license form; drop the license classifier.
- [ ] Per-minor Python classifiers (3.10–3.13).
- [ ] Add `ruff`/`mypy` to `dev`; compose `dev` from `[plot]`.

Verification commands used:
```
uv build --out-dir <scratch>/distout
unzip -l <scratch>/distout/hilbertplot-0.1.0-py3-none-any.whl
tar tzf  <scratch>/distout/hilbertplot-0.1.0.tar.gz
ls -la   <scratch>/distout            # wheel 38,454 B ; sdist 7,216,560 B
uvx twine check <scratch>/distout/*   # both PASSED
grep -n __version__ src/hilbertplot/__init__.py   # line 54
```
