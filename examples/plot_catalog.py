"""Render the catalogue as PNG grids.

    python examples/plot_catalog.py

Writes to examples/output/.
"""

import os

import hilbertplot as hp

OUT = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT, exist_ok=True)


def main() -> None:
    hp.gallery(
        hp.homogeneous(),
        order=4,
        ncols=6,
        title="The 12 homogeneous Hilbert curves (order 4)",
        save=os.path.join(OUT, "homogeneous.png"),
    )
    hp.gallery(
        hp.inhomogeneous(),
        order=3,
        ncols=7,
        title="The 28 inhomogeneous Hilbert curves (order 3)",
        save=os.path.join(OUT, "inhomogeneous.png"),
    )
    hp.gallery(
        hp.catalog(),
        order=3,
        ncols=8,
        title="All 40 two-dimensional Hilbert curves (order 3)",
        save=os.path.join(OUT, "all40.png"),
    )
    hp.curve(0).save(6, os.path.join(OUT, "hilbert_order6.png"))
    print(f"wrote plots to {OUT}")


if __name__ == "__main__":
    main()
