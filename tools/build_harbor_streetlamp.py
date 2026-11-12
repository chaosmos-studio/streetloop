"""Build the harbor block's twin-arm streetlamp in Blender."""

import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
from export_static_by_material import export_static_by_material


PROJECT = Path(__file__).resolve().parents[1]
COLLECTION_NAME = "A007 Harbor twin-arm streetlamp"


def material(name: str, color: tuple[float, float, float], roughness: float, metallic: float = 0.0, emission: float = 0.0) -> bpy.types.Material:
    result = bpy.data.materials.new(name)
    result.diffuse_color = (*color, 1.0)
    result.use_nodes = True
    surface = result.node_tree.nodes.get("Principled BSDF")
    surface.inputs["Base Color"].default_value = (*color, 1.0)
    surface.inputs["Roughness"].default_value = roughness
    surface.inputs["Metallic"].default_value = metallic
    if emission:
        surface.inputs["Emission Color"].default_value = (*color, 1.0)
        surface.inputs["Emission Strength"].default_value = emission
    return result


def painted_metal() -> tuple[bpy.types.Material, list[bpy.types.Image]]:
    size = 512
    base_pixels = []
    orm_pixels = []
    normal_pixels = []
    for y in range(size):
        v = y / size
        for x in range(size):
            u = x / size
            fine = math.sin(math.tau * u * 113) * math.sin(math.tau * v * 97)
            broad = math.sin(math.tau * (v * 2.8 + u * 0.5)) * math.sin(math.tau * (u * 3.1 - v * 0.2))
            salt = math.sin(math.tau * (u * 29.0 + v * 37.0)) * math.sin(math.tau * (v * 51.0 - u * 11.0))
            tone = 1.0 + 0.035 * broad + 0.012 * salt
            base_pixels.extend((0.17 * tone, 0.28 * tone, 0.29 * tone, 1.0))
            orm_pixels.extend((1.0, 0.55 + 0.026 * broad, 0.52, 1.0))
            normal_pixels.extend((0.5 + 0.018 * fine, 0.5 + 0.018 * salt, 1.0, 1.0))

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

    base = save("A007 weathered petrol paint", "A007_streetlamp_base.png", "sRGB", base_pixels)
    orm = save("A007 paint ORM", "A007_streetlamp_orm.png", "Non-Color", orm_pixels)
    normal = save("A007 powdercoat normal", "A007_streetlamp_normal.png", "Non-Color", normal_pixels)
    result = bpy.data.materials.new("SL streetlamp weathered petrol paint")
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
    normal_map.inputs["Strength"].default_value = 0.28
    links = result.node_tree.links
    links.new(base_node.outputs["Color"], surface.inputs["Base Color"])
    links.new(orm_node.outputs["Color"], channels.inputs["Color"])
    links.new(channels.outputs["Green"], surface.inputs["Roughness"])
    links.new(channels.outputs["Blue"], surface.inputs["Metallic"])
    links.new(normal_node.outputs["Color"], normal_map.inputs["Color"])
    links.new(normal_map.outputs["Normal"], surface.inputs["Normal"])
    links.new(surface.outputs["BSDF"], output.inputs["Surface"])
    return result, [base, orm, normal]


def move(obj: bpy.types.Object, collection: bpy.types.Collection) -> bpy.types.Object:
    for other in list(obj.users_collection):
        other.objects.unlink(obj)
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
        modifier = obj.modifiers.new("Manufactured edge", "BEVEL")
        modifier.width = bevel
        modifier.segments = 2
        obj.modifiers.new("Weighted normals", "WEIGHTED_NORMAL")
    return move(obj, collection)


def cylinder(name: str, position: tuple[float, float, float], radius: float, depth: float, surface: bpy.types.Material, collection: bpy.types.Collection, vertices: int = 12) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=position)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(surface)
    modifier = obj.modifiers.new("Cast edge", "BEVEL")
    modifier.width = min(radius * 0.15, 0.018)
    modifier.segments = 1
    obj.modifiers.new("Weighted normals", "WEIGHTED_NORMAL")
    return move(obj, collection)


