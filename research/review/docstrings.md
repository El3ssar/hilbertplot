# Production-readiness audit — Docstrings & type hints

Reviewer: senior audit (dimension: docstrings & type hints)
Scope: the public API, i.e. exactly the names in `hilbertplot.__all__`
(`curve`, `catalog`, `homogeneous`, `inhomogeneous`, `proper`, `improper`, `closed`,
`generalizing`, `by_kernels`, `hilbert_plot`, `gallery`) plus the classes reachable from
them (`Curve`, `CurveList`, `HilbertPlot`) and their public methods/properties.

## Verdict

Strong. The docstrings are the best-maintained part of this package: numpy-style throughout,
with Parameters / Returns / Raises / Examples / See Also used consistently and accurately,
and no stale post-rename or post-square-fit references found. Every doctest passes. The
`py.typed` marker is present and correctly declared. One real defect keeps this from being
1.0-clean: a public method's return annotation is an unresolvable forward reference that
crashes runtime type introspection. A handful of minor polish items round it out.

Readiness for this dimension: **8/10**.

## What I ran

```
$ uv run pytest --doctest-modules src/hilbertplot -q
.........................                                                [100%]
25 passed in 0.16s
```

```
$ uvx pyright --pythonpath .venv/bin/python src/hilbertplot
  .../_core/curve.py:316:35 - error: "HilbertPlot" is not defined (reportUndefinedVariable)
  .../_core/curve.py:399:19 - error: Cannot access attribute "savefig" for class "SubFigure"
  .../_core/curve.py:400:24 - error: Argument ... "Figure | SubFigure" ... (reportArgumentType)
  .../_viz/hilbert_plot.py:339:19 - error: Cannot access attribute "savefig" for class "SubFigure"
  .../_viz/hilbert_plot.py:340:24 - error: Argument ... "Figure | SubFigure" ...
  .../_viz/render.py:59:29 - error: Argument of type "NDArray" ... "Sequence[ArrayLike]"
6 errors, 0 warnings
```

```
$ .venv/bin/python -c "import typing; from hilbertplot._core.curve import Curve; \
    print(typing.get_type_hints(Curve.plot_data))"
NameError: name 'HilbertPlot' is not defined

$ .venv/bin/python -c "import hilbertplot; print(hasattr(hilbertplot,'plot_data'))"
False

$ .venv/bin/python  # data-property mutation check
>>> p = hilbertplot.hilbert_plot(0, np.arange(10.0)); d = p.data; d[0] = -999
>>> p.data[0], p.data is p._data
(-999.0, True)
```

## Strengths (verified)

- **py.typed shipped and advertised.** `src/hilbertplot/py.typed` exists; `pyproject.toml`
  carries `Typing :: Typed`. Package data lands in the wheel via the hatchling package config.
- **All 25 doctests pass**, including the non-trivial round-trip example in `Curve.unroll`
  (curve.py:254-258) and the exact curve-word strings in `Curve.word` / the `Curve` class
  example (curve.py:65-68, 150-152).
- **Numpy-style discipline is real, not decorative.** `Raises` is documented wherever the
  code raises (`Curve.grid` curve.py:199-203, `Curve.unroll` curve.py:247-250, `curve`
  curve.py:487-490). `See Also` cross-links `Curve.difference_map` ↔ `HilbertPlot.show`
  (curve.py:300-303).
- **The square-fit feature is documented accurately and currently.** `HilbertPlot.image`'s
  `fit={"auto","square","pad","truncate"}` block (hilbert_plot.py:120-126) matches the
  actual branching in `_layout` (hilbert_plot.py:179-198); the `generalizes`→square logic is
  described correctly. No stale "power-of-four only" wording survives anywhere.
- **Return types on the maths/lookup surface are complete and correct**: every group
  function is `-> CurveList`, `curve(which: int | str) -> Curve`, `Curve.points/grid/
  difference_map -> np.ndarray`, `HilbertPlot.image/fourier -> np.ndarray`, etc.

## Findings

### 1. `Curve.plot_data` return annotation is an unresolvable forward reference — MAJOR
- **Location:** `src/hilbertplot/_core/curve.py:316`
  `def plot_data(self, data) -> "HilbertPlot":  # noqa: F821 (forward ref)`
- **Evidence:** `HilbertPlot` is never imported into module scope (only inside the function
  body at curve.py:337, to dodge a circular import), so the string annotation resolves to
  nothing. Both static and runtime introspection fail:
  - pyright: `curve.py:316:35 - error: "HilbertPlot" is not defined (reportUndefinedVariable)`
  - runtime: `typing.get_type_hints(Curve.plot_data)` raises
    `NameError: name 'HilbertPlot' is not defined`.
- **Impact:** This is a *public* method (it is how the README and the module docstrings tell
  users to build a `HilbertPlot`). The broken hint means IDEs show no return type,
  type-checkers error, and — worst — anything that calls `get_type_hints` on the class
  crashes. That includes Sphinx autodoc with `autodoc_typehints`, pydantic, dataclass-style
  introspection, and doc generators. The `# noqa: F821` comment shows the problem was seen
  and silenced rather than fixed.
