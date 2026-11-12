"""Build the articulated first playable Streetloop character in Blender."""

import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
from export_articulated_by_material import export_articulated_by_material


PROJECT = Path(__file__).resolve().parents[1]
COLLECTION_NAME = "A001 Harbor runner"
TEXTURE_SIZE = 512


def save_image(name: str, filename: str, color_space: str, pixels: list[float]) -> bpy.types.Image:
    image = bpy.data.images.new(name, width=TEXTURE_SIZE, height=TEXTURE_SIZE, alpha=True)
    image.colorspace_settings.name = color_space
    image.pixels.foreach_set(pixels)
    image.update()
    image.filepath_raw = str(PROJECT / "assets" / "textures" / filename)
    image.file_format = "PNG"
    image.save()
    image.pack()
    return image


def make_cloth_material(name: str, base: bpy.types.Image, orm: bpy.types.Image, normal: bpy.types.Image) -> bpy.types.Material:
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
    normal_map.inputs["Strength"].default_value = 0.3
    links = material.node_tree.links
    links.new(base_node.outputs["Color"], surface.inputs["Base Color"])
    links.new(orm_node.outputs["Color"], channels.inputs["Color"])
    links.new(channels.outputs["Green"], surface.inputs["Roughness"])
    links.new(channels.outputs["Blue"], surface.inputs["Metallic"])
    links.new(normal_node.outputs["Color"], normal_map.inputs["Color"])
    links.new(normal_map.outputs["Normal"], surface.inputs["Normal"])
    links.new(surface.outputs["BSDF"], output.inputs["Surface"])
    return material


def solid(name: str, color: tuple[float, float, float], roughness: float, metallic: float = 0.0) -> bpy.types.Material:
    material = bpy.data.materials.new(name)
    material.diffuse_color = (*color, 1.0)
    material.use_nodes = True
    surface = material.node_tree.nodes.get("Principled BSDF")
    surface.inputs["Base Color"].default_value = (*color, 1.0)
    surface.inputs["Roughness"].default_value = roughness
    surface.inputs["Metallic"].default_value = metallic
    return material


def make_fabric_images() -> tuple[list[bpy.types.Image], list[bpy.types.Material]]:
    colors = ((0.16, 0.31, 0.34), (0.20, 0.25, 0.28), (0.47, 0.25, 0.19))
    base_pixels: list[list[float]] = [[] for _ in colors]
    orm_pixels: list[float] = []
    normal_pixels: list[float] = []
    for y in range(TEXTURE_SIZE):
        v = y / TEXTURE_SIZE
        for x in range(TEXTURE_SIZE):
            u = x / TEXTURE_SIZE
            warp = math.sin(math.tau * (u * 76.0 + 0.04 * math.sin(v * 7.0)))
            weft = math.sin(math.tau * (v * 84.0 + 0.03 * math.sin(u * 6.0)))
            broad = math.sin(math.tau * (u * 2.2 + v * 0.8)) * math.sin(math.tau * (v * 3.7 - u * 0.4))
            weave = 0.5 * warp * weft + 0.25 * warp + 0.25 * weft
            variation = 1.0 + 0.07 * broad + 0.045 * weave
            for color, pixels in zip(colors, base_pixels):
                pixels.extend((color[0] * variation, color[1] * variation, color[2] * variation, 1.0))
            orm_pixels.extend((1.0, 0.81 + 0.055 * broad + 0.025 * weave, 0.0, 1.0))
            nx = -0.10 * math.cos(math.tau * u * 76.0) * weft
            ny = -0.10 * math.cos(math.tau * v * 84.0) * warp
            length = math.sqrt(nx * nx + ny * ny + 1.0)
            normal_pixels.extend((0.5 + 0.5 * nx / length, 0.5 + 0.5 * ny / length, 0.5 + 0.5 / length, 1.0))

    orm = save_image("A001 runner cloth ORM", "A001_runner_cloth_orm.png", "Non-Color", orm_pixels)
    normal = save_image("A001 runner cloth normal", "A001_runner_cloth_normal.png", "Non-Color", normal_pixels)
    images = [orm, normal]
    materials = []
    for index, pixels in enumerate(base_pixels):
        base = save_image(f"A001 runner cloth base {index + 1}", f"A001_runner_cloth_base_{index + 1}.png", "sRGB", pixels)
        images.append(base)
        name = ("SL runner faded teal canvas", "SL runner charcoal work denim", "SL runner rust lining")[index]
        materials.append(make_cloth_material(name, base, orm, normal))
    return images, materials


