# Production-Readiness Synthesis — `hilbertplot`

**Date:** 2026-07-25
**Inputs:** the seven dimension audits under `research/review/` (api, correctness, docs,
docstrings, hygiene, packaging, performance). Every finding below is de-duplicated and
traceable to at least one of those reports; where dimensions disagreed, the run-backed
verdict wins (noted inline).

---

## Executive verdict

**The engineering is 1.0-caliber; the distribution is not shippable today. Overall readiness: 6.5 / 10.**

The mathematical core is excellent and adversarially verified — all 40 curves space-fill,
all are distinct up to symmetry, the arbitrary-square construction is a valid Hamiltonian
path at every size tried, `grid(2**k)==points(k)` is exact, `unroll` round-trips bit-exact,
and the suite is 217 passing + 25 doctests at 96% line coverage (`correctness.md`). The API
shape, docstrings, and README are all genuinely good (7–8/10 across the board), with every
runnable README snippet executing against the live API. What holds the package back is a
single low-scoring dimension — **packaging (4/10)** — whose two blockers are *cheap to fix
but hard-gating*: the source distribution redistributes **five copyrighted academic PDFs**
(a legal problem) and ships the entire working tree (scratch files, coverage data, internal
review notes) because there is no sdist include-list. Neither touches code. Fix the packaging
gate and the placeholder metadata, and this is a credible `0.1.0`; the remaining work is the
performance cliff on the flagship curve's default path and a short list of API/typing polish
before a `1.0`.

**Score justification:** correctness 9 and the 7–8 cluster would average to ~7.5, but a
public release is *blocked outright* by packaging until the two P0 items are resolved, so the
shippable-today score is **6.5**. It rises to ~8 the moment P0 is closed — the highest
leverage-to-effort ratio in the whole audit.

---

## Prioritized punch-list

### P0 — must fix before *any* public release
1. **Remove the five copyrighted PDFs from what ships** — legal blocker; MIT-licensing third-party papers is not the project's right. *(packaging: BLOCKER; sdist root PDFs, ~7 MB)*
2. **Add `[tool.hatch.build.targets.sdist] include=[...]`** and verify `tar tzf` shows only `src/hilbertplot`, `tests`, `examples`, `README.md`, `LICENSE`, `pyproject.toml`, `CHANGELOG.md`. *(packaging: BLOCKER; no sdist control today, whole tree vacuumed)*
3. **Replace the placeholder `github.com/example/hilbertplot` URLs** with the real repo + add Issues — they 404 as the PyPI Homepage/Source. *(packaging: MAJOR, pyproject.toml:44-46)*
4. **Set a real author name + email and reconcile the LICENSE holder** (`HilbertPlots` vs `hilbertplot`). *(packaging: MAJOR, pyproject.toml:10 / LICENSE:3)*
5. **Fix the aspirational install line** so the README's first copy-paste step actually works (either publish, or lead with the editable/`git+https` install). *(docs: MAJOR, README.md:24-29)*

> Items 1–2 are the hard, non-negotiable blockers (legal + unacceptable artifact). Items 3–5
> are trivial edits but a public upload with dead links, an anonymous author, and a lying
> install command is not a real release — treat them as part of the same gate.

