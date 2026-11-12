"""Extract Blender's CC0 realistic body into an isolated Streetloop study."""

import sys
from pathlib import Path

import bpy
from mathutils import Vector


PROJECT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT / "art/source/A001_anatomy_study.blend"
EXPORT = PROJECT / "assets/models/A001_anatomy_proxy.glb"
REVIEW = PROJECT / "art/review/A001_anatomy_study"
SKIN_TEXTURE = PROJECT / "assets/textures/A001_skin_base.png"
BODY_NAME = "GEO-body_male_realistic"
EYE_NAMES = ("GEO-body_male_realistic.eye.L", "GEO-body_male_realistic.eye.R")


def skin_material():
    skin = bpy.data.materials.new("A001 warm brown skin study")
    skin.use_nodes = True
    nodes = skin.node_tree.nodes
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    shader = nodes.new("ShaderNodeBsdfPrincipled")
    shader.inputs["Roughness"].default_value = 0.77
    shader.inputs["Subsurface Weight"].default_value = 0.06
    broad = nodes.new("ShaderNodeTexNoise")
    broad.inputs["Scale"].default_value = 9
    broad.inputs["Detail"].default_value = 4
    tone = nodes.new("ShaderNodeValToRGB")
    tone.color_ramp.elements[0].position = 0.22
    tone.color_ramp.elements[0].color = (0.35, 0.205, 0.135, 1)
    tone.color_ramp.elements[1].position = 0.76
    tone.color_ramp.elements[1].color = (0.48, 0.305, 0.205, 1)
    texture = nodes.new("ShaderNodeTexNoise")
    texture.inputs["Scale"].default_value = 185
    texture.inputs["Detail"].default_value = 4
    texture.inputs["Roughness"].default_value = 0.65
    bump = nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.08
    bump.inputs["Distance"].default_value = 0.00035
    links = skin.node_tree.links
    links.new(broad.outputs["Fac"], tone.inputs["Fac"])
    links.new(tone.outputs["Color"], shader.inputs["Base Color"])
    links.new(texture.outputs["Fac"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], shader.inputs["Normal"])
    links.new(shader.outputs["BSDF"], output.inputs["Surface"])
    return skin


def simple_material(name, color, roughness):
    item = bpy.data.materials.new(name)
    item.use_nodes = True
    shader = item.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = (*color, 1)
    shader.inputs["Roughness"].default_value = roughness
    return item


def add_iris(name, location, material):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12)
    obj = bpy.context.object
    obj.name = name
    obj.location = location
    obj.scale = (0.0065, 0.0022, 0.0065)
    obj.data.materials.append(material)
    return obj


def bake_skin(proxy, material):
    SKIN_TEXTURE.parent.mkdir(parents=True, exist_ok=True)
    image = bpy.data.images.new("A001 baked skin color", width=2048, height=2048, alpha=False)
    image.generated_color = (0.43, 0.27, 0.185, 1)
    image_node = material.node_tree.nodes.new("ShaderNodeTexImage")
    image_node.image = image
    material.node_tree.nodes.active = image_node
    for selected in bpy.context.selected_objects:
        selected.select_set(False)
    proxy.hide_set(False)
    proxy.hide_render = False
    proxy.select_set(True)
    bpy.context.view_layer.objects.active = proxy
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 8
    scene.render.bake.margin = 12
    bpy.ops.object.bake(type="DIFFUSE", pass_filter={"COLOR"})
    image.filepath_raw = str(SKIN_TEXTURE)
    image.file_format = "PNG"
    image.save()
    image.pack()
    shader = material.node_tree.nodes.get("Principled BSDF")
    if shader is None:
        shader = next(node for node in material.node_tree.nodes if node.type == "BSDF_PRINCIPLED")
    material.node_tree.links.new(image_node.outputs["Color"], shader.inputs["Base Color"])
    proxy.hide_render = True
    proxy.hide_set(True)


def add_camera():
    camera_data = bpy.data.cameras.new("Anatomy review camera")
    camera = bpy.data.objects.new("Anatomy review camera", camera_data)
    bpy.context.collection.objects.link(camera)
    bpy.context.scene.camera = camera
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = 2.4
    return camera


def point_camera(camera, location, target):
    camera.location = location
    camera.rotation_euler = (Vector(target) - camera.location).to_track_quat("-Z", "Y").to_euler()


def add_light(name, location, power, size):
    data = bpy.data.lights.new(name, "AREA")
    data.energy = power
    data.shape = "DISK"
    data.size = size
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = (Vector((0, 0, 0.9)) - obj.location).to_track_quat("-Z", "Y").to_euler()


