# Granularity, Fourier and difference maps

All three are selected through `hp.plot()`. Each call produces one image.
`fourier` and `difference` default to `False` and are mutually exclusive.

```python
hp.plot(values, granularity=16)
hp.plot(values, fourier=True)
hp.plot(values, difference=True)
```

## Granularity: average consecutive blocks

A granularity of $g$ replaces every consecutive block of $g$ values with repeated copies
of its mean. The sequence keeps its original length; a final short block uses its own mean.

```python
hp.data.granulate([0, 2, 10, 14], 2)
# [1, 1, 12, 12]
```

This acts on the 1-D sequence before mapping, not on square blocks of image pixels.
It is an explicit information-losing transform. NaNs or masked values propagate through
block means rather than being silently omitted.

![The mapped signal after averaging consecutive blocks of 16](../_static/generated/granularity.png)

## Fourier: the mapped image's 2-D spectrum

```python
hp.plot(values, fourier=True, cmap="magma")
hp.plot(values, fourier=True, window=True, log=False, remove_dc=False)
spectrum = hp.data.fourier(values, window=True)
```

The steps are:

1. Map the sequence onto the selected curve and grid.
2. Replace NaN cells with the finite mean for the transform.
3. Subtract the image mean unless `remove_dc=False`.
4. Optionally apply a Hann window.
5. Compute the 2-D FFT, centre it, and take its magnitude.
6. Return `log(1 + magnitude)` unless `log=False`.

The result is **magnitude**, not squared power or the original signal's 1-D spectrum.
The visual pattern depends on the chosen curve, grid, padding, and preprocessing.
Rendered Fourier maps use percentile-based colour limits by default; the numerical array
is not clipped to those display limits.

### What the window does

For an $N\times N$ image, $N>1$, the one-dimensional weights are

$$w[k]=\frac12\left(1-\cos\frac{2\pi k}{N-1}\right).$$

The weight for pixel $(x,y)$ is $w[x]w[y]$. With default mean subtraction, the transformed
image is $J[y,x]=(I[y,x]-\bar I)w[y]w[x]$.
For five positions, weights are `[0, 0.5, 1, 0.5, 0]`: borders go to zero and central
values retain most of their weight. This reduces discontinuities between opposite edges,
but changes amplitudes and broadens peaks. `window=False` is the default.

![The centred 2-D Fourier magnitude of the mapped signal](../_static/generated/fourier.png)

## Difference: where spatial neighbours are far apart in sequence order

Let $L[y,x]$ be a cell's visit index. The difference field is

$$D[y,x]=\frac{1}{|\mathcal N|}\sum_{(u,v)\in\mathcal N}|L[y,x]-L[v,u]|,$$

where $\mathcal N$ contains the available up-to-eight neighbouring cells. Boundary cells
have fewer neighbours. The field measures geometry and does not depend on measurement values.
A one-cell grid has difference value zero.

```python
hp.plot(values, curve=12, difference=True)
field = hp.curves.difference_map(12, order=5)
labels = hp.curves.label_map(12, order=5)
```

Large values identify places where cells are close in the plane but far apart along the curve.
The full field is displayed; there is no threshold overlay. Granularity does not change this
geometric field. Combining `fourier=True` and `difference=True` raises an error.

![The full locality-loss field of a Hilbert curve](../_static/generated/difference.png)
