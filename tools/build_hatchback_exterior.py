"""Build the Tide hatchback's formed exterior panels in Blender."""

import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
from car_geometry import box, cylinder, export_collection, material, panel, tube


PROJECT = Path(__file__).resolve().parents[1]
NAME = "A137_tide_hatchback_exterior"
COLLECTION = "A137 Tide hatchback exterior"


def painted_enamel():
    size = 512
    base_pixels = []
    orm_pixels = []
    normal_pixels = []
    for y in range(size):
        v = y / size
        for x in range(size):
            u = x / size
            broad = math.sin(math.tau * (u * 2.4 + v * 0.8)) * math.sin(math.tau * (v * 3.2 - u * 0.5))
            fleck = math.sin(math.tau * u * 131.0) * math.sin(math.tau * v * 137.0)
            tone = 1.0 + broad * 0.034 + fleck * 0.012
            base_pixels.extend((0.22 * tone, 0.51 * tone, 0.55 * tone, 1.0))
            orm_pixels.extend((1.0, 0.43 + broad * 0.035 + fleck * 0.012, 0.22, 1.0))
            normal_pixels.extend((0.5 + fleck * 0.007, 0.5 + broad * 0.006, 1.0, 1.0))

    def save(name, filename, color_space, pixels):
        image = bpy.data.images.new(name, width=size, height=size, alpha=True)
        image.colorspace_settings.name = color_space
        image.pixels.foreach_set(pixels)
        image.update()
        image.filepath_raw = str(PROJECT / "assets" / "textures" / filename)
        image.file_format = "PNG"
        image.save()
        image.pack()
        return image

    base = save("A137 Tide petrol paint", "A137_tide_paint_base.png", "sRGB", base_pixels)
    orm = save("A137 Tide paint ORM", "A137_tide_paint_orm.png", "Non-Color", orm_pixels)
    normal = save("A137 Tide paint normal", "A137_tide_paint_normal.png", "Non-Color", normal_pixels)
    result = bpy.data.materials.new("SL Tide petrol blue enamel")
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
    normal_map.inputs["Strength"].default_value = 0.22
    links = result.node_tree.links
    links.new(base_node.outputs["Color"], surface.inputs["Base Color"])
    links.new(orm_node.outputs["Color"], channels.inputs["Color"])
    links.new(channels.outputs["Green"], surface.inputs["Roughness"])
    links.new(channels.outputs["Blue"], surface.inputs["Metallic"])
    links.new(normal_node.outputs["Color"], normal_map.inputs["Color"])
    links.new(normal_map.outputs["Normal"], surface.inputs["Normal"])
    links.new(surface.outputs["BSDF"], output.inputs["Surface"])
    return result, (base, orm, normal)


def body_section(collection, paint, trim):
    stations = [(-2.03, 0.68), (-1.88, 0.83), (-1.5, 0.88), (-0.75, 0.92), (0.45, 0.92), (1.32, 0.89), (1.9, 0.82), (2.04, 0.71)]
    lower = []
    upper = []
    for y, width in stations:
        lower.extend([(-width * 0.94, y, 0.52), (width * 0.94, y, 0.52)])
        upper.extend([(-width, y, 1.09), (width, y, 1.09)])
    vertices = lower + upper
    faces = []
    count = len(stations)
    for index in range(count - 1):
        for side in range(2):
            a = index * 2 + side
            b = (index + 1) * 2 + side
            faces.append((a, b, count * 2 + b, count * 2 + a))
        a = index * 2
        b = (index + 1) * 2
        faces.append((count * 2 + a, count * 2 + b, count * 2 + b + 1, count * 2 + a + 1))
    panel("Pressed lower body and shoulder", vertices, faces, paint, collection)
    box("Underfloor and sill core", (0, 0, 0.55), (1.54, 3.75, 0.18), trim, collection, 0.09)

    samples = [-2.02 + step * 4.04 / 72 for step in range(73)]
    for side in (-1, 1):
        vertices = []
        for y in samples:
            width = 0.91 - 0.07 * abs(y) / 2.02
            bottom = 0.49
            for wheel_y in (-1.26, 1.2):
                dy = y - wheel_y
                if abs(dy) < 0.455:
                    bottom = max(bottom, 0.38 + math.sqrt(0.455 * 0.455 - dy * dy))
            vertices.extend([(side * width, y, bottom), (side * width, y, 1.08)])
        faces = [(2 * i, 2 * i + 1, 2 * i + 3, 2 * i + 2) for i in range(len(samples) - 1) if vertices[2 * i][2] < 1.08 and vertices[2 * i + 2][2] < 1.08]
        panel(f"{'Left' if side < 0 else 'Right'} sculpted arch side", vertices, faces, paint, collection)
        for wheel_y in (-1.26, 1.2):
            points = [(side * 0.923, y, z) for y, z in [(wheel_y - 0.455, 0.38)] + [(wheel_y + 0.455 * math.cos(math.pi - math.pi * i / 24), 0.38 + 0.455 * math.sin(math.pi - math.pi * i / 24)) for i in range(25)] + [(wheel_y + 0.455, 0.38)]]
            tube(f"{'Left' if side < 0 else 'Right'} wheel opening lip {wheel_y}", points, 0.014, trim, collection)


