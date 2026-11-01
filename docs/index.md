# hilbertplot

```{raw} html
<p class="project-description">Plot one-dimensional arrays along Hilbert-type curves, and convert images to and from curve-ordered sequences.</p>
<div class="project-meta"><span>40 curve constructions</span><span>NumPy arrays</span><span>Matplotlib figures</span><span>MIT license</span></div>
```

```bash
pip install "hilbertplot[plot]"
```

```python
import numpy as np
import hilbertplot as hp

values = np.arange(256)
fig = hp.plot(values, curve=0, cmap="cividis")
```

## Analysis examples

### Fourier: Thue–Morse sequence

The input contains 1,048,576 binary values arranged on the Hilbert curve.
The corresponding centred 2-D Fourier magnitude shows a multiscale spectral pattern.
This is the spectrum of the **mapped image**, not the sequence's 1-D spectrum.

```{raw} html
<div class="plot-pair">
<figure><img src="_static/generated/fourier-input.png" alt="One million Thue-Morse terms on the Hilbert grid"></figure>
<figure><img src="_static/generated/fourier-spectrum.png" alt="Centred 2-D Fourier magnitude with Hann window"></figure>
</div>
```

[Sequence construction, transform settings and interpretation](guides/fourier.md)

### Granularity: interleaved periodic regions

The sequence alternates between runs of period 4 and period 6, both with mean 1/2.
At granularity 4, period-4 runs become uniform grey; period-6 runs retain variation.
The resulting regions are much easier to distinguish.

```{raw} html
<div class="plot-pair">
<figure><img src="_static/generated/granularity-input.png" alt="Interleaved periodic runs without averaging"></figure>
<figure><img src="_static/generated/granularity-result.png" alt="The same runs with granularity four"></figure>
</div>
```

[Dataset, block means and choice of granularity](guides/granularity.md)

## Operations

| Operation | Function | Result |
| --- | --- | --- |
| Plot a sequence | `hp.plot(values, curve=12)` | Matplotlib figure |
| Draw a curve | `hp.plot_curve(0, order=3)` | Matplotlib figure |
| Arrange values on a grid | `hp.data.to_grid(values, curve=12)` | NumPy array |
| Read an image along a curve | `hp.data.from_grid(image, curve=12)` | Flat NumPy array |
| Inspect a construction | `hp.curves.info(12)` | Metadata dictionary |

Each plotting call produces one plot. Select a curve by index, label, or paper symbol;
no curve object is required. Numeric conversion preserves dtypes and masks. Plotting
converts real samples to floating point.

## Documentation

The [curve classification](guides/curves.md) explains kernels, proper/improper constructions,
and homogeneous/inhomogeneous families. [Sequence mapping](guides/mapping.md) defines the
coordinate and array conventions. The usage chapters cover plotting, fitting and lossless
conversion. The analysis chapters define each transform and give reproducible examples.
The function reference lists parameters, return values and errors.

[GitHub](https://github.com/El3ssar/hilbertplot) ·
[PyPI](https://pypi.org/project/hilbertplot/) ·
[Zenodo DOI](https://doi.org/10.5281/zenodo.23858267)

```{toctree}
:hidden:
:caption: Introduction

installation
guides/curves
guides/mapping
```

```{toctree}
:hidden:
:caption: Usage

quickstart
guides/fitting
guides/conversion
guides/geometry
guides/resources
```

```{toctree}
:hidden:
:caption: Analysis

guides/granularity
guides/fourier
guides/locality
```

```{toctree}
:hidden:
:caption: Examples and catalog

gallery
catalog
recipes
```

```{toctree}
:hidden:
:caption: Function reference

reference/plotting
reference/data
reference/curves
reference/config
```

```{toctree}
:hidden:
:caption: Project

faq
migration
development
guides/transforms
```
