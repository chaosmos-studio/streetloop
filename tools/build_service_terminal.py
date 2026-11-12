"""Build the repair shop's computer, keyboard, mouse, and cables in Blender."""

import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
from export_static_by_material import export_static_by_material


PROJECT = Path(__file__).resolve().parents[1]
COLLECTION_NAME = "A157 Harbor service terminal"


def material(name: str, color: tuple[float, float, float], roughness: float, metallic: float = 0.0, emission: float = 0.0) -> bpy.types.Material:
    result = bpy.data.materials.new(name)
    result.use_nodes = True
    result.diffuse_color = (*color, 1.0)
    surface = result.node_tree.nodes.get("Principled BSDF")
    surface.inputs["Base Color"].default_value = (*color, 1.0)
    surface.inputs["Roughness"].default_value = roughness
    surface.inputs["Metallic"].default_value = metallic
    if emission:
        surface.inputs["Emission Color"].default_value = (*color, 1.0)
        surface.inputs["Emission Strength"].default_value = emission
    return result


def textured_housing() -> tuple[bpy.types.Material, list[bpy.types.Image]]:
    size = 512
    base_pixels = []
    orm_pixels = []
    normal_pixels = []
    for y in range(size):
        v = y / size
        for x in range(size):
            u = x / size
            fleck = math.sin(math.tau * u * 149) * math.sin(math.tau * v * 137)
            broad = math.sin(math.tau * (u * 2.9 + v * 0.6)) * math.sin(math.tau * (v * 3.8 - u * 0.4))
            tone = 1.0 + 0.07 * broad + 0.027 * fleck
            base_pixels.extend((0.065 * tone, 0.075 * tone, 0.079 * tone, 1.0))
            orm_pixels.extend((1.0, 0.7 + 0.035 * broad, 0.08, 1.0))
            normal_pixels.extend((0.5 + 0.018 * fleck, 0.5 + 0.018 * broad, 1.0, 1.0))

    directory = PROJECT / "assets" / "textures"
    directory.mkdir(parents=True, exist_ok=True)

    def save(name: str, filename: str, colorspace: str, pixels: list[float]) -> bpy.types.Image:
        image = bpy.data.images.new(name, width=size, height=size, alpha=True)
        image.colorspace_settings.name = colorspace
        image.pixels.foreach_set(pixels)
        image.update()
        image.filepath_raw = str(directory / filename)
        image.file_format = "PNG"
        image.save()
        image.pack()
        return image

    base = save("A157 terminal charcoal", "A157_terminal_base.png", "sRGB", base_pixels)
    orm = save("A157 terminal packed ORM", "A157_terminal_orm.png", "Non-Color", orm_pixels)
    normal = save("A157 terminal fine normal", "A157_terminal_normal.png", "Non-Color", normal_pixels)
    result = bpy.data.materials.new("SL terminal stippled charcoal")
    result.use_nodes = True
    nodes = result.node_tree.nodes
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
    normal_map.inputs["Strength"].default_value = 0.2
    links = result.node_tree.links
    links.new(base_node.outputs["Color"], surface.inputs["Base Color"])
    links.new(orm_node.outputs["Color"], channels.inputs["Color"])
    links.new(channels.outputs["Green"], surface.inputs["Roughness"])
    links.new(channels.outputs["Blue"], surface.inputs["Metallic"])
    links.new(normal_node.outputs["Color"], normal_map.inputs["Color"])
    links.new(normal_map.outputs["Normal"], surface.inputs["Normal"])
    links.new(surface.outputs["BSDF"], output.inputs["Surface"])
    return result, [base, orm, normal]


