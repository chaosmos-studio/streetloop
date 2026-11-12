"""Build a deforming adult runner and reference locomotion clips in Blender."""

import math
from pathlib import Path

import bpy


PROJECT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT / "art/source/A001_human_runner.blend"
EXPORT = PROJECT / "assets/models/A001_human_runner.glb"


def material(name, color, roughness):
    item = bpy.data.materials.new(name)
    item.diffuse_color = (*color, 1)
    item.use_nodes = True
    surface = item.node_tree.nodes.get("Principled BSDF")
    surface.inputs["Base Color"].default_value = (*color, 1)
    surface.inputs["Roughness"].default_value = roughness
    return item


def skinned_mesh(name, rings, group_weights, surface, rig, sides=16):
    vertices = []
    faces = []
    for x, y, z, width, depth in rings:
        for step in range(sides):
            angle = math.tau * step / sides
            vertices.append((x + width * math.cos(angle), y + depth * math.sin(angle), z))
    for row in range(len(rings) - 1):
        for step in range(sides):
            nxt = (step + 1) % sides
            faces.append((row * sides + step, row * sides + nxt, (row + 1) * sides + nxt, (row + 1) * sides + step))
    faces.append(tuple(reversed(range(sides))))
    faces.append(tuple((len(rings) - 1) * sides + step for step in range(sides)))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(surface)
    groups = {bone: obj.vertex_groups.new(name=bone) for bone in {name for weights in group_weights for name in weights}}
    for row, weights in enumerate(group_weights):
        for bone, amount in weights.items():
            groups[bone].add(list(range(row * sides, (row + 1) * sides)), amount, "REPLACE")
    modifier = obj.modifiers.new("Deform with human rig", "ARMATURE")
    modifier.object = rig
    obj.parent = rig
    for polygon in mesh.polygons:
        polygon.use_smooth = len(polygon.vertices) == 4
    return obj


def sphere(name, center, dimensions, surface, rig, bone, segments=20, rings=12):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings)
    obj = bpy.context.object
    obj.name = name
    obj.location = center
    obj.scale = tuple(v * 0.5 for v in dimensions)
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=True)
    obj.data.materials.append(surface)
    obj.vertex_groups.new(name=bone).add(list(range(len(obj.data.vertices))), 1, "REPLACE")
    modifier = obj.modifiers.new("Deform with human rig", "ARMATURE")
    modifier.object = rig
    obj.parent = rig
    for polygon in obj.data.polygons:
        polygon.use_smooth = True
    return obj


def make_rig():
    data = bpy.data.armatures.new("A001 human skeleton")
    rig = bpy.data.objects.new("HumanRig", data)
    bpy.context.collection.objects.link(rig)
    bpy.context.view_layer.objects.active = rig
    rig.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bones = [
        ("root", (0, 0, 0), (0, 0, 0.95), None),
        ("pelvis", (0, 0, 0.95), (0, 0, 1.08), "root"),
        ("spine", (0, 0, 1.07), (0, 0, 1.37), "pelvis"),
        ("chest", (0, 0, 1.36), (0, 0, 1.48), "spine"),
        ("neck", (0, 0, 1.48), (0, 0, 1.56), "chest"),
        ("head", (0, 0, 1.55), (0, 0, 1.76), "neck"),
    ]
    for side, sign in (("L", -1), ("R", 1)):
        bones.extend([
            (f"upper_arm.{side}", (sign * 0.225, 0, 1.435), (sign * 0.34, 0, 1.17), "chest"),
            (f"forearm.{side}", (sign * 0.34, 0, 1.17), (sign * 0.41, -0.01, 0.93), f"upper_arm.{side}"),
            (f"hand.{side}", (sign * 0.41, -0.01, 0.93), (sign * 0.44, -0.02, 0.78), f"forearm.{side}"),
            (f"thigh.{side}", (sign * 0.105, 0, 0.96), (sign * 0.115, 0, 0.53), "pelvis"),
            (f"shin.{side}", (sign * 0.115, 0, 0.53), (sign * 0.12, 0.01, 0.1), f"thigh.{side}"),
            (f"foot.{side}", (sign * 0.12, 0.01, 0.1), (sign * 0.12, -0.19, 0.045), f"shin.{side}"),
        ])
    for name, head, tail, parent in bones:
        bone = data.edit_bones.new(name)
        bone.head = head
        bone.tail = tail
        if parent:
            bone.parent = data.edit_bones[parent]
    bpy.ops.object.mode_set(mode="OBJECT")
    for bone in rig.pose.bones:
        bone.rotation_mode = "XYZ"
    rig.show_in_front = True
    return rig


