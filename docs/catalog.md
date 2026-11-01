# Curve catalog

The catalog indices are stable selectors. Friendly labels and paper symbols are also
accepted. [Construction and classification](guides/curves.md) defines the groups below;
[metadata queries](guides/geometry.md) describe how to inspect individual rules.

```python
import hilbertplot as hp

metadata = hp.curves.catalog()
assert len(metadata) == 40
fig = hp.gallery(order=3, ncols=5, color="steelblue")
```

[![All forty curves at order three](_static/generated/catalog.png)](_static/generated/catalog.png)

## Proper homogeneous: 0–5

Four Hilbert kernels with different quadrant transformations.

```python
fig = hp.gallery(hp.curves.proper(), order=3, ncols=3, color="steelblue")
```

![The six proper homogeneous curves](_static/generated/proper.png)

## Improper homogeneous: 6–11

Four Liu4 kernels, with reversal included in the construction rules.

```python
fig = hp.gallery(hp.curves.improper(), order=3, ncols=3, color="darkgoldenrod")
```

![The six improper homogeneous curves](_static/generated/improper.png)

## Inhomogeneous: 12–39

Mixed kernel types. The full catalog above shows each construction, including its index
and generated kernel-mix label. For a specific mixture:

```python
mixed = hp.curves.by_kernels(3, 5)
fig = hp.gallery(mixed, order=3, color="darkorchid")
```

## Arbitrary square/quasisquare support

Curves **0, 3, 4, 5, 24, 29, 30, 31** support the arbitrary-size construction.

```python
fig = hp.gallery(hp.curves.generalizing(), order=3, ncols=4, color="steelblue")
```

![Eight curves supporting arbitrary squares and quasisquares](_static/generated/generalizing.png)

This property is separate from the homogeneous/inhomogeneous classification. All forty
curves support power-of-two squares.
