# hilbertplot

```{raw} html
<section class="landing-hero" aria-labelledby="landing-title">
<div class="landing-intro">
<p class="landing-label">Python library · 40 curve constructions</p>
<h1 id="landing-title">hilbertplot</h1>
<p class="landing-description">Plot one-dimensional data along Hilbert curves. Read images as sequences, and reconstruct them along the same path or a different one.</p>
<div class="landing-actions">
<a class="landing-primary" href="quickstart.html">Start plotting <span aria-hidden="true">→</span></a>
<a class="landing-secondary" href="reference/plotting.html">API reference</a>
<a class="landing-source" href="https://github.com/El3ssar/hilbertplot">GitHub <span aria-hidden="true">↗</span></a>
</div>
<div class="landing-install">
<div class="install-label"><span>Install</span><a href="installation.html">Requirements &amp; setup</a></div>
<div class="install-line"><code id="install-command">pip install hilbertplot</code><button class="install-copy" type="button" aria-label="Copy installation command">Copy</button></div>
</div>
<p class="landing-packages"><span>Python ≥ 3.10</span><span aria-hidden="true">/</span><a href="https://pypi.org/project/hilbertplot/">PyPI</a><span aria-hidden="true">/</span><a href="https://doi.org/10.5281/zenodo.23858267">Zenodo DOI</a></p>
</div>
<figure class="landing-figure">
<div class="poster-label"><span>Hilbert</span><span>Curve 0</span></div>
<img src="_static/hero-curve.svg" width="310" height="310" alt="The standard Hilbert path at order four, with its entry and exit marked">
<figcaption><span>Order 4</span><span>256 cells · one continuous path</span></figcaption>
</figure>
</section>
```

## Start with your data

Choose a curve by its number, label or paper symbol. Plotting returns Matplotlib
figures; conversion returns NumPy arrays.

::::{container} landing-workflows
:::{container} landing-workflow

```{raw} html
<h3 id="plot-a-sequence">Plot a sequence</h3>
```

Successive values fill successive cells along the selected curve.

```python
import numpy as np
import hilbertplot as hp

values = np.sin(np.arange(4096) / 37)
fig = hp.plot(values, curve=0, cmap="cividis")
fig.savefig("sequence.png", dpi=180)
```

[Colors, fitting and saving figures →](quickstart.md)

:::
:::{container} landing-workflow

```{raw} html
<h3 id="read-and-reconstruct-an-image">Read and reconstruct an image</h3>
```

Use the same curve and original shape for an exact round trip.

```python
import numpy as np
import hilbertplot as hp

image = np.arange(256).reshape(16, 16)
sequence = hp.data.from_grid(image, curve=12)
restored = hp.data.to_grid(
    sequence, curve=12, shape=image.shape
)
np.testing.assert_array_equal(restored, image)
```

[Image conversion and reordering →](guides/conversion.md)

:::
::::

## Analysis examples

A curve sets the arrangement. Fourier and granularity operations make different
properties of that arrangement visible. Each example below links to its input,
settings and mathematical definition.

::::{container} landing-analysis
:::{container} landing-example

```{raw} html
<p class="landing-section-label">01 / Fourier transform</p>
```

```{raw} html
<h3 id="the-thuemorse-sequence">The Thue–Morse sequence</h3>
```

The same 1,048,576 binary values appear in both maps. The left map shows their
placement along the Hilbert curve; the right shows the centred 2-D Fourier
magnitude with a Hann window. Its multiscale spectral structure is easier to
identify than in the direct image. This is the spectrum of the **mapped image**,
not the sequence's 1-D spectrum.

```{raw} html
<div class="plot-pair">
<figure><img src="_static/generated/fourier-input.png" width="964" height="1008" alt="One million Thue-Morse terms mapped along the Hilbert curve"><figcaption><span>Input</span>Thue–Morse · 1024 × 1024 cells</figcaption></figure>
<figure><img src="_static/generated/fourier-spectrum.png" width="964" height="1007" alt="Centred 2-D Fourier magnitude showing multiscale structure"><figcaption><span>Fourier</span>Log magnitude · Hann window</figcaption></figure>
</div>
```

[Reproduce the Fourier maps →](guides/fourier.md)

:::
:::{container} landing-example

```{raw} html
<p class="landing-section-label">02 / Granularity</p>
```

```{raw} html
<h3 id="distinguish-periodic-regions">Distinguish periodic regions</h3>
```

This sequence interleaves period-4 and period-6 runs, both with mean 1/2.
Averaging consecutive blocks of four makes aligned period-4 runs uniform grey,
while period-6 runs retain variation. The input length and curve stay the same.

```{raw} html
<div class="plot-pair">
<figure><img src="_static/generated/granularity-input.png" width="737" height="781" alt="Interleaved period-four and period-six runs before averaging"><figcaption><span>Input</span>16,384 samples · granularity 1</figcaption></figure>
<figure><img src="_static/generated/granularity-result.png" width="737" height="781" alt="Uniform period-four regions and varying period-six regions after averaging"><figcaption><span>Block means</span>Same samples · granularity 4</figcaption></figure>
</div>
```

[Reproduce the granularity maps →](guides/granularity.md)

:::
::::

## Explore the documentation

```{raw} html
<nav class="landing-route" aria-label="Documentation guides">
<a class="landing-route-item" href="guides/curves.html"><span class="route-index" aria-hidden="true">01</span><strong>Understand the constructions</strong><span>Kernels, proper and improper curves, homogeneous and mixed assemblies.</span><span class="route-arrow" aria-hidden="true">→</span></a>
<a class="landing-route-item" href="catalog.html"><span class="route-index" aria-hidden="true">02</span><strong>Compare all 40 paths</strong><span>Individual curve drawings with indices, names and kernel types.</span><span class="route-arrow" aria-hidden="true">→</span></a>
<a class="landing-route-item" href="guides/locality.html"><span class="route-index" aria-hidden="true">03</span><strong>Measure spatial locality</strong><span>Difference maps show where neighbouring cells are far apart in sequence order.</span><span class="route-arrow" aria-hidden="true">→</span></a>
<a class="landing-route-item" href="recipes.html"><span class="route-index" aria-hidden="true">04</span><strong>Run the complete example</strong><span>Plotting, conversion, transforms, coordinates and resource controls.</span><span class="route-arrow" aria-hidden="true">→</span></a>
</nav>
```

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
