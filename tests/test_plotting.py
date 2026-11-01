"""Headless smoke tests for the plotting API (Agg backend, no window)."""

import matplotlib
import pytest

matplotlib.use("Agg")

from hilbertplot._core import curve as curves
from hilbertplot._viz.hilbert_plot import hilbert_plot as make_plot
from hilbertplot._viz.render import gallery as draw_gallery


def test_draw_returns_axes():
    ax = curves.curve(0).draw(3)
    line_and_collections = len(ax.lines) + len(ax.collections)
    assert line_and_collections > 0


def test_save_writes_file(tmp_path):
    out = tmp_path / "hilbert.png"
    returned = curves.curve("hilbert").save(str(out), 4)
    assert returned == str(out)
    assert out.exists()
    assert out.stat().st_size > 0


def test_solid_colour_option(tmp_path):
    out = tmp_path / "solid.png"
    curves.curve(12).save(str(out), 3, color="steelblue", endpoints=False)
    assert out.exists()


def test_gallery_saves_grid(tmp_path):
    out = tmp_path / "grid.png"
    fig = draw_gallery(curves.improper(), order=2, save=str(out))
    assert out.exists()
    assert len(fig.axes) >= 6


def test_line_mode_draws_a_path():
    ax = curves.curve(0).draw(4, mode="line")
    assert len(ax.lines) + len(ax.collections) > 0
    assert not ax.images


def test_fill_mode_draws_an_image():
    ax = curves.curve(0).draw(4, mode="fill")
    assert len(ax.images) == 1


def test_auto_mode_switches_to_fill_at_high_order():
    assert len(curves.curve(0).draw(3).images) == 0  # low order -> line
    assert len(curves.curve(0).draw(9).images) == 1  # high order -> fill image


def test_bad_mode_rejected():
    with pytest.raises(ValueError, match="mode must be one of"):
        curves.curve(0).draw(3, mode="nope")


def test_hilbertplot_draw_returns_image_axes():
    import numpy as np

    ax = curves.curve(0).plot_data(np.arange(256)).draw()
    assert len(ax.images) == 1


def test_hilbertplot_draw_accepts_a_colormap_name():
    import numpy as np

    ax = make_plot(0, np.arange(256)).draw("gray")
    assert len(ax.images) == 1


def test_hilbertplot_draw_accepts_a_colour_list():
    import numpy as np

    ax = make_plot(0, np.arange(1, 101)).draw(["red", "green", "tab:blue"])
    assert len(ax.images) == 1


def test_hilbertplot_save(tmp_path):
    import numpy as np

    out = tmp_path / "data.png"
    returned = make_plot("moore", np.tile([1, 0], 512)).save(str(out), "gray", granularity=2)
    assert returned == str(out)
    assert out.exists()
    assert out.stat().st_size > 0


def test_colour_list_interpolates_between_endpoints():
    from hilbertplot._viz.hilbert_plot import _resolve_cmap

    cm = _resolve_cmap(["red", "green", "tab:blue"])
    lo, hi = cm(0.0), cm(1.0)
    assert lo[0] > 0.9  # starts red
    assert lo[1] < 0.1
    assert hi[2] > 0.5  # ends blue-ish
    assert hi[0] < 0.5


def test_empty_colour_list_rejected():
    from hilbertplot._viz.hilbert_plot import _resolve_cmap

    with pytest.raises(ValueError, match="colour list is empty"):
        _resolve_cmap([])


def test_difference_map_replaces_the_data_image():
    import numpy as np

    data = np.arange(4096)
    ax = make_plot(0, data).draw("gray", difference=True)
    assert len(ax.images) == 1
    np.testing.assert_array_equal(ax.images[0].get_array(), curves.curve(0).difference_map(6))


def test_difference_map_flows_through_save(tmp_path):
    import numpy as np

    out = tmp_path / "diff.png"
    make_plot(0, np.arange(1024)).save(str(out), "viridis", difference=True)
    assert out.exists()
    assert out.stat().st_size > 0


def test_fourier_returns_spectrum_shape():
    import numpy as np

    spec = make_plot(0, np.zeros(1024)).fourier()
    assert spec.shape == (32, 32)
    assert np.isfinite(spec).all()


def test_fourier_reveals_hidden_periodicity():
    import numpy as np

    # a signal that looks noisy as a Hilbert plot but has a clean period:
    n = 4**5
    data = np.sin(2 * np.pi * np.arange(n) / 8.0)  # period-8 tone
    spec = make_plot(0, data).fourier()
    centre = spec.shape[0] // 2
    peak = np.unravel_index(np.argmax(spec), spec.shape)
    assert peak != (centre, centre)  # structure, not just DC


