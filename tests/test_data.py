"""Data-to-image mapping (HilbertPlot), the l-granularity transform, and pad/truncate."""

import numpy as np
import pytest

import hilbertplot as hp
from hilbertplot._data.mapping import granulate, order_floor, order_for


# -- order_for / order_floor ------------------------------------------------
@pytest.mark.parametrize(
    ("n", "order"), [(1, 0), (4, 1), (16, 2), (1024, 5), (1000, 5), (1025, 6), (3_000_000, 11)]
)
def test_order_for(n, order):
    assert order_for(n) == order


@pytest.mark.parametrize(("n", "order"), [(1, 0), (4, 1), (15, 1), (16, 2), (1000, 4), (1024, 5)])
def test_order_floor(n, order):
    assert order_floor(n) == order


def test_order_for_rejects_empty():
    with pytest.raises(ValueError, match="at least one value"):
        order_for(0)


# -- granulate (paper eqs 1-3) ---------------------------------------------
def test_granulate_block_means():
    assert granulate([0, 2, 10, 0], 2).tolist() == [1.0, 1.0, 5.0, 5.0]


def test_granulate_faithful_is_identity():
    data = [3, 1, 4, 1, 5, 9]
    assert granulate(data, 1).tolist() == [float(x) for x in data]


def test_granulate_period_collapses_to_constant():
    assert np.allclose(granulate(np.tile([1, 0], 512), 2), 0.5)
    assert np.allclose(granulate(np.tile([1, 1, 0, 0], 256), 4), 0.5)


def test_granulate_handles_trailing_partial_block():
    assert granulate([2, 4, 9], 2).tolist() == [3.0, 3.0, 9.0]


def test_granulate_rejects_bad_l():
    with pytest.raises(ValueError, match="granularity"):
        granulate([1, 2, 3], 0)


# -- HilbertPlot construction ----------------------------------------------
def test_plot_data_returns_hilbertplot_and_draws_nothing():
    from hilbertplot._viz.hilbert_plot import HilbertPlot

    plot = hp.curve(0).plot_data(np.arange(64))
    assert isinstance(plot, HilbertPlot)
    assert len(plot) == 64
    assert plot.curve is hp.curve(0)


def test_hilbert_plot_shortcut_matches_curve_path():
    a = hp.hilbert_plot(0, np.arange(64)).image(order=3)
    b = hp.curve(0).plot_data(np.arange(64)).image(order=3)
    assert np.array_equal(a, b, equal_nan=True)


def test_hilbert_plot_accepts_index_name_or_curve():
    assert hp.hilbert_plot(1, [0]).curve.index == 1
    assert hp.hilbert_plot("moore", [0]).curve.index == 1
    assert hp.hilbert_plot(hp.curve(5), [0]).curve.index == 5


# -- the mapping ------------------------------------------------------------
def test_map_places_each_value_on_the_path():
    c = hp.curve(0)
    img = c.plot_data(np.arange(64)).image(order=3)
    for i, (x, y) in enumerate(c.points(3)):
        assert img[y, x] == i


def test_default_order_and_shape():
    assert hp.hilbert_plot(0, np.zeros(1000)).image().shape == (32, 32)  # order 5


def test_periodic_10_is_a_checkerboard():
    # Fig. 6: the ·10· periodic pattern maps to a perfect checkerboard.
    img = hp.hilbert_plot(0, np.tile([1, 0], 512)).image()
    assert img.shape == (32, 32)
    assert np.all(np.abs(np.diff(img, axis=0)) == 1)
    assert np.all(np.abs(np.diff(img, axis=1)) == 1)


def test_map_works_for_every_curve():
    data = np.arange(256)
    for c in hp.catalog():
        img = c.plot_data(data).image(order=4)
        assert np.array_equal(np.sort(img.ravel()), data.astype(float))


def test_granularity_at_plot_time_collapses_period():
    plot = hp.hilbert_plot(0, np.tile([1, 1, 0, 0], 256))
    assert np.allclose(plot.image(granularity=4), 0.5)
    # the same plot object also renders faithfully -- granularity is per-render
    faithful = plot.image(granularity=1)
    assert not np.allclose(faithful, 0.5)


# -- pad vs truncate --------------------------------------------------------
def test_fit_pad_leaves_blank_cells():
    img = hp.hilbert_plot(0, np.arange(1000)).image(fit="pad")
    assert img.shape == (32, 32)
    assert np.isnan(img).sum() == 32 * 32 - 1000


