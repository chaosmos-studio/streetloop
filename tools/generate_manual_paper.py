"""Generate an original worn-paper surface for the service manual UI."""

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def main() -> None:
    width, height = 1024, 768
    rng = np.random.default_rng(156)
    y, x = np.mgrid[:height, :width]
    grain = rng.normal(0, 2.4, (height, width))
    warm = 1.4 * np.sin(x / 78) + 1.1 * np.sin(y / 51)
    edge = np.minimum.reduce((x, y, width - x - 1, height - y - 1))
    edge_tone = np.clip((36 - edge) / 36, 0, 1) * 9
    base = np.stack(
        (
            224 + grain + warm - edge_tone,
            211 + grain + warm - edge_tone * 1.3,
            179 + grain + warm - edge_tone * 1.7,
        ),
        axis=-1,
    )
    paper = Image.fromarray(np.uint8(np.clip(base, 0, 255)), "RGB").convert("RGBA")

    fibers = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(fibers)
    for _ in range(5100):
        px = int(rng.integers(0, width))
        py = int(rng.integers(0, height))
        length = int(rng.integers(2, 15))
        shade = (106, 90, 67, int(rng.integers(3, 15)))
        draw.line((px, py, px + length, py + int(rng.integers(-1, 2))), fill=shade)
    paper = Image.alpha_composite(paper, fibers)

    washes = Image.new("RGBA", (width, height))
    wash_draw = ImageDraw.Draw(washes)
    for cx, cy, radius, opacity in ((110, 155, 130, 10), (900, 685, 160, 9), (520, 60, 115, 6)):
        wash_draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=(135, 91, 46, opacity))
    paper = Image.alpha_composite(paper, washes.filter(ImageFilter.GaussianBlur(75)))

    detail = Image.new("RGBA", (width, height))
    detail_draw = ImageDraw.Draw(detail)
    for offset in (0, 7, 14):
        detail_draw.line((offset, 0, offset, height), fill=(29, 68, 70, 180 - offset * 7), width=2)
    detail_draw.line((width - 7, 10, width - 7, height - 10), fill=(114, 91, 66, 34), width=2)
    detail_draw.line((16, height - 15, width - 16, height - 15), fill=(114, 91, 66, 38), width=2)
    paper = Image.alpha_composite(paper, detail)

    output = Path(__file__).resolve().parents[1] / "assets" / "textures" / "A156_manual_paper.png"
    paper.convert("RGB").save(output, optimize=True)
    print(output, output.stat().st_size)


if __name__ == "__main__":
    main()