def link(obj: bpy.types.Object, collection: bpy.types.Collection, parent: bpy.types.Object | None = None) -> bpy.types.Object:
    for current in list(obj.users_collection):
        current.objects.unlink(obj)
    collection.objects.link(obj)
    obj.parent = parent
    return obj


def pivot(name: str, location: tuple[float, float, float], collection: bpy.types.Collection, parent: bpy.types.Object | None = None) -> bpy.types.Object:
    obj = bpy.data.objects.new(name, None)
    collection.objects.link(obj)
    obj.parent = parent
    obj.location = location
    obj.empty_display_size = 0.05
    return obj


def ellipsoid(name: str, location: tuple[float, float, float], dimensions: tuple[float, float, float], material: bpy.types.Material, collection: bpy.types.Collection, parent: bpy.types.Object, segments: int = 20, rings: int = 12) -> bpy.types.Object:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, radius=1)
    obj = bpy.context.object
    obj.name = name
    obj.scale = tuple(d * 0.5 for d in dimensions)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    link(obj, collection, parent)
    obj.location = location
    for polygon in obj.data.polygons:
        polygon.use_smooth = True
    return obj


def box(name: str, location: tuple[float, float, float], dimensions: tuple[float, float, float], material: bpy.types.Material, collection: bpy.types.Collection, parent: bpy.types.Object, bevel: float = 0.0) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cube_add(size=1)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    if bevel > 0:
        modifier = obj.modifiers.new("Soft constructed edge", "BEVEL")
        modifier.width = bevel
        modifier.segments = 2
        obj.modifiers.new("Weighted normals", "WEIGHTED_NORMAL")
    link(obj, collection, parent)
    obj.location = location
    return obj


def loft(name: str, rings: list[tuple[float, float, float, float, float]], material: bpy.types.Material, collection: bpy.types.Collection, parent: bpy.types.Object, sides: int = 16) -> bpy.types.Object:
    vertices = []
    faces = []
    for z, radius_x, radius_y, center_x, center_y in rings:
        for step in range(sides):
            angle = math.tau * step / sides
            vertices.append((center_x + radius_x * math.cos(angle), center_y + radius_y * math.sin(angle), z))
    for row in range(len(rings) - 1):
        for step in range(sides):
            next_step = (step + 1) % sides
            faces.append((row * sides + step, row * sides + next_step, (row + 1) * sides + next_step, (row + 1) * sides + step))
    faces.append(tuple(reversed(tuple(range(sides)))))
    faces.append(tuple((len(rings) - 1) * sides + step for step in range(sides)))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    uv = mesh.uv_layers.new(name="Fabric UV")
    height = max(r[0] for r in rings) - min(r[0] for r in rings)
    for polygon in mesh.polygons:
        for loop_index in polygon.loop_indices:
            vertex = mesh.vertices[mesh.loops[loop_index].vertex_index].co
            uv.data[loop_index].uv = ((math.atan2(vertex.y, vertex.x) + math.pi) / math.tau, (vertex.z - rings[0][0]) / max(height, 0.001))
        polygon.use_smooth = len(polygon.vertices) == 4
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    obj.parent = parent
    obj.data.materials.append(material)
    return obj


def cord(name: str, points: list[tuple[float, float, float]], radius: float, material: bpy.types.Material, collection: bpy.types.Collection, parent: bpy.types.Object) -> bpy.types.Object:
    data = bpy.data.curves.new(name, "CURVE")
    data.dimensions = "3D"
    data.bevel_depth = radius
    data.bevel_resolution = 2
    spline = data.splines.new("POLY")
    spline.points.add(len(points) - 1)
    for point, coordinate in zip(spline.points, points):
        point.co = (*coordinate, 1.0)
    obj = bpy.data.objects.new(name, data)
    collection.objects.link(obj)
    for other in bpy.context.selected_objects:
        other.select_set(False)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.convert(target="MESH")
    obj.data.materials.append(material)
    obj.parent = parent
    return obj


