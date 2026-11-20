"""Split a web export's engine into parts, since a Cloudflare Worker serves at most 25 MiB a file."""

import gzip
import json
import sys
from pathlib import Path


PART_SIZE = 4 * 1024 * 1024
ENGINE_TAG = '<script src="index.js"></script>'

root = Path(sys.argv[1] if len(sys.argv) > 1 else "build/web")
engine = root / "index.wasm"
raw = engine.read_bytes()
assert raw[:4] == b"\0asm", "Not a WebAssembly build"
for old in root.glob("index.wasm*.part*"):
    old.unlink()


def write_parts(data: bytes, prefix: str) -> list[str]:
    names = []
    for offset in range(0, len(data), PART_SIZE):
        name = f"{prefix}.part{offset // PART_SIZE}"
        (root / name).write_bytes(data[offset : offset + PART_SIZE])
        names.append(name)
    return names


compressed = gzip.compress(raw, compresslevel=9, mtime=0)
asset = {
    "size": len(raw),
    "parts": write_parts(raw, "index.wasm"),
    "gzip_parts": write_parts(compressed, "index.wasm.gz"),
}
assert b"".join((root / name).read_bytes() for name in asset["parts"]) == raw
assert gzip.decompress(b"".join((root / name).read_bytes() for name in asset["gzip_parts"])) == raw
engine.unlink()

loader = """// Godot fetches index.wasm whole, so this answers that fetch from the parts.
(() => {
  const asset = ASSET;
  const nativeFetch = window.fetch.bind(window);
  const engine = new URL('index.wasm', document.currentScript.src).href;
  const gzip = typeof DecompressionStream === 'function';
  window.fetch = async (resource, options) => {
    const url = new URL(resource instanceof Request ? resource.url : String(resource), location.href);
    if (url.href !== engine) return nativeFetch(resource, options);
    const responses = (gzip ? asset.gzip_parts : asset.parts).map((part) => nativeFetch(new URL(part, engine), options));
    const stream = new ReadableStream({
      async start(controller) {
        try {
          for (const pending of responses) {
            const response = await pending;
            if (!response.ok) throw new Error(`Engine download failed: ${response.status}`);
            const reader = response.body.getReader();
            for (let chunk = await reader.read(); !chunk.done; chunk = await reader.read()) controller.enqueue(chunk.value);
          }
          controller.close();
        } catch (error) {
          controller.error(error);
        }
      },
    });
    const body = gzip ? stream.pipeThrough(new DecompressionStream('gzip')) : stream;
    return new Response(body, {headers: {'Content-Type': 'application/wasm', 'Content-Length': String(asset.size)}});
  };
})();
""".replace("ASSET", json.dumps(asset))
(root / "wasm-loader.js").write_text(loader)

page = root / "index.html"
html = page.read_text()
if "wasm-loader.js" not in html:
    assert html.count(ENGINE_TAG) == 1, "index.html does not load index.js once"
    page.write_text(html.replace(ENGINE_TAG, f'<script src="wasm-loader.js"></script>\n\t\t{ENGINE_TAG}'))
(root / ".nojekyll").unlink(missing_ok=True)
assert max(path.stat().st_size for path in root.iterdir() if path.is_file()) < 25 * 1024 * 1024
print(f"index.wasm: {len(asset['parts'])} parts, {len(asset['gzip_parts'])} gzip parts")
