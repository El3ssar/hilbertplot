# hilbertplot

[![PyPI version](https://img.shields.io/pypi/v/hilbertplot.svg)](https://pypi.org/project/hilbertplot/)
[![CI](https://github.com/El3ssar/hilbertplot/actions/workflows/ci.yml/badge.svg)](https://github.com/El3ssar/hilbertplot/actions/workflows/ci.yml)
[![Python versions](https://img.shields.io/pypi/pyversions/hilbertplot.svg)](https://pypi.org/project/hilbertplot/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

The **complete set of forty two-dimensional Hilbert curves** — and a fast way to plot
long 1-D data on any of them.

Most software knows exactly one Hilbert curve. In fact there are **forty** distinct
space-filling curves of Hilbert type in two dimensions (up to rotation, reflection and
reversion), as proved by

> E. Estevez-Rams, D. Estevez-Moya, Y. Martínez-Camejo, D. Gómez-Gómez and
> B. Aragón-Fernández, *"Hilbert curves in two dimensions"*,
> Revista Cubana de Física **34**, 9 (2017).

| group | count | kernel(s) | members |
|-------|-------|-----------|---------|
| **homogeneous · proper**   | 6  | `Hilbert` | Hilbert, Moore, Liu1–4 |
| **homogeneous · improper** | 6  | `Liu4`    | Improper1–6 |
| **inhomogeneous**          | 28 | mixed     | e.g. `Liu2+Liu4 #1`, `Hilbert+Liu3 #1` |

*Homogeneous* curves build every quadrant from a **single** kernel curve type;
*inhomogeneous* curves mix **two or more** — and each inhomogeneous curve is named for
the recipe it uses.

## Install

```bash
pip install hilbertplot            # core (numpy only)
pip install "hilbertplot[plot]"    # + matplotlib for the plotting / visualisation features
```

or, with [uv](https://docs.astral.sh/uv/):

```bash
uv add "hilbertplot[plot]"
```

Development (editable, with tests):

```bash
git clone https://github.com/El3ssar/hilbertplot
cd hilbertplot
uv venv && uv pip install -e ".[dev]"
uv run pytest
```

## Curves — you think "curve *i* of order *j*"

```python
import hilbertplot

c = hilbertplot.curve(0)          # by index 0–39, name ("Moore"), or symbol ("12H")
c.show(6)                   # draw order 6 in a window
c.save(6, "hilbert.png")    # ...or to a file
c.points(6)                 # (4096, 2) integer lattice points, in visit order
c.word(6)                   # the u/d/l/r stroke string
c                           # repr is just the name:  Hilbert
```

Rendering adapts to the order so it stays fast at every scale (`mode="auto"`): low orders
draw the colour-graded polyline; from order 8 up, where strokes are sub-pixel, it paints a
visit-order **fill heatmap** (a million points in a fraction of a second). Force it with
`mode="line"` / `mode="fill"`, or pass `color="steelblue"` for a solid line.

## Grouping

The group functions return a list that **prints as a table**:

```python
>>> print(hilbertplot.proper())
#  name     kind    closed
-  -------  ------  ------
0  Hilbert  proper
1  Moore    proper  yes
2  Liu1     proper  yes
3  Liu2     proper
4  Liu3     proper
5  Liu4     proper
```

```python
hilbertplot.homogeneous()   hilbertplot.inhomogeneous()    # 12 + 28
hilbertplot.proper()        hilbertplot.improper()         # 6 + 6
hilbertplot.by_kernels(3, 5)                         # the six Liu2+Liu4 curves
hilbertplot.closed()                                 # Moore, Liu1, Improper1, Improper4
hilbertplot.generalizing()                           # the 8 that tile any n×n square
```

Any single curve tells you where it sits:

```python
c = hilbertplot.curve("Liu2+Liu4 #1")
c.kind             # 'inhomogeneous'
c.is_homogeneous   # False
c.kernels          # frozenset({3, 5})
c.is_closed        # False
```

## Visualising data — Hilbert plots

Lay a long 1-D vector onto a 2-D image by walking a curve and dropping `data[i]` on the
`i`-th cell it visits (Estevez-Rams et al., *Comput. Phys. Commun.* **197** (2015) 118).
`plot_data` (or the `hilbert_plot` shortcut) returns a **`HilbertPlot`** that holds the
data and draws *nothing* until you ask:

```python
import numpy as np, hilbertplot

plot = hilbertplot.hilbert_plot(0, values)   # or: hilbertplot.curve(0).plot_data(values)
plot.show("viridis")                   # a matplotlib colormap by name...
plot.show(["red", "green", "tab:blue"])   # ...or colours to interpolate across
plot.save("out.png", "gray")           # straight to a file
img = plot.image()                     # just the 2-D array (for a Fourier map, etc.)
```

Pass a **list of colours** and the library builds a smooth colormap through them and
spreads it over the data's min→max — so `1..100` with `["red","green","tab:blue"]` sweeps
red → green → blue along the curve. A single string is a built-in matplotlib colormap.

**Granularity** (block-mean coarsening that makes periodic structure pop) and the **fit**
(how the grid is sized) are chosen per render, so one `HilbertPlot` gives every view:

```python
plot.show(granularity=4)             # coarsen: blocks of 4 -> their mean
plot.show()                          # fit="auto": tight ceil(√N) square for the 8
                                     #   generalizing curves, else pad to 2^k
plot.show(fit="square")             # force the tight square (generalizing curves only)
plot.show(fit="pad")                 # smallest enclosing 2^k grid, extra cells blank
plot.show(fit="pad", fill=0.0)       # ...pad with a value that won't skew the colours
plot.show(fit="truncate")            # largest 2^k grid that fits inside; drop the tail
plot.show(order=6)                   # force a 2^order grid
```

`fit` answers "what if my data length isn't a power of four?" For the eight
[generalizing curves](#arbitrary-square-sizes) the default is a **tight `⌈√N⌉` square**
(so 10 000 values → `100×100`, not `128×128`); for the other 32 it falls back to **pad**
(smallest enclosing `2^k`) or **truncate**. See `examples/plot_data.py`.

### Arbitrary square sizes

Eight of the forty curves — `hilbertplot.generalizing()` — can be laid on **any** `n×n` square,
not just `2^k` (proved in `research/quasisquares/`; the other 32 are provably obstructed):

```python
hilbertplot.curve(0).grid(100)        # Hilbert on a 100×100 grid -> (10000, 2)
hilbertplot.curve(0).generalizes      # True
hilbertplot.curve(9).grid(100)        # ValueError: Improper4 can't tile arbitrary squares
```

`grid(2**k)` equals `points(k)` exactly, so the two are interchangeable.

### Where locality breaks — the difference map

Toggle a **difference-map** overlay to mark, in colour, where the curve breaks locality —
cells that are neighbours on the plane but far apart along the curve (Pérez-Demydenko et
al., *Appl. Math. Comput.* **234** (2014) 531). The threshold is tunable: **higher marks
fewer, worse sites**, lower marks more.

```python
plot.show()                                   # data only
plot.show(difference=True)                    # + strong-locality barrier
plot.show(difference=True, difference_threshold=0.5)   # mark more of it
plot.show(difference=True, difference_color="red")

hilbertplot.curve(0).difference_map(6)              # the raw field, independent of any data
```

The barrier is the locus of cells above `mean + threshold·std` of the difference field;
there is always one between quadrants 1 and 4.

### Fourier map — hidden patterns

Toggle `fourier=True` to render the **2-D Fourier map** (centred power spectrum) of the
Hilbert plot instead of the data. Periodic and self-similar structure that's invisible in
the raw plot shows up as bright peaks and symmetric patterns (Estevez-Rams et al., 2015):

```python
plot.show(fourier=True)                 # the 2-D Fourier map
plot.show(fourier=True, window=True)    # Hann window first (kills edge artifacts)
spec = plot.fourier()                   # the raw spectrum array

# paper-style side by side
fig, (a, b) = plt.subplots(1, 2)
plot.draw("gray", ax=a); plot.draw("magma", ax=b, fourier=True)
```

A Thue–Morse sequence gives a self-similar 4-fold-symmetric map; a periodic signal buried
in noise (which looks like static as a Hilbert plot) reveals a clean bright cluster.

## Round trip — 2-D back to 1-D

`unroll` reads a square array back into a 1-D vector in curve order — the inverse of the
data mapping, and a locality-preserving way to flatten an image. The side may be any `n`
for a generalizing curve, else a power of two:

```python
img  = hilbertplot.hilbert_plot(3, data).image()   # 1-D -> 2-D
back = hilbertplot.curve(3).unroll(img)            # 2-D -> 1-D   (back == data)
```

## Performance

Producing the **whole** curve at order `n` is `O(4ⁿ)` — the curve *is* `4ⁿ` points. The
generator runs on numpy stroke-code arrays (a morphism is a 4-entry lookup, reversion an
array reversal, quadrant assembly a `concatenate`) with no Python loop over strokes:

| order | points | `points()` | `save()` |
|------:|-------:|-----------:|---------:|
|  8 |     65 536 |  ~4 ms |  ~80 ms |
| 10 |  1 048 576 | ~40 ms | ~180 ms |
| 12 | 16 777 216 | ~0.7 s |  ~2.4 s |

## Design

The public API is small — `curve`, `catalog`, the group filters (`homogeneous`,
`inhomogeneous`, `proper`, `improper`, `closed`, `generalizing`, `by_kernels`), `gallery`
and `hilbert_plot`. `curve(i)` hands you a `Curve`; `plot_data` / `hilbert_plot` hand you a
`HilbertPlot`. Everything else is internal, organised into three subpackages:

```
hilbertplot/
├── _core/     the curve maths (numpy + nothing else)
│   ├── symmetry.py     the square's symmetry group D4, morphisms, reversion
│   ├── catalog.py      the declarative table of all 40 curves (single source of truth)
│   ├── generation.py   the tag-system generator (numpy stroke codes, memoised)
│   ├── geometry.py     codes → points, space-filling validation, canonicalisation
│   ├── arbitrary.py    arbitrary n×n squares (AEP) for the 8 generalizing curves
│   └── curve.py        the Curve object, CurveList, and catalogue lookups
├── _data/     1-D ↔ 2-D mapping, granularity, pad/truncate fitting, difference map
│   └── mapping.py
└── _viz/      matplotlib rendering (imported lazily)
    ├── render.py       curve rendering + gallery
    └── hilbert_plot.py the HilbertPlot object
```

Correctness is enforced by tests that check **all forty** curves are space-filling at
several orders and are **pairwise distinct** under the sixteen-element
symmetry-plus-reversion group — which, by the paper's completeness theorem, means the set
is exactly right. Curve 0 is additionally cross-checked against the standard `d2xy`
algorithm, and the homogeneous curves against Table 3 of the paper.

```bash
uv run pytest                        # 217 tests
uv run pytest --doctest-modules src/hilbertplot   # + the docstring examples
```

## Roadmap

* **done:** 1-D → 2-D on any curve, granularity, `unroll` back to 1-D, difference-map
  overlays, the **2-D Fourier map**, and **arbitrary `n×n` squares for the eight
  generalizing curves** (full classification + impossibility proofs in
  `research/quasisquares/`);
* arbitrary **rectangles** `w×h` (the classification for these is open — next phase);
* faster single-point mapping — `index → (x, y)` in `O(n)` without building the whole curve.

## License

MIT.