def build() -> dict[str, object]:
    if bpy.data.collections.get(COLLECTION_NAME):
        raise ValueError(f"Collection already exists: {COLLECTION_NAME}")
    (PROJECT / "assets" / "textures").mkdir(parents=True, exist_ok=True)
    collection = bpy.data.collections.new(COLLECTION_NAME)
    bpy.context.scene.collection.children.link(collection)
    images, cloth = make_fabric_images()
    skin = solid("SL runner warm brown skin", (0.45, 0.27, 0.18), 0.73)
    skin_shadow = solid("SL runner skin shadow", (0.30, 0.17, 0.12), 0.78)
    hair = solid("SL runner dark curly hair", (0.105, 0.085, 0.075), 0.9)
    leather = solid("SL runner aged brown leather", (0.19, 0.13, 0.095), 0.69)
    sole = solid("SL runner rubber soles", (0.06, 0.065, 0.064), 0.94)
    brass = solid("SL runner aged brass", (0.42, 0.31, 0.15), 0.48, 0.68)
    light = solid("SL runner warm ivory stitch", (0.72, 0.65, 0.52), 0.86)
    eyes = solid("SL runner deep eyes", (0.045, 0.04, 0.035), 0.55)

    root = pivot("HarborRunnerRoot", (0, 0, 0), collection)
    hips = pivot("HipsPivot", (0, 0, 0.94), collection, root)
    loft("Jacket body", [(0.0, 0.18, 0.115, 0, 0), (0.11, 0.195, 0.13, 0, 0), (0.34, 0.235, 0.142, 0, 0), (0.44, 0.26, 0.134, 0, 0), (0.49, 0.115, 0.092, 0, 0)], cloth[0], collection, hips)
    loft("Canvas jacket hem", [(-0.015, 0.185, 0.12, 0, 0), (0.025, 0.188, 0.12, 0, 0)], cloth[0], collection, hips)
    ellipsoid("Neck", (0, 0, 0.515), (0.105, 0.095, 0.18), skin, collection, hips)
    ellipsoid("Head and cheeks", (0, -0.01, 0.67), (0.225, 0.21, 0.27), skin, collection, hips)
    ellipsoid("Nose bridge", (0, -0.13, 0.66), (0.043, 0.065, 0.085), skin, collection, hips, 12, 8)
    ellipsoid("Left ear", (-0.115, 0.004, 0.66), (0.045, 0.044, 0.075), skin, collection, hips, 12, 8)
    ellipsoid("Right ear", (0.115, 0.004, 0.66), (0.045, 0.044, 0.075), skin, collection, hips, 12, 8)
    ellipsoid("Hair cap", (0, 0.015, 0.765), (0.236, 0.225, 0.15), hair, collection, hips)
    for index in range(25):
        angle = math.tau * index / 25
        z = 0.77 + 0.028 * math.sin(index * 4.19)
        radius = 0.075 + 0.016 * math.sin(index * 3.61)
        ellipsoid(f"Hair curl {index + 1:02d}", (0.082 * math.cos(angle), 0.079 * math.sin(angle), z), (radius, radius, radius * 0.9), hair, collection, hips, 10, 6)
    for side, x in (("Left", -0.051), ("Right", 0.051)):
        ellipsoid(f"{side} eye white", (x, -0.117, 0.695), (0.038, 0.01, 0.019), light, collection, hips, 12, 8)
        ellipsoid(f"{side} pupil", (x, -0.124, 0.695), (0.014, 0.011, 0.015), eyes, collection, hips, 10, 6)
        box(f"{side} brow", (x, -0.117, 0.718), (0.05, 0.008, 0.007), hair, collection, hips, 0.002)
    cord("Quiet mouth", [(-0.028, -0.117, 0.614), (0, -0.128, 0.609), (0.028, -0.117, 0.614)], 0.003, skin_shadow, collection, hips)

    box("Jacket zip tape", (0, -0.132, 0.245), (0.024, 0.009, 0.44), cloth[2], collection, hips, 0.003)
    for index in range(13):
        box(f"Zip tooth {index + 1:02d}", (0, -0.141, 0.044 + index * 0.033), (0.022, 0.004, 0.006), brass, collection, hips)
    for side, x in (("Left", -0.15), ("Right", 0.15)):
        box(f"{side} chest pocket", (x, -0.141, 0.292), (0.105, 0.014, 0.115), cloth[0], collection, hips, 0.006)
        cord(f"{side} pocket seam", [(x - 0.046, -0.151, 0.33), (x + 0.046, -0.151, 0.33)], 0.0025, light, collection, hips)
    box("Shoulder signal patch", (0.21, -0.101, 0.388), (0.075, 0.006, 0.045), cloth[2], collection, hips, 0.004)

    for side, direction in (("Left", -1.0), ("Right", 1.0)):
        shoulder = pivot(f"{side}ShoulderPivot", (0.275 * direction, 0.0, 0.42), collection, hips)
        ellipsoid(f"{side} jacket shoulder", (0.013 * direction, 0, -0.028), (0.18, 0.205, 0.17), cloth[0], collection, shoulder)
        loft(f"{side} upper sleeve", [(0.0, 0.079, 0.086, 0, 0), (-0.23, 0.068, 0.072, 0.028 * direction, 0)], cloth[0], collection, shoulder)
        elbow = pivot(f"{side}ElbowPivot", (0.028 * direction, 0, -0.23), collection, shoulder)
        loft(f"{side} forearm sleeve", [(0.0, 0.067, 0.072, 0, 0), (-0.23, 0.05, 0.057, 0, 0)], cloth[0], collection, elbow)
        box(f"{side} cuff", (0, 0, -0.233), (0.11, 0.115, 0.045), cloth[2], collection, elbow, 0.01)
        ellipsoid(f"{side} hand", (0, -0.005, -0.285), (0.1, 0.07, 0.115), skin, collection, elbow, 14, 8)
        thumb = ellipsoid(f"{side} thumb", (-0.051 * direction, -0.032, -0.275), (0.043, 0.046, 0.07), skin, collection, elbow, 12, 8)
        thumb.rotation_euler[1] = 0.28 * direction

        leg = pivot(f"{side}HipPivot", (0.105 * direction, 0, 0.0), collection, hips)
        loft(f"{side} work trouser thigh", [(0.0, 0.095, 0.105, 0, 0), (-0.32, 0.092, 0.091, 0, 0), (-0.4, 0.077, 0.078, 0, 0)], cloth[1], collection, leg)
        knee = pivot(f"{side}KneePivot", (0, 0, -0.39), collection, leg)
        ellipsoid(f"{side} reinforced knee", (0, -0.08, -0.025), (0.145, 0.026, 0.125), cloth[1], collection, knee, 16, 10)
        loft(f"{side} work trouser calf", [(0.01, 0.079, 0.08, 0, 0), (-0.31, 0.064, 0.068, 0, 0), (-0.38, 0.069, 0.07, 0, 0)], cloth[1], collection, knee)
        box(f"{side} trouser cuff", (0, 0, -0.38), (0.14, 0.145, 0.06), cloth[2], collection, knee, 0.015)
        ellipsoid(f"{side} boot leather", (0, -0.055, -0.45), (0.18, 0.31, 0.16), leather, collection, knee, 20, 12)
        box(f"{side} boot sole", (0, -0.069, -0.512), (0.195, 0.335, 0.045), sole, collection, knee, 0.015)
        for lace in range(3):
            cord(f"{side} boot lace {lace + 1}", [(-0.045, -0.203, -0.415 - lace * 0.026), (0.045, -0.203, -0.415 - lace * 0.026)], 0.003, light, collection, knee)

    cord("Satchel shoulder strap", [(-0.22, -0.11, 0.47), (-0.11, -0.155, 0.38), (0.04, -0.162, 0.24), (0.2, -0.137, 0.1), (0.29, -0.06, -0.02)], 0.014, leather, collection, hips)
    box("Satchel body", (0.31, -0.025, 0.03), (0.19, 0.11, 0.22), leather, collection, hips, 0.025)
    box("Satchel flap", (0.31, -0.089, 0.083), (0.192, 0.016, 0.09), leather, collection, hips, 0.008)
    box("Satchel buckle", (0.31, -0.101, 0.045), (0.045, 0.012, 0.045), brass, collection, hips, 0.006)

    bpy.context.view_layer.update()
    source = PROJECT / "art" / "source" / "A001_harbor_runner.blend"
    bpy.data.libraries.write(str(source), {collection, *images}, compress=True)
    output = PROJECT / "assets" / "models" / "A001_harbor_runner.glb"
    export_result = export_articulated_by_material(COLLECTION_NAME, str(output))
    collection.hide_viewport = True
    mesh_objects = [obj for obj in collection.objects if obj.type == "MESH"]
    triangles = sum(sum(max(0, len(poly.vertices) - 2) for poly in obj.data.polygons) for obj in mesh_objects)
    return {"source": str(source), "export": str(output), "mesh_objects": len(mesh_objects), "export_meshes": export_result["export_meshes"], "triangles_before_modifiers": triangles, "textures": [image.filepath_raw for image in images]}


if __name__ == "__main__":
    print(build())