def bent_arm(name: str, sign: float, surface: bpy.types.Material, collection: bpy.types.Collection) -> bpy.types.Object:
    path = bpy.data.curves.new(name, "CURVE")
    path.dimensions = "3D"
    path.resolution_u = 10
    path.bevel_depth = 0.052
    path.bevel_resolution = 2
    spline = path.splines.new("BEZIER")
    spline.bezier_points.add(2)
    coordinates = ((0, 0, 5.31), (sign * 0.74, 0, 5.65), (sign * 1.52, 0, 5.45))
    for control, coordinate in zip(spline.bezier_points, coordinates):
        control.co = coordinate
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
    paint, images = painted_metal()
    casting = material("SL streetlamp dark cast iron", (0.09, 0.13, 0.14), 0.68, 0.55)
    steel = material("SL streetlamp brushed stainless", (0.43, 0.46, 0.43), 0.43, 0.78)
    gasket = material("SL streetlamp rubber seal", (0.035, 0.047, 0.047), 0.87)
    diffuser = material("SL streetlamp warm opal diffuser", (0.77, 0.72, 0.58), 0.48, emission=0.12)
    rust = material("SL streetlamp edge rust", (0.31, 0.13, 0.075), 0.8, 0.22)

    cylinder("Anchor flange", (0, 0, 0.045), 0.32, 0.09, casting, collection, 20)
    cylinder("Raised base socket", (0, 0, 0.19), 0.23, 0.30, casting, collection, 20)
    for index in range(6):
        angle = math.tau * index / 6
        x, y = math.cos(angle) * 0.26, math.sin(angle) * 0.26
        cylinder(f"Anchor bolt {index + 1}", (x, y, 0.102), 0.022, 0.035, steel, collection, 8)
        cylinder(f"Bolt seat {index + 1}", (x, y, 0.083), 0.035, 0.006, rust, collection, 12)

    bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.145, radius2=0.068, depth=5.15, location=(0, 0, 2.92))
    pole = bpy.context.object
    pole.name = "Tapered dodecagonal pole"
    pole.data.materials.append(paint)
    bevel = pole.modifiers.new("Soft cast arrises", "BEVEL")
    bevel.width = 0.012
    bevel.segments = 2
    pole.modifiers.new("Weighted normals", "WEIGHTED_NORMAL")
    move(pole, collection)
    for height, radius in ((0.52, 0.153), (2.73, 0.117), (5.18, 0.086)):
        cylinder(f"Service collar {height:.2f}", (0, 0, height), radius, 0.048, casting, collection, 16)
        cylinder(f"Collar edge {height:.2f}", (0, 0, height + 0.027), radius + 0.004, 0.008, steel, collection, 16)

    box("Service door shadow gap", (0, -0.145, 1.17), (0.19, 0.014, 0.36), gasket, collection, 0.018)
    box("Service door powdercoat skin", (0, -0.153, 1.17), (0.175, 0.012, 0.345), paint, collection, 0.015)
    box("Service door brushed inset", (0, -0.161, 1.17), (0.105, 0.004, 0.22), steel, collection, 0.006)
    for height in (1.06, 1.29):
        cylinder(f"Panel hinge {height:.2f}", (-0.095, -0.164, height), 0.013, 0.048, steel, collection, 12)
    cylinder("Quarter turn service latch", (0.06, -0.17, 1.17), 0.018, 0.018, casting, collection, 12)
    box("Cable access outlet", (0, -0.16, 0.69), (0.07, 0.016, 0.10), gasket, collection, 0.008)
    box("Lower rain stain", (0.09, -0.12, 0.42), (0.025, 0.006, 0.13), rust, collection, 0.004)

    cylinder("Arm junction casting", (0, 0, 5.35), 0.105, 0.21, casting, collection, 16)
    for index, sign in enumerate((-1.0, 1.0)):
        bent_arm(f"Swept tubular arm {index + 1}", sign, paint, collection)
        x = sign * 1.53
        cylinder(f"Head swivel collar {index + 1}", (x, 0, 5.46), 0.083, 0.12, casting, collection, 16)
        box(f"Lamp gasket {index + 1}", (x, 0, 5.32), (0.72, 0.39, 0.11), gasket, collection, 0.05)
        box(f"Powdercoat luminaire {index + 1}", (x, 0, 5.42), (0.76, 0.42, 0.17), paint, collection, 0.065)
        box(f"Reflector lip {index + 1}", (x, 0, 5.335), (0.70, 0.35, 0.035), steel, collection, 0.015)
        box(f"Opal lens {index + 1}", (x, 0, 5.314), (0.62, 0.28, 0.014), diffuser, collection, 0.01)
        for front in (-0.13, 0.13):
            for side in (-0.28, 0.28):
                cylinder(f"Lens screw {index + 1} {front:.2f} {side:.2f}", (x + side, front, 5.305), 0.009, 0.012, steel, collection, 8)

    bpy.context.view_layer.update()
    source = PROJECT / "art" / "source" / "A007_harbor_twin_arm_streetlamp.blend"
    bpy.data.libraries.write(str(source), {collection, *images}, compress=True)
    output = PROJECT / "assets" / "models" / "A007_harbor_twin_arm_streetlamp.glb"
    export_result = export_static_by_material(COLLECTION_NAME, str(output))
    collection.hide_viewport = True
    return {"source": str(source), "export": str(output), "objects": export_result["source_objects"], "meshes": export_result["export_meshes"], "textures": [image.filepath_raw for image in images]}


if __name__ == "__main__":
    print(build())