def build_geometry(rig):
    canvas = material("Faded teal work canvas", (0.17, 0.29, 0.32), 0.85)
    denim = material("Charcoal cotton denim", (0.18, 0.2, 0.23), 0.89)
    skin = material("Warm brown skin", (0.46, 0.29, 0.2), 0.72)
    hair = material("Short dark curls", (0.085, 0.07, 0.06), 0.94)
    leather = material("Worn brown boot leather", (0.23, 0.14, 0.095), 0.76)
    sole = material("Rubber boot sole", (0.055, 0.057, 0.057), 0.95)
    pale = material("Eye white", (0.68, 0.57, 0.44), 0.6)
    eye = material("Brown iris", (0.045, 0.032, 0.027), 0.32)
    skinned_mesh("Continuous jacket body", [
        (0, 0, 0.96, 0.15, 0.11), (0, 0, 1.05, 0.17, 0.12),
        (0, 0, 1.2, 0.18, 0.12), (0, 0, 1.34, 0.205, 0.13),
        (0, 0, 1.42, 0.23, 0.125), (0, 0, 1.47, 0.125, 0.09),
    ], [
        {"pelvis": 1}, {"pelvis": 0.8, "spine": 0.2},
        {"spine": 1}, {"spine": 0.75, "chest": 0.25},
        {"chest": 1}, {"chest": 1},
    ], canvas, rig, 24)
    skinned_mesh("Denim pelvis", [
        (0, 0, 0.9, 0.16, 0.1), (0, 0, 0.98, 0.16, 0.12),
        (0, 0, 1.04, 0.15, 0.11),
    ], [{"pelvis": 1}] * 3, denim, rig, 24)
    sphere("Neck", (0, 0, 1.5), (0.105, 0.098, 0.14), skin, rig, "neck")
    sphere("Adult head and jaw", (0, 0, 1.645), (0.172, 0.187, 0.245), skin, rig, "head", 32, 20)
    sphere("Nose", (0, -0.105, 1.628), (0.044, 0.057, 0.083), skin, rig, "head", 14, 10)
    sphere("Hair silhouette", (0, 0.01, 1.753), (0.18, 0.19, 0.075), hair, rig, "head", 24, 12)
    for index in range(18):
        angle = math.tau * index / 18
        sphere(f"Curl {index + 1:02d}", (0.076 * math.cos(angle), 0.076 * math.sin(angle), 1.735 + 0.015 * math.sin(index * 4.2)), (0.04, 0.04, 0.046), hair, rig, "head", 10, 6)
    for side, sign in (("L", -1), ("R", 1)):
        sphere(f"Ear {side}", (sign * 0.087, 0, 1.64), (0.04, 0.036, 0.063), skin, rig, "head", 12, 8)
        sphere(f"Eye sclera {side}", (sign * 0.042, -0.087, 1.66), (0.03, 0.013, 0.013), pale, rig, "head", 12, 8)
        sphere(f"Iris {side}", (sign * 0.042, -0.097, 1.66), (0.013, 0.009, 0.012), eye, rig, "head", 12, 8)
        x = sign * 0.105
        skinned_mesh(f"Continuous sleeve {side}", [
            (sign * 0.22, 0, 1.44, 0.081, 0.085),
            (sign * 0.27, 0, 1.36, 0.076, 0.076),
            (sign * 0.34, 0, 1.17, 0.065, 0.066),
            (sign * 0.365, -0.005, 1.09, 0.058, 0.059),
            (sign * 0.41, -0.01, 0.94, 0.047, 0.048),
        ], [
            {f"upper_arm.{side}": 1}, {f"upper_arm.{side}": 1},
            {f"upper_arm.{side}": 0.5, f"forearm.{side}": 0.5},
            {f"forearm.{side}": 1}, {f"forearm.{side}": 1},
        ], canvas, rig)
        skinned_mesh(f"Hand and fingers {side}", [
            (sign * 0.41, -0.01, 0.945, 0.041, 0.034),
            (sign * 0.423, -0.013, 0.895, 0.046, 0.03),
            (sign * 0.43, -0.016, 0.845, 0.038, 0.024),
            (sign * 0.43, -0.018, 0.805, 0.022, 0.016),
        ], [{f"hand.{side}": 1}] * 4, skin, rig, 12)
        for finger in range(4):
            sphere(f"{side} finger {finger + 1}", (sign * (0.405 + 0.014 * finger), -0.018, 0.801 - 0.008 * abs(finger - 1.5)), (0.011, 0.019, 0.043), skin, rig, f"hand.{side}", 8, 6)
        sphere(f"{side} thumb", (sign * 0.37, -0.041, 0.871), (0.024, 0.023, 0.065), skin, rig, f"hand.{side}", 10, 8)
        skinned_mesh(f"Continuous trouser leg {side}", [
            (x, 0, 0.97, 0.095, 0.10),
            (sign * 0.11, 0, 0.81, 0.09, 0.093),
            (sign * 0.115, 0, 0.58, 0.074, 0.077),
            (sign * 0.115, 0, 0.52, 0.072, 0.075),
            (sign * 0.12, 0, 0.36, 0.067, 0.07),
            (sign * 0.12, 0.01, 0.13, 0.073, 0.075),
        ], [
            {f"thigh.{side}": 1}, {f"thigh.{side}": 1},
            {f"thigh.{side}": 0.75, f"shin.{side}": 0.25},
            {f"thigh.{side}": 0.35, f"shin.{side}": 0.65},
            {f"shin.{side}": 1}, {f"shin.{side}": 1},
        ], denim, rig)
        sphere(f"Leather boot {side}", (sign * 0.12, -0.075, 0.091), (0.164, 0.32, 0.14), leather, rig, f"foot.{side}", 24, 12)
        sphere(f"Rubber sole {side}", (sign * 0.12, -0.085, 0.034), (0.17, 0.34, 0.04), sole, rig, f"foot.{side}", 24, 8)


