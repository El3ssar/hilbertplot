"""Robustness of the public surface: degenerate inputs, guards, and warning hygiene.

Every test here corresponds to an input a user can plausibly supply.  The rule the suite
enforces is that such an input either works or raises a *specific, actionable* error --
never a numpy ``RuntimeWarning``, never a silently wrong result.
"""

import pathlib
import re
import warnings

import numpy as np
import pytest

import hilbertplot as hp
from hilbertplot._core import curve as curves
from hilbertplot._viz.hilbert_plot import HilbertPlot as _HilbertPlot
from hilbertplot._viz.hilbert_plot import hilbert_plot as make_plot
from hilbertplot._viz.render import gallery as draw_gallery

FEASIBLE = [0, 3, 4, 5, 24, 29, 30, 31]


# --------------------------------------------------------------------------
# No public entry point may emit a warning on ordinary input.
# --------------------------------------------------------------------------
@pytest.mark.parametrize("order", [0, 1, 2, 5])
def test_difference_map_is_warning_free_at_every_order(order):
    """Order 0 used to divide 0/0, emitting a RuntimeWarning and returning NaN."""
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        result = curves.curve(0).difference_map(order)
    assert result.shape == (2**order, 2**order)
    assert np.isfinite(result).all()
    assert (result >= 0).all()


def test_difference_map_of_a_single_cell_is_zero():
    assert curves.curve(0).difference_map(0).tolist() == [[0.0]]


def test_difference_map_survives_a_degenerate_grid():
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        ax = make_plot(0, [1.0]).draw(difference=True)
    assert ax is not None


@pytest.mark.parametrize(
    "data",
    [[1.0], [0.0] * 16, np.arange(100.0), np.zeros(1000)],
    ids=["single", "constant", "square-fit", "padded"],
)
def test_image_is_warning_free(data):
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        make_plot(0, data).image()


def test_fourier_is_warning_free_on_padded_data():
    """Padding leaves NaN cells, which fourier_spectrum has to fill before transforming."""
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        spec = make_plot(1, np.arange(1000.0)).fourier()  # Moore pads to 32x32
    assert np.isfinite(spec).all()


# --------------------------------------------------------------------------
# The data buffer must be genuinely immutable, not merely flagged.
# --------------------------------------------------------------------------
def test_plot_data_cannot_be_mutated_through_the_property():
    plot = make_plot(0, np.arange(16.0))
    exposed = plot.data
    assert not exposed.flags.writeable
    with pytest.raises(ValueError, match="read-only"):
        exposed[0] = 999.0
    # ...and the read-only flag itself must not be re-enableable
    with pytest.raises(ValueError, match="WRITEABLE"):
        exposed.flags.writeable = True
    assert plot.image(order=2)[0, 0] == 0.0


def test_plot_does_not_alias_the_caller_array():
    source = np.arange(16.0)
    plot = make_plot(0, source)
    source[0] = 999.0
    assert plot.data[0] == 0.0


# --------------------------------------------------------------------------
# fit= / order= validation
# --------------------------------------------------------------------------
def test_bad_fit_is_rejected_even_when_order_is_given():
    """fit= used to be ignored entirely whenever order= was passed."""
    with pytest.raises(ValueError, match="fit must be one of"):
        make_plot(0, np.arange(64.0)).image(order=3, fit="utter-nonsense")


def test_fit_error_names_every_legal_value():
    with pytest.raises(ValueError, match="fit must be one of") as exc:
        make_plot(0, [1.0, 2.0]).image(fit="nope")
    message = str(exc.value)
    for legal in ("auto", "square", "pad", "truncate"):
        assert legal in message


@pytest.mark.parametrize("order", [-1, -5])
def test_negative_order_is_rejected(order):
    with pytest.raises(ValueError, match="non-negative"):
        make_plot(0, np.arange(16.0)).image(order=order)


# --------------------------------------------------------------------------
# curve() lookup: strict about types, tolerant about spelling
# --------------------------------------------------------------------------
def test_curve_is_idempotent():
    original = curves.curve(7)
    assert curves.curve(original) is original


def test_curve_accepts_numpy_integers():
    assert curves.curve(np.int64(3)).index == 3


@pytest.mark.parametrize("bad", [True, False])
def test_curve_rejects_bool(bad):
    """bool is an int subclass, so curve(True) used to silently return Moore."""
    with pytest.raises(TypeError):
        curves.curve(bad)


@pytest.mark.parametrize("bad", [3.0, 3.5, None, (), b"Moore"])
def test_curve_rejects_non_integer_non_string(bad):
    with pytest.raises(TypeError):
        curves.curve(bad)


