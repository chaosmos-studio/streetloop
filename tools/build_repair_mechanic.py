"""Build the first Streetloop repair mechanic from an editable character scale set."""

from array import array
from pathlib import Path
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_harbor_runner import box, cord, ellipsoid, loft, solid
from export_articulated_by_material import export_articulated_by_material


PROJECT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT / "art" / "source" / "A001_harbor_runner.blend"
NAME = "A085 Repair mechanic"


def recolor(image: bpy.types.Image, name: str, filename: str, original: tuple[float, float, float], target: tuple[float, float, float]) -> bpy.types.Image:
    pixels = array("f", [0.0]) * (image.size[0] * image.size[1] * 4)
    image.pixels.foreach_get(pixels)
    for index in range(0, len(pixels), 4):
        for channel in range(3):
            pixels[index + channel] *= target[channel] / original[channel]
    replacement = image.copy()
    replacement.name = name
    replacement.pixels.foreach_set(pixels)
    replacement.update()
    replacement.filepath_raw = str(PROJECT / "assets" / "textures" / filename)
    replacement.file_format = "PNG"
    replacement.save()
    replacement.pack()
    return replacement


def set_color(material_name: str, color: tuple[float, float, float]) -> bpy.types.Material:
    material = bpy.data.materials[material_name]
    material.name = material_name.replace("SL runner", "SL mechanic")
    material.diffuse_color = (*color, 1.0)
    material.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = (*color, 1.0)
    return material


def render_views(collection: bpy.types.Collection) -> list[str]:
    scene = bpy.data.scenes.new("A085 mechanic review")
    scene.collection.children.link(collection)
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 640
    scene.render.resolution_y = 800
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.world = bpy.data.worlds.new("A085 review world")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes.get("Background").inputs["Color"].default_value = (0.27, 0.30, 0.30, 1.0)
    scene.world.node_tree.nodes.get("Background").inputs["Strength"].default_value = 0.7
    camera_data = bpy.data.cameras.new("A085 review camera")
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = 2.3
    camera = bpy.data.objects.new("A085 review camera", camera_data)
    scene.collection.objects.link(camera)
    scene.camera = camera
    for name, location, energy, size in (
        ("Warm key", (-2.5, -3.0, 4.2), 440, 4.0),
        ("Cool fill", (2.5, -1.5, 2.4), 250, 3.0),
        ("Soft rim", (0.5, 2.5, 3.1), 380, 2.5),
    ):
        light = bpy.data.lights.new(name, "AREA")
        light.energy = energy
        light.shape = "DISK"
        light.size = size
        obj = bpy.data.objects.new(name, light)
        scene.collection.objects.link(obj)
        obj.location = location
        obj.rotation_euler = (Vector((0, 0, 1)) - obj.location).to_track_quat("-Z", "Y").to_euler()
    output_dir = PROJECT / "art" / "review" / "A085_repair_mechanic"
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = []
    for name, position in (("front", (0, -4, 1)), ("side", (4, 0, 1)), ("rear", (0, 4, 1))):
        camera.location = position
        camera.rotation_euler = (Vector((0, 0, 0.87)) - camera.location).to_track_quat("-Z", "Y").to_euler()
        output = output_dir / f"{name}.png"
        scene.render.filepath = str(output)
        bpy.ops.render.render(write_still=True, scene=scene.name)
        outputs.append(str(output))
    bpy.data.scenes.remove(scene)
    return outputs


