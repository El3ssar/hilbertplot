"""Headless smoke tests for the plotting API (Agg backend, no window)."""

import matplotlib
import pytest

matplotlib.use("Agg")

import hilbertplot as hp  # noqa: E402


def test_plot_returns_axes():
    ax = hp.curve(0).plot(3)
    line_and_collections = len(ax.lines) + len(ax.collections)
    assert line_and_collections > 0


def test_save_writes_file(tmp_path):
    out = tmp_path / "hilbert.png"
    returned = hp.curve("hilbert").save(4, str(out))
    assert returned == str(out)
    assert out.exists() and out.stat().st_size > 0


def test_solid_colour_option(tmp_path):
    out = tmp_path / "solid.png"
    hp.curve(12).save(3, str(out), color="steelblue", endpoints=False)
    assert out.exists()


def test_gallery_saves_grid(tmp_path):
    out = tmp_path / "grid.png"
    fig = hp.gallery(hp.improper(), order=2, save=str(out))
    assert out.exists()
    assert len(fig.axes) >= 6


def test_line_mode_draws_a_path():
    ax = hp.curve(0).plot(4, mode="line")
    assert len(ax.lines) + len(ax.collections) > 0
    assert not ax.images


def test_fill_mode_draws_an_image():
    ax = hp.curve(0).plot(4, mode="fill")
    assert len(ax.images) == 1


def test_auto_mode_switches_to_fill_at_high_order():
    assert len(hp.curve(0).plot(3).images) == 0  # low order -> line
    assert len(hp.curve(0).plot(9).images) == 1  # high order -> fill image


def test_bad_mode_rejected():
    with pytest.raises(ValueError):
        hp.curve(0).plot(3, mode="nope")


def test_hilbertplot_draw_returns_image_axes():
    import numpy as np
    ax = hp.curve(0).plot_data(np.arange(256)).draw()
    assert len(ax.images) == 1


def test_hilbertplot_draw_accepts_a_colormap_name():
    import numpy as np
    ax = hp.hilbert_plot(0, np.arange(256)).draw("gray")
    assert len(ax.images) == 1


def test_hilbertplot_draw_accepts_a_colour_list():
    import numpy as np
    ax = hp.hilbert_plot(0, np.arange(1, 101)).draw(["red", "green", "tab:blue"])
    assert len(ax.images) == 1


def test_hilbertplot_save(tmp_path):
    import numpy as np
    out = tmp_path / "data.png"
    returned = hp.hilbert_plot("moore", np.tile([1, 0], 512)).save(
        str(out), "gray", granularity=2)
    assert returned == str(out)
    assert out.exists() and out.stat().st_size > 0


def test_colour_list_interpolates_between_endpoints():
    from hilbertplot._viz.hilbert_plot import _resolve_cmap
    cm = _resolve_cmap(["red", "green", "tab:blue"])
    lo, hi = cm(0.0), cm(1.0)
    assert lo[0] > 0.9 and lo[1] < 0.1        # starts red
    assert hi[2] > 0.5 and hi[0] < 0.5        # ends blue-ish


def test_empty_colour_list_rejected():
    from hilbertplot._viz.hilbert_plot import _resolve_cmap
    with pytest.raises(ValueError):
        _resolve_cmap([])


def test_difference_overlay_adds_a_layer():
    import numpy as np
    data = np.arange(4096)
    without = hp.hilbert_plot(0, data).draw("gray")
    with_overlay = hp.hilbert_plot(0, data).draw("gray", difference=True)
    assert len(without.images) == 1
    assert len(with_overlay.images) == 2      # data image + barrier overlay


def test_difference_overlay_flows_through_save(tmp_path):
    import numpy as np
    out = tmp_path / "diff.png"
    hp.hilbert_plot(0, np.arange(1024)).save(
        str(out), "viridis", difference=True, difference_threshold=0.5)
    assert out.exists() and out.stat().st_size > 0


def test_fourier_returns_spectrum_shape():
    import numpy as np
    spec = hp.hilbert_plot(0, np.zeros(1024)).fourier()
    assert spec.shape == (32, 32)
    assert np.isfinite(spec).all()


def test_fourier_reveals_hidden_periodicity():
    import numpy as np
    # a signal that looks noisy as a Hilbert plot but has a clean period:
    n = 4 ** 5
    data = np.sin(2 * np.pi * np.arange(n) / 8.0)      # period-8 tone
    spec = hp.hilbert_plot(0, data).fourier(remove_dc=True) if False else \
        hp.hilbert_plot(0, data).fourier()
    centre = spec.shape[0] // 2
    peak = np.unravel_index(np.argmax(spec), spec.shape)
    assert peak != (centre, centre)                    # structure, not just DC


def test_fourier_toggle_draws_an_image():
    import numpy as np
    ax = hp.hilbert_plot(0, np.arange(1024)).draw("magma", fourier=True)
    assert len(ax.images) == 1
    assert "Fourier" in ax.get_title()


def test_fourier_flows_through_save(tmp_path):
    import numpy as np
    out = tmp_path / "fft.png"
    hp.hilbert_plot(0, np.arange(4096)).save(str(out), "magma", fourier=True, window=True)
    assert out.exists() and out.stat().st_size > 0
