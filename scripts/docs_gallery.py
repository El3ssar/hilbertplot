"""Reproducible documentation figures generated with the public hilbertplot API."""

from pathlib import Path


def build(output: Path):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    import hilbertplot as hp

    output.mkdir(parents=True, exist_ok=True)
    t = np.arange(4096)
    values = np.sin(2 * np.pi * t / 97) + 0.4 * np.cos(2 * np.pi * t / 31)
    plt.rcParams.update({"figure.facecolor": "white", "savefig.facecolor": "white"})
    figures = {
        "curve": hp.plot_curve(0, order=4, title="Hilbert curve · order 4"),
        "quasisquare": hp.plot_curve(3, shape=(15, 16), mode="line", title="Liu2 · 15 x 16"),
        "data": hp.plot(values, curve=0, title="A sequence on the Hilbert curve"),
        "moore": hp.plot(values, curve="Moore", title="The same sequence on Moore"),
        "fourier": hp.plot(
            values, fourier=True, window=True, cmap="magma", title="2-D Fourier map"
        ),
        "difference": hp.plot(values, difference=True, cmap="magma", title="Locality-loss field"),
        "granularity": hp.plot(values, granularity=16, title="Consecutive blocks averaged at 16"),
        "catalog": hp.gallery(order=3, ncols=8),
    }
    for name, fig in figures.items():
        fig.savefig(output / f"{name}.png", dpi=130, bbox_inches="tight")
        plt.close(fig)


if __name__ == "__main__":
    build(Path(__file__).resolve().parents[1] / "docs" / "_static" / "generated")
