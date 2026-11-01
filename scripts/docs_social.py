"""Render the social sharing poster from the actual order-4 Hilbert path."""

from pathlib import Path

import matplotlib
from PIL import Image, ImageDraw, ImageFont

import hilbertplot as hp


def build(destination):
    """Write a 1200 by 630 PNG using bundled fonts for reproducible rendering."""
    scale = 2
    canvas = Image.new("RGB", (1200 * scale, 630 * scale), "#fbfaf7")
    draw = ImageDraw.Draw(canvas)
    fonts = Path(matplotlib.get_data_path()) / "fonts" / "ttf"

    def font(size, serif=False, mono=False):
        name = "DejaVuSerif.ttf" if serif else "DejaVuSansMono.ttf" if mono else "DejaVuSans.ttf"
        return ImageFont.truetype(str(fonts / name), round(size * scale))

    def text(xy, value, size, color="#202725", **options):
        draw.text(
            tuple(round(v * scale) for v in xy), value, font=font(size, **options), fill=color
        )

    def line(points, color, width=1):
        draw.line(
            [(round(x * scale), round(y * scale)) for x, y in points],
            fill=color,
            width=round(width * scale),
        )

    # An editorial title block paired with the same mathematical subject as the hero.
    line([(58, 58), (1142, 58)], "#dedfd8")
    text((58, 82), "PYTHON / SCIENTIFIC VISUALIZATION", 14, "#606963", mono=True)
    text((52, 181), "hilbertplot", 73, serif=True)
    text((58, 298), "Plot arrays along Hilbert curves.", 24)
    text((58, 337), "Convert images to sequences.", 24)
    line([(58, 419), (184, 419)], "#a56943", 3)
    text((58, 455), "40 curve constructions", 17, "#606963")
    text((58, 485), "NumPy + Matplotlib", 17, "#606963")
    text((58, 561), "el3ssar.github.io/hilbertplot", 15, "#285f86", mono=True)

    # Dense enough to show the recursive structure; endpoints remain distinct.
    left, top, right, bottom = 663, 98, 1142, 577
    draw.rectangle(
        tuple(round(v * scale) for v in (left, top, right, bottom)),
        fill="#f1f1eb",
        outline="#dedfd8",
        width=scale,
    )
    text((663, 74), "0 / HILBERT", 13, "#606963", mono=True)
    text((1049, 74), "ORDER 4", 13, "#606963", mono=True)
    points = hp.curves.points(0, order=4)
    coordinates = [(left + 34 + 27.4 * x, bottom - 34 - 27.4 * y) for x, y in points]
    line(coordinates, "#285f86", 3.3)
    x, y = coordinates[0]
    radius = 5 * scale
    draw.ellipse(
        (
            round(x * scale) - radius,
            round(y * scale) - radius,
            round(x * scale) + radius,
            round(y * scale) + radius,
        ),
        fill="#a56943",
    )
    x, y = coordinates[-1]
    draw.rectangle(
        (
            round(x * scale) - radius,
            round(y * scale) - radius,
            round(x * scale) + radius,
            round(y * scale) + radius,
        ),
        fill="#a56943",
    )
    canvas.resize((1200, 630), Image.Resampling.LANCZOS).save(destination, optimize=True)


if __name__ == "__main__":
    build(Path(__file__).resolve().parents[1] / "docs" / "_static" / "social-preview.png")
