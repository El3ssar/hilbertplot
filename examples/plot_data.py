"""Visualise 1-D data as Hilbert plots.

    python examples/plot_data.py

Writes to examples/output/:
* data_periodic.png    -- periodic ·10· as a checkerboard (reproduces Fig. 6)
* data_granularity.png -- one interleaved sequence at three granularities (cf. Fig. 8)
* data_curves.png      -- the same data mapped through six different curves
"""

import os

import numpy as np

import hilbertplot as hp

OUT = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT, exist_ok=True)


def interleaved_sequence(n):
    """Random interleaving of ·1001· (period 4) and ·1101011· (period 7) chunks."""
    rng = np.random.default_rng(0)
    blocks = {4: [1, 0, 0, 1], 7: [1, 1, 0, 1, 0, 1, 1]}
    out = []
    while len(out) < n:
        out += blocks[rng.choice([4, 7])] * rng.integers(3, 8)
    return np.array(out[:n], dtype=float)


def main() -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # 1) periodic ·10· -> checkerboard, coloured with a custom colour sweep
    hp.hilbert_plot(0, np.tile([1, 0], 4**6 // 2)).save(
        os.path.join(OUT, "data_periodic.png"), "gray",
        title="Periodic ·10·  (Hilbert plot)")

    # 2) the same data at three granularities (granularity chosen per render)
    data = interleaved_sequence(4**7)
    plot = hp.hilbert_plot(0, data)
    fig, axes = plt.subplots(1, 3, figsize=(11, 4))
    for ax, g in zip(axes, (1, 4, 7)):
        label = "faithful" if g == 1 else f"{g}-granularity"
        plot.draw("gray_r", granularity=g, ax=ax, title=label)
    fig.suptitle("Interleaved ·1001· / ·1101011· at three granularities", fontsize=12)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "data_granularity.png"), dpi=140, bbox_inches="tight")
    plt.close(fig)

    # 3) the same signal through several different curves
    signal = np.sin(np.linspace(0, 40 * np.pi, 4**6)) + np.linspace(0, 2, 4**6)
    fig, axes = plt.subplots(2, 3, figsize=(10, 7))
    for ax, i in zip(axes.ravel(), (0, 1, 3, 5, 9, 12)):
        hp.hilbert_plot(i, signal).draw("viridis", ax=ax)
    fig.suptitle("One signal, six different curve mappings", fontsize=12)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "data_curves.png"), dpi=140, bbox_inches="tight")
    plt.close(fig)

    # 4) numbers 1..100 with a custom colour sweep (red -> green -> blue)
    hp.hilbert_plot(0, np.arange(1, 101)).save(
        os.path.join(OUT, "data_colours.png"), ["red", "green", "tab:blue"],
        fit="truncate", title="1..100  swept red -> green -> blue")

    # 5) the difference-map overlay, toggled and at two thresholds
    plot = hp.hilbert_plot(0, np.arange(4**5))
    fig, axes = plt.subplots(1, 3, figsize=(11, 4))
    plot.draw("gray", ax=axes[0], title="Hilbert plot")
    plot.draw("gray", ax=axes[1], difference=True, title="+ difference map (thr=1.0)")
    plot.draw("gray", ax=axes[2], difference=True, difference_threshold=0.4,
              title="+ difference map (thr=0.4)")
    fig.suptitle("Where the curve breaks locality (difference map overlay)", fontsize=12)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "data_difference.png"), dpi=140, bbox_inches="tight")
    plt.close(fig)

    # 6) Fourier maps: hidden structure made visible (cf. the paper's Fig. 7/9)
    def thue_morse(n):
        s = [0]
        while len(s) < n:
            s = s + [1 - x for x in s]
        return np.array(s[:n], dtype=float)

    rng = np.random.default_rng(0)
    N = 4 ** 7
    signals = {
        "Thue-Morse": thue_morse(N),
        "period-97 + noise": np.sin(2 * np.pi * np.arange(N) / 97) + 0.8 * rng.standard_normal(N),
        "two tones": np.sin(2 * np.pi * np.arange(N) / 64) + np.sin(2 * np.pi * np.arange(N) / 31),
    }
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    for col, (name, data) in enumerate(signals.items()):
        plot = hp.hilbert_plot(0, data)
        plot.draw("gray", ax=axes[0, col], title=name)
        plot.draw("magma", ax=axes[1, col], fourier=True, window=True,
                  title=f"{name} - Fourier map")
    fig.suptitle("Hilbert plots and their 2-D Fourier maps", fontsize=12)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "data_fourier.png"), dpi=120, bbox_inches="tight")
    plt.close(fig)

    print(f"wrote data plots to {OUT}")


if __name__ == "__main__":
    main()