@pytest.mark.parametrize("bad", [-1, 40, 1000])
def test_curve_rejects_out_of_range_index(bad):
    with pytest.raises(IndexError):
        curves.curve(bad)


def test_curve_rejects_unknown_name_with_a_helpful_error():
    with pytest.raises(KeyError, match="did you mean"):
        curves.curve("Morre")  # typo -> the message should suggest real names


# --------------------------------------------------------------------------
# grid()/points() size guards
# --------------------------------------------------------------------------
@pytest.mark.parametrize("bad", [0, -1])
def test_grid_rejects_non_positive_n(bad):
    with pytest.raises(ValueError, match="n must be >= 1"):
        curves.curve(0).grid(bad)


@pytest.mark.parametrize("bad", [2.5, 4.0, None, "8"])
def test_grid_rejects_non_integer_n(bad):
    with pytest.raises(TypeError):
        curves.curve(0).grid(bad)


def test_points_refuses_an_order_that_cannot_fit_in_memory():
    """An order of 20 is 10^12 cells; it must say so rather than exhaust the machine."""
    with pytest.raises(ValueError, match=r"cell limit|GiB"):
        curves.curve(0).points(20)


def test_grid_refuses_a_side_that_cannot_fit_in_memory():
    with pytest.raises(ValueError, match=r"cell limit|GiB"):
        curves.curve(0).grid(10_000_000)


# --------------------------------------------------------------------------
# granulate
# --------------------------------------------------------------------------
@pytest.mark.parametrize("bad", [0, -1])
def test_granularity_must_be_positive(bad):
    with pytest.raises(ValueError, match="granularity"):
        make_plot(0, np.arange(16.0)).image(granularity=bad)


def test_granularity_larger_than_the_data_flattens_it():
    image = make_plot(0, np.arange(16.0)).image(granularity=100)
    assert np.allclose(image[np.isfinite(image)], np.arange(16.0).mean())


# --------------------------------------------------------------------------
# unroll
# --------------------------------------------------------------------------
@pytest.mark.parametrize(
    "array", [np.zeros((4, 8)), np.zeros(16), np.zeros((2, 2, 2)), np.zeros((0, 0))]
)
def test_unroll_rejects_non_square_or_wrong_rank(array):
    with pytest.raises(ValueError, match=r"square 2-D array|side >= 1"):
        curves.curve(0).unroll(array)


def test_unroll_accepts_a_nested_list():
    assert curves.curve(0).unroll([[0, 1], [3, 2]]).tolist() == [0, 3, 2, 1]


@pytest.mark.parametrize("index", FEASIBLE)
@pytest.mark.parametrize("side", [1, 3, 7, 10, 15])
def test_unroll_round_trips_at_arbitrary_sides_for_every_generalizing_curve(index, side):
    data = np.arange(side * side, dtype=float)
    image = make_plot(index, data).image()
    assert image.shape == (side, side)
    assert np.array_equal(curves.curve(index).unroll(image), data)


# --------------------------------------------------------------------------
# Lazy backend imports and damaged-installation diagnostics
# --------------------------------------------------------------------------
def test_every_render_entry_point_explains_how_to_install_matplotlib(monkeypatch):
    import builtins

    real_import = builtins.__import__

    def without_matplotlib(name, *args, **kwargs):
        if name == "matplotlib" or name.startswith("matplotlib."):
            raise ModuleNotFoundError(f"No module named {name!r}")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", without_matplotlib)
    plot = make_plot(0, np.arange(16.0))
    entry_points = [
        lambda: curves.curve(0).draw(2),
        lambda: curves.curve(0).show(2),
        lambda: plot.draw(),
        lambda: plot.show(),
        lambda: draw_gallery(curves.proper()),
    ]
    for call in entry_points:
        with pytest.raises(ModuleNotFoundError, match="required dependency 'matplotlib'"):
            call()


def test_numerical_operations_do_not_initialize_matplotlib(monkeypatch):
    import builtins

    real_import = builtins.__import__

    def without_matplotlib(name, *args, **kwargs):
        if name == "matplotlib" or name.startswith("matplotlib."):
            raise ModuleNotFoundError(f"No module named {name!r}")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", without_matplotlib)
    curve = curves.curve(0)
    assert curve.points(3).shape == (64, 2)
    assert curve.grid(10).shape == (100, 2)
    assert len(curve.word(3)) == 63
    assert curve.difference_map(3).shape == (8, 8)
    assert make_plot(0, np.arange(100.0)).image().shape == (10, 10)
    assert make_plot(0, np.arange(100.0)).fourier().shape == (10, 10)
    assert curve.unroll(np.zeros((8, 8))).shape == (64,)


