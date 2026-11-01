# Migrating from 0.2

Version 1.0 replaces public library-defined objects with functions. The specialist tools
are grouped into namespaces so top-level completion stays small.

| Before | Version 1.0 |
| --- | --- |
| `hp.hilbert_plot(12, values).draw()` | `hp.plot(values, curve=12)` |
| `hp.curve(12).draw(4)` | `hp.plot_curve(12, order=4)` |
| `plot.save(path)` | `fig = hp.plot(values); fig.savefig(path)` |
| `plot.show()` | `hp.plot(values); plt.show()` |
| `hp.curve(12).points(4)` | `hp.curves.points(12, order=4)` |
| `hp.curve(12).unroll(image)` | `hp.data.from_grid(image, curve=12)` |
| `hp.curve(12).name` | `hp.curves.info(12)["name"]` |
| `hp.proper().names` | `[c["name"] for c in hp.curves.proper()]` |
| `hp.curve(12).encode(i, order)` | `hp.curves.index_to_xy(i, order, curve=12)` |
| `hp.curve(12).decode(x, y, order)` | `hp.curves.xy_to_index(x, y, order, curve=12)` |
| `plot.image()` | `hp.data.to_grid(values, curve=12)` |

## Behaviour changes

- Plotting functions return a Matplotlib `Figure`, rather than an axes or deferred plot object.
- `fourier` and `difference` are boolean flags on `plot()` and cannot both be enabled.
- `difference=True` renders the complete difference field, rather than a threshold overlay.
- Data plotting defaults to enclosing power-of-two padding. Use `fit="auto"` or `"square"`
  when you want the compact arbitrary-square layout on a supported curve.
- An explicitly too-small order raises unless `fit="truncate"` authorizes dropping the tail.
- Raw conversion preserves dtype and masks. Default integer padding uses NumPy masked arrays.
- Plotting requires an explicit real 1-D scalar sequence; multidimensional and complex values
  need a deliberate choice before display. Conversion supports trailing channel axes.
- Only supported squares and quasisquares are accepted. General rectangles are unsupported.

The old `Curve`, `CurveList`, `HilbertPlot`, and `hilbert_plot` top-level exports are removed.
Native NumPy and Matplotlib objects remain the input/output types.
