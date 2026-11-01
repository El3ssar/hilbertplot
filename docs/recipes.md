# Plotting and conversion recipes

Run examples in order within each page. Every figure is a standard Matplotlib `Figure`.
In scripts, call `plt.show()` to open windows. Save vector graphics with `fig.savefig("plot.svg")`
or raster figures with `fig.savefig("plot.png", dpi=200)`.

```python
import numpy as np
import matplotlib.pyplot as plt
import hilbertplot as hp

t = np.arange(4096)
values = np.sin(2 * np.pi * t / 97) + 0.4 * np.cos(2 * np.pi * t / 31)
```

## Draw data or just the path

```python
fig = hp.plot(values, curve=12)
fig = hp.plot(values, curve="Moore")
fig = hp.plot_curve(0, order=3, mode="line", color="#147d86")
fig = hp.plot_curve(0, shape=(15, 16), mode="line", linewidth=1.5)
```

Use `hp.curves.info(12)` to look up a curve, including one without a memorable label.
No curve object is needed.

## Choose how the sequence fits

```python
short = np.arange(900)
fig = hp.plot(short, fit="pad")       # 32 x 32; 124 padding cells
fig = hp.plot(short, fit="square")    # 30 x 30; curve 0 supports it
fig = hp.plot(short, fit="truncate")  # 16 x 16; keeps only 256 values
```

![The same nine hundred values with pad, square and truncate](_static/generated/fitting.png)

Truncation discards values. Padding preserves them. An explicit `order=5` fixes a 32-square;
excess data raises unless `fit="truncate"`. [Full fitting rules →](guides/fitting.md)

## Control colors

A color list supplies stops in **one continuous gradient**. It does not select several plots
or assign a separate colormap to each curve.

```python
fig = hp.plot(values, cmap="magma")
fig = hp.plot(values, cmap=["#12343f", "#81d8c0", "#fff0b8"])
fig = hp.plot(values, cmap="RdBu_r", vmin=-1.5, vmax=1.5, colorbar=True)
```

![Viridis, magma and a custom continuous color gradient](_static/generated/colors.png)

For positive data spanning orders of magnitude, use a Matplotlib normalization object.
Give limits to the object itself; do not also pass `vmin`/`vmax` to `hp.plot()`.

```python
from matplotlib.colors import LogNorm

positive = np.exp(3 * np.sin(t / 37))
fig = hp.plot(positive, cmap="magma", norm=LogNorm(vmin=0.04, vmax=21))
```

![Linear versus logarithmic normalization of positive data](_static/generated/normalization.png)

Normalization changes colors, not the underlying array returned by `hp.data.to_grid()`.

## Mark missing data

```python
missing = values.copy()
missing[300:700] = np.nan
fig = hp.plot(missing)
```

![Transparent cells for a missing interval in the sequence](_static/generated/missing.png)

Masked samples also become transparent for plotting. For raw conversion, masks and dtypes
are retained. Large integer plotting can lose precision during floating-point conversion;
use the conversion API when exact values matter. Replace infinities explicitly before plotting.

## Average blocks, then choose a transform

```python
coarse = hp.data.granulate(values, 16)
fig = hp.plot(values, granularity=16)
fig = hp.plot(values, fourier=True, window=True, cmap="magma")
spectrum = hp.data.fourier(values, window=True, log=False)
fig = hp.plot(values, difference=True, cmap="magma")
```

`fourier=True` and `difference=True` are incompatible. Granularity can accompany either,
although a difference map ignores sample amplitudes. [Transform definitions →](guides/transforms.md)

## Images to sequences

```python
image = np.arange(16 * 16, dtype=np.uint16).reshape(16, 16)
sequence = hp.data.from_grid(image, curve=12)
restored = hp.data.to_grid(sequence, curve=12, shape=image.shape)
np.testing.assert_array_equal(restored, image)
```

For RGB or RGBA, include the channel axis in the reconstruction shape. The returned
sequence is truly one-dimensional: R, G, B for one visited pixel, then the next pixel.

```python
rgb = np.arange(16 * 16 * 3, dtype=np.uint16).reshape(16, 16, 3)
sequence = hp.data.from_grid(rgb, curve=12)
restored = hp.data.to_grid(sequence, curve=12, shape=rgb.shape)
np.testing.assert_array_equal(restored, rgb)
```

Arbitrary supported sizes work the same way:

```python
image = np.arange(15 * 16).reshape(15, 16)
sequence = hp.data.from_grid(image, curve=0)
restored = hp.data.to_grid(sequence, curve=0, shape=image.shape)
np.testing.assert_array_equal(restored, image)
```

## Keep exact integers and masks

```python
values64 = np.arange(100, dtype=np.uint64) + 2**63
grid = hp.data.to_grid(values64, curve=12)
assert np.ma.isMaskedArray(grid)  # padding masked; uint64 retained
recovered = hp.data.from_grid(grid, curve=12, length=len(values64))
np.testing.assert_array_equal(recovered, values64)
assert recovered.dtype == values64.dtype

ordinary = hp.data.to_grid(values64, curve=12, fill=0)
assert not np.ma.isMaskedArray(ordinary)
```

NaN padding becomes masked padding for integer/bool arrays to avoid lossy float conversion.
`length` counts flattened values, including channels. It never guesses which NaNs or masks
are padding.

## Read with one curve, write with another

```python
original = np.arange(64)
grid = hp.data.to_grid(original, curve=0)
permuted = hp.data.from_grid(grid, curve=12)
back = hp.data.to_grid(permuted, curve=12)
recovered = hp.data.from_grid(back, curve=0)
np.testing.assert_array_equal(recovered, original)
```

Retain every entry, including padding, when inverting a permutation. Another curve can move
padding away from the tail.

## Compose with Matplotlib

Each call still draws one plot. Use ordinary Matplotlib axes to choose your own layout.

```python
fig, axes = plt.subplots(1, 2, figsize=(9, 4))
hp.plot(values, ax=axes[0], title="Measurements", colorbar=False)
hp.plot(values, ax=axes[1], fourier=True, window=True, title="2-D spectrum")
fig.tight_layout()
fig.savefig("comparison.svg")
```

## Inspect a subset of curves

```python
metadata = hp.curves.catalog()
assert len(metadata) == 40
fig = hp.gallery([0, "Moore", 12, 24], order=3)
fig = hp.gallery(hp.curves.generalizing(), order=3)
```

[Geometry, indexing and catalog queries →](guides/geometry.md)
