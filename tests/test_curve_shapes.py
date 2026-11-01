"""Explicit square/quasisquare paths must cover every cell and stay connected."""

import numpy as np
import pytest

import hilbertplot as hp

FEASIBLE = [0, 3, 4, 5, 24, 29, 30, 31]


@pytest.mark.parametrize("index", FEASIBLE)
def test_explicit_shapes_cover_the_grid_and_have_no_jumps(index):
    for n in [*range(1, 34), 63, 64, 65, 100, 257]:
        for rows, columns in ((n, n), (n, n + 1), (n + 1, n)):
            pts = hp.curves.grid((rows, columns), curve=index)
            assert pts.shape == (rows * columns, 2)
            np.testing.assert_array_equal(pts.min(axis=0), [0, 0])
            np.testing.assert_array_equal(pts.max(axis=0), [columns - 1, rows - 1])
            assert np.unique(pts[:, 1] * columns + pts[:, 0]).size == rows * columns
            assert (np.abs(np.diff(pts, axis=0)).sum(axis=1) == 1).all()


def test_shape_squares_agree_with_both_existing_constructions():
    for index in range(40):
        np.testing.assert_array_equal(
            hp.curves.grid((16, 16), curve=index), hp.curves.points(index, order=4)
        )
    for index in FEASIBLE:
        np.testing.assert_array_equal(
            hp.curves.grid((15, 15), curve=index), hp.curves.grid(15, curve=index)
        )


@pytest.mark.parametrize("index", FEASIBLE)
@pytest.mark.parametrize("shape", [(15, 15), (15, 16), (16, 15)])
def test_line_rendering_follows_the_exact_path(index, shape):
    pytest.importorskip("matplotlib")
    pts = hp.curves.grid(shape, curve=index)
    fig = hp.plot_curve(index, shape=shape, mode="line", color="steelblue")
    ax = fig.axes[0]
    assert len(fig.axes) == 1
    assert not ax.images
    np.testing.assert_array_equal(ax.lines[0].get_xydata(), pts)
    assert "x" in ax.get_title()


def test_gradient_line_and_filled_quasisquare_rendering():
    pytest.importorskip("matplotlib")
    fig = hp.plot_curve("Liu2", shape=(15, 16), mode="line")
    ax = fig.axes[0]
    assert ax.collections
    assert not ax.images
    fig = hp.plot_curve(3, shape=(15, 16), mode="fill")
    artist = fig.axes[0].images[0]
    assert artist.get_array().shape == (15, 16)
    assert tuple(artist.get_extent()) == (-0.5, 15.5, -0.5, 14.5)


def test_invalid_or_unsupported_shapes_fail_before_creating_a_figure():
    pytest.importorskip("matplotlib")
    import matplotlib.pyplot as plt

    before = plt.get_fignums()
    for shape, error in [
        ((0, 1), ValueError),
        ((10, 13), ValueError),
        ((True, 2), TypeError),
        ((3.5, 4), TypeError),
        (15, TypeError),
    ]:
        with pytest.raises(error):
            hp.plot_curve(0, shape=shape)
    with pytest.raises(ValueError, match="either order or shape"):
        hp.plot_curve(0, order=4, shape=(15, 16))
    with pytest.raises(ValueError, match="one of curves"):
        hp.plot_curve(12, shape=(15, 16))
    assert plt.get_fignums() == before


def test_shape_path_respects_the_cell_limit():
    previous = hp.config.set_cell_limit(100)
    try:
        with pytest.raises(ValueError, match="cell limit"):
            hp.curves.grid((10, 11))
    finally:
        hp.config.set_cell_limit(previous)
