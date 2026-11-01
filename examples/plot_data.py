"""One call, one plot: python examples/plot_data.py. Writes examples/output/."""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import hilbertplot as hp


def main():
    out = Path(__file__).parent / "output"
    out.mkdir(exist_ok=True)
    t = np.arange(1000)
    data = np.sin(2 * np.pi * t / 97) + 0.4 * np.cos(2 * np.pi * t / 31)
    for name, options in (
        ("data", {}),
        ("granularity", {"granularity": 16}),
        ("fourier", {"fourier": True, "window": True}),
        ("difference", {"difference": True}),
    ):
        fig = hp.plot(data, curve=12, **options)
        fig.savefig(out / f"{name}.png", dpi=160)
        plt.close(fig)
    fig = hp.plot(data, curve="Moore", cmap=["navy", "white", "firebrick"])
    fig.savefig(out / "colours.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    main()
