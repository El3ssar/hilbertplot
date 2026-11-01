# Sequences become pictures. Pictures become sequences.

```{raw} html
<p class="home-lead">Plot a 1-D array along any of forty Hilbert-type curves, or read an image back into a sequence along a chosen path.</p>
```

```python
import numpy as np
import hilbertplot as hp

values = np.sin(np.arange(1024) / 20)
fig = hp.plot(values, curve=12)

image = np.arange(256).reshape(16, 16)
sequence = hp.data.from_grid(image, curve=12)
restored = hp.data.to_grid(sequence, curve=12, shape=image.shape)
```

```{raw} html
<div class="figure-grid">
<figure><img src="_static/generated/curve.png" alt="A continuous Hilbert curve on a 16 by 16 grid, coloured by visit order"><figcaption>Inspect the path itself, with clear entry and exit markers.</figcaption></figure>
<figure><img src="_static/generated/data.png" alt="A numeric sequence placed on a Hilbert grid and coloured by value"><figcaption>Map a long sequence into a spatial pattern without averaging its values.</figcaption></figure>
</div>
```

## Start with one task

- [Plot a sequence](quickstart.md): one call, one figure, with a curve index or label.
- [Read and reconstruct an image](guides/conversion.md): preserve dtype, masks, and colour channels.
- [Choose a curve and shape](guides/curves.md): inspect the catalog, arbitrary squares, and quasisquares.
- [Explore structure](guides/transforms.md): granularity, Fourier maps, and locality-loss fields.
- [Browse examples](gallery.md) or look up a function in the [API reference](reference/plotting.md).

## A small surface

`hp.` exposes six entries: `plot`, `plot_curve`, `gallery`, `curves`, `data`, and `config`.
The three namespaces hold specialist functions. There are no public library-defined classes
to construct or configure. Plotting returns ordinary Matplotlib figures; conversion returns
NumPy arrays or masked arrays.

The numerical core needs only NumPy. Matplotlib is optional until you draw a figure.
Supported spatial shapes are squares and quasisquares. General rectangles are intentionally
outside this version's scope.

```{toctree}
:hidden:
:caption: Get started

installation
quickstart
gallery
```

```{toctree}
:hidden:
:caption: Guides

guides/curves
guides/fitting
guides/conversion
guides/transforms
```

```{toctree}
:hidden:
:caption: Reference

reference/plotting
reference/data
reference/curves
reference/config
migration
development
```
