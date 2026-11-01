# Analysis overview

The three operations answer different questions and have separate chapters.

| Operation | Acts on | Meaning | Chapter |
| --- | --- | --- | --- |
| Granularity | Consecutive sequence blocks | Repeated block means | [Granularity](granularity.md) |
| Fourier | The mapped 2-D image | Centred FFT magnitude | [Fourier maps](fourier.md) |
| Difference | Curve visit indices | Mean distance to spatial neighbours | [Locality](locality.md) |

## Granularity: average consecutive blocks

Use `hp.plot(values, granularity=4)` or obtain values with `hp.data.granulate()`.
[The periodic-region example](granularity.md) explains the choice of block length.

## Fourier: the mapped image's 2-D spectrum

Use `hp.plot(values, fourier=True)` or `hp.data.fourier()`.
[The Thue–Morse example](fourier.md) includes preprocessing, equations and contrast limits.

## Difference: where spatial neighbours are far apart in sequence order

Use `hp.plot(values, difference=True)` or `hp.curves.difference_map()`.
[The locality chapter](locality.md) defines the field and shows comparable color scales.

Each plotting call produces one image. Fourier and difference are mutually exclusive.
