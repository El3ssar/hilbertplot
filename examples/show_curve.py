"""Draw a curve: python examples/show_curve.py 12 4 --save curve.png."""

import argparse

import matplotlib.pyplot as plt

import hilbertplot as hp


def main():
    parser = argparse.ArgumentParser(description="Draw a curve by index or label")
    parser.add_argument("curve", nargs="?", default="0")
    parser.add_argument("order", type=int, nargs="?", default=4)
    parser.add_argument("--save", metavar="FILE")
    parser.add_argument("--mode", choices=("auto", "line", "fill"), default="auto")
    parser.add_argument("--solid", action="store_true")
    args = parser.parse_args()
    selector = int(args.curve) if args.curve.lstrip("-").isdigit() else args.curve
    fig = hp.plot_curve(
        selector, order=args.order, mode=args.mode, color="steelblue" if args.solid else None
    )
    if args.save:
        fig.savefig(args.save, dpi=160)
        plt.close(fig)
    else:
        plt.show()


if __name__ == "__main__":
    main()
