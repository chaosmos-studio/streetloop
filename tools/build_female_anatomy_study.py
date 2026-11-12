"""Preserve an editable second anatomical base for original identities."""

from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = Path("/tmp/human-base-meshes-bundle-v1.4.1/human_base_meshes_bundle.blend")
SOURCE = ROOT / "art/source/A001_female_anatomy_study.blend"


def main():
    if not BUNDLE.is_file():
        raise FileNotFoundError(BUNDLE)
    bpy.ops.wm.open_mainfile(filepath=str(BUNDLE))
    bpy.context.preferences.filepaths.save_version = 0
    names = {"GEO-body_female_realistic", "GEO-body_female_realistic.eye.L", "GEO-body_female_realistic.eye.R"}
    for obj in list(bpy.data.objects):
        if obj.name not in names:
            bpy.data.objects.remove(obj, do_unlink=True)
    body = bpy.data.objects["GEO-body_female_realistic"]
    eyes = [bpy.data.objects[name] for name in sorted(names) if ".eye." in name]
    for eye in eyes:
        world = eye.matrix_world.copy()
        eye.parent = None
        eye.matrix_world = world
    scale = 1.77 / body.dimensions.z
    offset = body.location.copy()
    for obj in [body, *eyes]:
        obj.location = (obj.location - offset) * scale
        obj.scale *= scale
    body.name = "A001 female anatomical sculpt"
    proxy = body.copy()
    proxy.data = body.data.copy()
    bpy.context.collection.objects.link(proxy)
    proxy.name = "A001 gameplay topology proxy"
    proxy.modifiers.clear()
    proxy.hide_set(False)
    proxy.hide_render = False
    for eye in eyes:
        eye.name = eye.name.replace("GEO-body_female_realistic.eye", "A001 eye")
    for index, eye in enumerate(eyes):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12)
        iris = bpy.context.object
        iris.name = f"A001 iris {index + 1}"
        iris.location = eye.location + Vector((0, -0.012, 0))
        iris.scale = (0.0065, 0.0022, 0.0065)
    SOURCE.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE), compress=True)
    print({"source": str(SOURCE), "body_height": body.dimensions.z, "proxy_vertices": len(proxy.data.vertices)})


if __name__ == "__main__":
    main()
