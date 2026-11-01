# Sequence mapping

A curve defines an ordered list of grid coordinates. If its $i$th coordinate is
$(x_i,y_i)$ and the sequence is $s$, the mapped array satisfies

$$I[y_i,x_i] = s[i].$$

This operation rearranges values. It does not interpolate between samples.
Successive sequence positions occupy adjacent cells. The converse does not hold:
two spatially adjacent cells can be far apart in sequence order.

## A four-value example

For the standard Hilbert curve at order 1, the path is
`(0,0) → (0,1) → (1,1) → (1,0)`.

```python
import numpy as np
import hilbertplot as hp

values = np.array([10, 20, 30, 40])
grid = hp.data.to_grid(values, curve=0)
assert grid.tolist() == [[10, 40], [20, 30]]
recovered = hp.data.from_grid(grid, curve=0)
np.testing.assert_array_equal(recovered, values)
```

Coordinates are `(x, y)`; NumPy indexing is `[y, x]`. Plots use `origin="lower"`
by default, so row zero appears at the bottom. `origin="upper"` changes display
orientation, not the ordering used in conversion.

## Visit indices versus measurements

These 4 × 4 arrays contain visit indices for Hilbert and Moore at order 2.
For example, cell `(0,0)` has the index printed in the lower-left corner.
The index arrays differ because the curves visit the cells in different orders.

```{raw} html
<div class="plot-pair">
<figure><img src="../_static/generated/labels-hilbert.png" alt="Hilbert visit indices zero to fifteen" width="910" height="954"></figure>
<figure><img src="../_static/generated/labels-moore.png" alt="Moore visit indices zero to fifteen" width="910" height="954"></figure>
</div>
```

```python
points = hp.curves.points(0, order=3)
labels = hp.curves.label_map(0, order=3)
for i, (x, y) in enumerate(points):
    assert labels[y, x] == i
```

Plotting a measurement sequence assigns colors to its values. The path specifies
where those colors appear. Curve choice can therefore change the apparent spatial
pattern without changing the input samples.

## Plotting and conversion have different outputs

`hp.plot()` returns a Matplotlib figure and uses floating-point values for display.
`hp.data.to_grid()` returns the numeric array, retaining dtype and masks when no
averaging is requested. Use conversion functions for exact reconstruction, especially
for large integers, complex data, or multi-channel images.

A non-square sequence needs a fitting policy. The default pads to an enclosing
power-of-two square; values are discarded only when truncation is explicitly allowed.
[Grid fitting](fitting.md) defines the alternatives.