### P1 — before 1.0
6. **Export the three public types** `Curve`, `HilbertPlot`, `CurveList` in `__all__` — users cannot `isinstance`/type-hint against them today. Purely additive. *(api: MAJOR-1; also unblocks docs cross-refs)*
7. **Fix the broken `Curve.plot_data -> "HilbertPlot"` forward ref** via a `TYPE_CHECKING` import — currently `get_type_hints()` *crashes* (breaks Sphinx autodoc/pydantic) and pyright errors. *(docstrings: MAJOR, curve.py:316)*
8. **`HilbertPlot.data` is a "copy-safe" lie** — it returns the live writable buffer; mutating it silently corrupts the plot. Return a read-only view. **[triple-flagged: api MINOR-6, correctness #2, docstrings #3]** *(hilbert_plot.py:101-104)*
9. **Vectorize `grid()`/`_fill` and cache `grid()`/`points()`** — the flagship curve's *default* `fit="auto"` path is pure-Python recursion: 1.6 s vs 47 ms for the same 1M cells, recomputed every render. **[resolved: performance MAJOR x2 + MINOR #3 outrank correctness's "nit" framing — run evidence 1624 ms]** *(hilbert_plot.py:186-195, arbitrary.py:65-100)*
10. **Unify the render-to-axes verb** — `Curve.plot` vs `HilbertPlot.draw` are identical semantics under different names; rename to `draw` with a deprecated `plot` alias. *(api: MAJOR-2)*
11. **Refactor `_core/arbitrary.py`** from research-grade density (22 cryptic names, 11 compound lines, no docstrings/`__all__`) to the rest of the package's style — no behaviour change, tests as the net. *(hygiene: MAJOR)*
12. **Guard `difference_map(0)`** — degenerate 1×1 grid emits a numpy `RuntimeWarning` and returns `nan`; also leaks through `draw(difference=True)`. *(correctness #1, mapping.py:247)*
13. **Wire doctests into CI** (`addopts = "--doctest-modules"`) so the 25 README-facing examples can't drift. *(correctness #3)*
14. **Single-source the version** — `pyproject.toml:7` and `__init__.py:54` both hard-code `0.1.0`; use dynamic hatchling version. *(packaging: MAJOR)*
15. **Add `CHANGELOG.md`** (Keep a Changelog) with a `0.1.0` entry, linked from `[project.urls]`. *(packaging: MAJOR; docs finding 4)*
16. **Add CI** — pytest matrix (3.10–3.13) + tag-triggered build & Trusted-Publishing upload. *(packaging: MINOR)*
17. **Commit a `[tool.ruff]` config and run it in CI** — no committed lint config is why the `arbitrary.py` drift (#11) went unnoticed. *(hygiene #3)*
18. **Align `show()` return types** — `Curve.show -> None` but `HilbertPlot.show -> Axes`; make `Curve.show` return the axes too. *(api: MINOR-3)*
19. **Document `catalog()` / `gallery()` with examples and fix the non-Python "menu" blocks** that raise `SyntaxError` on paste. *(docs #2, #3)*
20. **Annotate `gallery()`** — the only public function with zero type hints, a hole in the `py.typed` surface. *(docstrings #2)*

### P2 — nice-to-have / polish
- **inf-data contract** — decide/sanitize/validate; `fourier()` and vmin/vmax silently degenerate on `±inf`. *(correctness #4)*
- **Close test gaps** — parametrize arbitrary-square `unroll` across all 8 `FEASIBLE` curves; cover the `fourier` NaN-padding branch; smoke-test `show()`/`gallery` on a headless backend. *(correctness #5)*
- **API ergonomics** — make `curve()` idempotent (accept a `Curve`); validate `fit=` once with all four legal values in the message; surface common `**style` kwargs. *(api MINOR-5, MINOR-7, MINOR-8)*
- **Hygiene autofixes** — delete dead `compose_all` + its `Iterable` import; convert `_self_check` bare `assert`s to `raise` (survive `python -O`); `ruff --fix` clears 19 safe modernizations. *(hygiene #2, #4, #5)*
- **Typing/docstring polish** — add `-> Axes` on `draw`/`show`/`plot`; complete the `**style` list; fix the package-docstring `plot_data` blurb; the `savefig`-on-`SubFigure` pyright nuance. *(docstrings #4-7)*
- **Docs polish** — CONTRIBUTING + a lightweight hosted API reference (mkdocstrings/pdoc); match the stale `grid()` comment to the real message; document or underscore `combination`/`rule`; unify the dev-setup uv idiom. *(docs #4-7)*
- **Packaging polish** — PEP 639 license form + drop the license classifier; per-minor Python classifiers; add `ruff` to the `dev` extra; compose `dev` from `[plot]`. *(packaging MINOR/NIT)*
- **Perf polish (high order only, ≥ order 11)** — `codes_to_points` int16 + 1-D cumsum (~3× faster); `difference_map` float32 scratch buffer. Does not bite at the 1M-cell target. *(performance #4, #5)*
- **Input-type cosmetics** — `curve()` raising `KeyError`/accepting `bool` as an index. *(api NIT-10/11, correctness #6)*

---

## Per-dimension scorecard

| Dimension | Score | State | P0 | P1 items owned |
|---|---|---|---|---|
| Correctness, edge cases & tests (adversarial) | **9/10** | Excellent — no correctness blockers | — | #12, #13 |
| Docstrings & type hints | 8/10 | Strong; one crashing forward ref | — | #7, #8*, #20 |
| README & user documentation | 8/10 | Accurate & complete; install line aspirational | #5 | #15*, #19 |
| API design & ergonomics | 7/10 | Well-shaped; two consistency gaps | — | #6, #8*, #10, #18 |
| Code hygiene, structure & style | 7/10 | Textbook layering; one research-grade module | — | #11, #17 |
| Performance & scalability | 7/10 | Pow-2 path great; one scaling cliff | — | #9 |
| **Packaging & release readiness** | **4/10** | **Not shippable — two hard blockers** | #1-#4 | #14, #16 |
| **Overall** | **6.5/10** | Blocked by packaging; ~8 once P0 closes | | |

\* shared/cross-dimension item, listed once under its owning dimension.

---

## What is already strong — do NOT touch

- **The mathematical core.** Curve generation, symmetry, the arbitrary-square (AEP)
  construction, `unroll`, and the `grid(2**k)==points(k)` invariant are all adversarially
  verified correct. No changes needed. *(correctness.md)*
- **The power-of-two performance path.** Fully numpy-vectorized, `lru_cache`d, `bytes.translate`
  for `word()`; 1M cells end-to-end in ~250 ms. The `line→fill` auto-switch at order 8 is the
  right call. Leave it. *(performance.md — only the `grid` recursion needs work)*
- **Docstring discipline.** NumPy-style throughout, Parameters/Returns/Raises/Examples/See-Also
  used accurately, all 25 doctests pass, no stale post-rename/post-square-fit wording. *(docstrings.md)*
- **README accuracy.** Every runnable snippet executes; all counts/shapes/timings/test-counts
  verified exact; the `hilbo→hilbertplot` rename is residue-free. Preserve this with the CI
  doctest gate (#13). *(docs.md)*
- **The wheel.** Minimal, correct, 38 KB, `py.typed` present, LICENSE placed correctly,
  `twine check` passes. Only the *sdist* is broken. *(packaging.md)*
- **Package layering & lazy-import discipline.** `_core`/`_data`/`_viz` with one-directional
  deps, matplotlib imported only inside render functions with a friendly install message,
  numpy-only path genuinely preserved. Keep. *(hygiene.md)*
- **Error messages.** Infeasible-curve gating names the witness size and points at
  `generalizing()`; validation is consistent and actionable across the public surface. *(api.md, correctness.md)*

---

## Suggested release checklist

**Gate for a public `0.1.0` (all P0):**
- [ ] Move the five PDFs out of the tree (git-ignored `papers/`); confirm none ship.
- [ ] Add `[tool.hatch.build.targets.sdist] include=[...]`; `uv build` then `tar tzf` shows only intended files.
- [ ] Real `[project.urls]` (Homepage/Source/Issues); real author name + email; LICENSE holder reconciled.
- [ ] README install line matches reality; `uvx twine check dist/*` passes on both artifacts.

**Before `1.0` (P1 essentials):**
- [ ] Export `Curve`/`HilbertPlot`/`CurveList`; fix `plot_data` forward ref; make `data` read-only.
- [ ] Vectorize + cache `grid()`/`points()`; refactor `arbitrary.py`.
- [ ] Guard `difference_map(0)`; add `--doctest-modules` and a `[tool.ruff]` config to CI.
- [ ] Single-source the version; add `CHANGELOG.md`; add pytest-matrix + release CI.
- [ ] Unify the `draw` verb (+ deprecated `plot` alias); align `show()` returns; annotate `gallery()`; document `catalog()`/`gallery()`.

**Polish pass (P2) as capacity allows** — see list above.

---

## Contradictions resolved
- **`grid()` default performance:** correctness.md rated it a *nit*, performance.md a *MAJOR*.
  Resolved toward MAJOR — the performance measurement (1624 ms vs 47 ms for the flagship
  curve's *default* render at the paper's stated 1M-cell scale) is decisive run evidence. → P1 #9.
- **`HilbertPlot.data` mutability:** flagged independently by api, correctness, and docstrings.
  De-duplicated into a single P1 item (#8).
- **CHANGELOG:** raised by both packaging (MAJOR) and docs (finding 4). Merged into #15.
