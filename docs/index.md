# hilbertplot

```{raw} html
<section class="home-hero">
  <div class="hero-copy">
    <p class="eyebrow">HILBERTPLOT · PYTHON / NUMPY / MATPLOTLIB</p>
    <h1>Follow the curve.<br><em>Find the structure.</em></h1>
    <p class="home-lead">A different way to see a long sequence. Arrange your data along a Hilbert curve, explore its patterns, and read images back into sequences.</p>
    <div class="hero-actions"><a class="primary-action" href="quickstart.html">Start plotting <span aria-hidden="true">↗</span></a><a class="secondary-action" href="gallery.html">Explore the gallery →</a></div>
    <code class="install-command">pip install "hilbertplot[plot]"</code>
  </div>
  <figure class="hero-art"><img src="_static/generated/hero.svg" alt="The actual standard Hilbert curve at order four, colored along its continuous path"><figcaption>CURVE 0 / ORDER 4 / 256 CELLS</figcaption></figure>
</section>
<div class="fact-strip"><span><strong>40</strong> Hilbert-type curves</span><span><strong>8</strong> arbitrary-size constructions</span><span><strong>2</strong> directions: sequence ↔ grid</span></div>
```

## Your sequence, a new perspective

Each value becomes one cell. The selected curve determines which cells follow each other.
Color carries the measurement; the path provides a spatial arrangement.

```python
import numpy as np
import hilbertplot as hp

values = np.sin(np.arange(4096) / 20)
fig = hp.plot(values, curve=0)
fig.savefig("my-sequence.png", dpi=180)
```

```{raw} html
<div class="figure-grid">
<figure><img src="_static/generated/data.png" alt="A periodic sequence mapped to the standard Hilbert curve"><figcaption>One sequence, arranged along Hilbert.</figcaption></figure>
<figure><img src="_static/generated/moore.png" alt="The identical sequence mapped to Moore with the same color scale"><figcaption>The same values, following Moore.</figcaption></figure>
</div>
```

Choose a curve by **index**, **label**, or **paper symbol**. Use a power-of-two square with
any curve, or an arbitrary square/quasisquare with a supporting construction.
[Meet the curves →](guides/curves.md)

## Go from an image to a sequence. And back.

Conversion rearranges values without color normalization. Keep the same shape and curve
to recover the original array, including its dtype, masks, and color channels.

```python
image = np.arange(32 * 32 * 3, dtype=np.uint16).reshape(32, 32, 3)
sequence = hp.data.from_grid(image, curve=12)
restored = hp.data.to_grid(sequence, curve=12, shape=image.shape)
np.testing.assert_array_equal(restored, image)
```

![RGB image, exact reconstruction, and a deliberate reordering using a different curve](_static/generated/rgb_roundtrip.png)

Read with one curve and write with another to experiment with permutations.
[Understand the round trip →](guides/conversion.md)

## Look at different kinds of structure

Average consecutive blocks to inspect coarser structure, transform the mapped image into
its 2-D Fourier spectrum, or examine where a curve loses locality. Each `hp.plot()` call
makes one figure.

```{raw} html
<div class="feature-triptych">
<figure><img src="_static/generated/granularity.png" alt="Sequence blocks of sixteen replaced by their means"><figcaption><strong>Granularity</strong><br>Coarsen the sequence, keeping its length.</figcaption></figure>
<figure><img src="_static/generated/fourier.png" alt="The centered two-dimensional Fourier magnitude"><figcaption><strong>Fourier</strong><br>Inspect frequencies of the mapped image.</figcaption></figure>
<figure><img src="_static/generated/difference.png" alt="Mean index distance to eight neighboring cells"><figcaption><strong>Difference maps</strong><br>Explore the geometry of locality.</figcaption></figure>
</div>
```

[Explore the transforms →](guides/transforms.md) · [See every recipe →](recipes.md)

## Small interface. Full control.

`hp.` exposes `plot`, `plot_curve`, `gallery`, `curves`, `data`, and `config`.
Plots return ordinary Matplotlib figures. Data operations return NumPy arrays or masked
arrays. Metadata comes back as dictionaries and lists; no custom classes to configure.
The numerical core needs only NumPy. Install Matplotlib when you want to draw.

```{raw} html
<div class="next-steps"><a href="reference/plotting.html"><strong>Function reference ↗</strong><span>Every parameter, return value, and important edge case.</span></a><a href="installation.html"><strong>Install &amp; run ↗</strong><span>From a clean environment to your first saved figure.</span></a></div>
```

MIT licensed. [Source on GitHub](https://github.com/El3ssar/hilbertplot) ·
[Releases on PyPI](https://pypi.org/project/hilbertplot/) ·
[Cite with Zenodo](https://doi.org/10.5281/zenodo.23858267).

```{toctree}
:hidden:
:caption: Get started

installation
quickstart
gallery
recipes
```

```{toctree}
:hidden:
:caption: Guides

guides/curves
guides/fitting
guides/conversion
guides/transforms
guides/geometry
guides/resources
faq
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
