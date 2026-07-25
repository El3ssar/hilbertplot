# hilbertplot

[![PyPI version](https://img.shields.io/pypi/v/hilbertplot.svg)](https://pypi.org/project/hilbertplot/)
[![CI](https://github.com/El3ssar/hilbertplot/actions/workflows/ci.yml/badge.svg)](https://github.com/El3ssar/hilbertplot/actions/workflows/ci.yml)
[![Python versions](https://img.shields.io/pypi/pyversions/hilbertplot.svg)](https://pypi.org/project/hilbertplot/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

The **complete set of 40 two-dimensional Hilbert curves** — and a fast way to plot long
1-D data on any of them.

Most software knows one Hilbert curve. In fact there are **forty** distinct space-filling
curves of Hilbert type in two dimensions (up to rotation, reflection and reversion), as
proved by Estevez-Rams et al., *"Hilbert curves in two dimensions"*, Rev. Cub. Fís. **34**,
9 (2017). `hilbertplot` implements all forty with pure-numpy generation and uses them to lay
long 1-D vectors onto 2-D images.

## Install

```bash
pip install "hilbertplot[plot]"   # drop [plot] for a numpy-only core (no matplotlib)
```

## Draw a curve

```python
import hilbertplot

c = hilbertplot.curve(0)     # by index 0–39, by name ("Moore"), or by symbol
c.show(6)                    # draw order 6 in a window
pts = c.points(6)            # (4096, 2) integer lattice points, in visit order
```

The forty curves come in named groups — `hilbertplot.proper()`, `.improper()`,
`.homogeneous()`, `.inhomogeneous()`, `.generalizing()` — each of which prints as a table.

## Plot data

Walk a curve and drop `data[i]` on the *i*-th cell it visits: a locality-preserving
1-D → 2-D map where nearby values stay nearby.

```python
import numpy as np, hilbertplot

plot = hilbertplot.hilbert_plot(0, np.arange(10_000))
plot.show("viridis")          # a matplotlib colormap name, or a list of colours to blend
plot.show(granularity=4)      # block-mean coarsening that makes periodic structure pop
```

## More

A `HilbertPlot` (and each `Curve`) can do a bit more:

- `plot.show(difference=True)` — overlay where the curve breaks locality
- `plot.show(fourier=True)` — a 2-D Fourier map that surfaces hidden periodic structure
- `curve.unroll(img)` — read a 2-D array back into 1-D, in curve order
- `curve.grid(n)` — the eight `generalizing()` curves tile **any** `n×n` square, not just `2ᵏ`

Runnable demos for all of these live in [`examples/`](examples/); the arbitrary-square
classification and its proofs are in `research/quasisquares/`.

## License

MIT © Daniel Estevez
