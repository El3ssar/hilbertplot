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

<p align="center">
  <img src="https://raw.githubusercontent.com/El3ssar/hilbertplot/main/assets/curve.png"
       width="440" alt="The Hilbert curve at order 4, drawn as a colour-graded path">
</p>

## Install

```bash
pip install "hilbertplot[plot]"   # drop [plot] for a numpy-only core (no matplotlib)
```

## Draw a curve

```python
import hilbertplot

c = hilbertplot.curve(0)     # by index 0–39, by name ("Moore"), or by symbol
c.show(4)                    # draw order 4 in a window
pts = c.points(4)            # (256, 2) integer lattice points, in visit order
```

The forty curves come in named groups — `hilbertplot.proper()`, `.improper()`,
`.homogeneous()`, `.inhomogeneous()`, `.generalizing()` — each of which prints as a table.

## Plot data

Walk a curve and drop `data[i]` on the *i*-th cell it visits: a locality-preserving
1-D → 2-D map where nearby values stay nearby.

```python
import numpy as np, hilbertplot

plot = hilbertplot.hilbert_plot(0, np.arange(1, 257))
plot.show("viridis")          # a matplotlib colormap name, or a list of colours to blend
```

![The same data laid on two different curves](https://raw.githubusercontent.com/El3ssar/hilbertplot/main/assets/data_two_curves.png)

*The same numbers on curve 0 and curve 32 — one reason to have all forty.*

## Seeing more than the data

**Coarse-grain it.** `plot.show(granularity=4)` replaces each block of values by its mean.
Below, a binary sequence interleaves stretches of two periodic patterns with identical
density — invisible in the faithful plot, obvious once averaged.

![Periodic regions revealed by coarse-graining](https://raw.githubusercontent.com/El3ssar/hilbertplot/main/assets/granularity.png)

**Find where locality breaks.** `plot.show(difference=True)` marks the cells that are
neighbours in the plane but far apart along the curve. A higher threshold keeps only the
worst offenders.

![The difference map at two thresholds](https://raw.githubusercontent.com/El3ssar/hilbertplot/main/assets/difference.png)

**Transform it.** `plot.show(fourier=True)` renders the 2-D Fourier map, exposing periodic
and self-similar structure — here, a Thue–Morse sequence.

![A Thue–Morse sequence and its Fourier map](https://raw.githubusercontent.com/El3ssar/hilbertplot/main/assets/thue_morse.png)

## Also

- `curve.unroll(img)` — read a 2-D array back into 1-D, in curve order
- `curve.grid(n)` — the eight `generalizing()` curves tile **any** `n×n` square, not just `2ᵏ`

Every figure above is reproducible: `python examples/readme_figures.py`. More runnable
demos are in [`examples/`](examples/); the arbitrary-square classification and its proofs
are in `research/quasisquares/`.

## License

MIT © Daniel Estevez
