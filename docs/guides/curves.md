# Curve construction and classification

The catalog contains 40 two-dimensional Hilbert-type constructions: 12 homogeneous
and 28 inhomogeneous. These are the constructions classified in
[Estevez-Rams et al., *Hilbert curves in two dimensions* (2017)](https://estevez-moya.com/es/publicaciones/hilbert-curves-in-two-dimensions).
The library represents their finite-resolution paths through grid cells.

## Orders, quadrants and kernels

![The standard Hilbert curve at orders one through four](../_static/generated/orders.png)

An order-$k$ curve visits $4^k$ cells on a $2^k$ by $2^k$ grid. To build it, divide
the grid into four quadrants. Each quadrant contains a transformed order-$(k-1)$
path. The construction connects these paths in quadrant order: bottom left, top
left, top right, bottom right.

The **kernel** is the lower-order curve chosen for a quadrant. Its placement may
be rotated or reflected. **Reversion** exchanges entry and exit by traversing the
same path backwards; it changes traversal order, not the spatial reflection.

## Homogeneous and inhomogeneous

A **homogeneous** construction uses one kernel type in all four quadrants.
An **inhomogeneous** construction mixes at least two kernel types. Different
orientations of the same kernel do not make a construction inhomogeneous.

## Proper and improper

The twelve homogeneous constructions split into two families:

- **Proper, indices 0–5:** use the standard Hilbert kernel (0), with quadrant
  rotations/reflections. They are Hilbert, Moore, Liu1, Liu2, Liu3 and Liu4.
- **Improper, indices 6–11:** use Liu4 (5) as the kernel and include quadrant
  reversion in their construction rules. They are named Improper1 through Improper6.

“Improper” is the classification term; these are valid connected paths, not faulty
curves. The reversion-based construction is described in
[Pérez-Demydenko et al., sections 3–4](https://arxiv.org/abs/1311.2868).

```{raw} html
<div class="plot-three">
<figure><img src="../_static/generated/classification-1.png" alt="Moore with four blue Hilbert kernels"></figure>
<figure><img src="../_static/generated/classification-6.png" alt="Improper1 with four orange Liu4 kernels"></figure>
<figure><img src="../_static/generated/classification-12.png" alt="Curve twelve with purple Liu2 and orange Liu4 kernels"></figure>
</div>
```

Moore uses four Hilbert kernels (blue). Improper1 uses four Liu4 kernels (orange).
Curve 12 uses Liu2 (purple) in two quadrants and Liu4 in two, so it is inhomogeneous.
The thin grey segments are the connections between quadrants. Colors encode kernel
identity, not visit order or sample values.

The hierarchy is:

```text
40 curves
├── 12 homogeneous: one kernel type
│   ├── 6 proper: Hilbert kernel
│   └── 6 improper: Liu4 kernel, with quadrant reversion
└── 28 inhomogeneous: mixed kernel types
```

## Query the classification

```python
import hilbertplot as hp

assert len(hp.curves.proper()) == 6
assert len(hp.curves.improper()) == 6
assert len(hp.curves.homogeneous()) == 12
assert len(hp.curves.inhomogeneous()) == 28

assert hp.curves.info("Moore")["kernels"] == [0]
assert hp.curves.info(6)["kernels"] == [5]
assert hp.curves.info(12)["kernels"] == [3, 5]
assert not hp.curves.info(12)["homogeneous"]

mixed = hp.curves.by_kernels(3, 5)  # exact kernel set, not "contains"
fig = hp.gallery(mixed, order=3, color="steelblue")
```

The four kernel indices, their transformations, and reversion flags are encoded
in each metadata dictionary's `rule`. `kernels` lists only the distinct kernel indices.
A generated label is optional when plotting; every curve accepts its index or paper
symbol, for example `curve=12` or `curve="12H"`.

## Closed curves and arbitrary-size support

These are additional properties, separate from the hierarchy above.

| Property | Meaning | Selection |
| --- | --- | --- |
| Closed | Construction classified as closed; includes Moore, Liu1, Improper1 and Improper4 | `hp.curves.closed()` |
| Generalizing | Supports arbitrary square and quasisquare sizes | `hp.curves.generalizing()` |

Eight curves generalize: **0, 3, 4, 5, 24, 29, 30, 31**. They are not the first eight
catalog entries. Every curve supports power-of-two squares; arbitrary sizes require
one of these eight. A quasisquare has sides differing by one. General rectangles are
unsupported.

```python
fig = hp.plot_curve(0, order=3, color="steelblue")
fig = hp.plot_curve(3, shape=(15, 16), color="darkorchid")
```

![Square and quasisquare paths with connected orientations](../_static/generated/shapes.png)

For explicit shapes, `(rows, columns)` is the array convention. The implementation
selects a connected top-level orientation for quasisquares. Use either `shape=` or
`order=`, not both. See [fitting](fitting.md) for grids selected from sequence length,
and the [complete catalog](../catalog.md) for all forty curves.
