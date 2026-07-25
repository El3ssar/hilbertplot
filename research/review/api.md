# API Design & Ergonomics — Production-Readiness Audit

**Dimension:** Public API surface (`hilbertplot.__all__` + `Curve` / `HilbertPlot` / `CurveList`).
**Reviewer role:** senior, back every claim with a run or a `file:line`.
**Date:** 2026-07-25

## Verdict

**Readiness 7/10 — strong, ship-worthy shape with two structural gaps to close before 1.0.**

This is an unusually well-designed small API. The newcomer path — *"curve `i`, plot my
data"* — is genuinely one obvious line (`hilbertplot.hilbert_plot(i, data).show()`),
docstrings are thorough and example-driven, infeasible-curve gating is excellent, and the
numpy/matplotlib split is clean. The blockers-to-1.0 are (a) the three public *types*
(`Curve`, `HilbertPlot`, `CurveList`) are not exported, so users cannot `isinstance`/type-hint
against them, and (b) two render methods with identical semantics carry different verbs
(`Curve.plot` vs `HilbertPlot.draw`) and the `.show()` pair disagrees on return type. Nothing
here is a correctness blocker; the findings are ergonomics and consistency polish.

## Strengths (verified)

- **Tight, curated `__all__`** — 12 names, all functions.
  `.venv/bin/python -c "import hilbertplot as h; print([n for n in dir(h) if not n.startswith('_')])"`
  → `['annotations', 'by_kernels', 'catalog', 'closed', 'curve', 'gallery', 'generalizing', 'hilbert_plot', 'homogeneous', 'improper', 'inhomogeneous', 'proper']`.
- **Obvious newcomer path.** `hilbertplot.hilbert_plot(0, range(1024)).show()` and
  `hilbertplot.curve(0).plot_data(data)` are both spelled out; the shortcut and the method agree.
- **Tolerant, delightful lookup.** `curve()` takes index / friendly name / paper symbol,
  case/space/`#`-insensitive (`curve.py:460-505`). `curve("moore")`, `curve("12H")`,
  `curve("liu2+liu4 1")` all resolve.
- **Excellent infeasible-curve gating with actionable messages.** `grid`, `fit='square'`
  and `unroll` all raise `ValueError` naming the failing `n` and pointing at
  `hilbertplot.generalizing()` (`curve.py:214-222`, `hilbert_plot.py:188-193`,
  `curve.py:273-277`). Verified:
  `curve('Moore').grid(10)` → *"Moore does not tile arbitrary squares (it fails at n=7); use points(order)…"*.
- **On-demand rendering.** `HilbertPlot` holds only curve+data and draws nothing until
  asked; colormap/granularity/fit are all render-time, so one object yields every variant
  (`hilbert_plot.py:64-107`). Cheap construction.
- **Clean dependency separation.** `points/word/image/fourier/difference_map/grid/unroll`
  are numpy-only; matplotlib is imported lazily inside render methods, with a friendly
  `ModuleNotFoundError` when absent (`render.py:33-42`).
- **`CurveList` prints as a table** (`curve.py:436-451`) — great discoverability of the 40 curves.
- **`save()` returns its path** on both `Curve` and `HilbertPlot` (`curve.py:401`,
  `hilbert_plot.py:341`) — consistent and chainable.
- **Good `__slots__` + value semantics** on `Curve` (`__eq__`/`__hash__` by index,
  `curve.py:404-408`), so curves are usable as dict keys / set members.

## Findings

### MAJOR-1 — Public types are not exported (`Curve`, `HilbertPlot`, `CurveList`)
**Location:** `src/hilbertplot/__init__.py:56-69`.
**Evidence:**
```
$ .venv/bin/python -c "import hilbertplot as h; print([hasattr(h,n) for n in ('Curve','HilbertPlot','CurveList')])"
[False, False, False]
$ .venv/bin/python -c "import hilbertplot as h; print(type(h.curve(0)).__module__)"
hilbertplot._core.curve
```
Every public factory (`curve`, `catalog`, group filters, `hilbert_plot`) *returns* one of
these three types, yet a user cannot `from hilbertplot import Curve` to write an `isinstance`
check or a type annotation (`def f(c: Curve)`). They are forced to reference a private path
(`hilbertplot._core.curve.Curve`) that the docs explicitly call internal (README:209,
`__init__.py:35`). This also makes the docstring cross-references unresolvable (see MINOR-4).
**Recommendation:** add the three class names to `__all__` and import them in `__init__.py`.
They become documentable, importable, and type-hint-able without exposing any new behaviour.
```python
# __init__.py — before
from ._core.curve import by_kernels, catalog, closed, curve, ...
# after: also surface the types
from ._core.curve import Curve, CurveList, ...
from ._viz.hilbert_plot import HilbertPlot, hilbert_plot
__all__ = ["Curve", "HilbertPlot", "CurveList", "curve", ...]
```
**Backward-compat:** purely additive, non-breaking.

