"""Generate seamless neutral cotton and denim weave for tintable garments."""

import math
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/textures/characters"
SIZE = 256


def texture(kind):
    image = Image.new("RGB", (SIZE, SIZE))
    pixels = image.load()
    for y in range(SIZE):
        for x in range(SIZE):
            warp = math.cos(math.tau * (x % 8) / 8)
            weft = math.cos(math.tau * (y % 8) / 8)
            offset = 2 * math.cos(math.tau * x / 64) * math.cos(math.tau * y / 64)
            if kind == "denim":
                diagonal = math.cos(math.tau * ((x - y) % 12) / 12)
                value = 226 + int(8 * diagonal + 4 * warp + 2 * weft + offset)
            else:
                value = 228 + int(6 * warp + 6 * weft + 3 * warp * weft + offset)
            pixels[x, y] = (value, value, value)
    OUT.mkdir(parents=True, exist_ok=True)
    image.save(OUT / f"{kind}_weave.png")


for fabric in ("cotton", "denim"):
    texture(fabric)
