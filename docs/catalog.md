# Curve catalog

Each drawing is the actual order-3 path (64 cells). The circle marks entry and
the square exit. The caption gives the curve index, label, family and distinct
kernel indices. Select a curve using its index, label or paper symbol.

[The construction chapter](guides/curves.md) explains how to read the families:
proper curves use Hilbert kernels, improper curves use Liu4 kernels with reversal,
and inhomogeneous curves mix kernel types within an assembly.

```{raw} html
:file: _static/generated/catalog.inc
```

## Use a selection

```python
import hilbertplot as hp

info = hp.curves.info(12)
assert info["kernels"] == [3, 5]
fig = hp.plot_curve(12, order=3, color="steelblue")
fig = hp.gallery([0, 1, 6, 12], order=3, color="steelblue")
```

`proper()`, `improper()`, `homogeneous()`, `inhomogeneous()`, `closed()` and
`generalizing()` return lists of metadata dictionaries that can be passed directly
to `gallery()`. `by_kernels(3, 5)` selects exactly that kernel set. The full metadata
fields are documented under [catalog queries](guides/geometry.md).