def build() -> dict[str, object]:
    with bpy.data.libraries.load(str(SOURCE), link=False) as (source, loaded):
        loaded.collections = ["A001 Harbor runner"]
    collection = loaded.collections[0]
    collection.name = NAME
    bpy.context.scene.collection.children.link(collection)
    for obj in list(collection.objects):
        if obj.name.startswith("Hair curl") or obj.name.startswith("Satchel") or obj.name == "Hair cap":
            bpy.data.objects.remove(obj, do_unlink=True)

    cloth_specs = (
        ("SL runner faded teal canvas", "A001 runner cloth base 1", "A085 mechanic petrol work shirt", "A085_mechanic_shirt_base.png", (0.16, 0.31, 0.34), (0.17, 0.26, 0.28)),
        ("SL runner charcoal work denim", "A001 runner cloth base 2", "A085 mechanic grey work trouser", "A085_mechanic_trouser_base.png", (0.20, 0.25, 0.28), (0.25, 0.27, 0.27)),
        ("SL runner rust lining", "A001 runner cloth base 3", "A085 mechanic rust cloth detail", "A085_mechanic_detail_base.png", (0.47, 0.25, 0.19), (0.42, 0.23, 0.16)),
    )
    new_images = []
    for material_name, image_name, new_name, filename, original, target in cloth_specs:
        material = bpy.data.materials[material_name]
        material.name = new_name
        image = recolor(bpy.data.images[image_name], new_name, filename, original, target)
        new_images.append(image)
        for node in material.node_tree.nodes:
            if node.type == "TEX_IMAGE" and node.image.name == image_name:
                node.image = image

    set_color("SL runner warm brown skin", (0.37, 0.22, 0.16))
    set_color("SL runner skin shadow", (0.25, 0.14, 0.10))
    set_color("SL runner dark curly hair", (0.075, 0.07, 0.065))
    set_color("SL runner aged brown leather", (0.18, 0.125, 0.09))
    set_color("SL runner rubber soles", (0.055, 0.06, 0.06))
    set_color("SL runner aged brass", (0.39, 0.30, 0.17))
    set_color("SL runner warm ivory stitch", (0.70, 0.66, 0.55))
    set_color("SL runner deep eyes", (0.04, 0.04, 0.035))
    apron = solid("SL mechanic oil-dark canvas apron", (0.095, 0.14, 0.15), 0.91)
    apron_edge = solid("SL mechanic apron edge stitching", (0.48, 0.49, 0.40), 0.84)
    cap = solid("SL mechanic charcoal cap", (0.105, 0.115, 0.115), 0.87)
    steel = solid("SL mechanic satin steel tools", (0.45, 0.48, 0.47), 0.35, 0.72)
    handle = solid("SL mechanic oiled timber tool handles", (0.32, 0.18, 0.10), 0.73)
    rubber = solid("SL mechanic rubber grip", (0.08, 0.085, 0.082), 0.92)

    hips = next(obj for obj in collection.objects if obj.name == "HipsPivot")
    ellipsoid("Close cropped hair", (0, 0.012, 0.76), (0.227, 0.218, 0.15), bpy.data.materials["SL mechanic dark curly hair"], collection, hips)
    ellipsoid("Hair gathered at nape", (0, 0.104, 0.72), (0.12, 0.085, 0.095), bpy.data.materials["SL mechanic dark curly hair"], collection, hips)
    loft("Mechanic cap crown", [(0.77, 0.105, 0.108, 0, 0), (0.83, 0.12, 0.11, 0, 0), (0.88, 0.08, 0.09, 0, 0)], cap, collection, hips)
    ellipsoid("Cap bill", (0, -0.12, 0.806), (0.22, 0.18, 0.026), cap, collection, hips)
    cord("Cap crown seam", [(-0.095, -0.064, 0.85), (0, -0.105, 0.878), (0.095, -0.064, 0.85)], 0.0025, apron_edge, collection, hips)
    box("Apron bib", (0, -0.158, 0.27), (0.30, 0.025, 0.30), apron, collection, hips, 0.025)
    box("Apron lower panel", (0, -0.16, 0.005), (0.385, 0.032, 0.28), apron, collection, hips, 0.025)
    box("Apron top seam", (0, -0.18, 0.405), (0.31, 0.005, 0.005), apron_edge, collection, hips)
    for side, direction in (("Left", -1.0), ("Right", 1.0)):
        x = direction * 0.145
        cord(f"{side} apron neck strap", [(x, -0.162, 0.42), (direction * 0.10, -0.08, 0.56), (direction * 0.035, 0.015, 0.59)], 0.012, apron, collection, hips)
        cord(f"{side} apron edge seam", [(direction * 0.19, -0.179, -0.12), (direction * 0.19, -0.179, 0.12), (direction * 0.15, -0.174, 0.405)], 0.0025, apron_edge, collection, hips)
        cord(f"{side} apron waist tie", [(direction * 0.18, -0.16, 0.105), (direction * 0.24, 0.02, 0.105), (direction * 0.12, 0.15, 0.1)], 0.008, apron, collection, hips)
    box("Apron parts pocket", (-0.095, -0.189, -0.01), (0.15, 0.012, 0.12), apron, collection, hips, 0.009)
    cord("Parts pocket top stitch", [(-0.165, -0.197, 0.045), (-0.025, -0.197, 0.045)], 0.0025, apron_edge, collection, hips)
    box("Utility belt", (0, -0.015, 0.05), (0.46, 0.25, 0.055), handle, collection, hips, 0.012)
    box("Belt buckle", (0, -0.147, 0.05), (0.065, 0.018, 0.055), steel, collection, hips, 0.006)
    box("Wrench shaft", (0.29, -0.052, 0.03), (0.022, 0.028, 0.29), steel, collection, hips, 0.007)
    ellipsoid("Wrench open head", (0.29, -0.052, 0.19), (0.07, 0.026, 0.06), steel, collection, hips, 12, 8)
    box("Pencil body", (-0.23, -0.11, 0.11), (0.013, 0.013, 0.19), handle, collection, hips, 0.003)
    box("Pencil graphite tip", (-0.23, -0.11, 0.005), (0.007, 0.007, 0.018), rubber, collection, hips)
    box("Shop rag", (-0.27, -0.03, -0.04), (0.12, 0.06, 0.20), bpy.data.materials["A085 mechanic rust cloth detail"], collection, hips, 0.013)
    cord("Back apron seam", [(-0.17, 0.16, 0.11), (0, 0.17, 0.10), (0.17, 0.16, 0.11)], 0.003, apron_edge, collection, hips)

    bpy.context.view_layer.update()
    source_path = PROJECT / "art" / "source" / "A085_repair_mechanic.blend"
    bpy.data.libraries.write(str(source_path), {collection, *new_images}, compress=True)
    output = PROJECT / "assets" / "models" / "A085_repair_mechanic.glb"
    export_data = export_articulated_by_material(NAME, str(output))
    reviews = render_views(collection)
    triangles = sum(sum(len(face.vertices) - 2 for face in obj.data.polygons) for obj in collection.objects if obj.type == "MESH")
    return {"source": str(source_path), "export": str(output), "triangles_before_modifiers": triangles, "export_meshes": export_data["export_meshes"], "textures": [str(image.filepath_raw) for image in new_images], "views": reviews}


if __name__ == "__main__":
    print(build())
