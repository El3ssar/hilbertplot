"""Worked curve-construction diagrams, checked against the documented coordinates."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedLocator

import hilbertplot as hp


def figures(bg, fg, edge, colors):
    """Return teaching figures with visit numbers, directions and quadrant connections."""
    result = {}

    def board(ax, side):
        ax.set(xlim=(-0.5, side - 0.5), ylim=(-0.5, side - 0.5), aspect="equal")
        ax.set_xticks(range(side))
        ax.set_yticks(range(side))
        ax.xaxis.set_minor_locator(FixedLocator(np.arange(side + 1) - 0.5))
        ax.yaxis.set_minor_locator(FixedLocator(np.arange(side + 1) - 0.5))
        ax.grid(which="minor", color=edge, alpha=0.25, lw=0.6)
        ax.tick_params(which="minor", length=0)
        ax.tick_params(which="major", length=0, labelsize=9, pad=5)
        ax.set_xlabel("x (column)", fontsize=10)
        ax.set_ylabel("y (row)", fontsize=10)
        for spine in ax.spines.values():
            spine.set_visible(False)

    for index, name in [(0, "hilbert"), (5, "liu4")]:
        pts = hp.curves.points(index, order=2)
        color = colors[index]
        fig, ax = plt.subplots(figsize=(4.8, 4.8), layout="constrained")
        board(ax, 4)
        ax.plot(pts[:, 0], pts[:, 1], color=color, lw=2.2, zorder=2)
        for i, (x, y) in enumerate(pts):
            box = {
                "boxstyle": "square,pad=0.3" if i == 15 else "circle,pad=0.28",
                "fc": bg,
                "ec": color if i in (0, 15) else "none",
                "lw": 1.8,
            }
            ax.text(
                x, y, str(i), ha="center", va="center", fontsize=11, color=fg, bbox=box, zorder=4
            )
        ax.set_title(f"{hp.curves.info(index)['name']}, order 2", fontsize=13, pad=12)
        result[f"kernel-{name}"] = fig

    endpoints = {
        1: [((3, 0), (3, 3)), ((3, 4), (3, 7)), ((4, 7), (4, 4)), ((4, 3), (4, 0))],
        6: [((3, 2), (1, 3)), ((1, 4), (3, 5)), ((4, 5), (6, 4)), ((6, 3), (4, 2))],
    }
    for index, name, kernels in [
        (1, "moore", [0, 0, 0, 0]),
        (6, "improper", [5, 5, 5, 5]),
        (12, "mixed", [3, 5, 5, 3]),
    ]:
        pts = hp.curves.points(index, order=3)
        quadrants = np.split(pts, 4)
        if index in endpoints:
            np.testing.assert_array_equal(
                [(part[0], part[-1]) for part in quadrants], endpoints[index]
            )
        assert set(kernels) == set(hp.curves.info(index)["kernels"])
        fig, ax = plt.subplots(figsize=(6.2, 6.2), layout="constrained")
        board(ax, 8)
        ax.axvline(3.5, color=edge, ls="--", lw=1.3)
        ax.axhline(3.5, color=edge, ls="--", lw=1.3)
        for q, part in enumerate(quadrants):
            color = colors[kernels[q]]
            ax.plot(part[:, 0], part[:, 1], color=color, lw=2.1, zorder=2)
            ax.scatter(*part[0], marker="o", s=75, facecolor=bg, edgecolor=color, lw=1.8, zorder=5)
            ax.scatter(*part[-1], marker="s", s=65, facecolor=bg, edgecolor=color, lw=1.8, zorder=5)
            ax.annotate(
                "",
                xy=part[2],
                xytext=part[1],
                arrowprops={"arrowstyle": "->", "color": color, "lw": 2},
                zorder=4,
            )
            if q < 3:
                other = quadrants[q + 1]
                assert np.abs(part[-1] - other[0]).sum() == 1
                ax.annotate(
                    "",
                    xy=other[0],
                    xytext=part[-1],
                    arrowprops={
                        "arrowstyle": "->",
                        "color": "#df7644",
                        "lw": 2.5,
                        "shrinkA": 6,
                        "shrinkB": 6,
                    },
                    zorder=6,
                )
        for q, x, y in [(0, 1.5, -1.45), (1, 1.5, 8.0), (2, 5.5, 8.0), (3, 5.5, -1.45)]:
            reverse = (
                " (reversed)" if index in (6, 12) and q in ((1, 3) if index == 6 else (1,)) else ""
            )
            ax.text(
                x,
                y,
                f"Q{q}: kernel {kernels[q]}{reverse}",
                fontsize=9,
                ha="center",
                va="center",
                color=colors[kernels[q]],
                clip_on=False,
            )
        ax.set_title(f"{hp.curves.info(index)['name']}, order 3", fontsize=13, pad=34)
        ax.xaxis.labelpad = 24
        result[f"construction-{name}"] = fig
    return result


def catalog_assets(output):
    """Write one vector path per curve and a responsive catalog fragment."""
    from html import escape

    items = []
    colors = {"proper": "#477ab4", "improper": "#b37a3e", "inhomogeneous": "#9470b5"}
    for info in hp.curves.catalog():
        index = info["index"]
        points = hp.curves.points(index, order=3)
        xy = " ".join(f"{14 + 20 * x},{154 - 20 * y}" for x, y in points)
        first, last = points[0], points[-1]
        color = colors[info["kind"]]
        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 168 168">'
            f'<polyline points="{xy}" fill="none" stroke="{color}" '
            'stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<circle cx="{14 + 20 * first[0]}" cy="{154 - 20 * first[1]}" r="3" fill="{color}"/>'
            f'<rect x="{11 + 20 * last[0]}" y="{151 - 20 * last[1]}" width="6" height="6" '
            f'fill="{color}"/></svg>\n'
        )
        (output / f"catalog-{index}.svg").write_text(svg)
        label = escape(f"{index}: {info['name']}")
        kind = escape(info["kind"])
        kernels = ", ".join(map(str, info["kernels"]))
        items.append(
            f'<figure><a href="_static/generated/catalog-{index}.svg">'
            f'<img src="_static/generated/catalog-{index}.svg" alt="{label}, order 3"></a>'
            f"<figcaption><strong>{label}</strong><span>{kind}; kernels {kernels}</span>"
            "</figcaption></figure>"
        )
    (output / "catalog.inc").write_text('<div class="curve-catalog">' + "\n".join(items) + "</div>")
