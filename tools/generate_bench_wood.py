"""Build original packed PBR textures for the mechanic workbench."""

import math
from pathlib import Path

import bpy


def generate_bench_wood(project_root: str) -> dict[str, str]:
    root = Path(project_root)
    texture_dir = root / "assets" / "textures"
    texture_dir.mkdir(parents=True, exist_ok=True)
    width = 1024
    height = 512
    base_pixels: list[float] = []
    orm_pixels: list[float] = []
    normal_pixels: list[float] = []
    heights = [0.0] * (width * height)

    for y in range(height):
        v = y / height
        for x in range(width):
            u = x / width
            warp = 0.075 * math.sin(u * math.tau * 2.4 + v * 4)
            warp += 0.018 * math.sin(u * math.tau * 9.1 + v * 11)
            broad = math.sin(math.tau * (v * 27 + warp))
            fine = math.sin(math.tau * (v * 113 + warp * 1.7))
            pore = math.sin(math.tau * (u * 58 + v * 71))
            pore *= math.sin(math.tau * (u * 101 - v * 47))
            knot = math.exp(-((u - 0.32) / 0.055) ** 2 - ((v - 0.49) / 0.09) ** 2)
            scratch = float(abs(math.sin(math.tau * (v * 76 + u * 0.24))) > 0.997 and 0.18 < u < 0.86)
            grain = 0.54 + 0.17 * broad + 0.055 * fine + 0.022 * pore - 0.13 * knot + 0.045 * scratch
            warmth = 0.92 + 0.06 * math.sin(math.tau * (u * 1.3 + v * 0.7))
            base_pixels.extend((0.43 * grain * warmth + 0.09, 0.26 * grain * warmth + 0.04, 0.14 * grain * warmth + 0.026, 1.0))
            roughness = max(0.60, min(0.91, 0.75 - 0.055 * broad + 0.018 * pore + 0.04 * scratch))
            orm_pixels.extend((1.0, roughness, 0.0, 1.0))
            heights[y * width + x] = 0.0038 * broad + 0.0009 * fine + 0.001 * pore + 0.002 * scratch

    for y in range(height):
        for x in range(width):
            dx = (heights[y * width + (x + 1) % width] - heights[y * width + (x - 1) % width]) * 14
            dy = (heights[((y + 1) % height) * width + x] - heights[((y - 1) % height) * width + x]) * 14
            length = math.sqrt(dx * dx + dy * dy + 1)
            normal_pixels.extend((0.5 - 0.5 * dx / length, 0.5 - 0.5 * dy / length, 0.5 + 0.5 / length, 1.0))

    def save_image(name: str, filename: str, color_space: str, pixels: list[float]) -> bpy.types.Image:
        existing = bpy.data.images.get(name)
        if existing:
            bpy.data.images.remove(existing)
        image = bpy.data.images.new(name, width=width, height=height, alpha=True)
        image.colorspace_settings.name = color_space
        image.pixels.foreach_set(pixels)
        image.update()
        image.filepath_raw = str(texture_dir / filename)
        image.file_format = "PNG"
        image.save()
        image.pack()
        return image

    base = save_image("A164 Workbench matte wood base color", "A164_workbench_wood_base.png", "sRGB", base_pixels)
    orm = save_image("A164 Workbench occlusion roughness metallic", "A164_workbench_wood_orm.png", "Non-Color", orm_pixels)
    normal = save_image("A164 Workbench fine grain normal", "A164_workbench_wood_normal.png", "Non-Color", normal_pixels)

    material = bpy.data.materials["SL bench weathered hardwood"]
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
    normal_map.inputs["Strength"].default_value = 0.65
    links = material.node_tree.links
    links.new(base_node.outputs["Color"], surface.inputs["Base Color"])
    links.new(orm_node.outputs["Color"], channels.inputs["Color"])
    links.new(channels.outputs["Green"], surface.inputs["Roughness"])
    links.new(channels.outputs["Blue"], surface.inputs["Metallic"])
    links.new(normal_node.outputs["Color"], normal_map.inputs["Color"])
    links.new(normal_map.outputs["Normal"], surface.inputs["Normal"])
    links.new(surface.outputs["BSDF"], output.inputs["Surface"])

    material_source = root / "art" / "source" / "A164_bench_surface_material.blend"
    bpy.data.libraries.write(str(material_source), {material, base, orm, normal}, compress=True)
    return {
        "base": str(base.filepath_raw),
        "orm": str(orm.filepath_raw),
        "normal": str(normal.filepath_raw),
        "source": str(material_source),
    }