- **Recommendation:** Add a typing-only import so the name resolves under `TYPE_CHECKING`
  without a runtime circular import:
  ```python
  from typing import TYPE_CHECKING
  if TYPE_CHECKING:
      from .._viz.hilbert_plot import HilbertPlot
  ```
  Then drop the `# noqa`. With `from __future__ import annotations` already in the file the
  annotation stays a string at runtime, and `get_type_hints`, pyright, and Sphinx all resolve
  it correctly.

### 2. `gallery` — the only public function with no type hints at all — MINOR
- **Location:** `src/hilbertplot/_viz/render.py:114-115`
  `def gallery(curves, order=3, *, ncols=None, save=None, mode="auto", cmap="viridis",
  color=None, title=None, dpi=140):`
- **Evidence:** No parameter annotations and no return annotation, while every other public
  function is fully annotated. The docstring documents `Returns: matplotlib.figure.Figure`
  (render.py:139-141) but the signature does not. Under a strict checker the `None`-defaulted
  params (`ncols`, `save`, `color`, `title`) infer as `None`, so a caller passing
  `ncols=6` / `save="x.png"` would be flagged.
- **Impact:** For a `py.typed` library this is a visible hole in the typed surface; editors
  offer no completion/validation on `gallery`.
- **Recommendation:** Annotate it, e.g.
  `curves: Iterable["Curve"], order: int = 3, *, ncols: int | None = None,
  save: str | None = None, mode: str = "auto", cmap: str = "viridis",
  color: str | None = None, title: str | None = None, dpi: int = 140` and add a
  `-> "Figure"` return (import `Figure` under `TYPE_CHECKING`).

### 3. `HilbertPlot.data` docstring claims "copy-safe" but returns the live array — MINOR
- **Location:** `src/hilbertplot/_viz/hilbert_plot.py:101-104`
  ```python
  @property
  def data(self) -> np.ndarray:
      """The 1-D data vector (a copy-safe view of the held values)."""
      return self._data
  ```
- **Evidence:** It returns `self._data` directly. Verified mutation leaks into internal
  state: after `d = p.data; d[0] = -999`, `p.data[0] == -999.0` and `p.data is p._data`.
- **Impact:** "copy-safe" is factually wrong; a user who trusts the docstring can silently
  corrupt the plot's data.
- **Recommendation:** Either make it true — return a read-only view
  (`v = self._data.view(); v.flags.writeable = False; return v`) or `self._data.copy()` — or
  fix the wording to "the held 1-D data vector (do not mutate)".

### 4. Public matplotlib-returning methods omit their return annotation — MINOR
- **Locations:** `Curve.plot` (curve.py:342), `HilbertPlot.draw` (hilbert_plot.py:201),
  `HilbertPlot.show` (hilbert_plot.py:290).
- **Evidence:** Each docstring documents `Returns: matplotlib.axes.Axes`, but the signatures
  have no `->` annotation (pyright basic mode infers them, so these are not current errors —
  hence MINOR not MAJOR). `Curve.save` and `HilbertPlot.save` by contrast are correctly
  `-> str`.
- **Impact:** Inconsistent typed surface; chained calls like `plot.draw(...).set_xlabel(...)`
  get no editor help. Would become hard errors under `--strict` / `reportUnknownParameterType`.
- **Recommendation:** Add `-> "Axes"` (import `matplotlib.axes.Axes` under `TYPE_CHECKING`)
  to `Curve.plot`, `HilbertPlot.draw`, `HilbertPlot.show`. Optionally annotate the
  matplotlib-typed params (`ax`, `vmin`, `vmax`, `cmap`) at the same time.

### 5. `Curve.plot` `**style` list is incomplete — NIT
- **Location:** curve.py:352-353. The docstring lists `mode, color, cmap, linewidth` but the
  underlying `draw` (render.py:69-80) also accepts `endpoints` and `title`.
- **Recommendation:** Add `endpoints` and `title` to the `**style` description, or say
  "see :func:`hilbertplot._viz.render.draw`".

### 6. `Curve.show` / `Curve.save` say kwargs go "to :meth:`plot`" but they call `draw` — NIT
- **Location:** curve.py:370-371 and 388-389 say `**style ... Forwarded to :meth:`plot``, but
  the bodies call `draw(...)` directly (curve.py:374, 398). The accepted kwargs are identical
  (`plot` is a thin wrapper over `draw`), so behaviour is unaffected.
- **Recommendation:** Harmless; reword to "Forwarded to the renderer" for precision if
  touched.

### 7. Package docstring lists `plot_data` as a top-level entry point — NIT
- **Location:** `src/hilbertplot/__init__.py:21` — "`plot_data` / `hilbert_plot` return a
  `HilbertPlot`".
- **Evidence:** `hasattr(hilbertplot, "plot_data")` is `False`; `plot_data` is a `Curve`
  method, not a package-level function. Reads as if `hilbertplot.plot_data` exists.
- **Recommendation:** Write `Curve.plot_data` / `hilbert_plot`, or drop `plot_data` from the
  top-level blurb.

## Out-of-dimension note (not counted above)

pyright also flags `ax.figure.savefig(...)` / `plt.close(ax.figure)` in `Curve.save`
(curve.py:399-400) and `HilbertPlot.save` (hilbert_plot.py:339-340) because matplotlib types
`Axes.figure` as `Figure | SubFigure` and `SubFigure` has no `savefig`. This is an
implementation-typing nuance (a `# type: ignore` or `assert isinstance(ax.figure, Figure)`
clears it), not a docstring/public-signature issue, so it is recorded for completeness only.
