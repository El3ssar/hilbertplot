"""Exercise the public API; each plotting call creates its own figure.

Run: python examples/try_api.py
Headless: MPLBACKEND=Agg python examples/try_api.py --save-only
Images are saved to examples/output/try_api/.
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm

import hilbertplot as hp


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save-only", action="store_true")
    args = parser.parse_args()
    t = np.arange(1000)
    values = np.exp(np.sin(2 * np.pi * t / 97) + 0.4 * np.cos(2 * np.pi * t / 31))

    # Each entry is a separate call and a separate figure, never automatic subplots.
    figures = {
        "curve_line": hp.plot_curve(12, order=4),
        "curve_solid": hp.plot_curve("Moore", order=4, color="steelblue", linewidth=2),
        "curve_fill": hp.plot_curve(0, order=5, mode="fill"),
        "arbitrary_square_line": hp.plot_curve(3, shape=(15, 15), mode="line"),
        "quasisquare_line": hp.plot_curve(3, shape=(15, 16), mode="line"),
        "data_index": hp.plot(values, curve=12),
        "data_label": hp.plot(values, curve="Moore", cmap=["navy", "white", "firebrick"]),
        "granularity": hp.plot(values, curve=12, granularity=16),
        "fourier": hp.plot(values, curve=12, fourier=True, window=True),
        "fourier_raw": hp.plot(values, curve=12, fourier=True, log=False, remove_dc=False),
        "difference": hp.plot(values, curve=12, difference=True),
        "log_colours": hp.plot(values, norm=LogNorm(), colorbar=True),
        "compact_square": hp.plot(values[:900], fit="square"),
        "truncate": hp.plot(values, fit="truncate"),
        "fixed_order": hp.plot(values, order=6),
        "gallery": hp.gallery([0, "Moore", 12], order=3),
    }

    # Plot on existing axes when composing your own Matplotlib figures.
    fig, ax = plt.subplots()
    assert hp.plot(values, curve="12H", ax=ax, vmin=0, vmax=5, alpha=0.9) is fig
    figures["existing_axes"] = fig

    # Numeric outputs stay under hp.data; no custom objects are involved.
    image = hp.data.to_grid(values, curve=12)
    np.testing.assert_allclose(hp.data.from_grid(image, curve=12, length=len(values)), values)
    # Read one curve's grid along another curve, then reverse that permutation.
    reordered = hp.data.from_grid(image, curve=0)
    restored_grid = hp.data.to_grid(reordered, curve=0)
    np.testing.assert_allclose(restored_grid, image, equal_nan=True)
    # Images (including RGB) become a flat 1-D sequence and reconstruct exactly.
    rgb = np.arange(16 * 16 * 3, dtype=np.uint16).reshape(16, 16, 3)
    sequence = hp.data.from_grid(rgb, curve=12)
    assert sequence.ndim == 1
    restored = hp.data.to_grid(sequence, curve=12, shape=rgb.shape)
    np.testing.assert_array_equal(restored, rgb)
    assert restored.dtype == rgb.dtype
    quasisquare = np.arange(15 * 16, dtype=np.uint64).reshape(15, 16) + 2**63
    sequence = hp.data.from_grid(quasisquare, curve=3)
    np.testing.assert_array_equal(
        hp.data.to_grid(sequence, curve=3, shape=quasisquare.shape), quasisquare
    )
    spectrum = hp.data.fourier(values, curve=12, window=True)
    assert spectrum.shape == image.shape
    averaged = hp.data.granulate(values, 16)
    assert len(averaged) == len(values)
    assert np.allclose(averaged[:16], values[:16].mean())
    assert hp.data.to_grid(values[:900], fit="auto").shape == (30, 30)
    assert hp.data.to_grid(values, fit="truncate").shape == (16, 16)
    compact = hp.data.to_grid(values[:900], fit="square")
    np.testing.assert_allclose(hp.data.from_grid(compact), values[:900])

    # Curve metadata, groups, geometry and indexing stay under hp.curves.
    print([(c["index"], c["name"]) for c in hp.curves.catalog()])
    assert hp.curves.info("Moore")["index"] == 1
    for group in (
        hp.curves.proper(),
        hp.curves.improper(),
        hp.curves.homogeneous(),
        hp.curves.inhomogeneous(),
        hp.curves.closed(),
        hp.curves.generalizing(),
        hp.curves.by_kernels(3, 5),
    ):
        print([c["index"] for c in group])
    side = image.shape[0]
    labels = hp.curves.label_map(12, side=side)
    differences = hp.curves.difference_map(12, side=side)
    assert labels.shape == differences.shape == image.shape
    pts = hp.curves.points(12, order=4)
    assert hp.curves.is_space_filling(pts, 16)
    assert len(hp.curves.word(12, order=4)) == len(pts) - 1
    assert hp.curves.is_space_filling(hp.curves.grid(30), 30)
    assert hp.curves.canonical_form(pts) == hp.curves.canonical_form(pts[::-1])
    xy = hp.curves.index_to_xy(10**18, 40, curve=12)
    assert hp.curves.xy_to_index(*xy, 40, curve=12) == 10**18

    # Transform flags are mutually exclusive and fail before creating a figure.
    try:
        hp.plot(values, fourier=True, difference=True)
    except ValueError:
        print("Mutually exclusive Fourier/difference flags: OK")
    else:
        raise AssertionError("Conflicting transformations should have failed")

    # Optional resource controls stay under hp.config.
    limit = hp.config.cell_limit()
    previous = hp.config.set_cell_limit(4**10)
    try:
        assert hp.config.cell_limit() == 4**10
    finally:
        hp.config.set_cell_limit(previous)
    assert hp.config.cell_limit() == limit
    print(hp.config.cache_info())
    hp.config.clear_cache()

    out = Path(__file__).parent / "output" / "try_api"
    out.mkdir(parents=True, exist_ok=True)
    for name, figure in figures.items():
        figure.savefig(out / f"{name}.png", dpi=150)
    print(f"All checks passed; {len(figures)} separate figures saved to {out}")
    if not args.save_only:
        plt.show()
    for figure in figures.values():
        plt.close(figure)


if __name__ == "__main__":
    main()