# --------------------------------------------------------------------------
# Cache management
# --------------------------------------------------------------------------
def test_clear_cache_is_public_and_frees_the_generation_memo():
    from hilbertplot._core.generation import _codes

    curves.curve(0).points(6)
    assert _codes.cache_info().currsize > 0
    hp.config.clear_cache()
    assert _codes.cache_info().currsize == 0
    # and the library still works afterwards
    assert curves.curve(0).points(3).shape == (64, 2)


# --------------------------------------------------------------------------
# Data-integrity guards
# --------------------------------------------------------------------------
def test_non_numeric_data_is_rejected_clearly():
    with pytest.raises((TypeError, ValueError)):
        make_plot(0, ["a", "b", "c"])


def test_empty_data_is_rejected():
    with pytest.raises(ValueError, match="empty"):
        make_plot(0, [])


def test_two_dimensional_input_is_flattened_in_reading_order():
    plot = make_plot(0, np.arange(16.0).reshape(4, 4))
    assert len(plot) == 16
    assert plot.data.tolist() == list(range(16))


# --------------------------------------------------------------------------
# The package ships py.typed, so its annotations must be introspectable.
# --------------------------------------------------------------------------
def _public_callables():
    """Every public function, method and property getter, with a readable name."""
    from typing import get_type_hints  # noqa: F401 - imported by the caller

    found = []
    for namespace in (hp, hp.curves, hp.data, hp.config):
        for name in namespace.__all__:
            obj = getattr(namespace, name)
            if callable(obj) and not isinstance(obj, type):
                found.append((f"{namespace.__name__}.{name}", obj))
    for cls in (curves.Curve, curves.CurveList, _HilbertPlot):
        for attr in dir(cls):
            if attr.startswith("__"):
                continue
            member = getattr(cls, attr)
            if callable(member):
                found.append((f"{cls.__name__}.{attr}", member))
            elif isinstance(member, property) and member.fget is not None:
                found.append((f"{cls.__name__}.{attr}", member.fget))
    return found


def test_every_public_annotation_resolves_at_runtime():
    """``get_type_hints`` must not raise anywhere on the public surface.

    ``from __future__ import annotations`` makes annotations strings that are evaluated in
    the module namespace, so a name imported only under ``TYPE_CHECKING`` raises NameError
    at runtime -- which breaks Sphinx autodoc, pydantic, and anything else introspecting a
    ``py.typed`` package.  Matplotlib types therefore need runtime stand-ins.
    """
    failures = [
        problem for name, obj in _public_callables() if (problem := _hint_failure(name, obj))
    ]
    assert not failures, "annotations that do not resolve:\n  " + "\n  ".join(failures)


def _hint_failure(name: str, obj: object) -> str | None:
    """Return a description if ``get_type_hints`` raises for ``obj``, else ``None``."""
    from typing import get_type_hints

    try:
        get_type_hints(obj)
    except Exception as exc:
        return f"{name}: {type(exc).__name__}: {exc}"
    return None


def test_importing_the_package_does_not_import_matplotlib():
    """Importing the package must not eagerly initialize the plotting backend."""
    import subprocess
    import sys

    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys, hilbertplot; print(any(m.startswith('matplotlib') for m in sys.modules))",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "False", "importing hilbertplot pulled in matplotlib"


# --------------------------------------------------------------------------
# Coherence gaps found in review of this change set
# --------------------------------------------------------------------------
def test_fourier_knobs_are_reachable_from_draw():
    """`fourier()` grew `remove_dc`; `draw(fourier=True)` must expose the same knob."""
    plot = make_plot(0, np.tile([1.0, 0.0], 512))
    with_dc = plot.draw(fourier=True, remove_dc=False).images[-1].get_array()
    without = plot.draw(fourier=True, remove_dc=True).images[-1].get_array()
    assert not np.array_equal(with_dc, without)


def test_a_typo_of_a_draw_parameter_is_caught_not_forwarded_to_matplotlib():
    """Otherwise it surfaces as `AxesImage.set() got an unexpected keyword argument`."""
    with pytest.raises(TypeError, match="did you mean 'granularity'"):
        make_plot(0, np.arange(64.0)).draw(granularty=4)


def test_genuine_imshow_keywords_still_reach_matplotlib():
    ax = make_plot(0, np.arange(64.0)).draw(alpha=0.5, zorder=7)
    assert ax.images[-1].get_alpha() == 0.5


