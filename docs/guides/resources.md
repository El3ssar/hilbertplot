# Memory, caching and large data

## Size grows quickly

An order-$k$ square has $4^k$ cells. Coordinates alone take 16 bytes per cell as two
64-bit integers. These figures exclude the data image, transforms, plotting objects,
caches, and temporary arrays.

| Order | Side | Cells | Coordinate array alone |
| --- | ---: | ---: | ---: |
| 8 | 256 | 65,536 | 1 MiB |
| 10 | 1,024 | 1,048,576 | 16 MiB |
| 12 | 4,096 | 16,777,216 | 256 MiB |
| 14 | 16,384 | 268,435,456 | 4 GiB |

`plot_curve()` automatically changes from line to filled cells at effective order 8.
Forcing millions of line segments can be expensive. Direct single-cell indexing avoids
allocating a complete path, but plotting and array conversion necessarily materialize data.

## The cell limit

A guard rejects accidental oversized materialization. It is a **ceiling per request**, not
a memory reservation or a guarantee of safe total peak memory. Its default is `2**28` cells.

```python
import hilbertplot as hp

previous = hp.config.cell_limit()
try:
    hp.config.set_cell_limit(4**10)
    points = hp.curves.points(0, order=5)
finally:
    hp.config.set_cell_limit(previous)
```

Only raise the limit when you have budgeted the intermediates and outputs. `None` restores
the default. It does not disable the guard. The setting is process-global, so coordinate
changes across threads in applications that share it.

## Inspect and release cached construction data

```python
stats = hp.config.cache_info()
print(stats.hits, stats.misses, stats.currsize)
hp.config.clear_cache()
```

The generation cache memoizes recursive stroke arrays shared across curves. `cache_info()`
returns the standard `functools` cache statistics; its count is entries, not bytes.
`clear_cache()` clears those cached arrays. It does not close figures, free arrays that your
own code still references, or guarantee a decrease in the operating system's RSS metric.

For loops creating figures, save and close each one:

```python
import matplotlib.pyplot as plt

for curve in [0, 1, 12]:
    fig = hp.plot_curve(curve, order=3)
    fig.savefig(f"curve-{curve}.svg")
    plt.close(fig)
```

## Exact conversion versus display

`to_grid()` / `from_grid()` preserve dtype and masks. `plot()` converts real samples to
floating point; color rendering is not an archival encoding of the original values.
Averaging, truncation, Fourier preprocessing and color normalization each have a different
meaning. [Conversion guarantees](conversion.md) · [Transform details](transforms.md)
