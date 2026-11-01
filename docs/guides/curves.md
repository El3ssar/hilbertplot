# Curves and shapes

## Inspect the catalog

```python
import hilbertplot as hp

print([(c["index"], c["name"]) for c in hp.curves.catalog()])
print(hp.curves.info(12))
```

Metadata is a plain dictionary. Groups are plain lists of these dictionaries.

| Function under `hp.curves` | Contents |
| --- | --- |
| `catalog()` | All 40 curves |
| `proper()` | 6 proper homogeneous curves |
| `improper()` | 6 improper homogeneous curves |
| `homogeneous()` | All 12 homogeneous curves |
| `inhomogeneous()` | 28 mixed-kernel curves |
| `closed()` | 4 curves with adjacent entry/exit cells |
| `generalizing()` | 8 curves supporting arbitrary square sizes |
| `by_kernels(3, 5)` | Curves whose kernel set is exactly `{3, 5}` |

## Draw the line itself

```python
hp.plot_curve(12, order=4, mode="line")
hp.plot_curve("Moore", order=4, color="steelblue", linewidth=1)
```

Order $k$ gives a $2^k \times 2^k$ grid with $4^k$ visited cells.
The circle marks entry and the square marks exit. Use `endpoints=False` to hide them.

`mode="auto"` uses lines below order 8 and a filled visit-order image for larger orders.
Use `mode="line"` to force the polyline. Large line plots can be expensive and visually dense.

## Arbitrary squares and quasisquares

Eight specific curves support the arbitrary-size construction:
**0, 3, 4, 5, 24, 29, 30, 31**. They are not the first eight catalog entries.

```python
hp.plot_curve(3, shape=(15, 15), mode="line")  # arbitrary square
hp.plot_curve(3, shape=(15, 16), mode="line")  # quasisquare
hp.plot_curve(3, shape=(16, 15), mode="line")  # the other aspect
```

`shape` is `(rows, columns)`. A quasisquare's sides differ by one. The implementation
selects an orientation that keeps the path connected. Use either `shape=` or `order=`,
not both. General rectangles are unsupported; no cropped or disconnected fallback is substituted.

![Liu2 traversing a 15 by 16 quasisquare](../_static/generated/quasisquare.png)

## Obtain coordinates and individual cells

```python
points = hp.curves.points(12, order=4)  # integer (x, y) coordinates
points = hp.curves.grid((15, 16), curve=3)

x, y = hp.curves.index_to_xy(5, order=4, curve=12)
index = hp.curves.xy_to_index(x, y, order=4, curve=12)
assert index == 5
```

The individual-cell conversions take a power-of-two order and avoid building the full grid.
For explicit arbitrary shapes, use the ordered coordinates from `grid()`.

Coordinates are `(x, y)`. Arrays are indexed `[y, x]`, so the value at a coordinate is
`image[y, x]`.
