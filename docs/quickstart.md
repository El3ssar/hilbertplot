# Plotting

```python
import numpy as np
import matplotlib.pyplot as plt
import hilbertplot as hp

values = np.sin(np.arange(1000) / 15)
fig = hp.plot(values, curve=12)
plt.show()
```

The curve walks through a square grid. Value `values[i]` goes into the *i*-th visited
cell. A colour represents the value in that cell. Each call makes one plot.

## Choose by number or label

```python
hp.plot(values, curve=0)          # Hilbert, the default
hp.plot(values, curve="Moore")   # a named curve
hp.plot(values, curve="12H")     # a paper symbol
```

Every catalog entry has an index from 0 through 39. You never need to remember a generated label.

## Save the figure

```python
fig = hp.plot(values, curve=12)
fig.savefig("sequence.png", dpi=200)
fig.savefig("sequence.pdf")
plt.close(fig)
```

Drawing does not call `plt.show()` or close your figure. In scripts, call `plt.show()`
after preparing the figures you want. In notebooks, the plotting backend normally displays them.

## Colormaps

```python
hp.plot(values, cmap="viridis")
hp.plot(values, cmap=["navy", "white", "firebrick"], vmin=-1, vmax=1)
```

A colour list defines a smooth gradient: low values use its first colour, middle values
pass through the intermediate colours, and high values use its last colour. It does not
assign colours to categories.

![Sequential, diverging and custom colormaps on the same signed values](_static/generated/colors.png)

## Color normalization

For positive values with a large dynamic range:

```python
from matplotlib.colors import LogNorm

hp.plot(np.exp(values), norm=LogNorm(), colorbar=True)
```

Use either `norm=` or `vmin`/`vmax`. When passing a norm, put limits on the norm itself.

## Use your own axes

```python
fig, ax = plt.subplots()
hp.plot(values, curve=12, ax=ax, title="My sequence")
```

A colourbar is enabled by default. Pass `colorbar=False` to omit it.

## Missing values

NaNs and masked samples are transparent in the data image. Infinities are rejected.
Replace infinities using an explicit policy appropriate to the data before plotting.

![A missing sequence interval displayed as empty cells](_static/generated/missing.png)

## Curve rendering

`hp.plot_curve()` displays a path, rather than measurement values. A solid `color=`
uses one line color; `cmap=` colors visit order. `mode="fill"` colors cells by visit
order. Automatic mode uses lines below order 8 and filled cells at larger orders.

![Line and filled-cell representations of the same curve](_static/generated/modes.png)