### MAJOR-2 — `Curve.plot` vs `HilbertPlot.draw`: same semantics, different verb
**Location:** `curve.py:342-360` (`Curve.plot`), `hilbert_plot.py:201-288` (`HilbertPlot.draw`).
**Evidence:** both "render onto `ax` (created if `None`) and return the Axes, no window":
```
$ .venv/bin/python -c "... print(type(h.curve(0).plot(2)).__name__, type(h.hilbert_plot(0,range(64)).draw()).__name__)"
Axes Axes
```
The three-verb rendering vocabulary is otherwise beautifully symmetric —
`show` (open a window), `save` (to a file), and a third "just give me the axes". But that
third verb is `plot` on `Curve` and `draw` on `HilbertPlot`. A newcomer who learns
`curve.plot(order, ax=ax)` will reach for `plot.plot(...)` and find nothing.
**Recommendation:** pick one verb for "render to axes, return axes" across both classes.
`draw` is the better choice (`plot` collides conceptually with `plot_data` and with
matplotlib's `Axes.plot`). Rename `Curve.plot` → `Curve.draw`, keeping `plot` as a thin
deprecated alias for one release:
```python
def draw(self, order, ax=None, **style): ...
def plot(self, order, ax=None, **style):   # deprecated alias
    return self.draw(order, ax=ax, **style)
```
**Backward-compat:** renaming is breaking; the alias makes it non-breaking now and removable at 2.0.

### MINOR-3 — `show()` return type disagrees across the two classes
**Location:** `curve.py:362-375` (`Curve.show` → `None`), `hilbert_plot.py:290-308`
(`HilbertPlot.show` → `Axes`).
**Evidence:**
```
$ .venv/bin/python -c "... print(repr(h.curve(0).show(2)), type(h.hilbert_plot(0,range(64)).show()).__name__)"
None Axes
```
Two `show` methods that look parallel return different things; a user who writes
`ax = curve.show(6)` silently gets `None`.
**Recommendation:** make `Curve.show` `return ax` too (it already has the axes in hand at
`curve.py:374`). Aligns the pair and is the more useful contract.
**Backward-compat:** adding a return value where callers expected `None` is non-breaking.

### MINOR-4 — Broken/misleading docstring cross-references
**Location:** `hilbert_plot.py:4, 69, 225`; `render.py:129`.
**Evidence:** `grep -rn "hilbertplot.curve.Curve" src/` → four hits such as
`:meth:`hilbertplot.curve.Curve.plot_data``. But `hilbertplot.curve` is the lookup
*function*, not a module — the class actually lives at `hilbertplot._core.curve.Curve`.
These Sphinx refs resolve to nothing (and mislead readers reading the raw docstring).
**Recommendation:** once MAJOR-1 exports the type, rewrite these as `:meth:`hilbertplot.Curve.plot_data``
(and `:class:`hilbertplot.Curve`` in `render.py:1`). Depends on MAJOR-1.

### MINOR-5 — `curve()` is not idempotent, but `hilbert_plot()` is
**Location:** `curve.py:472-505` vs `hilbert_plot.py:370`.
**Evidence:**
```
$ .venv/bin/python -c "import hilbertplot as h; h.curve(h.curve(0))"
KeyError: 'curve index Hilbert out of range; expected an integer in 0..39'
```
`hilbert_plot(curve, data)` happily accepts an already-built `Curve`
(`c = curve if isinstance(curve, Curve) else _lookup_curve(curve)`), but `curve()` itself
rejects one with a confusing message. A user holding a `Curve` who calls `curve(c)` (a natural
normalise-my-input reflex) hits a wall.
**Recommendation:** short-circuit at the top of `curve()`:
```python
def curve(which):
    if isinstance(which, Curve):
        return which
    ...
```
**Backward-compat:** additive, non-breaking.

### MINOR-6 — `HilbertPlot.data` docstring promises "copy-safe" but returns the writable buffer
**Location:** `hilbert_plot.py:101-104`.
**Evidence:**
```
$ .venv/bin/python -c "
import hilbertplot as h, numpy as np
p = h.hilbert_plot(0, np.arange(16.0)); d = p.data
print(d is p._data, d.flags.writeable); d[0] = 999; print(p.data[0])"
True True
999.0
```
The docstring says *"a copy-safe view of the held values"*, but it hands back the live
internal `ndarray`; mutating it silently corrupts the plot.
**Recommendation:** return a read-only view (`v = self._data.view(); v.flags.writeable = False; return v`),
matching the promise. Cheap and non-breaking for read-only consumers.

### MINOR-7 — Invalid `fit=` value produces a message missing two valid options
**Location:** `hilbert_plot.py:179-198` (`_layout`) → `mapping.py:56` (`resolve_order`).
**Evidence:**
```
$ .venv/bin/python -c "import hilbertplot as h; h.hilbert_plot(0, range(16)).image(fit='bogus')"
ValueError: fit must be 'pad' or 'truncate', got 'bogus'
```
The documented domain is `{"auto","square","pad","truncate"}` (`hilbert_plot.py:120`), but an
unknown value falls through `_layout` and is reported by the deeper `resolve_order`, which only
knows about `pad`/`truncate`. The message misdirects the user.
**Recommendation:** validate `fit` once, up front, in `_layout` (or `image`), listing all four
legal values. Non-breaking.

### MINOR-8 — Curve render kwargs are opaque `**style` (poor discoverability)
**Location:** `curve.py:342` (`plot`), `:362` (`show`), `:377` (`save`).
**Evidence:** `inspect.signature(curve(0).plot)` → `(order: 'int', ax=None, **style)`. The real
knobs (`mode`, `color`, `cmap`, `linewidth`, `endpoints`) are only documented on the *private*
`render.draw` (`render.py:69-80`). Tab-completion and `help(Curve.plot)` reveal nothing; each
of `plot`/`show`/`save` just says "Forwarded to the renderer".
**Recommendation:** enumerate the common kwargs in the `Curve.plot` docstring (the others can
say "see :meth:`draw`"), or promote the frequent ones (`mode`, `color`, `cmap`) to explicit
keyword-only parameters. Docs-only fix is non-breaking; signature change is additive.

### MINOR-9 — `gallery` folds show-or-save into one function (inconsistent with the method split)
**Location:** `render.py:114-172`.
**Evidence:** everywhere else the verbs are separate methods (`show()` vs `save(path)`), but
`gallery(..., save=None)` decides between "open a window" and "save to path" via a keyword
(`render.py:167-171`). It's the odd one out in the vocabulary.
**Recommendation:** acceptable as-is (a single grid function is convenient), but for symmetry
consider `gallery(...)` returning the `Figure` (it already does) and letting the caller
`.savefig`, or documenting the `save=` shortcut as the deliberate exception. Low priority.

### NIT-10 — Non-int/non-str inputs to `curve()` raise `KeyError`, and `bool` resolves as `int`
**Location:** `curve.py:500-505`.
**Evidence:** `curve(3.5)` → `KeyError: 'curve index 3.5 out of range'` (a `TypeError` would be
truer); `curve(True)` → `Moore` (bool is an `int` subclass, index 1). Cosmetic edge cases.
**Recommendation:** optionally `raise TypeError` for non-`int`/non-`str`. Low value.

### NIT-11 — Integer out-of-range raises `KeyError`, not the idiomatic `IndexError`
**Location:** `catalog.py`/`curve.py:505` (`spec_by_index`).
**Evidence:** `curve(40)` → `KeyError: 'curve index 40 out of range…'`. The docstring documents
`KeyError`, so it is consistent, but `KeyError` for an *integer* index reads oddly (Python
convention is `IndexError`). Cosmetic; changing it is technically breaking, so leave unless a
broader exception review happens.

### NIT-12 — `annotations` leaks into `dir(hilbertplot)`
**Location:** `__init__.py:38` (`from __future__ import annotations`).
**Evidence:** it appears in `dir(h)` output above. It is **not** in `__all__`, so
`from hilbertplot import *` does not pull it in — harmless, cosmetic only.

## What I ran

- Introspected the public surface, class modules, and type-export state.
- Exercised error/gating paths: `curve(40|-1|"nope"|3.5|True)`, `word(-1)`, `points(-1)`,
  `grid` on a non-generalizing curve and `grid(0)`, `fit='square'` on Moore, `unroll` on a
  non-square array, `image(fit='bogus')`.
- Compared render-method names and return types across `Curve` and `HilbertPlot`
  (matplotlib `Agg` backend).
- Verified the `HilbertPlot.data` mutation leak and `curve()` non-idempotency.
- `grep`ed docstring cross-references for private-path leaks.
