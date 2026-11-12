"""Build the repair shop's close-inspection service manual in Blender."""

import math
import sys
from pathlib import Path

import bpy


PROJECT = Path(__file__).resolve().parents[1]
COLLECTION_NAME = "A156 Harbor service manual"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from export_articulated_by_material import export_articulated_by_material


def material(name: str, color: tuple[float, float, float], roughness: float, metallic: float = 0.0) -> bpy.types.Material:
    result = bpy.data.materials.new(name)
    result.diffuse_color = (*color, 1.0)
    result.use_nodes = True
    surface = result.node_tree.nodes.get("Principled BSDF")
    surface.inputs["Base Color"].default_value = (*color, 1.0)
    surface.inputs["Roughness"].default_value = roughness
    surface.inputs["Metallic"].default_value = metallic
    return result


def cover_material() -> tuple[bpy.types.Material, list[bpy.types.Image]]:
    size = 512
    base_pixels = []
    orm_pixels = []
    normal_pixels = []
    for y in range(size):
        v = y / size
        for x in range(size):
            u = x / size
            warp = math.sin(math.tau * u * 92)
            weft = math.sin(math.tau * v * 96)
            broad = math.sin(math.tau * (u * 2.6 + v * 0.5)) * math.sin(math.tau * (v * 4.1 - u * 0.3))
            variation = 1.0 + 0.04 * broad + 0.022 * warp * weft
            base_pixels.extend((0.105 * variation, 0.225 * variation, 0.25 * variation, 1.0))
            orm_pixels.extend((1.0, 0.84 + 0.035 * broad, 0.0, 1.0))
            normal_pixels.extend((0.5 + 0.035 * warp, 0.5 + 0.035 * weft, 1.0, 1.0))

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

    base = save("A156 service manual cloth color", "A156_manual_cover_base.png", "sRGB", base_pixels)
    orm = save("A156 service manual cloth ORM", "A156_manual_cover_orm.png", "Non-Color", orm_pixels)
    normal = save("A156 service manual cloth normal", "A156_manual_cover_normal.png", "Non-Color", normal_pixels)
    result = bpy.data.materials.new("SL manual weathered teal cloth")
    result.use_nodes = True
    nodes = result.node_tree.nodes
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    surface = nodes.new("ShaderNodeBsdfPrincipled")
    base_node = nodes.new("ShaderNodeTexImage")
    base_node.image = base
    orm_node = nodes.new("ShaderNodeTexImage")
    orm_node.image = orm
    separate = nodes.new("ShaderNodeSeparateColor")
    normal_node = nodes.new("ShaderNodeTexImage")
    normal_node.image = normal
    normal_map = nodes.new("ShaderNodeNormalMap")
    normal_map.inputs["Strength"].default_value = 0.25
    links = result.node_tree.links
    links.new(base_node.outputs["Color"], surface.inputs["Base Color"])
    links.new(orm_node.outputs["Color"], separate.inputs["Color"])
    links.new(separate.outputs["Green"], surface.inputs["Roughness"])
    links.new(separate.outputs["Blue"], surface.inputs["Metallic"])
    links.new(normal_node.outputs["Color"], normal_map.inputs["Color"])
    links.new(normal_map.outputs["Normal"], surface.inputs["Normal"])
    links.new(surface.outputs["BSDF"], output.inputs["Surface"])
    return result, [base, orm, normal]


def pivot(name: str, position: tuple[float, float, float], collection: bpy.types.Collection, parent: bpy.types.Object | None = None) -> bpy.types.Object:
    result = bpy.data.objects.new(name, None)
    collection.objects.link(result)
    result.parent = parent
    result.location = position
    return result


def box(name: str, position: tuple[float, float, float], dimensions: tuple[float, float, float], surface: bpy.types.Material, collection: bpy.types.Collection, parent: bpy.types.Object, bevel: float = 0.0) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cube_add(size=1)
    result = bpy.context.object
    result.name = name
    result.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    result.data.materials.append(surface)
    if bevel:
        modifier = result.modifiers.new("Soft bound edge", "BEVEL")
        modifier.width = bevel
        modifier.segments = 3
        result.modifiers.new("Weighted normals", "WEIGHTED_NORMAL")
    for current in list(result.users_collection):
        current.objects.unlink(result)
    collection.objects.link(result)
    result.parent = parent
    result.location = position
    return result


