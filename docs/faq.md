# Questions and limits

## Which function do I need?

| Task | Call |
| --- | --- |
| Plot a sequence | `hp.plot(values, curve=12)` |
| Draw the path | `hp.plot_curve(0, order=3)` |
| Draw a non-power-of-two path | `hp.plot_curve(0, shape=(15, 16))` |
| Make a data grid | `hp.data.to_grid(values, curve=12)` |
| Read an image | `hp.data.from_grid(image, curve=12)` |
| Reconstruct it | `hp.data.to_grid(sequence, curve=12, shape=image.shape)` |
| Transform without drawing | `hp.data.fourier(values)` |
| Get curve metadata | `hp.curves.info(12)` |
| Locate one index | `hp.curves.index_to_xy(index, order, curve=12)` |

## Why is nothing showing in my script?

The plotting functions return figures without opening windows. Call `matplotlib.pyplot.show()`
or save with `fig.savefig(...)`. For a machine without a display, set `MPLBACKEND=Agg`.
Notebook display behavior depends on the selected Matplotlib backend.

## Does square fitting discard values?

No. `fit="square"` uses side `ceil(sqrt(N))`, with padding if needed. It requires one of the
eight generalizing curves. `fit="pad"` selects an enclosing power-of-two square.
`fit="truncate"` explicitly allows dropping the tail. [Examples →](guides/fitting.md)

## Can I use a general rectangle?

This version supports squares and quasisquares, whose side lengths differ by one.
General rectangles raise an error. Arbitrary squares/quasisquares require a supporting
curve; all forty curves support power-of-two squares.

## Why did integer padding produce a masked array?

NaN cannot be represented as an integer. Masked padding preserves exact integer values,
including uint64 values above the exact range of float64. Use a representable explicit
`fill=0` if an ordinary integer array is preferable. Keep track of the original length.

## Does from_grid remove NaNs or masks?

No: those may be legitimate input values. Pass `length=original_length` to keep an explicit
number of flattened values. For color images, that number includes channels. Do not trim
padding before inverting a permutation created by using different curves.

## Is the Fourier map the signal's spectrum?

It is the **mapped image's 2-D FFT magnitude**. It is neither the original sequence's 1-D
spectrum nor squared power. Curve choice, fitting, missing-value fill, mean subtraction and
windowing affect it. Windowing changes amplitudes and has no gain correction; a two-cell
Hann axis is all zeros. [Exact steps →](guides/transforms.md)

## Why does the difference map ignore my values?

It measures spatial neighbours' separation in **visit index**. It is a geometric property
of the selected curve and grid, so it remains identical for different measurements on that
grid. Granularity changes measurements, and therefore does not change the difference map.

## Why do some curves look identical at low orders?

Distinct recursive constructions can share a low-order path. Their catalog classification
refers to the construction across orders, not just one tiny picture.

## Are the curves continuous mathematical objects?

The package materializes discrete cell paths at a chosen finite resolution. The catalog
is based on forty Hilbert-type constructions from the cited paper. It does not implement
every possible space-filling curve family.

## Can I use complex values?

Raw array conversion preserves complex dtypes. Plotting and the public Fourier helper require
real scalar sequences. Explicitly select `.real`, `.imag`, `np.abs(...)` or `np.angle(...)`
when that is the quantity you want to display.

## Is there a DOI?

Yes. [10.5281/zenodo.23858267](https://doi.org/10.5281/zenodo.23858267) represents all versions;
[1.0.1 has its own archived record](https://doi.org/10.5281/zenodo.23858268).
New GitHub releases are archived automatically. See `CITATION.cff` in the repository.
