"""Build the repair shop's reusable ceramic floor module in Blender."""

import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
from export_static_by_material import export_static_by_material


PROJECT = Path(__file__).resolve().parents[1]
COLLECTION_NAME = "A149 glazed ceramic floor"
TEXTURE_SIZE = 512


def smooth_noise(x: float, y: float, frequency: int) -> float:
    x *= frequency
    y *= frequency
    x0 = math.floor(x)
    y0 = math.floor(y)
    tx = x - x0
    ty = y - y0
    tx = tx * tx * (3.0 - 2.0 * tx)
    ty = ty * ty * (3.0 - 2.0 * ty)

    def corner(cx: int, cy: int) -> float:
        value = math.sin(cx * 127.1 + cy * 311.7 + 41.3) * 43758.5453
        return (value - math.floor(value)) * 2.0 - 1.0

    a = corner(x0, y0) * (1.0 - tx) + corner(x0 + 1, y0) * tx
    b = corner(x0, y0 + 1) * (1.0 - tx) + corner(x0 + 1, y0 + 1) * tx
    return a * (1.0 - ty) + b * ty


def save_image(name: str, filename: str, color_space: str, pixels: list[float]) -> bpy.types.Image:
    existing = bpy.data.images.get(name)
    if existing:
        bpy.data.images.remove(existing)
    image = bpy.data.images.new(name, width=TEXTURE_SIZE, height=TEXTURE_SIZE, alpha=True)
    image.colorspace_settings.name = color_space
    image.pixels.foreach_set(pixels)
    image.update()
    image.filepath_raw = str(PROJECT / "assets" / "textures" / filename)
    image.file_format = "PNG"
    image.save()
    image.pack()
    return image


def make_material(name: str, base: bpy.types.Image, orm: bpy.types.Image, normal: bpy.types.Image) -> bpy.types.Material:
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    surface = nodes.new("ShaderNodeBsdfPrincipled")
    base_node = nodes.new("ShaderNodeTexImage")
    base_node.image = base
    orm_node = nodes.new("ShaderNodeTexImage")
    orm_node.image = orm
    channels = nodes.new("ShaderNodeSeparateColor")
    normal_node = nodes.new("ShaderNodeTexImage")
    normal_node.image = normal
    normal_map = nodes.new("ShaderNodeNormalMap")
    normal_map.inputs["Strength"].default_value = 0.32
    links = material.node_tree.links
    links.new(base_node.outputs["Color"], surface.inputs["Base Color"])
    links.new(orm_node.outputs["Color"], channels.inputs["Color"])
    links.new(channels.outputs["Green"], surface.inputs["Roughness"])
    links.new(channels.outputs["Blue"], surface.inputs["Metallic"])
    links.new(normal_node.outputs["Color"], normal_map.inputs["Color"])
    links.new(normal_map.outputs["Normal"], surface.inputs["Normal"])
    links.new(surface.outputs["BSDF"], output.inputs["Surface"])
    return material


def move_to_collection(obj: bpy.types.Object, collection: bpy.types.Collection) -> None:
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    collection.objects.link(obj)


def box(name: str, location: tuple[float, float, float], dimensions: tuple[float, float, float], material: bpy.types.Material, collection: bpy.types.Collection, bevel: float = 0.0) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    if bevel:
        modifier = obj.modifiers.new("Eased ceramic edge", "BEVEL")
        modifier.width = bevel
        modifier.segments = 2
        obj.modifiers.new("Weighted corner normals", "WEIGHTED_NORMAL")
    move_to_collection(obj, collection)
    return obj


