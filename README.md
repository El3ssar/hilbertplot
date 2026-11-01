# hilbertplot

[![PyPI version](https://img.shields.io/pypi/v/hilbertplot.svg)](https://pypi.org/project/hilbertplot/)
[![CI](https://github.com/El3ssar/hilbertplot/actions/workflows/ci.yml/badge.svg)](https://github.com/El3ssar/hilbertplot/actions/workflows/ci.yml)
[![Python versions](https://img.shields.io/pypi/pyversions/hilbertplot.svg)](https://pypi.org/project/hilbertplot/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Plot long numeric sequences on any of **40 two-dimensional Hilbert-type curves**.
Choose a curve by number, label, or paper symbol. The interface is functions returning
ordinary arrays, dictionaries, lists, and Matplotlib figures; custom classes stay internal.

Top-level completion has just six entries: `plot`, `plot_curve`, `gallery`,
`curves`, `data`, and `config`. Specialist functions live under those three namespaces:
`hp.curves` for the catalog and geometry, `hp.data` for arrays, and `hp.config` for
optional cache and allocation controls.

## Install

```bash
pip install "hilbertplot[plot]"   # omit [plot] for numpy-only operations
```

## Plot your data

```python
import numpy as np
import matplotlib.pyplot as plt
import hilbertplot as hp

data = np.sin(np.arange(1000) / 10)
fig = hp.plot(data)                       # standard Hilbert curve
fig = hp.plot(data, curve=12)             # any curve index 0..39
fig = hp.plot(data, curve="Moore")        # or a label; "12H" also works
fig.savefig("data.png", dpi=200)
plt.show()                               # display figures in a script
```

Each call makes **one plot** and returns a Matplotlib `Figure`. No window is opened
implicitly. Use `ax=` to draw on your own Matplotlib axes. Figures remain open until
you close them with `plt.close(fig)`.

## Fourier, difference, and granularity maps

```python
fig = hp.plot(data, fourier=True)          # centred 2-D Fourier magnitude
fig = hp.plot(data, difference=True)       # full locality-loss field
fig = hp.plot(data, granularity=16)        # average consecutive blocks of 16
fig = hp.plot(data, fourier=True, granularity=16, window=True)
```

`fourier` and `difference` are boolean flags, both off by default (`False` / `0`).
They are **mutually exclusive**: setting both raises `ValueError`.

- **Fourier:** transforms the mapped 2-D image, not the original 1-D signal. Defaults
  to `log1p(abs(FFT))` with the mean subtracted. Use `log=False` for raw magnitude,
  `remove_dc=False` to retain the mean, or `window=True` for a Hann window.
- **Difference:** displays the mean absolute visit-index distance to each cell's up-to-eight
  neighbours. It describes the curve's geometry, independently of data values.
- **Granularity:** replaces each consecutive sequence block by copies of its mean.
  The sequence and image retain their sizes; this is not image downsampling. It affects
  the data and its Fourier transform. Geometry-based difference maps stay unchanged.

## Draw a curve

```python
fig = hp.plot_curve(12, order=4)
fig = hp.plot_curve("Moore", order=4, color="steelblue")
fig = hp.plot_curve(0, order=8, mode="fill")

# Arbitrary square and quasisquare: draw the path itself, with no data.
fig = hp.plot_curve(3, shape=(15, 15), mode="line")
fig = hp.plot_curve(3, shape=(15, 16), mode="line")
fig = hp.plot_curve(3, shape=(16, 15), mode="line")
```

`order=k` visits `4**k` cells in a `2**k` square. Curve drawing automatically switches
from coloured lines to a filled visit-order image at order 8. Explicit `mode="line"`
or `"fill"`, `linewidth`, and endpoint markers are also available.

`shape=(rows, columns)` selects explicit dimensions instead of an order. A
quasisquare's sides differ by one. Arbitrary squares and quasisquares require one
of curves **0, 3, 4, 5, 24, 29, 30, 31**. Quasisquare orientation is selected
automatically to keep every step connected. Use either `shape` or `order`, not both.
`hp.curves.grid((rows, columns), curve=...)` returns the same path as coordinates.

## Colour and fitting

```python
from matplotlib.colors import LogNorm

fig = hp.plot(np.arange(1, 1001), norm=LogNorm(), colorbar=True)
fig = hp.plot(data, cmap=["navy", "white", "firebrick"], vmin=-1, vmax=1)
compact = hp.data.to_grid(data, fit="square")      # supported curves only
```

`hp.plot()` and `hp.data.to_grid()` share these layout choices:

| `fit` | Behaviour |
| --- | --- |
| `"pad"` (default) | Smallest enclosing power-of-two square; works with every curve |
| `"square"` | Tight `ceil(sqrt(N))` square; only the eight generalizing curves |
| `"auto"` | Tight square where supported, otherwise power-of-two padding |
| `"truncate"` | Largest power-of-two square inside the data; explicitly discards the tail |

Padding is NaN and appears transparent. `order=` fixes the grid; if it is too small,
the call raises unless you explicitly choose `fit="truncate"`. Pass either `norm=`
or `vmin`/`vmax`, not both. Extra Matplotlib image options such as `alpha` are supported.

## Arrays and index maths (no Matplotlib needed)

```python
img = hp.data.to_grid(data, curve=12)
spectrum = hp.data.fourier(data, curve=12, window=True)
recovered = hp.data.from_grid(img, curve=12, length=len(data))
labels = hp.curves.label_map(12, side=img.shape[0])
differences = hp.curves.difference_map(12, side=img.shape[0])

pts = hp.curves.points(12, order=4)              # (256, 2) array of (x, y) cells
word = hp.curves.word(12, order=4)               # u/d/l/r strokes
arbitrary = hp.curves.grid(100, curve=0)         # arbitrary square, supported curves only
xy = hp.curves.index_to_xy(10**18, 40, curve=12)      # O(order), no full-grid allocation
assert hp.curves.xy_to_index(*xy, 40, curve=12) == 10**18
assert hp.curves.is_space_filling(pts, 16)
key = hp.curves.canonical_form(pts)             # compare paths up to symmetry/reversal
```

Images are indexed `[y, x]`; coordinates are `(x, y)`. Plotting and Fourier maps
accept real, nonempty scalar sequences; choose magnitude, phase, real or imaginary
values explicitly for complex data. Plotting rejects infinities. NaNs propagate
through granularity block means; Fourier maps mean-fill missing cells and require
at least one finite value.

Array conversion is separate from display: `to_grid()` / `from_grid()` preserve
numeric dtypes, complex values, large integers, and masks. With no padding or
averaging, conversion is exact. Default NaN padding keeps floating/complex dtypes;
integer and boolean padding uses a NumPy masked array to retain precision. Use
`fill=0` for ordinary integer padding. `length=` explicitly selects a prefix without
deleting legitimate NaNs or masked values.

```python
# A square RGB image becomes a truly 1-D sequence. Each pixel's channels
# stay consecutive; use the full original shape when reconstructing.
rgb = np.arange(16 * 16 * 3, dtype=np.uint16).reshape(16, 16, 3)
sequence = hp.data.from_grid(rgb, curve=12)
assert sequence.ndim == 1 and sequence.size == rgb.size
restored = hp.data.to_grid(sequence, curve=12, shape=rgb.shape)
np.testing.assert_array_equal(restored, rgb)
assert restored.dtype == rgb.dtype

# The same functions use exact quasisquare paths for supported curves.
square_or_quasisquare = np.arange(15 * 16).reshape(15, 16)
sequence = hp.data.from_grid(square_or_quasisquare, curve=3)
restored = hp.data.to_grid(sequence, curve=3, shape=square_or_quasisquare.shape)
np.testing.assert_array_equal(restored, square_or_quasisquare)
```

Conversion uses the same connected path as `plot_curve(shape=...)`. Spatial
shapes must be supported squares or quasisquares; general rectangles are not
supported. Unsupported shapes raise an error without padding or cropping them
into a different traversal. `shape=` specifies the output's original dimensions;
it cannot be combined with `order=`. Converting a grid with another curve gives a
reversible reordering; keep all entries, including padding, when reversing it.

## Discover curves

```python
info = hp.curves.info(12)                       # ordinary metadata dictionary
print(info["name"], info["index"], info["kernels"])
print([(c["index"], c["name"]) for c in hp.curves.catalog()])
print([c["index"] for c in hp.curves.generalizing()])
fig = hp.gallery(hp.curves.by_kernels(3, 5), order=3)
```

Under `hp.curves`, `catalog()` lists all 40 curves: 6 `proper()`, 6 `improper()` (together 12
`homogeneous()`), and 28 `inhomogeneous()`. Groups return ordinary lists of metadata
dictionaries. `closed()` lists the four loops; `generalizing()` lists curves
0, 3, 4, 5, 24, 29, 30, and 31, which support arbitrary square sizes.

Under `hp.config`, `clear_cache()` releases cached generation data, and `cache_info()`
reports its use.
`cell_limit()` / `set_cell_limit(n)` control the allocation guard. Grid size grows
exponentially with order; the default limit is a ceiling, not a memory reservation.

More runnable examples are in [examples/](examples/). The curve classification follows
Estevez-Rams et al., *Hilbert curves in two dimensions*, Rev. Cub. Fís. **34**, 9 (2017).
The arbitrary-square research is in [research/quasisquares/](research/quasisquares/).

## Try all the features

The [complete runnable example](examples/try_api.py) draws separate figures for the
curve, data, coarse-grained data, Fourier and difference maps, colour options, fitting
modes, and a gallery. It also checks numeric round trips, geometry, indexing and groups.

```bash
python examples/try_api.py
# Save figures and run all checks without opening windows:
MPLBACKEND=Agg python examples/try_api.py --save-only
```

Figures are saved in `examples/output/try_api/`.

## Documentation

The documentation source is in [docs/](docs/), with guides, a generated gallery,
and a complete function reference. See [CONTRIBUTING.md](CONTRIBUTING.md#documentation)
to preview it locally. The GitHub Pages site is prepared for publication at
`https://el3ssar.github.io/hilbertplot/` once Pages is enabled.

## Migrating from 0.2

Version 1.0 replaces the object-based 0.2.0 interface:

| Previous | New |
| --- | --- |
| `hilbert_plot(12, data).draw()` | `plot(data, curve=12)` |
| `curve(12).draw(4)` | `plot_curve(12, order=4)` |
| `plot.save(path)` | `fig = plot(data); fig.savefig(path)` |
| `curve(12).points(4)` | `hp.curves.points(12, order=4)` |
| `curve(12).unroll(img)` | `hp.data.from_grid(img, curve=12)` |
| `curve(12).name` | `hp.curves.info(12)["name"]` |
| `proper().names` | `[c["name"] for c in hp.curves.proper()]` |

The old `Curve`, `CurveList`, `HilbertPlot`, and `hilbert_plot` exports are removed.
`difference=True` now renders the complete difference map. Rendering defaults to
power-of-two padding. See the documentation migration guide for these intentional interface changes.

## License

MIT © Daniel Estevez — [LICENSE](LICENSE).