def top_surfaces(collection, paint, trim, glass):
    bonnet = [(-0.79, 1.04, 1.105), (0, 1.04, 1.15), (0.79, 1.04, 1.105), (-0.77, 1.53, 1.025), (0, 1.53, 1.07), (0.77, 1.53, 1.025), (-0.7, 1.98, 0.955), (0, 1.98, 0.995), (0.7, 1.98, 0.955)]
    panel("Crowned bonnet with formed shoulders", bonnet, [(0, 1, 4, 3), (1, 2, 5, 4), (3, 4, 7, 6), (4, 5, 8, 7)], paint, collection)
    panel("Short hatch deck", [(-0.75, -1.91, 1.015), (0, -1.91, 1.04), (0.75, -1.91, 1.015), (-0.79, -1.35, 1.105), (0, -1.35, 1.13), (0.79, -1.35, 1.105)], [(0, 1, 4, 3), (1, 2, 5, 4)], paint, collection)
    roof_vertices = [(-0.67, -0.89, 1.72), (0.67, -0.89, 1.72), (0.69, 0.66, 1.72), (-0.69, 0.66, 1.72), (-0.63, -0.87, 1.77), (0.63, -0.87, 1.77), (0.65, 0.64, 1.77), (-0.65, 0.64, 1.77)]
    panel("Crowned steel roof", roof_vertices, [(4, 5, 6, 7), (0, 4, 7, 3), (1, 2, 6, 5), (2, 3, 7, 6), (0, 1, 5, 4)], paint, collection)
    panel("Front windscreen", [(-0.75, 1.02, 1.12), (0.75, 1.02, 1.12), (0.65, 0.67, 1.71), (-0.65, 0.67, 1.71)], [(0, 1, 2, 3)], glass, collection, False)
    panel("Rear windscreen", [(-0.78, -1.32, 1.12), (0.78, -1.32, 1.12), (0.65, -0.88, 1.7), (-0.65, -0.88, 1.7)], [(0, 1, 2, 3)], glass, collection, False)
    for side in (-1, 1):
        x = side
        tube(f"{'Left' if side < 0 else 'Right'} front A pillar", [(x * 0.77, 1.04, 1.1), (x * 0.67, 0.67, 1.72)], 0.029, paint, collection)
        tube(f"{'Left' if side < 0 else 'Right'} rear C pillar", [(x * 0.79, -1.36, 1.1), (x * 0.67, -0.88, 1.72)], 0.043, paint, collection)
        tube(f"{'Left' if side < 0 else 'Right'} B pillar", [(x * 0.76, -0.25, 1.1), (x * 0.68, -0.25, 1.72)], 0.03, paint, collection)
        panel(f"{'Left' if side < 0 else 'Right'} front side glass", [(x * 0.775, -0.23, 1.13), (x * 0.69, -0.23, 1.69), (x * 0.69, 0.63, 1.69), (x * 0.77, 1.0, 1.13)], [(0, 1, 2, 3)], glass, collection, False)
        panel(f"{'Left' if side < 0 else 'Right'} rear side glass", [(x * 0.77, -1.28, 1.13), (x * 0.68, -0.87, 1.68), (x * 0.68, -0.28, 1.68), (x * 0.775, -0.28, 1.13)], [(0, 1, 2, 3)], glass, collection, False)
        tube(f"{'Left' if side < 0 else 'Right'} window belt", [(x * 0.79, -1.34, 1.11), (x * 0.79, 1.02, 1.11)], 0.013, trim, collection)


