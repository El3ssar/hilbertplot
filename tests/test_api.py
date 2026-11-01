"""User-facing function contracts, checked against geometry and numpy reference results."""

import inspect
import subprocess
import sys

import numpy as np
import pytest

import hilbertplot as hp


def test_top_level_completion_is_small_and_matches_the_actual_exports():
    expected = {"__version__", "plot", "plot_curve", "gallery", "curves", "data", "config"}
    assert set(dir(hp)) == set(hp.__all__) == expected
    for name in ("plot", "plot_curve", "gallery"):
        assert inspect.isfunction(getattr(hp, name))
    for namespace in (hp.curves, hp.data, hp.config):
        assert inspect.ismodule(namespace)
        assert dir(namespace) == sorted(namespace.__all__)
        for name in namespace.__all__:
            assert inspect.isfunction(getattr(namespace, name))
            assert not hasattr(hp, name)
    for name in ("Curve", "CurveList", "HilbertPlot", "hilbert_plot", "map"):
        assert not hasattr(hp, name)
        assert name not in dir(hp)
        assert name not in hp.__all__


def test_standard_repl_completion_shows_only_the_main_entry_points():
    import rlcompleter

    completer = rlcompleter.Completer({"hp": hp})
    matches = []
    for i in range(20):
        match = completer.complete("hp.", i)
        if match is None:
            break
        matches.append(match.rstrip("()"))
    assert set(matches) == {f"hp.{name}" for name in hp.__all__ if not name.startswith("_")}


def test_metadata_is_plain_detached_containers():
    records = hp.curves.catalog()
    assert type(records) is list
    assert [r["index"] for r in records] == list(range(40))
    assert all(type(r) is dict for r in records)
    records[0]["kernels"].append(99)
    records[0]["name"] = "changed"
    assert hp.curves.info(0)["name"] == "Hilbert"
    assert hp.curves.info(0)["kernels"] == [0]
    assert [c["index"] for c in hp.curves.by_kernels(3, 5)] == list(range(12, 18))
    assert len(hp.curves.proper()) == len(hp.curves.improper()) == 6
    assert len(hp.curves.homogeneous()) == 12
    assert len(hp.curves.inhomogeneous()) == 28
    assert [c["index"] for c in hp.curves.closed()] == [1, 2, 6, 9]
    assert [c["index"] for c in hp.curves.generalizing()] == [0, 3, 4, 5, 24, 29, 30, 31]


def test_mapping_names_describe_their_direction_without_old_aliases():
    assert "to_grid" in dir(hp.data)
    assert "from_grid" in dir(hp.data)
    assert "index_to_xy" in dir(hp.curves)
    assert "xy_to_index" in dir(hp.curves)
    assert not hasattr(hp.data, "image")
    assert not hasattr(hp.data, "unroll")
    assert not hasattr(hp.curves, "encode")
    assert not hasattr(hp.curves, "decode")


def test_reading_with_another_curve_is_a_reversible_permutation():
    values = np.arange(64.0)
    grid = hp.data.to_grid(values, curve=0)
    reordered = hp.data.from_grid(grid, curve=12)
    assert not np.array_equal(reordered, values)
    np.testing.assert_array_equal(np.sort(reordered), values)
    restored_grid = hp.data.to_grid(reordered, curve=12)
    np.testing.assert_array_equal(restored_grid, grid)
    np.testing.assert_array_equal(hp.data.from_grid(restored_grid, curve=0), values)


@pytest.mark.parametrize("index", range(40))
def test_mapping_and_index_functions_work_for_every_curve(index):
    data = np.arange(64.0)
    for selector in (index, hp.curves.info(index)["name"], f"{index}H"):
        img = hp.data.to_grid(data, curve=selector)
        np.testing.assert_array_equal(hp.data.from_grid(img, curve=selector), data)
    points = hp.curves.points(index, 3)
    labels = hp.curves.label_map(index, 3)
    assert hp.curves.is_space_filling(points, 8)
    assert len(hp.curves.word(index, 3)) == 63
    for i, (x, y) in enumerate(points):
        assert hp.curves.index_to_xy(i, 3, curve=index) == (x, y)
        assert hp.curves.xy_to_index(x, y, 3, curve=index) == labels[y, x] == i


def test_arbitrary_square_arrays_and_fields_align():
    data = np.arange(100.0)
    img = hp.data.to_grid(data, fit="square")
    assert img.shape == (10, 10)
    assert hp.curves.grid(10).shape == (100, 2)
    assert (
        hp.curves.difference_map(side=10).shape == hp.curves.label_map(side=10).shape == img.shape
    )
    np.testing.assert_array_equal(hp.data.from_grid(img), data)
    # A power-of-two side works even on a non-generalizing curve.
    assert hp.curves.label_map("Moore", side=16).shape == (16, 16)
    with pytest.raises(ValueError, match="either order or side"):
        hp.curves.label_map(order=3, side=8)


def test_explicit_size_cannot_silently_discard_values():
    with pytest.raises(ValueError, match="do not fit"):
        hp.data.to_grid(range(100), order=3)
    small = hp.data.to_grid(range(100), order=3, fit="truncate")
    np.testing.assert_array_equal(hp.data.from_grid(small), np.arange(64))


