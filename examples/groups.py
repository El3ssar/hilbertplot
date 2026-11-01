"""Print the curve groups using ordinary dictionaries: python examples/groups.py."""

import hilbertplot as hp


def main():
    for group in (hp.curves.proper(), hp.curves.improper(), hp.curves.inhomogeneous()):
        for c in group:
            print(f"{c['index']:2}  {c['name']:24}  {c['kind']:15}  kernels={c['kernels']}")
        print()


if __name__ == "__main__":
    main()
