"""``encode`` / ``decode``: single-cell index maths, checked against the built curve.

The contract is exact agreement with :meth:`Curve.points` -- ``encode(i, k)`` must be
``points(k)[i]`` and ``decode`` must invert it -- for every one of the forty curves, not
just the classic Hilbert curve.  These tests verify that exhaustively at small orders and
by sampling at larger ones, plus the round trip at orders no machine could materialise.
"""

from __future__ import annotations

import numpy as np
import pytest

import hilbertplot as hp

ALL_CURVES = list(range(40))


# --------------------------------------------------------------------------
# Exact agreement with the materialised curve
# --------------------------------------------------------------------------
@pytest.mark.parametrize("index", ALL_CURVES)
@pytest.mark.parametrize("order", [0, 1, 2, 3, 4])
def test_encode_matches_points_for_every_cell(index, order):
    curve = hp.curve(index)
    points = curve.points(order)
    assert [curve.encode(i, order) for i in range(len(points))] == [
        (int(x), int(y)) for x, y in points
    ]


@pytest.mark.parametrize("index", ALL_CURVES)
@pytest.mark.parametrize("order", [0, 1, 2, 3, 4])
def test_decode_inverts_encode_for_every_cell(index, order):
    curve = hp.curve(index)
    for i, (x, y) in enumerate(curve.points(order)):
        assert curve.decode(int(x), int(y), order) == i


@pytest.mark.parametrize("index", ALL_CURVES)
def test_encode_matches_points_at_higher_orders_by_sampling(index):
    curve = hp.curve(index)
    rng = np.random.default_rng(index)
    for order in (6, 8):
        points = curve.points(order)
        for i in rng.integers(0, 4**order, 40):
            i = int(i)
            cell = curve.encode(i, order)
            assert cell == (int(points[i, 0]), int(points[i, 1]))
            assert curve.decode(*cell, order) == i


# --------------------------------------------------------------------------
# Orders far beyond what points() could build
# --------------------------------------------------------------------------
@pytest.mark.parametrize("index", [0, 1, 5, 24, 39])
@pytest.mark.parametrize("order", [20, 32, 64])
def test_round_trip_at_unmaterialisable_orders(index, order):
    """At order 64 the curve has 3.4e38 cells; the index maths does not care."""
    curve = hp.curve(index)
    for i in (0, 1, 4**order - 1, 4**order // 3, 10**18 % 4**order):
        assert curve.decode(*curve.encode(i, order), order) == i


def test_encode_stays_inside_the_grid_at_a_huge_order():
    order = 50
    x, y = hp.curve(0).encode(7 * 10**28, order)
    assert 0 <= x < 2**order
    assert 0 <= y < 2**order


def test_encode_needs_no_memory_budget():
    """The cell limit guards materialisation; index maths materialises nothing."""
    previous = hp.set_cell_limit(16)
    try:
        assert hp.curve(0).encode(12345, 12) is not None
        with pytest.raises(ValueError, match="cell limit"):
            hp.curve(0).points(12)
    finally:
        hp.set_cell_limit(previous)


# --------------------------------------------------------------------------
# Endpoints and structure
# --------------------------------------------------------------------------
@pytest.mark.parametrize("index", ALL_CURVES)
def test_first_and_last_steps_match_the_curve_endpoints(index):
    curve = hp.curve(index)
    order = 5
    points = curve.points(order)
    assert curve.encode(0, order) == (int(points[0, 0]), int(points[0, 1]))
    assert curve.encode(4**order - 1, order) == (int(points[-1, 0]), int(points[-1, 1]))


@pytest.mark.parametrize("index", ALL_CURVES)
def test_consecutive_steps_are_adjacent_cells(index):
    """Space-filling means step i and i+1 differ by one unit move -- check without points()."""
    curve = hp.curve(index)
    order = 6
    previous = curve.encode(0, order)
    for i in range(1, 400):
        current = curve.encode(i, order)
        assert abs(current[0] - previous[0]) + abs(current[1] - previous[1]) == 1
        previous = current


def test_order_zero_is_the_single_origin_cell():
    for index in ALL_CURVES:
        assert hp.curve(index).encode(0, 0) == (0, 0)
        assert hp.curve(index).decode(0, 0, 0) == 0


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------
@pytest.mark.parametrize("i", [-1, 16, 100])
def test_encode_rejects_a_step_outside_the_curve(i):
    with pytest.raises(ValueError, match=r"must be in 0\.\."):
        hp.curve(0).encode(i, 2)


@pytest.mark.parametrize(("x", "y"), [(-1, 0), (0, -1), (4, 0), (0, 4), (4, 4)])
def test_decode_rejects_a_cell_outside_the_grid(x, y):
    with pytest.raises(ValueError, match=r"must lie in 0\.\."):
        hp.curve(0).decode(x, y, 2)


@pytest.mark.parametrize("bad", [1.0, "2", None, True])
def test_index_maths_rejects_non_integer_arguments(bad):
    with pytest.raises(TypeError):
        hp.curve(0).encode(bad, 2)
    with pytest.raises(TypeError):
        hp.curve(0).encode(1, bad)


def test_negative_order_is_rejected():
    with pytest.raises(ValueError, match="non-negative"):
        hp.curve(0).encode(0, -1)


# --------------------------------------------------------------------------
# label_map
# --------------------------------------------------------------------------
@pytest.mark.parametrize("index", [0, 1, 5, 24, 39])
def test_label_map_is_the_inverse_of_points(index):
    curve = hp.curve(index)
    order = 4
    labels = curve.label_map(order)
    assert labels.shape == (2**order, 2**order)
    assert sorted(labels.ravel().tolist()) == list(range(4**order))
    for i, (x, y) in enumerate(curve.points(order)):
        assert labels[y, x] == i


def test_label_map_agrees_with_decode():
    curve = hp.curve(0)
    order = 3
    labels = curve.label_map(order)
    for y in range(2**order):
        for x in range(2**order):
            assert labels[y, x] == curve.decode(x, y, order)
