# Gallery

These figures are generated during the documentation build from the public API.
The full reproducible script is `scripts/docs_gallery.py` in the repository.

## One signal, different curves

The input is a deterministic mixture of periods 97 and 31. Each mapping uses the same
4096 values and the same enclosing grid size.

```python
values = np.sin(2 * np.pi * t / 97) + 0.4 * np.cos(2 * np.pi * t / 31)
hp.plot(values, curve=0)
hp.plot(values, curve="Moore")
```

```{raw} html
<div class="figure-grid">
<figure><img src="_static/generated/data.png" alt="Periodic sequence mapped on the standard Hilbert curve"><figcaption>Curve 0 — Hilbert.</figcaption></figure>
<figure><img src="_static/generated/moore.png" alt="The same sequence mapped on the Moore curve"><figcaption>Curve 1 — Moore.</figcaption></figure>
</div>
```

## All forty curves

```python
fig = hp.gallery(order=3, ncols=8)
```

![All forty Hilbert-type curves at order three, with their labels](./_static/generated/catalog.png)

## Run the full example

```bash
python examples/try_api.py
MPLBACKEND=Agg python examples/try_api.py --save-only
```

It covers separate curve/data figures, colour options, granularity, Fourier and difference
maps, fitting, conversion round trips, metadata, indexing, and resource controls.