def screen_material(image: bpy.types.Image) -> bpy.types.Material:
    result = bpy.data.materials.new("SL terminal original standby display")
    result.use_nodes = True
    nodes = result.node_tree.nodes
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    surface = nodes.new("ShaderNodeBsdfPrincipled")
    image_node = nodes.new("ShaderNodeTexImage")
    image_node.image = image
    surface.inputs["Roughness"].default_value = 0.35
    surface.inputs["Emission Strength"].default_value = 0.7
    links = result.node_tree.links
    links.new(image_node.outputs["Color"], surface.inputs["Base Color"])
    links.new(image_node.outputs["Color"], surface.inputs["Emission Color"])
    links.new(surface.outputs["BSDF"], output.inputs["Surface"])
    return result


def move(obj: bpy.types.Object, collection: bpy.types.Collection) -> bpy.types.Object:
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


def box(name: str, position: tuple[float, float, float], dimensions: tuple[float, float, float], surface: bpy.types.Material, collection: bpy.types.Collection, bevel: float = 0.0) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cube_add(size=1, location=position)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(surface)
    if bevel:
        modifier = obj.modifiers.new("Molded edge", "BEVEL")
        modifier.width = bevel
        modifier.segments = 2
        obj.modifiers.new("Weighted normals", "WEIGHTED_NORMAL")
    return move(obj, collection)


def cylinder(name: str, position: tuple[float, float, float], radius: float, depth: float, surface: bpy.types.Material, collection: bpy.types.Collection, vertices: int = 12) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=position)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(surface)
    return move(obj, collection)


def cable(name: str, points: list[tuple[float, float, float]], radius: float, surface: bpy.types.Material, collection: bpy.types.Collection) -> bpy.types.Object:
    path = bpy.data.curves.new(name, "CURVE")
    path.dimensions = "3D"
    path.bevel_depth = radius
    path.bevel_resolution = 2
    spline = path.splines.new("BEZIER")
    spline.bezier_points.add(len(points) - 1)
    for control, position in zip(spline.bezier_points, points):
        control.co = position
        control.handle_left_type = "AUTO"
        control.handle_right_type = "AUTO"
    obj = bpy.data.objects.new(name, path)
    collection.objects.link(obj)
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.convert(target="MESH")
    obj.data.materials.append(surface)
    return obj


