"""Build deterministic scientific illustrations and branding from the public API."""

from pathlib import Path


def brand(static):
    """Write an SVG favicon containing curve 0, order 3, without smoothing the path."""
    import hilbertplot as hp

    points = hp.curves.points(0, order=3)
    coordinates = " ".join(f"{10 + 6 * x},{54 - 6 * y}" for x, y in points)
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
        '<rect width="64" height="64" rx="12" fill="#102c35"/>'
        f'<polyline points="{coordinates}" fill="none" stroke="#79e3ce" '
        'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
        "</svg>\n"
    )
    (static / "favicon.svg").write_text(svg)


def build(output: Path):
    """Generate the gallery, comparisons and exact-conversion demonstrations."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.colors import LinearSegmentedColormap, LogNorm

    import hilbertplot as hp

    output.mkdir(parents=True, exist_ok=True)
    brand(output.parent)
    plt.rcParams.update(
        {
            "figure.facecolor": "#ffffff",
            "savefig.facecolor": "#ffffff",
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.titleweight": "normal",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.labelcolor": "#294650",
            "text.color": "#18343e",
            "axes.edgecolor": "#b7c8cd",
        }
    )
    t = np.arange(4096)
    values = np.sin(2 * np.pi * t / 97) + 0.4 * np.cos(2 * np.pi * t / 31)

    def save(name, fig):
        fig.savefig(output / f"{name}.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

    def compare(name, items, render, *, columns=None):
        columns = columns or len(items)
        rows = (len(items) + columns - 1) // columns
        fig, axes = plt.subplots(rows, columns, figsize=(4 * columns, 3.8 * rows), squeeze=False)
        for ax, item in zip(axes.flat, items, strict=False):
            render(ax, item)
        for ax in list(axes.flat)[len(items) :]:
            ax.set_visible(False)
        fig.tight_layout(pad=1.5)
        save(name, fig)

    save("curve", hp.plot_curve(0, order=4, title="Hilbert / order 4"))
    save("quasisquare", hp.plot_curve(3, shape=(15, 16), mode="line", title="Liu2 / 15 x 16"))
    for name, kw in {
        "data": {"curve": 0, "title": "Hilbert / 4096 samples"},
        "moore": {"curve": "Moore", "title": "Moore / same samples"},
        "fourier": {
            "fourier": True,
            "window": True,
            "cmap": "magma",
            "title": "Centred FFT magnitude",
        },
        "difference": {
            "difference": True,
            "cmap": "magma",
            "title": "Mean neighbour index distance",
        },
        "granularity": {"granularity": 16, "title": "Blocks of 16 / means repeated"},
    }.items():
        save(name, hp.plot(values, **kw))
    save("catalog", hp.gallery(order=3, ncols=5))
    save("proper", hp.gallery(hp.curves.proper(), order=3, ncols=3))
    save("improper", hp.gallery(hp.curves.improper(), order=3, ncols=3))
    save("generalizing", hp.gallery(hp.curves.generalizing(), order=3, ncols=4))

    compare(
        "orders",
        [1, 2, 3, 4],
        lambda ax, k: hp.plot_curve(0, order=k, ax=ax, title=f"Order {k} / {4**k} cells"),
    )
    compare(
        "modes",
        ["line", "fill"],
        lambda ax, mode: hp.plot_curve(0, order=4, mode=mode, ax=ax, title=mode.capitalize()),
    )
    compare(
        "shapes",
        [(10, 10), (15, 16), (16, 15)],
        lambda ax, shape: hp.plot_curve(
            0, shape=shape, mode="line", ax=ax, title=f"{shape[0]} x {shape[1]}"
        ),
    )
    compare(
        "curves_signal",
        [0, 1, 12, 24],
        lambda ax, c: hp.plot(
            values, curve=c, ax=ax, colorbar=False, title=f"Curve {c} / {hp.curves.info(c)['name']}"
        ),
        columns=2,
    )
    compare(
        "fitting",
        ["pad", "square", "truncate"],
        lambda ax, fit: hp.plot(
            np.arange(900),
            fit=fit,
            ax=ax,
            title=f"{fit} / side {hp.data.to_grid(np.arange(900), fit=fit).shape[0]}",
            colorbar=False,
        ),
    )
    compare(
        "granularities",
        [1, 4, 16, 64],
        lambda ax, g: hp.plot(
            values, granularity=g, ax=ax, title=f"Block length {g}", colorbar=False
        ),
        columns=2,
    )
    compare(
        "windows",
        [False, True],
        lambda ax, w: hp.plot(
            values,
            fourier=True,
            window=w,
            cmap="magma",
            ax=ax,
            title=f"Hann window: {w}",
            colorbar=False,
        ),
    )
    compare(
        "spectra",
        [0, 1, 12],
        lambda ax, c: hp.plot(
            values,
            curve=c,
            fourier=True,
            window=True,
            cmap="magma",
            ax=ax,
            title=f"Fourier / curve {c}",
            colorbar=False,
        ),
    )
    compare(
        "locality",
        [0, 1, 12, 24],
        lambda ax, c: hp.plot(
            values,
            curve=c,
            difference=True,
            cmap="magma",
            ax=ax,
            vmin=0,
            vmax=4095,
            title=f"Curve {c} / common scale",
            colorbar=False,
        ),
        columns=2,
    )
    compare(
        "colors",
        ["viridis", "magma", ["#12343f", "#81d8c0", "#fff0b8"]],
        lambda ax, cm: hp.plot(
            values,
            cmap=cm,
            ax=ax,
            title=cm if isinstance(cm, str) else "Custom color stops",
            colorbar=False,
        ),
    )
    heavy = np.exp(3 * np.sin(t / 37))
    compare(
        "normalization",
        [False, True],
        lambda ax, log: hp.plot(
            heavy,
            ax=ax,
            norm=LogNorm() if log else None,
            cmap="magma",
            title="Logarithmic colors" if log else "Linear colors",
        ),
    )

    fig, ax = plt.subplots(figsize=(10, 2.4))
    ax.plot(t[:400], values[:400], color="#147d86", lw=1.5)
    ax.set(xlabel="Sequence index", ylabel="Value", title="Two periods / one input sequence")
    fig.tight_layout()
    save("signal", fig)
    fig, ax = plt.subplots(figsize=(10, 2.6))
    small = values[:160]
    ax.plot(small, color="#91a6ad", lw=1, label="Original")
    ax.step(
        np.arange(160),
        hp.data.granulate(small, 16),
        where="mid",
        color="#137b80",
        lw=2,
        label="Block length 16",
    )
    ax.legend(frameon=False, ncols=2)
    ax.set(xlabel="Sequence index", ylabel="Value")
    fig.tight_layout()
    save("block_means", fig)

    y, x = np.mgrid[0:32, 0:32]
    rgb = np.stack((x / 31, y / 31, 0.5 + 0.5 * np.sin((x + y) / 5)), axis=-1)
    sequence = hp.data.from_grid(rgb, curve=0)
    permuted = hp.data.to_grid(sequence, curve=12, shape=rgb.shape)
    restored = hp.data.to_grid(sequence, curve=0, shape=rgb.shape)
    np.testing.assert_array_equal(restored, rgb)
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for ax, img, title in zip(
        axes,
        [rgb, restored, permuted],
        ["Original RGB image", "Same curve / exact recovery", "Write with curve 12 / reordered"],
        strict=True,
    ):
        ax.imshow(img, origin="lower")
        ax.set_title(title, fontsize=10)
        ax.set_axis_off()
    fig.tight_layout()
    save("rgb_roundtrip", fig)

    fig, ax = plt.subplots(figsize=(6, 2.8))
    ax.plot(sequence[:150], color="#147d86", lw=1)
    ax.set(
        xlabel="Flattened value index (R, G, B per pixel)",
        ylabel="Channel value",
        title="The image read along curve 0",
    )
    fig.tight_layout()
    save("rgb_sequence", fig)
    missing = values.copy()
    missing[300:700] = np.nan
    save("missing", hp.plot(missing, title="Missing sequence interval / transparent cells"))
    compare(
        "labels",
        [0, 12],
        lambda ax, c: (
            ax.imshow(hp.curves.label_map(c, order=3), origin="lower", cmap="viridis"),
            ax.set_title(f"Visit indices / curve {c}"),
            ax.set_axis_off(),
        ),
    )

    # A wide, transparent artwork for the landing page, using the actual path.
    fig, ax = plt.subplots(figsize=(7, 7))
    hp.plot_curve(
        0,
        order=4,
        ax=ax,
        cmap=LinearSegmentedColormap.from_list("hero", ["#118c91", "#7fd9ba", "#d99c43"]),
        linewidth=2.3,
        endpoints=False,
        title="",
    )
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    fig.savefig(output / "hero.svg", transparent=True, bbox_inches="tight", pad_inches=0)
    plt.close(fig)


if __name__ == "__main__":
    build(Path(__file__).resolve().parents[1] / "docs" / "_static" / "generated")