def key_pose(rig, frame, phase, mode):
    walk = mode == "Walk"
    run = mode == "Run"
    swing = math.sin(math.tau * phase)
    stride = 0.35 if walk else 0.58 if run else 0.0
    knee_lift = 0.42 if walk else 0.78 if run else 0.0
    bob = (0.018 if walk else 0.048 if run else 0.004) * (1 - math.cos(4 * math.pi * phase)) * 0.5
    bones = rig.pose.bones
    bones["root"].location.z = bob
    bones["pelvis"].rotation_euler = (0, 0.025 * swing, 0.026 * swing)
    bones["spine"].rotation_euler = (-0.025 if run else 0, -0.014 * swing, -0.018 * swing)
    bones["chest"].rotation_euler = (0, 0, -0.012 * swing)
    for side, offset in (("L", 0), ("R", 0.5)):
        leg_phase = (phase + offset) % 1
        wave = math.cos(math.tau * leg_phase)
        lift = max(0, -math.sin(math.tau * leg_phase))
        bones[f"thigh.{side}"].rotation_euler = (stride * wave, 0, 0)
        bones[f"shin.{side}"].rotation_euler = (-0.045 - knee_lift * lift, 0, 0)
        foot_roll = -0.16 * wave + 0.12 * lift if walk else -0.2 * wave if run else 0.0
        bones[f"foot.{side}"].rotation_euler = (foot_roll, 0, 0)
        bones[f"upper_arm.{side}"].rotation_euler = (-stride * 0.75 * wave, 0, 0)
        bones[f"forearm.{side}"].rotation_euler = (-0.13 - 0.35 * lift if run else -0.13 - 0.09 * lift, 0, 0)
        bones[f"hand.{side}"].rotation_euler = (0.06 * wave, 0, 0)
    if mode == "Jump":
        bones["root"].location.z = 0.04
        for side in ("L", "R"):
            bones[f"thigh.{side}"].rotation_euler.x = -0.24
            bones[f"shin.{side}"].rotation_euler.x = -0.45
            bones[f"upper_arm.{side}"].rotation_euler.x = -0.75
    if mode == "Land":
        bones["root"].location.z = -0.045
        for side in ("L", "R"):
            bones[f"thigh.{side}"].rotation_euler.x = 0.22
            bones[f"shin.{side}"].rotation_euler.x = -0.48
            bones[f"upper_arm.{side}"].rotation_euler.x = 0.18
    for bone in bones:
        bone.keyframe_insert(data_path="location", frame=frame)
        bone.keyframe_insert(data_path="rotation_euler", frame=frame)


def build_actions(rig):
    for name, end in (("Idle", 48), ("Walk", 24), ("Run", 16), ("Jump", 14), ("Land", 10)):
        action = bpy.data.actions.new(name)
        rig.animation_data_create()
        rig.animation_data.action = action
        for frame in range(1, end + 1):
            phase = (frame - 1) / (end - 1)
            key_pose(rig, frame, phase, name)
        action.use_fake_user = True
        track = rig.animation_data.nla_tracks.new()
        track.name = name
        track.strips.new(name, 1, action)
        track.mute = True
    rig.animation_data.action = bpy.data.actions["Idle"]


def main():
    bpy.context.preferences.filepaths.save_version = 0
    bpy.context.scene.render.fps = 30
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    rig = make_rig()
    build_geometry(rig)
    build_actions(rig)
    bpy.context.scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE), compress=True)
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.export_scene.gltf(
        filepath=str(EXPORT), export_format="GLB", use_selection=True,
        export_animations=True, export_animation_mode="ACTIONS",
        export_force_sampling=False, export_apply=False,
    )
    print(f"Built {SOURCE} and {EXPORT}")


if __name__ == "__main__":
    main()
