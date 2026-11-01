# hilbertplot

```{raw} html
<section class="landing-hero" aria-labelledby="landing-title">
<div class="landing-intro">
<p class="landing-label">Python · scientific visualization</p>
<h1 id="landing-title">hilbertplot</h1>
<p class="landing-description">Plot one-dimensional data along Hilbert curves. Convert images to sequences and reconstruct them along a selected path.</p>
<div class="landing-actions">
<a class="landing-primary" href="quickstart.html">Get started</a>
<a class="landing-secondary" href="reference/plotting.html">API reference</a>
<a class="landing-source" href="https://github.com/El3ssar/hilbertplot">GitHub</a>
</div>
<div class="landing-install">
<div class="install-label"><span>Install with pip</span><a href="installation.html">Installation options</a></div>
<div class="install-line"><code id="install-command">pip install hilbertplot</code><button class="install-copy" type="button" aria-label="Copy installation command">Copy</button></div>
</div>
<p class="landing-packages"><a href="https://pypi.org/project/hilbertplot/">PyPI package</a><span aria-hidden="true">·</span><a href="https://doi.org/10.5281/zenodo.23858267">Zenodo DOI</a><span aria-hidden="true">·</span><span>Python ≥ 3.10</span></p>
</div>
<figure class="landing-figure"><img src="_static/hero-curve.svg" alt="Standard Hilbert curve at order four, showing its entry and exit"><figcaption>Curve 0 · order 4 · 256 cells</figcaption></figure>
</section>
<nav class="landing-starts" aria-label="Documentation starting points">
<a href="quickstart.html"><span class="start-category">Plotting</span><strong>Plot your data</strong><span>Select a curve, set colors, and save a figure.</span></a>
<a href="guides/conversion.html"><span class="start-category">Conversion</span><strong>Images and sequences</strong><span>Read an image in curve order and reconstruct it.</span></a>
<a href="guides/curves.html"><span class="start-category">Mathematics</span><strong>Curve constructions</strong><span>Kernels, classifications, and supported shapes.</span></a>
</nav>
```

## Basic usage

```python
import numpy as np
import hilbertplot as hp

values = np.arange(256)
fig = hp.plot(values, curve=0, cmap="cividis")
fig.savefig("hilbertplot.png", dpi=180)
```

Select any of the forty curves by index, label or paper symbol. Plotting returns a
standard Matplotlib figure; array conversion returns NumPy arrays.

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
development
guides/transforms
```
