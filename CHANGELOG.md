# Changelog

All notable changes to **hilbertplot** are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/), and the project aims to adhere to
[Semantic Versioning](https://semver.org/).

Released versions below are generated automatically by python-semantic-release;
new entries are inserted at the marker.

## Local API redesign (unreleased)

- Make array conversion lossless for dtypes, large integers, complex values and
  masks; keep padding masked where NaN would require lossy integer conversion.
- Convert supported square and quasisquare arrays to flat 1-D sequences,
  retaining RGB/RGBA channel order; restore with `to_grid(..., shape=original.shape)`.
  Reject general rectangles and unsupported curve/shape combinations without a
  fallback. Add explicit `from_grid(..., length=...)` prefix handling.
- Run the release build hook after semantic version stamping to regenerate and
  commit `uv.lock` automatically. Verify title-driven patch/minor/breaking releases
  in disposable repositories in CI; versions remain semantic-release-owned.
- Allow `plot_curve(..., shape=(rows, columns))` to draw supported arbitrary
  squares and quasisquares directly as lines. Select a connected quasisquare
  orientation internally. `curves.grid` also accepts the same shape pair.
- Use `hp.data.to_grid` / `from_grid` and `hp.curves.index_to_xy` /
  `xy_to_index` for explicit mapping directions. Remove the former `image`,
  `unroll`, `encode`, and `decode` aliases from these namespaces.
- Keep top-level completion to `plot`, `plot_curve`, `gallery`, `curves`, `data`,
  and `config`. Move metadata/geometry, array operations, and resource controls
  into their respective module namespaces; remove their top-level aliases.
- Add `examples/try_api.py` to exercise the complete function-based interface.
- Add data-first `plot(data, curve=...)` and `plot_curve(curve, order=...)`.
  Each call returns a standard Matplotlib Figure, without opening a window.
- Keep `fourier=False` and `difference=False` as mutually exclusive flags on
  `plot`; difference mode displays the full geometric field instead of a threshold overlay.
- Keep custom classes internal. Remove the `Curve`, `CurveList`, `HilbertPlot`,
  and `hilbert_plot` exports. Curve metadata and groups return plain dicts/lists.
- Expose array, coordinate, and indexing operations as functions; retain the
  numpy-only computational path. See the README migration table for replacements.
- Default new data functions to power-of-two padding; require explicit truncation
  when an order is too small. Reject ambiguous multidimensional/complex input,
  handle masked integer data, and report invalid Fourier inputs without warnings.
- Normalize the memory regression test's RSS units on macOS as well as Linux.

These changes are under local review and have not been released.

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

## v1.0.0 (2026-11-01)

### Features

- Simplify plotting and add lossless curve conversions
  ([`f45f2a6`](https://github.com/El3ssar/hilbertplot/commit/f45f2a6219bfc1f6259d72a64d01c8b19ae7d28e))

### Breaking Changes

- Replace public curve/plot objects and top-level numerical helpers with function-based plotting and
  namespaced to_grid/from_grid/index_to_xy/xy_to_index operations. Data plots default to
  power-of-two padding; difference=True renders the full locality-loss field. General rectangles are
  intentionally unsupported.


## v0.2.0 (2026-07-25)

### Bug Fixes

- Close the gaps found by the second review round
  ([`9df64f4`](https://github.com/El3ssar/hilbertplot/commit/9df64f463b2619d0d19ca7d3d818a16e2c25d7d8))

- Keep the new guards from costing more than they save
  ([`bbaa464`](https://github.com/El3ssar/hilbertplot/commit/bbaa4646af8ca401aa27174277cbae22910cd34f))

### Continuous Integration

- Bump actions, exempt dependabot from title check, curb ruff bumps
  ([`aa74d78`](https://github.com/El3ssar/hilbertplot/commit/aa74d7810fa542e259dfcee77c23ad9aa491374a))

- Stop Dependabot from bumping ruff
  ([`f639fc0`](https://github.com/El3ssar/hilbertplot/commit/f639fc0aa5ab67c615bf31470cfd1bd10f5248b5))

- Stop the floors job re-resolving the pins it exists to test
  ([`106b08f`](https://github.com/El3ssar/hilbertplot/commit/106b08f8bedcf0d6c2c0ff023a60c2ff020265e4))

### Documentation

- Add status badges and tidy the 0.1.0 changelog entry
  ([`7d967ca`](https://github.com/El3ssar/hilbertplot/commit/7d967caae998903d0885a81c4801b50b974aef62))

- Illustrate the README with generated figures
  ([`0f245b9`](https://github.com/El3ssar/hilbertplot/commit/0f245b941fbb933141b10d60ee16157c463b8501))

- Streamline the README to install + two examples
  ([`fb53eab`](https://github.com/El3ssar/hilbertplot/commit/fb53eab38129a8e60c42160d5bfa3959677a37db))

### Features

- Make the arbitrary-square path fast, harden the public surface, add encode/decode
  ([`a6ce0da`](https://github.com/El3ssar/hilbertplot/commit/a6ce0da3463acaacc6c69d349a1ef06804a817f4))


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
