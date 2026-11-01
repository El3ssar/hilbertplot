# Catalog, coordinates and indexing

## Catalog queries

`hp.curves.info()` returns a dictionary. Every selection below returns a list of those
dictionaries, in index order, ready to pass to `hp.gallery()`.

```python
import numpy as np
import hilbertplot as hp

info = hp.curves.info(12)
print(info["index"], info["name"], info["rule"])
all_curves = hp.curves.catalog()
proper = hp.curves.proper()                 # 6
improper = hp.curves.improper()             # 6
homogeneous = hp.curves.homogeneous()       # 12
mixed = hp.curves.inhomogeneous()           # 28
loops = hp.curves.closed()                  # 4
arbitrary = hp.curves.generalizing()        # 8
hilbert_kernels = hp.curves.by_kernels(0)    # exact kernel set
```

Metadata fields:

| Key | Meaning |
| --- | --- |
| `index` | Stable selector from 0 through 39 |
| `name` | Friendly label, where available |
| `symbol` | Paper notation, such as `12H` |
| `kind` | `proper`, `improper`, or `inhomogeneous` |
| `homogeneous` | One kernel type is used throughout the quadrants |
| `closed` | A construction classified as closed in the catalog |
| `generalizes` | Supports arbitrary squares and quasisquares |
| `kernels` | Sorted list of quadrant kernel indices |
| `combination` | Kernel mix in paper notation |
| `rule` | Tag-system construction rule |

A missing memorable name is no obstacle: pass the integer index or paper symbol.
`by_kernels()` requires an **exact** set match; it does not mean “contains this kernel.”

## Coordinates versus array indexing

Coordinates are `(x, y)`: x is the column and y is the row. NumPy array access is
`image[y, x]`. Plots default to `origin="lower"`, so row zero is displayed at the bottom.
For an image convention with row zero at the top, explicitly use `origin="upper"` when displaying.
Changing display origin does not change conversion order.

```python
points = hp.curves.points(0, order=3)  # shape (64, 2)
assert hp.curves.is_space_filling(points, side=8)
word = hp.curves.word(0, order=3)      # 63 letters: u, d, l, r
assert len(word) == len(points) - 1
arbitrary_points = hp.curves.grid((15, 16), curve=3)
assert arbitrary_points.shape == (240, 2)
```

Order zero contains one cell and an empty direction word. `is_space_filling()` validates
**squares**, not quasisquares: it verifies full coverage, uniqueness, bounds and, by default,
unit-step connectivity. Pass `connected=False` to check coverage alone.

## Labels are the inverse coordinate lookup

```python
labels = hp.curves.label_map(0, order=3)
for index, (x, y) in enumerate(points):
    assert labels[y, x] == index
```

```{raw} html
<div class="plot-pair">
<figure><img src="../_static/generated/labels-hilbert.png" alt="Hilbert visit indices zero to fifteen"></figure>
<figure><img src="../_static/generated/labels-moore.png" alt="Moore visit indices zero to fifteen"></figure>
</div>
```

`hp.curves.difference_map()` compares these labels at spatially neighbouring cells.
[Its definition is in the transform guide](transforms.md#difference-where-spatial-neighbours-are-far-apart-in-sequence-order).

## Direct indexing

```python
index = 10**18
xy = hp.curves.index_to_xy(index, order=40, curve=12)
recovered = hp.curves.xy_to_index(*xy, order=40, curve=12)
assert recovered == index
```

These routines follow the recursive construction in $O(k)$ work for order $k$, without
materializing $4^k$ cells. Python integers keep the result exact. Coordinates must lie
in `[0, 2**order)`; sequence indices in `[0, 4**order)`. This direct indexing currently
supports power-of-two squares only. Use `grid()` for other supported path sizes.

## Compare paths up to square symmetry

```python
key = hp.curves.canonical_form(points)
assert isinstance(key, bytes)
assert key == hp.curves.canonical_form(points[::-1])
```

The byte key ignores square rotations/reflections, translation to the origin, and traversal
reversal. It is an in-process comparison tool, not a portable on-disk identifier: it uses
the array's dtype and byte representation. Use compatible integer arrays when comparing.