def build() -> dict[str, object]:
    previous = bpy.data.collections.get(COLLECTION_NAME)
    if previous:
        for obj in list(previous.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(previous)
    for name in ("SL ceramic warm grey 1", "SL ceramic warm grey 2", "SL ceramic warm grey 3", "SL ceramic recessed warm grout"):
        material = bpy.data.materials.get(name)
        if material and material.users == 0:
            bpy.data.materials.remove(material)
    texture_dir = PROJECT / "assets" / "textures"
    texture_dir.mkdir(parents=True, exist_ok=True)
    collection = bpy.data.collections.new(COLLECTION_NAME)
    bpy.context.scene.collection.children.link(collection)
    images = []
    tone_colors = ((0.62, 0.60, 0.53), (0.67, 0.65, 0.58), (0.57, 0.56, 0.51))
    bases = [[] for _ in tone_colors]
    orm_pixels = []
    normal_pixels = []
    heights = [0.0] * (TEXTURE_SIZE * TEXTURE_SIZE)
    for y in range(TEXTURE_SIZE):
        v = y / TEXTURE_SIZE
        for x in range(TEXTURE_SIZE):
            u = x / TEXTURE_SIZE
            clouds = 0.58 * smooth_noise(u, v, 7) + 0.27 * smooth_noise(u, v, 23)
            speck = 0.15 * smooth_noise(u, v, 79)
            variation = 1.0 + 0.044 * clouds + 0.014 * speck
            for color, pixels in zip(tone_colors, bases):
                pixels.extend((color[0] * variation, color[1] * variation, color[2] * variation, 1.0))
            roughness = max(0.47, min(0.69, 0.58 + 0.035 * clouds + 0.018 * speck))
            orm_pixels.extend((1.0, roughness, 0.0, 1.0))
            heights[y * TEXTURE_SIZE + x] = 0.008 * clouds + 0.003 * speck

    for y in range(TEXTURE_SIZE):
        for x in range(TEXTURE_SIZE):
            dx = (heights[y * TEXTURE_SIZE + (x + 1) % TEXTURE_SIZE] - heights[y * TEXTURE_SIZE + (x - 1) % TEXTURE_SIZE]) * 10.0
            dy = (heights[((y + 1) % TEXTURE_SIZE) * TEXTURE_SIZE + x] - heights[((y - 1) % TEXTURE_SIZE) * TEXTURE_SIZE + x]) * 10.0
            length = math.sqrt(dx * dx + dy * dy + 1.0)
            normal_pixels.extend((0.5 - 0.5 * dx / length, 0.5 - 0.5 * dy / length, 0.5 + 0.5 / length, 1.0))

    orm = save_image("A149 ceramic packed ORM", "A149_ceramic_orm.png", "Non-Color", orm_pixels)
    normal = save_image("A149 ceramic fine normal", "A149_ceramic_normal.png", "Non-Color", normal_pixels)
    images.extend((orm, normal))
    tile_materials = []
    for index, pixels in enumerate(bases):
        base = save_image(f"A149 ceramic tone {index + 1}", f"A149_ceramic_base_{index + 1}.png", "sRGB", pixels)
        images.append(base)
        tile_materials.append(make_material(f"SL ceramic warm grey {index + 1}", base, orm, normal))

    grout = bpy.data.materials.new("SL ceramic recessed warm grout")
    grout.diffuse_color = (0.29, 0.27, 0.24, 1.0)
    grout.use_nodes = True
    grout.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = grout.diffuse_color
    grout.node_tree.nodes.get("Principled BSDF").inputs["Roughness"].default_value = 0.9
    box("Recessed grout bed", (0, 0, -0.007), (2, 2, 0.008), grout, collection)

    for row in range(4):
        for column in range(4):
            x = -0.75 + column * 0.5
            y = -0.75 + row * 0.5
            tone = (row * 2 + column * 5 + row * column) % len(tile_materials)
            box(
                f"Ceramic tile {row + 1:02d}-{column + 1:02d}",
                (x, y, -0.0075),
                (0.495, 0.495, 0.015),
                tile_materials[tone],
                collection,
                bevel=0.0025,
            )

    bpy.context.view_layer.update()
    source = PROJECT / "art" / "source" / "A149_glazed_ceramic_floor.blend"
    bpy.data.libraries.write(str(source), {collection, *images}, compress=True)
    output = PROJECT / "assets" / "models" / "A149_glazed_ceramic_floor.glb"
    export_result = export_static_by_material(COLLECTION_NAME, str(output))
    collection.hide_viewport = True
    return {"source": str(source), "export": str(output), "source_objects": len(collection.objects), "export_meshes": export_result["export_meshes"], "texture_files": [image.filepath_raw for image in images]}


if __name__ == "__main__":
    print(build())