def details(collection, paint, trim, chrome, lamp, brake, dark):
    for side in (-1, 1):
        x = side
        for y in (-0.43, 0.73):
            tube(f"Door shutline {side} {y}", [(x * 0.927, y, 0.52), (x * 0.931, y, 1.08)], 0.006, dark, collection)
        box(f"Front door handle {side}", (x * 0.944, 0.17, 1.005), (0.037, 0.19, 0.034), chrome, collection, 0.012)
        box(f"Rear door handle {side}", (x * 0.946, -0.94, 1.005), (0.037, 0.16, 0.034), chrome, collection, 0.012)
        box(f"Lower protective side molding {side}", (x * 0.931, -0.27, 0.69), (0.025, 2.45, 0.038), trim, collection, 0.014)
        box(f"Mirror stalk {side}", (x * 0.91, 0.82, 1.22), (0.21, 0.075, 0.07), trim, collection, 0.016)
        box(f"Mirror shell {side}", (x * 1.04, 0.81, 1.29), (0.22, 0.22, 0.14), paint, collection, 0.07)
        box(f"Mirror face {side}", (x * 1.17, 0.8, 1.29), (0.009, 0.155, 0.093), chrome, collection, 0.004)
        box(f"Swept front lamp recess {side}", (x * 0.64, 2.035, 0.95), (0.42, 0.045, 0.19), dark, collection, 0.026)
        box(f"Front lens {side}", (x * 0.65, 2.069, 0.96), (0.36, 0.014, 0.13), lamp, collection, 0.025)
        box(f"Rear lamp pocket {side}", (x * 0.69, -2.036, 0.95), (0.38, 0.043, 0.26), dark, collection, 0.02)
        box(f"Rear brake lens {side}", (x * 0.69, -2.065, 0.975), (0.33, 0.014, 0.17), brake, collection, 0.025)
        box(f"Rear reverse lens {side}", (x * 0.69, -2.068, 0.865), (0.29, 0.014, 0.04), lamp, collection, 0.01)
    box("Front bumper fascia", (0, 2.075, 0.6), (1.73, 0.16, 0.17), trim, collection, 0.075)
    box("Rear bumper fascia", (0, -2.075, 0.6), (1.73, 0.16, 0.17), trim, collection, 0.075)
    box("Front lower grille", (0, 2.162, 0.67), (0.77, 0.012, 0.09), dark, collection, 0.014)
    box("Rear hatch release", (0, -2.059, 1.04), (0.1, 0.025, 0.035), chrome, collection, 0.014)
    box("Rear hatch plate recess", (0, -2.071, 0.79), (0.5, 0.012, 0.135), dark, collection, 0.02)
    box("Front plate recess", (0, 2.164, 0.55), (0.5, 0.012, 0.125), dark, collection, 0.018)
    for index in range(7):
        box(f"Lower grille vane {index}", (-0.32 + index * 0.105, 2.175, 0.67), (0.015, 0.012, 0.074), trim, collection, 0.004)
    tube("Hatch outline", [(-0.79, -1.35, 1.1), (-0.73, -1.87, 1.1), (-0.66, -2.06, 1.04), (0.66, -2.06, 1.04), (0.73, -1.87, 1.1), (0.79, -1.35, 1.1)], 0.006, dark, collection)


def build():
    previous = bpy.data.collections.get(COLLECTION)
    if previous:
        for obj in list(previous.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(previous)
    collection = bpy.data.collections.new(COLLECTION)
    bpy.context.scene.collection.children.link(collection)
    paint, images = painted_enamel()
    trim = material("SL Tide charcoal bumper polymer", (0.045, 0.06, 0.064), 0.81)
    chrome = material("SL Tide satin aluminium", (0.43, 0.49, 0.48), 0.37, 0.81)
    lamp = material("SL Tide warm ivory lamp lens", (0.76, 0.78, 0.68), 0.25)
    brake = material("SL Tide deep vermilion lamp lens", (0.44, 0.035, 0.025), 0.3)
    dark = material("SL Tide dark panel gaps", (0.015, 0.026, 0.029), 0.91)
    glass = material("SL Tide smoke glass", (0.11, 0.2, 0.205), 0.27, 0.1, 0.57)
    body_section(collection, paint, trim)
    top_surfaces(collection, paint, trim, glass)
    details(collection, paint, trim, chrome, lamp, brake, dark)
    return export_collection(NAME, collection, PROJECT, images)


if __name__ == "__main__":
    print(build())
