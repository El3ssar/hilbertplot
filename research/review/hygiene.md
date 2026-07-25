# Production-readiness audit — Code hygiene, structure & style

**Scope:** the shipped package `src/hilbertplot/` (13 files, 2326 lines). Research
scripts under `research/` were consulted only to trace usage; they are out of scope.

**Verdict:** *Good, with one clear exception.* The package is cleanly layered
(`_core` / `_data` / `_viz`), heavily and accurately documented (NumPy-style docstrings
with runnable doctests), disciplined about lazy imports, and uses named constants over
magic numbers. `217 passed in 2.07s`, so nothing here is a correctness issue. Two things
hold it back from a polished 1.0: the arbitrary-size module (`_core/arbitrary.py`) was
shipped at research-grade density and departs sharply from the rest of the codebase's
style, and there is no committed linter config to catch that drift. One genuinely dead
function also survives. Readiness: **7/10**.

## Tooling run (paper trail)

`pyflakes` is not installed in `.venv`; `ruff` is available at `/home/elessar/.local/bin/ruff`.

```
$ .venv/bin/python -m py_compile $(find src/hilbertplot -name "*.py")   # COMPILE OK
$ .venv/bin/python -m pyflakes src/hilbertplot                          # No module named pyflakes
$ ruff check src/hilbertplot --select F                                 # 0 findings (no unused imports/names)
$ ruff check src/hilbertplot --select F,E,W,I,C90,PLR,PLW,B,SIM,RUF,UP,ARG --statistics
    56 E501, 22 N803/N806, 11 E701/E702, 7 RUF022, 5 PLR0913, 5 PLR2004, 5 UP037,
    4 I001, 2 PLW2901, 2 SIM114, 2 UP035, 1 B905, 1 E741, 1 UP033, ...
$ ruff check src/hilbertplot --select C901 --config lint.mccabe.max-complexity=8
    1 finding (hilbert_plot.py:201 draw, complexity 9)
$ uv run pytest -q                                                      # 217 passed in 2.07s
```

There is **no** committed lint/format config (`pyproject.toml` has no `[tool.ruff]`), yet a
stray `.ruff_cache/` sits in the repo root — ruff has been run ad hoc but nothing enforces it.

## Strengths

- **Layering is textbook.** `_core` (pure math: catalog → generation → geometry →
  symmetry → arbitrary), `_data/mapping.py` (curve-agnostic data placement), `_viz`
  (matplotlib). Dependencies point one direction; `_core` never imports `_viz`/`_data`
  except via deferred in-method imports.
- **Lazy-import discipline is deliberate and documented.** matplotlib is imported only
  inside render functions (`render.py:35`, `hilbert_plot.py:31,55,251`), with the rationale
  stated in `render.py:1-6` and `pyplot()` (`render.py:33-42`) giving a friendly install
  message. The numpy-only import path is genuinely preserved — verified: no top-level
  matplotlib import anywhere.
- **Magic numbers are named** where it matters: `render.py:27-30`
  (`_AUTO_FILL_ORDER=8`, `_GRADIENT_MAX_ORDER=7`, `_DEFAULT_COLOR`).
- **Error handling is consistent and actionable.** `ValueError` with remediation hints
  (`curve.py:215-219`, `hilbert_plot.py:190-193`, `render.py:99`), `KeyError`/`from None`
  chaining (`curve.py:503`, `catalog.py:311-314`), `TypeError` guard in
  `HilbertPlot.__init__` (`hilbert_plot.py:91`).
- **`catalog.py` is pure declarative data** with an import-time `_self_check()` that
  cross-validates family vs. kernels — a nice guard against transcription typos.
- **No unused imports** anywhere (`ruff --select F` clean).

## Findings

### 1. `_core/arbitrary.py` is research-grade code shipped into the package — MAJOR
**Location:** `src/hilbertplot/_core/arbitrary.py` (whole file, esp. lines 46-90)
**Evidence:** every style violation in the package is concentrated here.
```
$ ruff check src/hilbertplot --select N,E701,E702 --output-format concise
  arbitrary.py: 22 × N803/N806  (A, B, M, Wc, Hc, Wc1, Wc2, Hc1, Hc2, ...)
  arbitrary.py: 11 × E701/E702  (lines 52,53,54,61,73,74,75,76,77,78,86)
  # zero such findings in any other module
```
The file uses one-letter/cryptic names (`Wc`, `Hc`, `mnx`, `mny`, `sw`, `sh`, `revi`,
`axs`, `ays`, `f`, `M`), compound one-line statements (`if (Wc,Hc)==(1,1): return [(0,0)]`
at 52-55; `mnx = ...; mny = ...` at 61; `Wc1 = Wc//2; Wc2 = Wc-Wc1` at 73), has **no
`__all__`**, and its four internal helpers (`_matmul`, `_base_cells`, `_mapper`, `_fill`)
carry **no docstrings** while every other `_core` helper is documented. `_fill` takes 7
positional args (`PLR0913`). This is correct and tested, but it reads nothing like the rest
of the package — a maintainer moving here from `geometry.py`/`generation.py` hits a wall.
**Recommendation:** before 1.0, refactor for readability: descriptive names
(`width_cells`, `height_cells`, `min_x`, `swap_w`, ...), one statement per line, docstrings
on the four helpers explaining the AEP recursion, add `__all__ = ["FEASIBLE", "WITNESS",
"square_points"]`. No behaviour change; keep the tests as the safety net.

