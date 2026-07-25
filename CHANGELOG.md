# Changelog

All notable changes to **hilbertplot** are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/), and the project aims to adhere to
[Semantic Versioning](https://semver.org/).

Released versions below are generated automatically by python-semantic-release;
new entries are inserted at the marker.

## Migrating from 0.1.0

`hilbertplot` is on `0.x`, where [semver §4](https://semver.org/#spec-item-4) allows the
interface to change in a minor release. Two spellings changed; both fail loudly rather
than silently, and nothing else in the 0.1.0 surface was removed.

| 0.1.0 | now | why |
| --- | --- | --- |
| `curve.plot(order)` | `curve.draw(order)` | one verb for "render onto axes", shared with `HilbertPlot.draw` |
| `curve.save(order, path)` | `curve.save(path, order)` | matches `HilbertPlot.save(path, ...)`; the old order raises a `TypeError` naming the fix |
| `repr(curve)` → `'Hilbert'` | `repr(curve)` → `'<Curve 0H Hilbert (proper)>'` | `repr` is now unambiguous; `str(curve)` is still `'Hilbert'` |

Behaviour that was buggy and is now stricter: `curve(True)` and `curve(3.0)` raise
`TypeError` instead of silently meaning `curve(1)` / `curve(3)`; an out-of-range index
raises `IndexError` rather than `KeyError` (both are `LookupError`); `plot.data` is
genuinely immutable rather than merely flagged; and `image(order=..., fit=...)` now
validates `fit` instead of ignoring it.

<!-- version list -->

## v0.1.0 (2026-07-25)

First public release — the complete set of 40 two-dimensional Hilbert curves,
with fast numpy generation and data-visualisation tooling.

### Added
- The complete set of **40** two-dimensional Hilbert curves (Estevez-Rams et al., 2017):
  `curve(i)` by index, name or symbol; `points(order)`, `word(order)`; family groups
  `homogeneous` / `inhomogeneous` / `proper` / `improper` / `closed` / `by_kernels`,
  returned as a `CurveList` that prints as a table.
- Fast numpy stroke-code generation (no per-stroke Python loop); order-10 curve (~1M
  points) in tens of milliseconds.
- Curve rendering: `curve.show/save/plot(order)` with automatic line→fill mode by order,
  colour-graded traversal, and `gallery()` for grids of curves.
- **Data visualisation** ("Hilbert plots", Estevez-Rams et al., 2015): `hilbert_plot`
  / `curve.plot_data` return a `HilbertPlot` that maps a 1-D vector onto 2-D on demand,
  with colormap-by-name or colour-list interpolation, the `l`-granularity transform,
  and `pad` / `truncate` fits.
- **Difference map** overlay (`difference=True`, tunable threshold) marking where a curve
  breaks locality (Pérez-Demydenko et al., 2014); `curve.difference_map(order)`.
- **2-D Fourier map** (`fourier=True`; `HilbertPlot.fourier()`) revealing hidden periodic
  and self-similar structure.
- **`unroll`**: read a 2-D square array back into a 1-D vector in curve order.
- **Arbitrary `n x n` squares** for the eight curves that support it
  (`curve.grid(n)`, `curve.generalizes`, `hilbertplot.generalizing()`); the data mapping
  square-fits to a tight `ceil(sqrt(N))` grid by default for those curves. The full
  feasibility classification and impossibility proofs are in `research/quasisquares/`.

### Notes
- Requires Python 3.10+. `numpy` is the only runtime dependency; `matplotlib` is the
  optional `[plot]` extra.