def test_curve_show_and_save_forward_ax_like_hilbertplot_does(tmp_path, monkeypatch):
    import matplotlib.pyplot as plt

    monkeypatch.setattr(plt, "show", lambda *a, **k: None)
    _, ax = plt.subplots()
    assert curves.curve(0).show(3, ax=ax) is ax
    _, ax2 = plt.subplots()
    out = tmp_path / "on-my-axes.png"
    assert curves.curve(0).save(str(out), 3, ax=ax2) == str(out)
    assert out.exists()


def test_a_bad_n_blames_the_argument_not_the_curve():
    """`grid(-2)` on an infeasible curve used to quote a size the caller never passed."""
    with pytest.raises(ValueError, match="n must be >= 1"):
        curves.curve("Moore").grid(-2)
    with pytest.raises(TypeError, match="n must be an int"):
        curves.curve("Moore").grid("10")


def test_plot_level_difference_and_label_maps_follow_the_plot_grid():
    """Curve.difference_map is 2**k-only; the plot's own grid may be an arbitrary square."""
    plot = make_plot(0, np.arange(100.0))  # tight 10x10, the fit="auto" default
    assert plot.image().shape == (10, 10)
    assert plot.difference_map().shape == (10, 10)
    assert plot.label_map().shape == (10, 10)
    assert sorted(plot.label_map().ravel().tolist()) == list(range(100))


def test_unknown_name_only_suggests_when_there_is_a_real_match():
    with pytest.raises(KeyError, match="did you mean one of 'Hilbert'"):
        curves.curve("Hilbrt")
    with pytest.raises(KeyError, match=re.escape("see hilbertplot.curves.catalog")):
        curves.curve("zzzzzz")


def test_curves_are_orderable_so_curvelists_sort():
    assert [c.name for c in sorted(curves.catalog())[:3]] == ["Hilbert", "Moore", "Liu1"]
    assert max(curves.proper()).index == 5
    assert min(curves.improper()).index == 6
    assert curves.curve(0) < curves.curve(1)
    assert curves.curve(0).__lt__("not a curve") is NotImplemented


def test_internal_curve_class_rejects_a_non_spec():
    """Internal handles require a real specification."""
    with pytest.raises(TypeError, match="Curve is internal"):
        curves.Curve(0)


def test_the_cell_limit_message_quotes_the_size_actually_being_built():
    """A word is one byte per stroke, not a 16-byte coordinate pair."""
    with pytest.raises(ValueError, match=re.escape("1,024.0 GiB")):
        curves.curve(0).word(20)
    with pytest.raises(ValueError, match=re.escape("16,384.0 GiB")):
        curves.curve(0).points(20)


def test_set_cell_limit_actually_reaches_the_guards():
    """A module-level constant read at import time would not; a function read at call time does."""
    previous = hp.config.set_cell_limit(4**5)
    try:
        assert hp.config.cell_limit() == 4**5
        curves.curve(0).points(5)  # exactly at the limit
        with pytest.raises(ValueError, match="cell limit"):
            curves.curve(0).points(6)
        with pytest.raises(ValueError, match="cell limit"):
            curves.curve(0).grid(64)
    finally:
        hp.config.set_cell_limit(previous)
    curves.curve(0).points(6)  # restored


# --------------------------------------------------------------------------
# Second review round: guards whose promises did not hold
# --------------------------------------------------------------------------
@pytest.mark.parametrize(
    "make",
    [
        lambda: np.arange(16.0),
        lambda: np.arange(16.0).reshape(4, 4).T,
        lambda: np.asfortranarray(np.arange(16.0).reshape(4, 4)),
        lambda: np.arange(32.0)[::2],
    ],
    ids=["c-contiguous", "transposed", "fortran-order", "strided"],
)
def test_data_is_immutable_through_every_route(make):
    """Freezing ndarray flags is not enough: an owner may always re-arm its own flag, and
    reshaping a non-contiguous input yields a fresh writable owner reachable as `.base`."""
    plot = make_plot(0, make())
    before = plot.data.copy()
    exposed = plot.data
    with pytest.raises(ValueError, match="read-only"):
        exposed[0] = -999.0
    with pytest.raises(ValueError, match="WRITEABLE"):
        exposed.setflags(write=True)
    base = exposed.base
    while isinstance(base, np.ndarray):
        assert not base.flags.writeable
        with pytest.raises(ValueError, match="WRITEABLE"):
            base.setflags(write=True)
        base = base.base
    assert np.array_equal(plot.data, before)


