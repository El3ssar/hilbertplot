# Production-readiness audit — README & user documentation

**Dimension:** README & user documentation
**Reviewer:** senior docs audit
**Date:** 2026-07-25
**Scope:** `README.md` end-to-end, cross-checked against the live `hilbertplot` API, plus
`examples/*.py`, the package docstring, install instructions, and feature coverage.

## Verdict

**Readiness: 8/10 — in good shape.** The README is accurate, well-organised, and complete:
**every runnable code snippet executes against the real API**, all counts/shapes/timings I
checked match, the `hilbo → hilbertplot` rename is clean (zero residue), and all four
`examples/` scripts run. The doctest suite (`--doctest-modules`) passes (25) and the
advertised "217 tests" figure is exact. A newcomer can get productive fast from this README
alone.

The gaps are narrow: the **PyPI install line is aspirational** (package is unpublished and
the project URLs are placeholders), two public API names (`catalog`, `gallery`) are named
but never shown, and a couple of "menu" blocks are not valid Python. None are blockers.

## What I ran (paper trail)

All commands run from `/home/elessar/Projects/HilbertPlots` with `.venv/bin/python`
(matplotlib present; `MPLBACKEND=Agg` for headless rendering).

- **Public API surface** — `dir(Curve)`, `dir(HilbertPlot)`, `inspect.signature` on every
  public callable. Confirms every method/attribute/kwarg used in the README exists.
- **Curves section** (README 40–49): `curve(0)`, `curve("Moore")`, `curve("12H")`,
  `.symbol` (`'0H'`), `.points(6).shape == (4096,2)`, `.word(6)`, `repr` → `Hilbert`. All OK.
- **Grouping** (57–88): `proper()`=6, `homogeneous()`=12, `inhomogeneous()`=28,
  `improper()`=6, `by_kernels(3,5)`=6, `closed()`=`['Moore','Liu1','Improper1','Improper4']`,
  `generalizing()`=8. `curve("Liu2+Liu4 #1")` → `.kind`, `.is_homogeneous`, `.kernels`
  (`frozenset({3,5})`), `.is_closed`. All OK.
- **Data plots** (90–128): `hilbert_plot(0,values)`, `.image()`, `.fourier()`, `.data`,
  `.curve`; and every `.save(...)` kwarg — `granularity=4`, `fit="square"/"pad"/"truncate"`,
  `fill=0.0`, `order=6`, `difference=True` (+`difference_threshold`, `difference_color`),
  `fourier=True` (+`window=True`), and the two-panel `plot.draw("gray",ax=a);
  plot.draw("magma",ax=b,fourier=True)`. All render without error.
- **fit=auto defaults** (116–128): generalizing curve, 10 000 values → `(100,100)`;
  non-generalizing curve (Improper4), 10 000 values → `(128,128)`. Matches the README's
  "100×100, not 128×128" and "pad to 2^k" claims exactly.
- **Arbitrary squares** (130–141): `curve(0).grid(100).shape == (10000,2)`,
  `curve(0).generalizes is True`, `grid(8) == points(3)` element-for-element,
  `curve(9).grid(100)` raises `ValueError` (Improper4 not generalizing).
- **Difference map** (143–160): `curve(0).difference_map(6).shape == (64,64)`; overlay kwargs OK.
- **Unroll** (181–190): `curve(3).unroll(hilbert_plot(3,data).image())` round-trips equal to
  the input. OK.
- **Curve rendering** (38–54): `curve.save(6,...)`, `mode="line"` + `color="steelblue"`,
  `mode="fill"`. All OK.
- **Performance table** (198–202): `points(8)=4.1 ms` (README ~4 ms), `points(10)=42.2 ms`
  (~40 ms), `points(12)=668 ms` (~0.7 s). Accurate.
- **Examples**: `examples/groups.py`, `examples/show_curve.py Moore 4 --save …`,
  `examples/plot_catalog.py`, `examples/plot_data.py` — all run and write output.
- **Tests / doctests**: `pytest --co` → "217 tests collected"; `pytest --doctest-modules
  src/hilbertplot` → "25 passed".
- **Rename residue**: `grep -rn 'hilbo'` (excluding "hilbert") over README/examples/src →
  no matches.

## Strengths

- Snippet-level accuracy is excellent — I could not find a single runnable README example
  that fails. This is rare and worth preserving with a doctest/CI gate.
- Feature coverage is complete: curves, symbol/name/index lookup, all six group filters,
  Hilbert plots, granularity, the four `fit` modes, `grid`/generalizing, difference map,
  2-D Fourier map, `unroll`, performance, and an architecture map are all documented.