def move_to_origin(objects, offset, factor):
    for obj in objects:
        obj.location = (obj.location - offset) * factor
        obj.scale *= factor


def unwrap_body(body):
    for selected in bpy.context.selected_objects:
        selected.select_set(False)
    body.select_set(True)
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(island_margin=0.012)
    bpy.ops.object.mode_set(mode="OBJECT")


def main(bundle):
    if not bundle.is_file():
        raise FileNotFoundError(f"Download Blender human base meshes v1.4.1: {bundle}")
    REVIEW.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=str(bundle))
    bpy.context.preferences.filepaths.save_version = 0
    keep = {BODY_NAME, *EYE_NAMES}
    for obj in list(bpy.data.objects):
        if obj.name not in keep:
            bpy.data.objects.remove(obj, do_unlink=True)
    body = bpy.data.objects[BODY_NAME]
    eyes = [bpy.data.objects[name] for name in EYE_NAMES]
    for eye in eyes:
        world = eye.matrix_world.copy()
        eye.parent = None
        eye.matrix_world = world
    factor = 1.77 / body.dimensions.z
    offset = body.location.copy()
    move_to_origin([body, *eyes], offset, factor)
    body.name = "A001 anatomical sculpt"
    unwrap_body(body)
    body.data.materials.clear()
    body.data.materials.append(skin_material())
    for eye in eyes:
        eye.name = eye.name.replace("GEO-body_male_realistic.eye", "A001 eye")
        eye.data.materials.clear()
        eye.data.materials.append(simple_material("A001 warm eye white", (0.62, 0.56, 0.48), 0.23))
    iris_material = simple_material("A001 deep brown iris", (0.095, 0.052, 0.031), 0.31)
    irises = [add_iris(f"A001 iris {index + 1}", eye.location + Vector((0, -0.012, 0)), iris_material) for index, eye in enumerate(eyes)]
    sculpt_modifier = next(mod for mod in body.modifiers if mod.type == "MULTIRES")
    sculpt_modifier.levels = 2
    sculpt_modifier.sculpt_levels = 3
    sculpt_modifier.render_levels = 3
    proxy = body.copy()
    proxy.data = body.data.copy()
    bpy.context.collection.objects.link(proxy)
    proxy.name = "A001 gameplay topology proxy"
    proxy.data.name = "A001 body base topology"
    proxy.modifiers.clear()
    proxy.hide_render = True
    proxy.hide_set(True)
    bake_skin(proxy, body.data.materials[0])
    camera = add_camera()
    add_light("Large soft key", (-2.2, -3.0, 4.0), 600, 3.0)
    add_light("Soft fill", (2.0, 1.5, 2.2), 240, 2.5)
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 768
    scene.render.resolution_y = 1024
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.world.color = (0.27, 0.30, 0.31)
    scene.view_settings.view_transform = "Standard"
    point_camera(camera, (0, -4, 1.55), (0, 0, 0.89))
    bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE), compress=True)
    for name, location in (
        ("front", (0, -4, 1.55)),
        ("side", (4, 0, 1.55)),
        ("rear", (0, 4, 1.55)),
    ):
        point_camera(camera, location, (0, 0, 0.89))
        scene.render.filepath = str(REVIEW / f"{name}.png")
        bpy.ops.render.render(write_still=True)
    camera.data.ortho_scale = 0.65
    point_camera(camera, (0, -1.2, 1.75), (0, 0, 1.55))
    scene.render.filepath = str(REVIEW / "face.png")
    bpy.ops.render.render(write_still=True)
    camera.data.ortho_scale = 0.58
    point_camera(camera, (0.7, -0.8, 1.1), (0.4, 0, 0.85))
    scene.render.filepath = str(REVIEW / "hand.png")
    bpy.ops.render.render(write_still=True)
    body.hide_render = True
    proxy.hide_render = False
    proxy.hide_set(False)
    bpy.ops.object.select_all(action="DESELECT")
    for obj in [proxy, *eyes, *irises]:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = proxy
    bpy.ops.export_scene.gltf(
        filepath=str(EXPORT), export_format="GLB", use_selection=True,
        export_animations=False, export_apply=False,
    )
    print({
        "source": str(SOURCE), "export": str(EXPORT),
        "base_vertices": len(proxy.data.vertices),
        "sculpt_subdivision": sculpt_modifier.total_levels,
        "source_bytes": SOURCE.stat().st_size,
        "export_bytes": EXPORT.stat().st_size,
    })


if __name__ == "__main__":
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    main(Path(args[0]) if args else Path("/tmp/human-base-meshes-bundle-v1.4.1/human_base_meshes_bundle.blend"))
