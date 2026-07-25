"""Print the 40 curves grouped by family -- the lists print themselves as tables.

python examples/groups.py
"""

import hilbertplot


def main() -> None:
    print("Proper (kernel Hilbert)\n")
    print(hilbertplot.proper())

    print("\n\nImproper (kernel Liu4)\n")
    print(hilbertplot.improper())

    print("\n\nInhomogeneous by kernel mix\n")
    for kernels in ((3, 5), (0, 4), (1, 5), (1, 3, 5)):
        print(hilbertplot.by_kernels(*kernels))
        print()

    print(
        f"Totals: {len(hilbertplot.homogeneous())} homogeneous "
        f"({len(hilbertplot.proper())} proper + {len(hilbertplot.improper())} improper) "
        f"+ {len(hilbertplot.inhomogeneous())} inhomogeneous = {len(hilbertplot.catalog())}"
    )


if __name__ == "__main__":
    main()