- Numeric claims (counts, image shapes, timings, test count) are all verifiable and correct.
- Good onboarding arc: "you think 'curve i of order j'" framing, then grouping, then data,
  each with copy-paste snippets.

## Findings

### 1. [MAJOR] Install section is aspirational — package unpublished, URLs are placeholders
- **Location:** `README.md:24–29`; `pyproject.toml:37–38`.
- **Evidence:** README's first actionable block is
  `uv pip install hilbertplot` / `uv pip install "hilbertplot[plot]"`. The package is not on
  PyPI, and `pyproject.toml` declares `Homepage`/`Source = "https://github.com/example/hilbertplot"`
  — a placeholder. A newcomer's very first copy-paste step cannot succeed, and the repo/source
  links are dead.
- **Recommendation:** Before any release, either (a) publish to PyPI and set real project
  URLs, or (b) replace the PyPI lines with a from-source/`git+https://…` install and fix the
  `[project.urls]` to the real repository. Until then, lead with the working
  `uv pip install -e ".[plot]"` (or `[dev]`) path.

### 2. [MINOR] `catalog()` and `gallery()` are public API but never shown
- **Location:** `README.md:206–207` (named in the Design prose only); `__init__.py:56–69`
  (both in `__all__`).
- **Evidence:** `catalog()` returns a 40-element `CurveList`; `gallery(...)` renders a grid.
  Neither has a usage example anywhere in the README — a reader cannot tell what they return
  or how to call them. (`gallery` is exercised in `examples/plot_catalog.py`, but the README
  never points there for it.)
- **Recommendation:** Add one-line examples, e.g. `print(hilbertplot.catalog())` in Grouping,
  and a `hilbertplot.gallery(hilbertplot.proper())` snippet (or a link to
  `examples/plot_catalog.py`) near the rendering discussion.

### 3. [MINOR] "Menu" blocks are not valid Python (copy-paste fails)
- **Location:** `README.md:72–78`.
- **Evidence:** Lines like
  `hilbertplot.homogeneous()   hilbertplot.inhomogeneous()    # 12 + 28` place two calls on
  one line inside a ```python fence; pasting the block raises `SyntaxError`. It reads as a
  catalogue of available calls, but it's fenced as runnable code.
- **Recommendation:** Split onto separate lines, or move the counts into trailing comments per
  call, so the fenced block is executable as-is.

### 4. [MINOR] No CONTRIBUTING / CHANGELOG, and no rendered API reference
- **Location:** repo root (`ls CHANGELOG* CONTRIBUTING* docs/` → none).
- **Evidence:** For a library heading toward 1.0 with a moderately rich surface (Curve +
  HilbertPlot, ~a dozen kwargs), there is no versioned changelog, no contributor guide, and
  no hosted API reference. The README is thorough enough that this is not urgent.
- **Recommendation:** Add a short CHANGELOG (the package already sets `__version__`), and
  consider a lightweight docs site (mkdocstrings/pdoc over the existing NumPy-style
  docstrings) before 1.0. Not needed for an alpha release.

### 5. [NIT] Stale ValueError text in the `grid()` comment
- **Location:** `README.md:138`.
- **Evidence:** README comment: `# ValueError: Improper4 can't tile arbitrary squares`.
  Actual message: `Improper4 does not tile arbitrary squares (it fails at n=5); use
  points(order) for a 2**order grid, or pick a curve from hilbertplot.generalizing().`
- **Recommendation:** Match the comment to the real message (or trim it), so it doesn't read
  as drift.

### 6. [NIT] Public `Curve` attributes `combination` and `rule` are undocumented
- **Location:** `dir(Curve)` exposes `combination`, `rule`; not mentioned in README.
- **Evidence:** They appear alongside documented attributes (`kind`, `kernels`, …) but have
  no README coverage; a reader introspecting a `Curve` will hit them with no explanation.
- **Recommendation:** Either document them in the "Any single curve tells you where it sits"
  block or, if internal, prefix with `_`. Low priority.

### 7. [NIT] Dev-setup mixes `uv pip install -e` with `uv run pytest`
- **Location:** `README.md:31–36`.
- **Evidence:** `uv venv && uv pip install -e ".[dev]"` then `uv run pytest`. This works
  (verified indirectly — the editable install is what the venv already has), but `uv pip`
  (manual venv) and `uv run` (project-managed env) are two different uv workflows and can
  confuse newcomers about which environment is active.
- **Recommendation:** Pick one idiom — e.g. `uv sync --extra dev && uv run pytest` — or add a
  one-line note that both use the project venv.

## Bottom line

The documentation is production-quality on accuracy and coverage; the only release-gating item
is the **unpublished-package install line + placeholder URLs** (finding 1). Fix that and the
two MINOR polish items, and the README is 1.0-ready without a separate docs site.
