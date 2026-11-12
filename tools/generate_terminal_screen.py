"""Make the original standby screen for the harbor service terminal."""

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def main() -> None:
    width, height = 1024, 640
    rng = np.random.default_rng(157)
    y, x = np.mgrid[:height, :width]
    noise = rng.normal(0, 1.8, (height, width))
    scan = np.where(y % 4 == 0, -2.5, 0.0)
    base = np.stack(
        (
            8 + noise + scan,
            36 + noise + scan,
            41 + noise + scan,
        ),
        axis=-1,
    )
    image = Image.fromarray(np.uint8(np.clip(base, 0, 255)), "RGB")
    draw = ImageDraw.Draw(image)
    font_file = "/usr/share/fonts/google-noto-vf/NotoSansMono[wght].ttf"
    heading = ImageFont.truetype(font_file, 43)
    regular = ImageFont.truetype(font_file, 28)
    small = ImageFont.truetype(font_file, 20)

    draw.rectangle((30, 30, 994, 610), outline=(67, 133, 139), width=3)
    draw.rectangle((55, 55, 72, 105), fill=(194, 121, 79))
    draw.text((96, 52), "HARBOR WORKS", font=heading, fill=(214, 226, 202))
    draw.text((98, 109), "SERVICE TERMINAL  /  UNIT 04", font=small, fill=(103, 170, 171))
    draw.line((98, 158, 944, 158), fill=(67, 133, 139), width=2)
    draw.text((98, 206), "SYSTEM READY", font=regular, fill=(216, 172, 100))
    draw.text((98, 268), "FAN CIRCUIT", font=small, fill=(145, 187, 179))
    draw.text((98, 310), "RUN DIAGNOSTIC AT WORKSTATION", font=regular, fill=(207, 219, 197))
    draw.line((98, 397, 944, 397), fill=(47, 98, 103), width=2)
    draw.text((98, 445), "SHIFT LOG  /  12 NOV 2026", font=small, fill=(145, 187, 179))
    draw.text((98, 488), "NO FAULT REPORT ON FILE", font=regular, fill=(207, 219, 197))
    draw.text((98, 565), "MORROW SERVICE COOPERATIVE", font=small, fill=(94, 154, 154))

    output = Path(__file__).resolve().parents[1] / "assets" / "textures" / "A157_terminal_screen.png"
    image.save(output, optimize=True)
    print(output, output.stat().st_size)


if __name__ == "__main__":
    main()