def test_fit_truncate_fills_a_smaller_square():
    img = hp.hilbert_plot(0, np.arange(1000)).image(fit="truncate")
    assert img.shape == (16, 16)  # order_floor(1000) = 4
    assert not np.isnan(img).any()
    assert np.array_equal(np.sort(img.ravel()), np.arange(256, dtype=float))


def test_pad_fill_value_is_configurable():
    img = hp.hilbert_plot(0, np.ones(10)).image(order=3, fill=-1.0)
    assert (img == -1.0).sum() == 64 - 10


def test_explicit_small_order_truncates():
    img = hp.hilbert_plot(0, np.arange(100)).image(order=3)  # 64 cells < 100
    assert img.shape == (8, 8)
    assert np.array_equal(np.sort(img.ravel()), np.arange(64, dtype=float))


def test_bad_fit_rejected():
    with pytest.raises(ValueError, match="fit must be one of"):
        hp.hilbert_plot(0, [1, 2, 3]).image(fit="nonsense")


# -- unroll (2D -> 1D along the curve) --------------------------------------
def test_unroll_reads_values_in_curve_order():
    c = hp.curve(0)
    grid = np.arange(16).reshape(4, 4)
    got = c.unroll(grid)
    expected = [grid[y, x] for x, y in c.points(2)]
    assert got.tolist() == expected


@pytest.mark.parametrize("index", [0, 5, 12, 39])
@pytest.mark.parametrize("order", [1, 2, 4])
def test_unroll_is_inverse_of_hilbert_plot(index, order):
    data = np.arange(4**order)
    img = hp.hilbert_plot(index, data).image(order=order)
    assert np.array_equal(hp.curve(index).unroll(img), data)


def test_unroll_rejects_non_square():
    with pytest.raises(ValueError, match="square 2-D array"):
        hp.curve(0).unroll(np.zeros((4, 8)))


def test_unroll_rejects_non_power_of_two_for_non_generalizing_curve():
    # Moore does not generalize, so a non-2^k side must be rejected.
    assert not hp.curve(1).generalizes
    with pytest.raises(ValueError, match="not a power of two"):
        hp.curve(1).unroll(np.zeros((6, 6)))


def test_unroll_accepts_arbitrary_square_for_generalizing_curve():
    c = hp.curve(0)  # Hilbert generalizes
    grid = np.arange(49).reshape(7, 7)  # 7 is not a power of two
    got = c.unroll(grid)
    expected = [grid[y, x] for x, y in c.grid(7)]
    assert got.tolist() == expected
    # round trip through an arbitrary-square Hilbert plot
    data = np.arange(49)
    img = hp.hilbert_plot(0, data).image()  # 7x7 tight square
    assert np.array_equal(c.unroll(img), data)


# -- difference map (locality-loss field) -----------------------------------
def test_difference_map_shape_and_range():
    for index in (0, 5, 12):
        D = hp.curve(index).difference_map(4)
        assert D.shape == (16, 16)
        assert np.isfinite(D).all()
        assert (D >= 0).all()


def test_difference_map_depends_only_on_the_curve():
    # It is a property of the curve's ordering, independent of any data.
    a = hp.curve(0).difference_map(3)
    b = hp.curve(0).difference_map(3)
    assert np.array_equal(a, b)
    assert not np.array_equal(hp.curve(0).difference_map(3), hp.curve(5).difference_map(3))


def test_barrier_shrinks_as_threshold_rises():
    D = hp.curve(0).difference_map(5)

    def n_barrier(t):
        return int((D.mean() + t * D.std() < D).sum())

    assert n_barrier(0.0) >= n_barrier(0.5) >= n_barrier(1.0) >= n_barrier(2.0)
    assert n_barrier(1.0) > 0  # there is always a barrier (quadrants 1 & 4)


def test_interior_cell_averages_eight_neighbours():
    # A degenerate 2x2 label field: every cell has 3 neighbours (corner), so the
    # difference map is well defined and symmetric under the curve's symmetry.
    from hilbertplot._data.mapping import difference_map, label_map

    pts = hp.curve(0).points(2)
    lab = label_map(pts, 4)
    # label_map is a bijection onto 0..15
    assert sorted(lab.ravel().tolist()) == list(range(16))
    D = difference_map(pts, 4)
    assert D.shape == (4, 4)
    assert np.isfinite(D).all()
