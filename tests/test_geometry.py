"""Geometry primitives, plus an independent cross-check of the Hilbert curve."""

import numpy as np
import pytest

import hilbertplot as hp
from hilbertplot._core.geometry import (
    canonical_form,
    is_space_filling,
    word_to_points,
    word_to_steps,
)


def _reference_hilbert(order: int) -> np.ndarray:
    """The classic Wikipedia d2xy Hilbert curve -- an independent oracle."""
    n = 2**order
    pts = []
    for d in range(n * n):
        rx = ry = 0
        x = y = 0
        t = d
        s = 1
        while s < n:
            rx = 1 & (t // 2)
            ry = 1 & (t ^ rx)
            if ry == 0:
                if rx == 1:
                    x = s - 1 - x
                    y = s - 1 - y
                x, y = y, x
            x += s * rx
            y += s * ry
            t //= 4
            s *= 2
        pts.append((x, y))
    return np.array(pts, dtype=np.int64)


@pytest.mark.parametrize("order", [1, 2, 3, 4, 5])
def test_curve0_is_the_hilbert_curve(order):
    ours = hp.curve(0).points(order)
    ref = _reference_hilbert(order)
    # Equal up to the symmetry/reversion equivalence.
    assert canonical_form(ours) == canonical_form(ref)


def test_word_to_steps_maps_letters():
    steps = word_to_steps("urdl")
    assert steps.tolist() == [[0, 1], [1, 0], [0, -1], [-1, 0]]


def test_word_to_points_walk_and_normalize():
    pts = word_to_points("urd")  # order-1 Hilbert
    assert pts.tolist() == [[0, 0], [0, 1], [1, 1], [1, 0]]


def test_empty_word_is_single_point():
    assert word_to_points("").tolist() == [[0, 0]]


def test_is_space_filling_positive_and_negative():
    good = hp.curve(0).points(3)
    assert is_space_filling(good, 8)  # a side, not an order
    # Wrong side claim should fail.
    assert not is_space_filling(good, 4)
    assert not is_space_filling(good, 3)
    # A path with a repeated cell is not space-filling.
    bad = word_to_points("uu")  # goes (0,0)->(0,1)->(0,2): not a square
    assert not is_space_filling(bad, 2)


def test_is_space_filling_accepts_arbitrary_squares():
    """It takes a side precisely so it can check `grid(n)`, not only `points(k)`."""
    for n in (1, 3, 7, 10, 15):
        assert is_space_filling(hp.curve(0).grid(n), n)
    assert not is_space_filling(hp.curve(0).grid(10), 9)


def test_is_space_filling_rejects_a_permutation_that_is_not_a_path():
    """Visiting every cell is not enough -- consecutive cells must be adjacent."""
    pts = hp.curve(0).points(3)
    shuffled = pts[np.random.default_rng(0).permutation(len(pts))]
    assert not is_space_filling(shuffled, 8)
    # ...unless the caller explicitly only wants the covering property.
    assert is_space_filling(shuffled, 8, connected=False)


def test_canonical_form_invariant_under_rotation_and_reversion():
    pts = hp.curve(3).points(3)
    base = canonical_form(pts)
    # 90-degree rotation
    rot = np.stack([-pts[:, 1], pts[:, 0]], axis=1)
    assert canonical_form(rot) == base
    # reversion (walk backwards)
    assert canonical_form(pts[::-1].copy()) == base
    # horizontal reflection
    refl = np.stack([-pts[:, 0], pts[:, 1]], axis=1)
    assert canonical_form(refl) == base
