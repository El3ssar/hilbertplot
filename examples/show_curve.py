"""Plot a single curve: `python examples/show_curve.py <curve> <order> [--save FILE]`.

Examples
--------
    python examples/show_curve.py 0 5           # Hilbert, order 5 (opens a window)
    python examples/show_curve.py 12 4          # inhomogeneous IH12, order 4
    python examples/show_curve.py moore 6 --save moore6.png
    python examples/show_curve.py 9 4 --solid   # single colour instead of gradient
"""

import argparse

import hilbertplot as hp


def main() -> None:
    p = argparse.ArgumentParser(description="Plot Hilbert curve i of order j.")
    p.add_argument("curve", help="curve index 0-39 or name (e.g. 'hilbert', 'moore')")
    p.add_argument("order", type=int, help="order j (recursion depth)")
    p.add_argument("--save", metavar="FILE", help="save to FILE instead of showing")
    p.add_argument("--mode", choices=("auto", "line", "fill"), default="auto",
                   help="line = polyline, fill = visit-order heatmap (default: auto)")
    p.add_argument("--solid", action="store_true", help="solid colour, no gradient")
    args = p.parse_args()

    which = int(args.curve) if args.curve.lstrip("-").isdigit() else args.curve
    c = hp.curve(which)
    style = {"mode": args.mode}
    if args.solid:
        style["color"] = "steelblue"

    print(f"{c.symbol}  {c.name}  |  {c.kind}  |  kernels={c.combination}  "
          f"|  {4 ** args.order} cells")

    if args.save:
        c.save(args.order, args.save, **style)
        print(f"saved -> {args.save}")
    else:
        c.show(args.order, **style)


if __name__ == "__main__":
    main()
