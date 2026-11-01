"""Generate reproducible documentation figures in matching light and dark themes."""

from pathlib import Path


def brand(static):
    """Write the exact order-3 curve-0 SVG favicon."""
    import hilbertplot as hp

    pts = hp.curves.points(0, order=3)
    xy = " ".join(f"{10 + 6 * x},{54 - 6 * y}" for x, y in pts)
    (static / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
        '<rect width="64" height="64" rx="8" fill="#172538"/>'
        f'<polyline points="{xy}" fill="none" stroke="#a6c5ee" '
        'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>\n'
    )


def build(output: Path):
    """Build figures from public functions and the README's sequence generators."""
    import importlib.util

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.colors import LogNorm

    import hilbertplot as hp

    source = Path(__file__).resolve().parents[1] / "examples" / "readme_figures.py"
    spec = importlib.util.spec_from_file_location("readme_datasets", source)
    datasets = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(datasets)
    tm = datasets.thue_morse(4**10)
    regions = datasets.interleaved_periodic(4**7, seed=3)
    t = np.arange(4096)
    signed = np.sin(2 * np.pi * t / 97) + 0.4 * np.cos(2 * np.pi * t / 31)
    output.mkdir(parents=True, exist_ok=True)
    for previous in output.glob("*.png"):
        previous.unlink()
    (output / "hero.svg").unlink(missing_ok=True)
    brand(output.parent)
    from docs_constructions import catalog_assets

    catalog_assets(output)

    def render_theme(dark):
        bg, fg, edge = (
            ("#171d27", "#dce5f1", "#465469") if dark else ("#ffffff", "#243348", "#c7d1df")
        )
        blue, orange, purple = (
            ("#83b4f2", "#f2b36b", "#c9a1ed") if dark else ("#2864a0", "#b56716", "#8452a4")
        )
        kernel_colors = {0: blue, 1: "#4ca497", 3: purple, 4: "#ce7393", 5: orange}
        suffix = "-dark" if dark else ""
        with plt.rc_context(
            {
                "figure.facecolor": bg,
                "savefig.facecolor": bg,
                "axes.facecolor": bg,
                "text.color": fg,
                "axes.labelcolor": fg,
                "axes.edgecolor": edge,
                "xtick.color": fg,
                "ytick.color": fg,
                "font.family": "DejaVu Sans",
                "font.size": 10,
                "axes.spines.top": False,
                "axes.spines.right": False,
            }
        ):

            def improve_labels(fig):
                for ax in fig.axes:
                    ax.title.set_fontsize(12)
                    ax.tick_params(labelsize=10)

            def save(name, fig, dpi=170):
                improve_labels(fig)
                fig.savefig(
                    output / f"{name}{suffix}.png", dpi=dpi, bbox_inches="tight", facecolor=bg
                )
                plt.close(fig)

            def save_parts(fig, names):
                improve_labels(fig)
                fig.canvas.draw()
                renderer = fig.canvas.get_renderer()
                from matplotlib.transforms import Bbox

                axes = [ax for ax in fig.axes if ax.images or ax.lines]
                for ax, name in zip(axes, names, strict=True):
                    boxes = [ax.get_tightbbox(renderer)]
                    if ax.images and ax.images[0].colorbar is not None:
                        boxes.append(ax.images[0].colorbar.ax.get_tightbbox(renderer))
                    bounds = Bbox.union(boxes).transformed(fig.dpi_scale_trans.inverted())
                    fig.savefig(
                        output / f"{name}{suffix}.png",
                        dpi=200,
                        bbox_inches=bounds.expanded(1.04, 1.04),
                        facecolor=bg,
                    )

            def compare(name, items, render, columns=None):
                columns = columns or len(items)
                rows = (len(items) + columns - 1) // columns
                fig, axes = plt.subplots(
                    rows, columns, figsize=(4.5 * columns, 4.1 * rows), squeeze=False
                )
                for ax, item in zip(axes.flat, items, strict=False):
                    render(ax, item)
                for ax in list(axes.flat)[len(items) :]:
                    ax.set_visible(False)
                fig.tight_layout(pad=1.3)
                parts = {
                    "granularity": ["granularity-input", "granularity-result"],
                    "fitting": ["fit-pad", "fit-square", "fit-truncate"],
                    "colors": ["color-sequential", "color-diverging", "color-custom"],
                    "locality": ["locality-0", "locality-1", "locality-12", "locality-24"],
                    "modes": ["mode-line", "mode-fill"],
                    "windows": ["window-off", "window-on"],
                    "spectra": ["spectrum-0", "spectrum-12", "spectrum-24"],
                    "normalization": ["norm-linear", "norm-log"],
                    "granularities": ["granularity-1", "granularity-4", "granularity-12"],
                }
                if name in parts:
                    # Colorbar axes have no image; crop only the actual image panels.
                    image_axes = [ax for ax in fig.axes if ax.images or ax.lines]
                    if len(image_axes) == len(parts[name]):
                        save_parts(fig, parts[name])
                save(name, fig)

            save("curve", hp.plot_curve(0, order=3, color=blue, title="Hilbert (0), order 3"))
            save(
                "quasisquare",
                hp.plot_curve(3, shape=(15, 16), color=purple, title="Liu2 (3), 15 x 16"),
            )
            compare(
                "modes",
                ["line", "fill"],
                lambda ax, m: hp.plot_curve(
                    0,
                    order=4,
                    mode=m,
                    color=blue if m == "line" else None,
                    cmap="cividis",
                    ax=ax,
                    title=m.capitalize(),
                ),
            )
            compare(
                "shapes",
                [(10, 10), (15, 16), (16, 15)],
                lambda ax, s: hp.plot_curve(
                    0, shape=s, color=blue, ax=ax, title=f"{s[0]} x {s[1]}"
                ),
            )
            from docs_constructions import figures

            for name, fig in figures(bg, fg, edge, kernel_colors).items():
                save(name, fig)
            # Mapping examples use a ramp so visit order is visible without an analysis transform.
            for name, c in [("data", 0), ("moore", 1)]:
                save(
                    name,
                    hp.plot(
                        np.arange(256), curve=c, cmap="cividis", title=f"Visit order, curve {c}"
                    ),
                )
            compare(
                "fitting",
                ["pad", "square", "truncate"],
                lambda ax, f: hp.plot(
                    np.arange(900),
                    fit=f,
                    cmap="cividis",
                    vmin=0,
                    vmax=899,
                    colorbar=False,
                    ax=ax,
                    title=(
                        f"{f}: "
                        f"{hp.data.to_grid(np.arange(900), fit=f).shape[0]} x "
                        f"{hp.data.to_grid(np.arange(900), fit=f).shape[1]}"
                    ),
                ),
            )
            compare(
                "colors",
                ["cividis", "RdBu_r", ["#244b72", "#f4f3ed", "#a94835"]],
                lambda ax, cm: hp.plot(
                    signed,
                    cmap=cm,
                    vmin=-1.4,
                    vmax=1.4,
                    colorbar=False,
                    ax=ax,
                    title=cm if isinstance(cm, str) else "Custom diverging gradient",
                ),
            )
            positive = np.exp(3 * np.sin(t / 37))
            compare(
                "normalization",
                [False, True],
                lambda ax, log: hp.plot(
                    positive,
                    cmap="inferno",
                    norm=LogNorm(vmin=np.exp(-3), vmax=np.exp(3)) if log else None,
                    ax=ax,
                    title="Logarithmic normalization" if log else "Linear normalization",
                ),
            )
            missing = signed.copy()
            missing[300:700] = np.nan
            save("missing", hp.plot(missing, cmap="RdBu_r", title="Missing samples 300:700"))
            # Same generator, seed, length and granularity as examples/readme_figures.py.
            compare(
                "granularity",
                [1, 4],
                lambda ax, g: hp.plot(
                    regions,
                    granularity=g,
                    cmap="gray",
                    vmin=0,
                    vmax=1,
                    colorbar=False,
                    ax=ax,
                    title=f"Granularity {g}",
                ),
            )
            compare(
                "granularities",
                [1, 4, 12],
                lambda ax, g: hp.plot(
                    regions,
                    granularity=g,
                    cmap="gray",
                    vmin=0,
                    vmax=1,
                    colorbar=False,
                    ax=ax,
                    title=f"Granularity {g}",
                ),
            )
            fig, ax = plt.subplots(figsize=(10, 2.8))
            ax.step(
                np.arange(72),
                np.tile([1, 0, 0, 1], 18),
                where="mid",
                color=blue,
                label="Period 4",
                lw=1,
            )
            ax.step(
                np.arange(72),
                np.tile([1, 1, 0, 1, 0, 0], 12) + 1.5,
                where="mid",
                color=orange,
                label="Period 6 (offset +1.5)",
                lw=1,
            )
            ax.set(xlabel="Sequence index", yticks=[0, 0.5, 1, 1.5, 2, 2.5])
            ax.legend(frameon=False, ncols=2, fontsize=9)
            fig.tight_layout()
            save("signal", fig)
            fig, axes = plt.subplots(2, 1, figsize=(10, 4), sharex=True)
            for ax, p in zip(axes, [[1, 0, 0, 1], [1, 1, 0, 1, 0, 0]], strict=True):
                v = np.tile(p, 24)[:72]
                ax.step(np.arange(72), v, where="mid", color=edge, lw=1, label="Original")
                ax.step(
                    np.arange(72),
                    hp.data.granulate(v, 4),
                    where="mid",
                    color=blue if len(p) == 4 else orange,
                    lw=2,
                    label="Granularity 4",
                )
                ax.set(ylim=(-0.1, 1.1), ylabel=f"Period {len(p)}")
            axes[0].legend(frameon=False, ncols=2, fontsize=9)
            axes[1].set_xlabel("Sequence index")
            fig.tight_layout()
            save("block_means", fig)

            def fft(ax, curve=0, window=True, cmap="gray_r"):
                lo, hi = np.percentile(hp.data.fourier(tm, curve=curve, window=window), [2, 99.5])
                hp.plot(
                    tm,
                    curve=curve,
                    fourier=True,
                    window=window,
                    cmap=cmap,
                    vmin=lo,
                    vmax=hi,
                    colorbar=False,
                    ax=ax,
                    title=f"2-D FFT, curve {curve}" if window else "2-D FFT, no window",
                )

            fig, axes = plt.subplots(1, 2, figsize=(10.2, 5))
            hp.plot(
                tm, cmap="gray", colorbar=False, ax=axes[0], title="Thue-Morse: 1,048,576 samples"
            )
            fft(axes[1])
            fig.tight_layout()
            save_parts(fig, ["fourier-input", "fourier-spectrum"])
            save("fourier", fig, dpi=200)
            compare("windows", [False, True], lambda ax, w: fft(ax, window=w))
            compare("spectra", [0, 12, 24], lambda ax, c: fft(ax, curve=c, cmap="magma"))
            # A shared log scale shows small distances and larger quadrant jumps.
            fields = [hp.curves.difference_map(c, order=5) for c in [0, 1, 12, 24]]
            vmax = max(float(f.max()) for f in fields)
            compare(
                "locality",
                [0, 1, 12, 24],
                lambda ax, c: hp.plot(
                    np.arange(1024),
                    curve=c,
                    difference=True,
                    cmap="inferno",
                    norm=LogNorm(vmin=1, vmax=vmax),
                    ax=ax,
                    colorbar=True,
                    title=f"Curve {c}",
                ),
                columns=2,
            )
            save(
                "difference",
                hp.plot(
                    np.arange(1024),
                    difference=True,
                    cmap="inferno",
                    norm=LogNorm(vmin=1, vmax=vmax),
                    title="Mean neighbour visit-index distance",
                ),
            )
            fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.7))
            for ax, c in zip(axes, [0, 1], strict=True):
                hp.plot(
                    np.arange(16),
                    curve=c,
                    cmap="cividis",
                    colorbar=False,
                    ax=ax,
                    title=f"{hp.curves.info(c)['name']}: visit indices",
                )
                labels = hp.curves.label_map(c, order=2)
                for y in range(4):
                    for x in range(4):
                        ax.text(
                            x,
                            y,
                            str(labels[y, x]),
                            ha="center",
                            va="center",
                            fontsize=13,
                            color="white" if labels[y, x] < 8 else "#172538",
                        )
            fig.tight_layout()
            save_parts(fig, ["labels-hilbert", "labels-moore"])
            save("labels", fig)
            y, x = np.mgrid[0:32, 0:32]
            rgb = np.full((32, 32, 3), 242, dtype=np.uint8)
            rgb[3:14, 3:14] = [49, 104, 173]
            rgb[(x - 22) ** 2 + (y - 10) ** 2 <= 36] = [218, 128, 56]
            rgb[(y > 18) & (np.abs(x - y + 6) < 3)] = [67, 143, 117]
            seq = hp.data.from_grid(rgb, curve=0)
            reconstructed = hp.data.to_grid(seq, curve=0, shape=rgb.shape)
            permuted = hp.data.to_grid(seq, curve=12, shape=rgb.shape)
            np.testing.assert_array_equal(rgb, reconstructed)
            fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.1))
            for ax, img, title in zip(
                axes,
                [rgb, reconstructed, permuted],
                ["Input RGB image", "Curve 0: exact reconstruction", "Curve 12: reordered pixels"],
                strict=True,
            ):
                ax.imshow(img, origin="lower")
                ax.set_title(title, fontsize=10)
                ax.set_axis_off()
            fig.tight_layout()
            save_parts(fig, ["rgb-input", "rgb-restored", "rgb-permuted"])
            save("rgb_roundtrip", fig)
            fig, ax = plt.subplots(figsize=(8, 2.4))
            ax.plot(seq[:150], color=blue, lw=1)
            ax.set(xlabel="Flattened component index (R, G, B per pixel)", ylabel="Value")
            fig.tight_layout()
            save("rgb_sequence", fig)

    for dark in (False, True):
        render_theme(dark)


if __name__ == "__main__":
    build(Path(__file__).resolve().parents[1] / "docs" / "_static" / "generated")