def title(name: str, content: str, position: tuple[float, float, float], size: float, surface: bpy.types.Material, collection: bpy.types.Collection, parent: bpy.types.Object) -> bpy.types.Object:
    curve = bpy.data.curves.new(name, "FONT")
    curve.body = content
    curve.size = size
    curve.align_x = "CENTER"
    curve.align_y = "CENTER"
    curve.extrude = 0.00015
    result = bpy.data.objects.new(name, curve)
    collection.objects.link(result)
    for other in bpy.context.selected_objects:
        other.select_set(False)
    result.select_set(True)
    bpy.context.view_layer.objects.active = result
    bpy.ops.object.convert(target="MESH")
    result.data.materials.append(surface)
    result.parent = parent
    result.location = position
    return result


def build() -> dict[str, object]:
    if bpy.data.collections.get(COLLECTION_NAME):
        raise ValueError(f"Collection already exists: {COLLECTION_NAME}")
    collection = bpy.data.collections.new(COLLECTION_NAME)
    bpy.context.scene.collection.children.link(collection)
    cover, images = cover_material()
    paper = material("SL manual uncoated cream paper", (0.72, 0.68, 0.57), 0.91)
    paper_edge = material("SL manual page edge shadow", (0.55, 0.50, 0.41), 0.93)
    label = material("SL manual aged linen label", (0.58, 0.52, 0.41), 0.88)
    ink = material("SL manual dark screen print", (0.055, 0.085, 0.085), 0.89)
    stitch = material("SL manual cream binding stitch", (0.68, 0.58, 0.43), 0.88)
    brass = material("SL manual tarnished brass", (0.42, 0.29, 0.12), 0.48, 0.62)

    root = pivot("ManualRoot", (0, 0, 0), collection)
    box("Lower hard cover", (0, 0, 0.002), (0.30, 0.215, 0.004), cover, collection, root, 0.002)
    box("Page block", (0.004, 0, 0.017), (0.282, 0.198, 0.025), paper, collection, root, 0.002)
    for index in range(8):
        height = 0.006 + index * 0.003
        box(f"Visible leaf edge {index + 1:02d}", (0.146, 0, height), (0.002, 0.195, 0.001), paper_edge, collection, root)
    box("Bound spine", (-0.148, 0, 0.018), (0.018, 0.216, 0.036), cover, collection, root, 0.004)
    for index, y in enumerate((-0.077, -0.045, 0.045, 0.077)):
        box(f"Spine binding rib {index + 1}", (-0.154, y, 0.019), (0.005, 0.008, 0.035), stitch, collection, root, 0.001)

    cover_pivot = pivot("TopCoverPivot", (-0.146, 0, 0.033), collection, root)
    box("Upper hard cover", (0.146, 0, 0.002), (0.298, 0.215, 0.004), cover, collection, cover_pivot, 0.002)
    box("Inset linen title panel", (0.156, 0, 0.005), (0.198, 0.135, 0.001), label, collection, cover_pivot, 0.004)
    title("Cover heading", "HARBOR", (0.156, 0.035, 0.006), 0.023, ink, collection, cover_pivot)
    title("Cover subject", "SERVICE", (0.156, 0.004, 0.006), 0.019, ink, collection, cover_pivot)
    title("Cover volume", "BOOK 04", (0.156, -0.037, 0.006), 0.013, ink, collection, cover_pivot)
    for index, y in enumerate((-0.078, 0.078)):
        box(f"Cover stitch top {index}", (0.146, y, 0.006), (0.264, 0.002, 0.001), stitch, collection, cover_pivot)
    for index, x in enumerate((0.016, 0.276)):
        box(f"Cover stitch side {index}", (x, 0, 0.006), (0.002, 0.157, 0.001), stitch, collection, cover_pivot)
    for x in (0.025, 0.267):
        for y in (-0.087, 0.087):
            box(f"Corner guard {x:.3f} {y:.3f}", (x, y, 0.006), (0.02, 0.02, 0.002), brass, collection, cover_pivot, 0.003)

    bpy.context.view_layer.update()
    source = PROJECT / "art" / "source" / "A156_harbor_service_manual.blend"
    bpy.data.libraries.write(str(source), {collection, *images}, compress=True)
    output = PROJECT / "assets" / "models" / "A156_harbor_service_manual.glb"
    export_result = export_articulated_by_material(COLLECTION_NAME, str(output))
    collection.hide_viewport = True
    return {"source": str(source), "export": str(output), "source_meshes": export_result["source_meshes"], "export_meshes": export_result["export_meshes"], "textures": [image.filepath_raw for image in images]}


if __name__ == "__main__":
    print(build())
