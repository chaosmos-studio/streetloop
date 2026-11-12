"""Render comparable full-body and face views for the identity review."""

from pathlib import Path
import sys

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "art/source/character_identities"
REVIEW = ROOT / "art/review/character_identities"


def target_camera(camera, position, target):
    camera.location = position
    camera.rotation_euler = (Vector(target) - camera.location).to_track_quat("-Z", "Y").to_euler()


def make_light(name, position, energy, size):
    data = bpy.data.lights.new(name, "AREA")
    data.energy = energy
    data.shape = "DISK"
    data.size = size
    light = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(light)
    light.location = position
    target_camera(light, position, (0, 0, 1.0))


identities = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ("mara", "dev", "sol")
for identity in identities:
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE / f"{identity}.blend"))
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 720
    scene.render.resolution_y = 960
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.view_settings.view_transform = "Standard"
    scene.world.color = (0.28, 0.31, 0.33)
    camera_data = bpy.data.cameras.new("Identity review camera")
    camera = bpy.data.objects.new("Identity review camera", camera_data)
    bpy.context.collection.objects.link(camera)
    camera_data.type = "ORTHO"
    scene.camera = camera
    make_light("Large front key", (-2.5, -3.5, 4.5), 500, 3.5)
    make_light("Soft side fill", (2.3, -1.5, 2.6), 250, 3.0)
    make_light("Edge light", (0.3, 2.5, 3.0), 330, 2.5)
    output = REVIEW / identity
    output.mkdir(parents=True, exist_ok=True)
    for view, position, target, scale in (
        ("front", (0, -4, 1.3), (0, 0, 0.88), 2.25),
        ("profile", (4, 0, 1.3), (0, 0, 0.88), 2.25),
        ("rear", (0, 4, 1.3), (0, 0, 0.88), 2.25),
        ("face", (0, -1.2, 1.72), (0, 0, 1.61), 0.46),
    ):
        target_camera(camera, position, target)
        camera_data.ortho_scale = scale
        scene.render.filepath = str(output / f"{view}.png")
        bpy.ops.render.render(write_still=True)