def test_masked_data_becomes_nan_rather_than_the_fill_value():
    """Masked entries are missing, not zero; NaN is what the renderer draws as blank."""
    masked = np.ma.masked_array([10.0, 20.0, 30.0, 40.0], mask=[True, False, True, False])
    plot = make_plot(0, masked)
    assert np.isnan(plot.data[0])
    assert np.isnan(plot.data[2])
    assert plot.data[1] == 20.0


@pytest.mark.parametrize(
    ("call", "kwargs"),
    [("points", {}), ("word", {}), ("label_map", {}), ("difference_map", {})],
)
def test_an_absurd_order_still_reports_the_cell_limit(call, kwargs):
    """The size arithmetic overflowed float above order 524, raising OverflowError from the
    one function whose whole job is to fail with a helpful message."""
    with pytest.raises(ValueError, match="cell limit"):
        getattr(curves.curve(0), call)(600, **kwargs)


def test_an_absurd_grid_side_still_reports_the_cell_limit():
    with pytest.raises(ValueError, match="cell limit"):
        curves.curve(0).grid(10**200)


@pytest.mark.parametrize("bad", [True, False, 2.5, 3.0, "3", None])
def test_granularity_is_type_checked_even_when_it_would_be_a_no_op(bad):
    """`granularity=True` used to slip through as "no coarsening" and yield a wrong plot."""
    with pytest.raises(TypeError, match="granularity must be an int"):
        make_plot(0, np.arange(64.0)).image(granularity=bad)


def test_is_space_filling_accepts_any_array_like():
    """It is exported as the tool for checking your own path; a list is the natural literal."""
    assert hp.curves.is_space_filling([[0, 0], [0, 1], [1, 1], [1, 0]], 2)
    assert not hp.curves.is_space_filling([[0, 0], [1, 1]], 2)


# --------------------------------------------------------------------------
# Third review round: cost of the guards themselves
# --------------------------------------------------------------------------
def test_construction_does_not_triple_peak_memory():
    """The immutability mechanism must not cost an extra full copy of the data.

    Freezing via `tobytes()` would make three copies live at once (caller's array, the
    private copy, the bytes); a read-only memoryview gives the same guarantee at two.
    """
    import subprocess
    import sys

    script = """
import numpy as np, tracemalloc
from hilbertplot._viz.hilbert_plot import hilbert_plot as make_plot
n = 8_000_000
# NumPy traces its data buffers. Start after imports so interpreter overhead and
# inherited process high-water marks cannot masquerade as another array copy.
tracemalloc.start()
data = np.arange(n, dtype=float)
plot = make_plot(0, data)
current, peak = tracemalloc.get_traced_memory()
if current < 2 * data.nbytes:
    raise AssertionError("NumPy data buffers were not tracked")
if plot.data[0] != 0.0:
    raise AssertionError("construction changed the input")
print(round(peak / data.nbytes, 2))
"""
    ratio = float(
        subprocess.run(
            [sys.executable, "-c", script], capture_output=True, text=True, check=True
        ).stdout.strip()
    )
    assert ratio < 2.8, f"peak was {ratio:.2f}x the data; a third full copy has crept in"


def test_rendering_does_not_copy_the_data_at_granularity_one():
    """`_layout` runs on every render; at granularity 1 the transform is the identity."""
    plot = make_plot(0, np.arange(1024.0))
    values, _, _ = plot._layout(1, None, "auto")
    assert values is plot._data, "granularity 1 copied the whole vector for nothing"
    coarsened, _, _ = plot._layout(4, None, "auto")
    assert coarsened is not plot._data


def test_a_rejected_draw_call_leaks_no_figure():
    """Argument checks must run before the figure is created, not after."""
    import matplotlib.pyplot as plt
    from matplotlib.colors import LogNorm

    plot = make_plot(0, np.arange(1.0, 65.0))
    plt.close("all")
    for _ in range(25):
        with pytest.raises(ValueError, match="either norm= or vmin"):
            plot.draw(norm=LogNorm(), vmin=1)
        with pytest.raises(TypeError, match="did you mean"):
            plot.draw(granularty=2)
    assert plt.get_fignums() == [], "rejected draw() calls left figures open"


def test_block_cells_floor_is_documented_and_honoured():
    """`_BLOCK_CELLS` is a termination condition, not only a speed knob: below 2 the
    recursion never bottoms out, so the floor must be stated where it is tuned."""
    from hilbertplot._core import arbitrary

    assert arbitrary._BLOCK_CELLS >= 2
    assert "at least 2" in arbitrary.__doc__ or "Must be at least 2" in (
        pathlib.Path(arbitrary.__file__).read_text()
    )
