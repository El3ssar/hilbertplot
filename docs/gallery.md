# A visual tour

Every illustration here is generated from the public API during the documentation build.
The deterministic source is [scripts/docs_gallery.py](https://github.com/El3ssar/hilbertplot/blob/main/scripts/docs_gallery.py).
No downloaded datasets are needed. Figures are demonstrations of the mappings, not a
claim that a particular curve is best for your data.

## Begin with a path

Recursion increases the resolution by four cells per previous cell. Order $k$ visits
$4^k$ cells on a $2^k$ by $2^k$ square.

```python
import numpy as np
import hilbertplot as hp

fig = hp.plot_curve(0, order=3)
```

![The Hilbert path at orders one through four](_static/generated/orders.png)

At lower resolutions, a line makes traversal clear. Filled cells make higher orders legible.

```python
fig = hp.plot_curve(0, order=4, mode="fill")
```

![The same order-four curve drawn as a line and filled cells](_static/generated/modes.png)

## Arbitrary squares and quasisquares

Eight curves support these constructions. Quasisquares have side lengths differing by one;
the top-level orientation is selected to maintain connectivity.

```python
fig = hp.plot_curve(0, shape=(15, 16), mode="line")
```

![Connected paths on a ten-square, a fifteen-by-sixteen quasisquare and its transpose](_static/generated/shapes.png)

## One signal, four paths

The input has 4096 samples: a sine with period 97 plus a smaller cosine with period 31.
The four maps use exactly the same values, grid size, and data color range.

```python
t = np.arange(4096)
values = np.sin(2 * np.pi * t / 97) + 0.4 * np.cos(2 * np.pi * t / 31)
fig = hp.plot(values, curve=12)
```

![The first four hundred input samples](_static/generated/signal.png)

![The same signal on curves zero, one, twelve and twenty-four](_static/generated/curves_signal.png)

## Resolve scale with granularity

Block means repeat over the original block, so length and grid size remain fixed.
This is averaging in sequence order, not blurring neighboring image pixels.

![Original signal and its repeated block means](_static/generated/block_means.png)

![Granularity one, four, sixteen and sixty-four on the same grid](_static/generated/granularities.png)

## See frequencies of the mapped image

The Fourier transform acts on the 2-D arrangement. Changing the curve changes that
arrangement and therefore the spectrum. These use mean subtraction, a Hann window, and
log1p magnitude. Each spectrum uses its own default contrast limits.

![Fourier maps for curves zero, one and twelve](_static/generated/spectra.png)

![The Fourier map without and with a Hann window](_static/generated/windows.png)

[Read the equations and caveats →](guides/transforms.md)

## Inspect locality

Difference maps depend on curve geometry, not signal amplitudes. Here all four use the
same fixed color range (0 to 4095); visually similar colors therefore indicate similar
mean index distances. A common broad range makes many low distances appear dark.

![Four difference maps on a shared color scale](_static/generated/locality.png)

## Preserve images, or deliberately rearrange them

Reading an RGB image along curve 0 and writing with curve 0 recovers it exactly.
Writing that same sequence with curve 12 creates a different arrangement of the same pixels.

![Original RGB image, exact reconstruction and an alternative curve arrangement](_static/generated/rgb_roundtrip.png)

![The initial values of the flattened RGB sequence](_static/generated/rgb_sequence.png)

[Try the conversion recipes →](recipes.md#images-to-sequences)

## All forty constructions

The six proper curves use Hilbert kernels; the six improper curves use Liu4 kernels.
The remaining twenty-eight combine kernels. The names and paper symbols refer to the
catalog used by the library, not every possible Hilbert-like construction.

```python
fig = hp.gallery(order=3, ncols=5)
```

[![All forty curves at order three, labeled by index and name](_static/generated/catalog.png)](_static/generated/catalog.png)

### Proper homogeneous curves

```python
fig = hp.gallery(hp.curves.proper(), order=3, ncols=3)
```

![The six proper homogeneous curves](_static/generated/proper.png)

### Improper homogeneous curves

```python
fig = hp.gallery(hp.curves.improper(), order=3, ncols=3)
```

![The six improper homogeneous curves](_static/generated/improper.png)

### Curves supporting arbitrary sizes

```python
fig = hp.gallery(hp.curves.generalizing(), order=3, ncols=4)
```

![The eight curves supporting arbitrary square and quasisquare shapes](_static/generated/generalizing.png)