def test_fourier_toggle_draws_an_image():
    import numpy as np

    ax = make_plot(0, np.arange(1024)).draw("magma", fourier=True)
    assert len(ax.images) == 1
    assert "Fourier" in ax.get_title()


def test_fourier_flows_through_save(tmp_path):
    import numpy as np

    out = tmp_path / "fft.png"
    make_plot(0, np.arange(4096)).save(str(out), "magma", fourier=True, window=True)
    assert out.exists()
    assert out.stat().st_size > 0


# --------------------------------------------------------------------------
# The renamed verb and the new render options
# --------------------------------------------------------------------------
def test_plot_is_gone_in_favour_of_draw():
    """One verb for "render onto axes", shared with HilbertPlot.draw."""
    assert not hasattr(curves.curve(0), "plot")
    assert callable(curves.curve(0).draw)
    assert callable(make_plot(0, [1.0]).draw)


def test_curve_show_returns_the_axes(monkeypatch):
    import matplotlib.pyplot as plt

    monkeypatch.setattr(plt, "show", lambda *a, **k: None)
    ax = curves.curve(0).show(3)
    assert ax is not None
    assert len(ax.lines) + len(ax.collections) > 0


def test_hilbertplot_show_returns_the_axes(monkeypatch):
    import matplotlib.pyplot as plt
    import numpy as np

    monkeypatch.setattr(plt, "show", lambda *a, **k: None)
    ax = make_plot(0, np.arange(64)).show()
    assert len(ax.images) == 1


def test_colorbar_option_attaches_one():
    import numpy as np

    ax = make_plot(0, np.arange(64)).draw(colorbar=True)
    # the colourbar lives on its own axes, added to the same figure
    assert len(ax.get_figure().axes) == 2


def test_draw_exposes_the_mappable_for_a_manual_colorbar():
    import numpy as np

    ax = make_plot(0, np.arange(64)).draw()
    assert ax.images
    ax.get_figure().colorbar(ax.images[-1], ax=ax)  # must not raise


def test_a_caller_supplied_norm_reaches_matplotlib():
    """A norm carries its own limits, so draw() must not also pass its default vmin/vmax."""
    import numpy as np
    from matplotlib.colors import LogNorm

    ax = make_plot(0, np.arange(1, 65)).draw(norm=LogNorm())
    assert isinstance(ax.images[-1].norm, LogNorm)


def test_norm_together_with_vmin_is_rejected_with_a_clear_message():
    import numpy as np
    from matplotlib.colors import LogNorm

    with pytest.raises(ValueError, match="either norm= or vmin"):
        make_plot(0, np.arange(1, 65)).draw(norm=LogNorm(), vmin=1)


def test_save_failure_does_not_leak_the_figure():
    import matplotlib.pyplot as plt
    import numpy as np

    plt.close("all")
    for _ in range(5):
        with pytest.raises(Exception):  # noqa: B017,PT011 - any savefig failure will do
            make_plot(0, np.arange(16)).save("/nonexistent-dir/x.png")
    assert plt.get_fignums() == [], "a failed save left figures open"


def test_curve_save_rejects_the_old_argument_order_with_a_clear_message(tmp_path):
    with pytest.raises(TypeError, match="now takes"):
        curves.curve(0).save(3, str(tmp_path / "swapped.png"))


# --------------------------------------------------------------------------
# Notebook reprs (matplotlib present here; absence is covered in test_robustness)
# --------------------------------------------------------------------------
def test_curve_renders_inline_as_png():
    data = curves.curve(0)._repr_png_()
    assert isinstance(data, bytes)
    assert data[:8] == b"\x89PNG\r\n\x1a\n"


def test_hilbertplot_renders_inline_as_png():
    import numpy as np

    data = make_plot(0, np.arange(256))._repr_png_()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"


def test_inline_render_does_not_leak_figures():
    import matplotlib.pyplot as plt

    plt.close("all")
    for index in (0, 1, 5):
        curves.curve(index)._repr_png_()
    assert plt.get_fignums() == []


def test_curvelist_gallery_saves(tmp_path):
    out = tmp_path / "group.png"
    fig = curves.by_kernels(3, 5).gallery(order=2, save=str(out))
    assert out.exists()
    assert len(fig.axes) >= 6


def test_gallery_rejects_bad_ncols():
    with pytest.raises(ValueError, match="ncols"):
        draw_gallery(curves.proper(), ncols=0)


def test_gallery_rejects_an_empty_group():
    with pytest.raises(ValueError, match="no curves to plot"):
        draw_gallery(curves.by_kernels(2))  # kernel 2 is never used