def test_input_policy_is_explicit_and_handles_integer_masks():
    with pytest.raises(ValueError, match="1-D"):
        hp.plot(np.zeros((2, 2)))
    with pytest.raises(TypeError, match="must be real"):
        hp.plot(np.array([1 + 2j]))
    with pytest.raises(ValueError, match="infinity"):
        hp.plot([1, np.inf])
    masked = np.ma.array([1, 2, 3, 4], mask=[0, 1, 0, 0])
    assert np.ma.getmaskarray(hp.data.from_grid(hp.data.to_grid(masked)))[1]
    with pytest.raises(ValueError, match="finite"):
        hp.data.fourier([np.nan] * 4)


def test_missing_only_plot_fails_cleanly_without_a_figure():
    import matplotlib.pyplot as plt

    before = plt.get_fignums()
    with pytest.raises(ValueError, match="finite"):
        hp.plot([np.nan] * 4)
    assert plt.get_fignums() == before


@pytest.mark.parametrize("transform", ["data", "fourier", "difference"])
@pytest.mark.parametrize("index", range(40))
def test_one_transformed_image_matches_the_numeric_result(index, transform):
    data = np.sin(np.arange(100.0))
    kwargs = {} if transform == "data" else {transform: True}
    fig = hp.plot(data, curve=index, colorbar=False, **kwargs)
    assert fig.__class__.__module__.startswith("matplotlib.")
    assert len(fig.axes) == len(fig.axes[0].images) == 1
    got = fig.axes[0].images[0].get_array()
    if transform == "data":
        expected = hp.data.to_grid(data, curve=index)
    elif transform == "fourier":
        expected = hp.data.fourier(data, curve=index)
    else:
        expected = hp.curves.difference_map(index, side=16)
    np.testing.assert_allclose(got.filled(np.nan), expected, equal_nan=True)


def test_conflicting_transforms_fail_before_data_or_figure_creation():
    import matplotlib.pyplot as plt

    before = plt.get_fignums()
    with pytest.raises(ValueError, match="mutually exclusive"):
        hp.plot(None, fourier=True, difference=True)
    assert plt.get_fignums() == before


@pytest.mark.parametrize("name", ["fourier", "difference"])
def test_boolean_flags_accept_zero_and_one_but_reject_other_values(name):
    hp.plot([1, 2, 3, 4], **{name: 0})
    hp.plot([1, 2, 3, 4], **{name: 1})
    for bad in ("yes", 2, [], None, 0.5):
        with pytest.raises(TypeError, match="boolean"):
            hp.plot([1, 2, 3, 4], **{name: bad})


def test_plain_and_fourier_figures_can_use_axes_and_save(tmp_path, monkeypatch):
    import matplotlib.pyplot as plt
    from matplotlib.colors import LogNorm

    def unexpected_show():
        pytest.fail("plotting functions must not open a window")

    monkeypatch.setattr(plt, "show", unexpected_show)
    fig, ax = plt.subplots()
    assert hp.plot(range(1, 101), curve="Moore", ax=ax, norm=LogNorm()) is fig
    assert len(fig.axes) == 2  # plot + requested-by-default colorbar
    out = tmp_path / "data.png"
    fig.savefig(out)
    assert out.stat().st_size > 0
    assert hp.plot_curve("12H", order=3).axes[0].collections
    assert hp.plot_curve(12, order=3, mode="fill").axes[0].images
    gallery = hp.gallery(hp.curves.proper(), order=2)
    assert len(gallery.axes) == 6


def test_plotting_options_match_arrays_and_support_imshow_overrides():
    data = np.arange(100.0)
    fig = hp.plot(
        data, granularity=7, fit="square", colorbar=False, origin="upper", interpolation="bilinear"
    )
    artist = fig.axes[0].images[0]
    np.testing.assert_array_equal(
        artist.get_array(), hp.data.to_grid(data, granularity=7, fit="square")
    )
    assert artist.origin == "upper"
    assert artist.get_interpolation() == "bilinear"
    fig = hp.plot(data, fourier=True, window=True, log=False, remove_dc=False, colorbar=False)
    np.testing.assert_allclose(
        fig.axes[0].images[0].get_array(),
        hp.data.fourier(data, window=True, log=False, remove_dc=False),
    )


def test_lazy_backend_loading_and_missing_dependency_diagnostic():
    script = """
import sys, numpy as np
class NoMatplotlib:
    def find_spec(self, fullname, path=None, target=None):
        if fullname == 'matplotlib' or fullname.startswith('matplotlib.'):
            raise ModuleNotFoundError('No matplotlib')
sys.meta_path.insert(0, NoMatplotlib())
import hilbertplot as hp
assert not any(m.startswith('matplotlib') for m in sys.modules)
assert hp.data.to_grid(range(100)).shape == (16, 16)
assert hp.data.fourier(range(100)).shape == (16, 16)
assert hp.curves.difference_map(side=10).shape == (10, 10)
assert hp.curves.xy_to_index(*hp.curves.index_to_xy(5, 2), 2) == 5
assert hp.curves.info(12)['index'] == 12
try:
    hp.plot([1, 2, 3, 4])
except ModuleNotFoundError as exc:
    assert "required dependency 'matplotlib'" in str(exc)
    assert 'pip install --upgrade --force-reinstall hilbertplot' in str(exc)
else:
    raise AssertionError('plot should explain how to repair the missing required dependency')
"""
    subprocess.run([sys.executable, "-c", script], check=True, capture_output=True, text=True)
