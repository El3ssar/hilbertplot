"""Regenerate the figures shown in the README.

    python examples/readme_figures.py

Writes to assets/:
* curve.png            -- curve 0 at order 4, drawn as a colour-graded path
* data_two_curves.png  -- the numbers 1-256 laid on curve 0 and on curve 32
* difference.png       -- the difference-map overlay at two thresholds
* thue_morse.png       -- a Thue-Morse sequence and its 2-D Fourier map
* granularity.png      -- periodic regions that only appear once coarse-grained
"""

import os

import numpy as np

import hilbertplot as hp

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")


def thue_morse(n):
    """The first ``n`` terms of the Thue-Morse sequence."""
    s = [0]
    while len(s) < n:
        s = s + [1 - x for x in s]
    return np.array(s[:n], dtype=float)


def interleaved_periodic(n, seed=3):
    """A random interleaving of two periodic patterns of *equal* density.

    ``.1001.`` (period 4) and ``.110100.`` (period 6) both have density 1/2, so no
    stretch is brighter than another and the faithful plot is featureless noise.  Every
    chunk length is a multiple of 12, which keeps chunk starts aligned to the
    granularity-4 block grid -- so 4-granularity collapses the period-4 stretches to a
    constant (solid blocks) while the period-6 ones keep varying.
    """
    p4, p6 = [1, 0, 0, 1], [1, 1, 0, 1, 0, 0]
    rng = np.random.default_rng(seed)
    seq = []
    while len(seq) < n:
        p = p4 if rng.integers(2) else p6
        length = 12 * int(rng.integers(16, 110))
        seq += (p * (-(-length // len(p))))[:length]
    return np.array(seq[:n], dtype=float)


def main() -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    os.makedirs(OUT, exist_ok=True)
    plt.rcParams.update({"figure.facecolor": "white", "savefig.facecolor": "white"})

    def save(fig, name, dpi=140):
        fig.savefig(os.path.join(OUT, name), dpi=dpi, bbox_inches="tight")
        plt.close(fig)

    # 1) the curve itself, colour-graded along the traversal
    fig, ax = plt.subplots(figsize=(5.2, 5.2))
    hp.curve(0).draw(4, ax=ax, cmap="viridis", title="The Hilbert curve (curve 0), order 4")
    save(fig, "curve.png")

    # 2) the same data laid on two different curves
    data = np.arange(1, 257)
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.9))
    hp.hilbert_plot(0, data).draw("viridis", ax=axes[0], title="curve 0 — Hilbert")
    hp.hilbert_plot(32, data).draw("viridis", ax=axes[1], title="curve 32 — Moore+Liu4 #1")
    fig.suptitle("The same data (1–256) laid on two different curves", fontsize=13, y=1.02)
    save(fig, "data_two_curves.png")

    # 3) where the curve breaks locality, at two thresholds
    plot = hp.hilbert_plot(0, np.arange(4**5))
    fig, axes = plt.subplots(1, 3, figsize=(12.6, 4.6))
    plot.draw("gray", ax=axes[0], title="Hilbert plot")
    for ax, thr in ((axes[1], 1.5), (axes[2], 0.5)):
        plot.draw(
            "gray",
            ax=ax,
            difference=True,
            difference_threshold=thr,
            difference_color="#ff3b30",
            title=f"difference map (threshold {thr})",
        )
    fig.suptitle(
        "Where the curve breaks locality — a higher threshold marks fewer, worse sites",
        fontsize=13,
        y=1.02,
    )
    save(fig, "difference.png")

    # 4) a Thue-Morse sequence and its Fourier map (paper-style: light ground)
    plot = hp.hilbert_plot(0, thue_morse(4**8))
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.9))
    plot.draw("gray", ax=axes[0], title="Thue–Morse sequence")
    lo, hi = np.percentile(plot.fourier(window=True), [2.0, 99.5])
    plot.draw(
        "gray_r",
        ax=axes[1],
        fourier=True,
        window=True,
        vmin=lo,
        vmax=hi,
        title="its 2-D Fourier map",
    )
    fig.suptitle("A Thue–Morse sequence and its self-similar Fourier map", fontsize=13, y=1.02)
    save(fig, "thue_morse.png")

    # 5) periodic regions that only show up once you coarse-grain
    plot = hp.hilbert_plot(0, interleaved_periodic(4**7))
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.9))
    plot.draw("gray", ax=axes[0], title="faithful — featureless noise")
    plot.draw("gray", ax=axes[1], granularity=4, title="granularity 4 — regions appear")
    fig.suptitle(
        "Periodic regions hidden in a binary sequence, exposed by coarse-graining",
        fontsize=13,
        y=1.02,
    )
    save(fig, "granularity.png")

    print(f"wrote README figures to {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