def build() -> dict[str, object]:
    previous = bpy.data.collections.get(COLLECTION_NAME)
    if previous:
        for obj in list(previous.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(previous)
    collection = bpy.data.collections.new(COLLECTION_NAME)
    bpy.context.scene.collection.children.link(collection)
    housing, images = textured_housing()
    display_image = bpy.data.images.load(str(PROJECT / "assets" / "textures" / "A157_terminal_screen.png"), check_existing=False)
    display_image.pack()
    images.append(display_image)
    display = screen_material(display_image)
    trim = material("SL terminal brushed aluminum", (0.33, 0.38, 0.38), 0.48, 0.78)
    keycap = material("SL terminal warm grey keycap", (0.23, 0.25, 0.24), 0.78)
    key_label = material("SL terminal worn key legend", (0.62, 0.65, 0.59), 0.92)
    cable_surface = material("SL terminal braided cable", (0.028, 0.036, 0.039), 0.9)
    indicator = material("SL terminal amber power indicator", (0.63, 0.23, 0.075), 0.4, emission=0.7)

    box("Monitor rear housing", (0, 0.14, 0.394), (0.58, 0.075, 0.388), housing, collection, 0.021)
    box("Inset display recess", (0, 0.186, 0.397), (0.525, 0.01, 0.333), cable_surface, collection, 0.006)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0.193, 0.397), rotation=(-math.pi / 2, 0, 0))
    screen = bpy.context.object
    screen.name = "Readable standby display"
    screen.dimensions = (0.505, 0.318, 0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    screen.data.materials.append(display)
    for loop in screen.data.uv_layers.active.data:
        loop.uv.x = 1.0 - loop.uv.x
        loop.uv.y = 1.0 - loop.uv.y
    move(screen, collection)
    for side in (-0.272, 0.272):
        box(f"Vertical bezel {side:.3f}", (side, 0.197, 0.397), (0.025, 0.015, 0.356), housing, collection, 0.006)
    for height in (0.217, 0.576):
        box(f"Horizontal bezel {height:.3f}", (0, 0.197, height), (0.56, 0.015, 0.025), housing, collection, 0.006)
    box("Lower brushed trim", (0, 0.208, 0.205), (0.32, 0.008, 0.012), trim, collection, 0.003)
    cylinder("Power button", (0.247, 0.208, 0.206), 0.008, 0.006, trim, collection, 16)
    cylinder("Power tell", (0.247, 0.214, 0.206), 0.003, 0.005, indicator, collection, 12)
    for side in (-1, 1):
        for index in range(6):
            box(f"Speaker vent {side} {index}", (side * 0.255, 0.208, 0.225 + index * 0.01), (0.025, 0.003, 0.004), cable_surface, collection)
    box("Monitor neck", (0, 0.075, 0.131), (0.068, 0.085, 0.21), trim, collection, 0.02)
    box("Monitor foot", (0, 0.105, 0.019), (0.31, 0.22, 0.038), housing, collection, 0.014)
    box("Monitor foot heel", (0, 0.105, 0.006), (0.27, 0.18, 0.009), cable_surface, collection, 0.004)
    for index in range(12):
        box(f"Rear cooling slot {index + 1}", (-0.22 + index * 0.04, 0.091, 0.505), (0.02, 0.004, 0.05), cable_surface, collection, 0.002)
    for side in (-1, 1):
        for height in (0.24, 0.55):
            cylinder(f"Rear panel fastener {side} {height}", (side * 0.235, 0.098, height), 0.006, 0.004, trim, collection, 10)

    box("Keyboard tray", (-0.02, 0.45, 0.022), (0.455, 0.175, 0.036), housing, collection, 0.013)
    for row in range(4):
        for column in range(13):
            x = -0.218 + column * 0.032
            y = 0.392 + row * 0.03
            box(f"Key {row:02d} {column:02d}", (x, y, 0.046), (0.026, 0.022, 0.009), keycap, collection, 0.002)
            if column % 3 == 0:
                box(f"Key legend {row:02d} {column:02d}", (x, y, 0.051), (0.009, 0.002, 0.001), key_label, collection)
    box("Worn space bar", (-0.02, 0.523, 0.046), (0.17, 0.022, 0.009), keycap, collection, 0.003)
    box("Enter key", (0.18, 0.486, 0.047), (0.036, 0.025, 0.011), trim, collection, 0.004)
    box("Mouse shell", (0.322, 0.46, 0.032), (0.082, 0.11, 0.055), housing, collection, 0.026)
    box("Mouse button seam", (0.322, 0.492, 0.061), (0.002, 0.034, 0.002), cable_surface, collection)
    cylinder("Mouse scroll wheel", (0.322, 0.491, 0.066), 0.007, 0.014, trim, collection, 12)
    cable("Keyboard USB cable", [(-0.02, 0.36, 0.028), (-0.06, 0.31, 0.02), (-0.08, 0.23, 0.012)], 0.003, cable_surface, collection)
    cable("Mouse USB cable", [(0.322, 0.505, 0.024), (0.37, 0.37, 0.012), (0.24, 0.24, 0.012)], 0.003, cable_surface, collection)
    cable("Monitor power lead", [(0, 0.105, 0.24), (0, 0.0, 0.17), (-0.03, -0.065, 0.03), (-0.05, -0.15, 0.012)], 0.004, cable_surface, collection)

    bpy.context.view_layer.update()
    source = PROJECT / "art" / "source" / "A157_harbor_service_terminal.blend"
    bpy.data.libraries.write(str(source), {collection, *images}, compress=True)
    output = PROJECT / "assets" / "models" / "A157_harbor_service_terminal.glb"
    export_result = export_static_by_material(COLLECTION_NAME, str(output))
    collection.hide_viewport = True
    return {"source": str(source), "export": str(output), "objects": export_result["source_objects"], "meshes": export_result["export_meshes"], "textures": [image.filepath_raw for image in images]}


if __name__ == "__main__":
    print(build())
