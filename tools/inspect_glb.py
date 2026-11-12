"""Report the authored mesh and material cost of a binary glTF asset."""

import json
import struct
import sys
from pathlib import Path


def inspect(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    magic, version, declared_size = struct.unpack_from("<III", raw)
    if magic != 0x46546C67 or version != 2 or declared_size != len(raw):
        raise ValueError(f"Invalid glTF 2 binary header: {path}")
    json_size, chunk_type = struct.unpack_from("<II", raw, 12)
    if chunk_type != 0x4E4F534A:
        raise ValueError(f"Missing JSON chunk: {path}")
    document = json.loads(raw[20:20 + json_size])
    accessors = document.get("accessors", [])
    triangles = 0
    primitives = 0
    for mesh in document.get("meshes", []):
        for primitive in mesh.get("primitives", []):
            if primitive.get("mode", 4) != 4:
                continue
            accessor_id = primitive.get("indices")
            count = accessors[accessor_id]["count"] if accessor_id is not None else accessors[primitive["attributes"]["POSITION"]]["count"]
            triangles += count // 3
            primitives += 1
    return {
        "path": str(path),
        "bytes": len(raw),
        "nodes": len(document.get("nodes", [])),
        "meshes": len(document.get("meshes", [])),
        "materials": len(document.get("materials", [])),
        "images": len(document.get("images", [])),
        "triangles": triangles,
        "primitives": primitives,
    }


if __name__ == "__main__":
    for argument in sys.argv[1:]:
        print(json.dumps(inspect(Path(argument)), indent=2))
