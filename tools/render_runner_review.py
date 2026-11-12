"""Render three neutral inspection angles of the Blender runner asset."""

from pathlib import Path

import bpy
from mathutils import Vector


PROJECT = Path(__file__).resolve().parents[1]


def render_review() -> dict[str, str]:
    collection = bpy.data.collections["A001 Harbor runner"]
    scene = bpy.data.scenes.new("Temporary A001 character review")
    scene.collection.children.link(collection)
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 640
    scene.render.resolution_y = 800
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.world = bpy.data.worlds.new("Temporary character review world")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes.get("Background").inputs["Color"].default_value = (0.28, 0.31, 0.32, 1.0)
    scene.world.node_tree.nodes.get("Background").inputs["Strength"].default_value = 0.7

    camera_data = bpy.data.cameras.new("A001 review camera")
    camera = bpy.data.objects.new("A001 review camera", camera_data)
    scene.collection.objects.link(camera)
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = 2.3
    scene.camera = camera

    def add_light(name: str, position: tuple[float, float, float], energy: float, size: float) -> None:
        data = bpy.data.lights.new(name, "AREA")
        data.energy = energy
        data.shape = "DISK"
        data.size = size
        obj = bpy.data.objects.new(name, data)
        scene.collection.objects.link(obj)
        obj.location = position
        obj.rotation_euler = (Vector((0, 0, 1.0)) - obj.location).to_track_quat("-Z", "Y").to_euler()

    add_light("Warm key", (-2.5, -3.0, 4.2), 440, 4.0)
    add_light("Cool fill", (2.5, -1.5, 2.4), 250, 3.0)
    add_light("Soft rim", (0.5, 2.5, 3.1), 380, 2.5)

    output_dir = PROJECT / "art" / "review" / "A001_harbor_runner"
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = {}
    for name, position in (
        ("front", (0, -4, 1.0)),
        ("side", (4, 0, 1.0)),
        ("rear", (0, 4, 1.0)),
    ):
        camera.location = position
        camera.rotation_euler = (Vector((0, 0, 0.87)) - camera.location).to_track_quat("-Z", "Y").to_euler()
        output = output_dir / f"{name}.png"
        scene.render.filepath = str(output)
        bpy.ops.render.render(write_still=True, scene=scene.name)
        outputs[name] = str(output)

    bpy.data.scenes.remove(scene)
    return outputs


if __name__ == "__main__":
    print(render_review())
