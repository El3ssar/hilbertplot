"""Render the catalogue as PNG grids.

    python examples/plot_catalog.py

Writes to examples/output/.
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import hilbertplot as hp

OUT = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT, exist_ok=True)


def main() -> None:
    fig = hp.gallery(
        hp.curves.homogeneous(),
        order=4,
        ncols=6,
        title="The 12 homogeneous Hilbert curves (order 4)",
    )
    fig.savefig(os.path.join(OUT, "homogeneous.png"), dpi=140)
    plt.close(fig)
    fig = hp.gallery(
        hp.curves.inhomogeneous(),
        order=3,
        ncols=7,
        title="The 28 inhomogeneous Hilbert curves (order 3)",
    )
    fig.savefig(os.path.join(OUT, "inhomogeneous.png"), dpi=140)
    plt.close(fig)
    fig = hp.gallery(
        hp.curves.catalog(),
        order=3,
        ncols=8,
        title="All 40 two-dimensional Hilbert curves (order 3)",
    )
    fig.savefig(os.path.join(OUT, "all40.png"), dpi=140)
    plt.close(fig)
    fig = hp.plot_curve(0, order=6)
    fig.savefig(os.path.join(OUT, "hilbert_order6.png"), dpi=140)
    plt.close(fig)
    print(f"wrote plots to {OUT}")


if __name__ == "__main__":
    main()