### 2. Dead function `compose_all` (and its lone-consumer import) — MINOR
**Location:** `src/hilbertplot/_core/symmetry.py:183-188`; import at `:34`
**Evidence:**
```
$ grep -rn "compose_all" . --include=*.py
  src/hilbertplot/_core/symmetry.py:183:def compose_all(...)   # definition only
```
`compose_all` is defined but referenced **nowhere** — not in the module's `__all__`
(`symmetry.py:36-52`), not in `src/`, `tests/`, or `research/`. It is the only user of
`Iterable` (imported at `symmetry.py:34`), so that import is vestigial too.
**Recommendation:** delete `compose_all` and drop `Iterable` from the import. (`Symmetry.__matmul__`
at `:128` is likewise unreferenced but is a natural operator dunder — reasonable to keep.)

### 3. No committed linter/formatter configuration — MINOR
**Location:** `pyproject.toml` (no `[tool.ruff]`), stray `.ruff_cache/`
**Evidence:** `ruff check src/hilbertplot` reports 102 issues against defaults; nothing in
the repo pins a line-length or select-set, which is precisely why finding #1 drifted in
unnoticed. **Recommendation:** add a `[tool.ruff]` block (line-length matching the code's
actual ~100-col style, and at minimum `select = ["E","F","I","N","UP","B","SIM"]`), run
`ruff check`/`ruff format` in CI. This turns findings #1/#4/#5 into build gates.

### 4. Import-time invariants use bare `assert` (stripped under `python -O`) — MINOR
**Location:** `catalog.py:320-339` (`_self_check`); also `geometry.py:125`, `generation.py`
**Evidence:** `_self_check()` validates the shipped 40-curve table (count, index range,
valid kernels, family/kernel agreement) entirely with `assert`. Under `python -O` these are
compiled out, so a corrupted table would ship silently. **Recommendation:** for
`_self_check` (which guards *shipped data*, not a hot path), convert the asserts to explicit
`raise ValueError(...)`. The per-call asserts in `geometry.canonical_form:125` are fine to
leave.

### 5. Autofixable modernizations & sort order — MINOR (cosmetic, `ruff --fix` clears all)
**Evidence:** `ruff check src/hilbertplot --select I001,UP035,UP037,UP033,RUF022`
- `RUF022` `__all__` not sorted — 7 modules (`__init__.py:56`, `curve.py:16`,
  `catalog.py:42`, `generation.py:28`, `geometry.py:24`, `symmetry.py:36`, `mapping.py:20`).
- `I001` unsorted import blocks — the in-function lazy imports at `curve.py:177`,
  `hilbert_plot.py:16,251`, `geometry.py:18`.
- `UP035` deprecated `typing.Mapping`/`Iterable` → `collections.abc` (`catalog.py:40`,
  `symmetry.py:34`).
- `UP037` quoted annotations no longer needed under `from __future__ import annotations`
  (`curve.py:316`, `symmetry.py:114,128`).
- `UP033` `@lru_cache(maxsize=None)` → `functools.cache` (`generation.py:62`).
**Recommendation:** `ruff check --fix` in one pass; all 19 are safe autofixes.

### 6. Minor readability nits — NIT
- `E741` ambiguous variable `l` in `granulate(data, l)` (`mapping.py:72`). Matches the
  paper's "l-granularity" notation, so defensible; consider `# noqa: E741` to document intent.
- `PLW2901` loop variable `s` rebound inside the loop in `_with_friendly_names`
  (`catalog.py:292,296`) — use a distinct name (`spec`/`named`).
- `SIM114` combinable branches (`arbitrary.py:74,77`), `B905` `zip()` without `strict=`
  (`render.py:159` — intentional: `flat` is longer than `curves`; add `strict=False` to say so).
- `C901` `HilbertPlot.draw` complexity 9 (`hilbert_plot.py:201`) — acceptable for a
  render entry point with many options; reads top-to-bottom. Leave unless it grows.

## Not problems (verified, for the record)
- `word_length`/`clear_cache` (`generation.py`) look unused in `src/` but are exercised by
  `tests/test_words.py:7,27,39,63` — legitimate public surface of the internal module.
- `is_space_filling`, `canonical_form`, `word_to_steps`, `word_to_points`, `apply_morphism`,
  `reverse_word` are all referenced by the test suite — kept as the correctness toolkit.
- The 56 `E501` long lines are unenforced (no configured line-length); the code deliberately
  runs ~100 cols. Fold into finding #3 rather than treating as a defect.
