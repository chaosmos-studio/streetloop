"""Build editable adult identity studies from the reviewed anatomy source."""

import math
import random
import sys
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "art/source/A001_anatomy_study.blend"
FEMALE_BASE = ROOT / "art/source/A001_female_anatomy_study.blend"
OUT_SOURCE = ROOT / "art/source/character_identities"
OUT_EXPORT = ROOT / "assets/models/characters"
IDENTITIES = {
    "mara": {"shoulders": 0.91, "waist": 0.88, "hips": 1.03, "jaw": 0.94, "cheeks": 1.04, "nose": 0.97, "head": 1.015, "skin": (0.34, 0.18, 0.095), "hair": (0.040, 0.023, 0.015), "shirt": (0.16, 0.23, 0.22), "pants": (0.075, 0.11, 0.15)},
    "dev": {"shoulders": 1.04, "waist": 1.01, "hips": 0.98, "jaw": 1.04, "cheeks": 0.99, "nose": 1.02, "head": 1.0, "skin": (0.24, 0.12, 0.062), "hair": (0.025, 0.020, 0.019), "shirt": (0.12, 0.17, 0.22), "pants": (0.065, 0.075, 0.085)},
    "sol": {"shoulders": 0.98, "waist": 1.10, "hips": 1.08, "jaw": 1.02, "cheeks": 1.06, "nose": 1.06, "head": 1.025, "skin": (0.48, 0.28, 0.16), "hair": (0.055, 0.035, 0.025), "shirt": (0.25, 0.17, 0.13), "pants": (0.13, 0.15, 0.14)},
}


def material(name, rgb, roughness):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*rgb, 1)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1)
    bsdf.inputs["Roughness"].default_value = roughness
    return mat


def copy_mesh(obj, name, surface):
    result = obj.copy()
    result.data = obj.data.copy()
    bpy.context.collection.objects.link(result)
    result.name = name
    result.data.materials.clear()
    result.data.materials.append(surface)
    return result


def modulate_body(body, spec):
    bpy.context.view_layer.objects.active = body
    body.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    for vertex in body.data.vertices:
        p = vertex.co
        if p.z > 1.47:
            head_influence = min(1.0, (p.z - 1.47) / 0.08)
            p.x *= 1.0 + (spec["head"] - 1.0) * head_influence
            p.z = 1.47 + (p.z - 1.47) * (1.0 + (spec["head"] - 1.0) * head_influence)
            if p.z < 1.59:
                p.x *= 1.0 + (spec["jaw"] - 1.0) * head_influence
            if 1.57 < p.z < 1.635 and p.y < -0.09:
                p.x *= spec["cheeks"]
            if p.y < -0.13 and 1.57 < p.z < 1.68 and abs(p.x) < 0.045:
                p.y *= spec["nose"]
        elif p.z > 0.93:
            torso = min(1.0, (p.z - 0.93) / 0.48)
            width = spec["waist"] * (1.0 - torso) + spec["shoulders"] * torso
            if abs(p.x) < 0.26:
                p.x *= width
        elif p.z > 0.48:
            influence = min(1.0, (p.z - 0.48) / 0.42)
            if abs(p.x) < 0.26:
                p.x *= 1.0 + (spec["hips"] - 1.0) * influence
    body.data.update()
    for polygon in body.data.polygons:
        polygon.use_smooth = True


def make_rig(name):
    armature = bpy.data.armatures.new("Shared adult skeleton")
    rig = bpy.data.objects.new("AdultRig", armature)
    bpy.context.collection.objects.link(rig)
    bpy.ops.object.select_all(action="DESELECT")
    rig.select_set(True)
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode="EDIT")
    bones = [
        ("root", (0, 0, 0), (0, 0, 0.94), None),
        ("pelvis", (0, 0, 0.94), (0, 0, 1.06), "root"),
        ("spine", (0, 0, 1.06), (0, 0, 1.32), "pelvis"),
        ("chest", (0, 0, 1.32), (0, 0, 1.46), "spine"),
        ("neck", (0, 0, 1.46), (0, 0, 1.55), "chest"),
        ("head", (0, 0, 1.55), (0, 0, 1.75), "neck"),
        ("jaw", (0, -0.065, 1.565), (0, -0.10, 1.61), "head"),
    ]
    thigh_x = 0.13 if name == "mara" else 0.16
    knee_x = 0.15 if name == "mara" else 0.17
    foot_x = 0.16 if name == "mara" else 0.215
    for side, sign in (("L", 1), ("R", -1)):
        bones.extend([
            (f"clavicle.{side}", (0, 0, 1.43), (sign * 0.17, 0, 1.43), "chest"),
            (f"upper_arm.{side}", (sign * 0.17, 0, 1.43), (sign * 0.32, 0, 1.17), f"clavicle.{side}"),
            (f"forearm.{side}", (sign * 0.32, 0, 1.17), (sign * 0.40, -0.01, 0.94), f"upper_arm.{side}"),
            (f"hand.{side}", (sign * 0.40, -0.01, 0.94), (sign * 0.45, -0.02, 0.82), f"forearm.{side}"),
            (f"thigh.{side}", (sign * thigh_x, 0, 0.94), (sign * knee_x, 0, 0.53), "pelvis"),
            (f"shin.{side}", (sign * knee_x, 0, 0.53), (sign * foot_x, 0, 0.11), f"thigh.{side}"),
            (f"foot.{side}", (sign * foot_x, 0, 0.11), (sign * foot_x, -0.12, 0.045), f"shin.{side}"),
            (f"toe.{side}", (sign * foot_x, -0.12, 0.045), (sign * foot_x, -0.17, 0.04), f"foot.{side}"),
        ])
        for finger in range(5):
            label = ("thumb", "index", "middle", "ring", "little")[finger]
            x = sign * (0.425 + finger * 0.011)
            first = (x, -0.02, 0.82)
            middle = (x, -0.02, 0.77)
            tip = (x, -0.02, 0.73)
            bones.append((f"{label}_1.{side}", first, middle, f"hand.{side}"))
            bones.append((f"{label}_2.{side}", middle, tip, f"{label}_1.{side}"))
    for name, head, tail, parent in bones:
        item = armature.edit_bones.new(name)
        item.head = head
        item.tail = tail
        if parent:
            item.parent = armature.edit_bones[parent]
    bpy.ops.object.mode_set(mode="OBJECT")
    for pose in rig.pose.bones:
        pose.rotation_mode = "XYZ"
    return rig


def attach_auto(obj, rig):
    bpy.ops.object.select_all(action="DESELECT")
    obj.hide_set(False)
    obj.select_set(True)
    rig.select_set(True)
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.parent_set(type="ARMATURE_AUTO")


def attach_bone(obj, rig, bone):
    group = obj.vertex_groups.new(name=bone)
    group.add(list(range(len(obj.data.vertices))), 1.0, "REPLACE")
    modifier = obj.modifiers.new("Adult skin", "ARMATURE")
    modifier.object = rig
    obj.parent = rig


def shell_from_body(body, name, surface, predicate, offset):
    shell = copy_mesh(body, name, surface)
    mesh = shell.data
    for vertex in mesh.vertices:
        vertex.co += vertex.normal * offset
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.verts.ensure_lookup_table()
    remove = [face for face in bm.faces if not predicate(face.calc_center_median())]
    bmesh.ops.delete(bm, geom=remove, context="FACES")
    if name in ("Cotton work shirt", "Denim trousers"):
        for vertex in bm.verts:
            if vertex.is_boundary:
                if name == "Cotton work shirt":
                    vertex.co.z = 0.99 if vertex.co.z < 1.2 else 1.49
                else:
                    vertex.co.z = 0.11 if vertex.co.z < 0.55 else 1.06
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    for polygon in mesh.polygons:
        polygon.use_smooth = True
    solid = shell.modifiers.new("Fabric thickness", "SOLIDIFY")
    solid.thickness = 0.003
    solid.offset = 0.0
    shell.parent = body.parent
    armature = shell.modifiers.new("Adult skin", "ARMATURE")
    armature.object = body.parent
    return shell


def sphere(name, xyz, scale, surface, rig, bone, segments=16):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=max(8, segments // 2), location=xyz)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(surface)
    attach_bone(obj, rig, bone)
    for face in obj.data.polygons:
        face.use_smooth = True
    return obj


def ring(name, xyz, radius, thickness, scale, surface, rig, bone):
    bpy.ops.mesh.primitive_torus_add(major_segments=32, minor_segments=8, location=xyz, major_radius=radius, minor_radius=thickness)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(surface)
    attach_bone(obj, rig, bone)
    for face in obj.data.polygons:
        face.use_smooth = True
    return obj


def bevelled_box(name, xyz, dimensions, bevel_width, surface, rig, bone):
    bpy.ops.mesh.primitive_cube_add(location=xyz)
    obj = bpy.context.object
    obj.name = name
    obj.scale = tuple(d / 2 for d in dimensions)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(surface)
    bevel = obj.modifiers.new("Soft constructed edge", "BEVEL")
    bevel.width = bevel_width
    bevel.segments = 3
    obj.modifiers.new("Weighted corner normals", "WEIGHTED_NORMAL")
    attach_bone(obj, rig, bone)
    return obj


def constructed_shoe(side, center_x, rig, leather, rubber, lace_surface):
    profiles = [(-0.165, 0.032, 0.052), (-0.120, 0.072, 0.080), (-0.045, 0.082, 0.095), (0.055, 0.075, 0.110), (0.125, 0.045, 0.085), (0.150, 0.008, 0.045)]
    vertices = []
    faces = []
    segments = 12
    for y, half_width, height in profiles:
        for segment in range(segments):
            angle = math.tau * segment / segments
            vertices.append((center_x + half_width * math.cos(angle), y, max(0.036, 0.045 + height * math.sin(angle))))
    for row in range(len(profiles) - 1):
        for segment in range(segments):
            next_segment = (segment + 1) % segments
            faces.append((row * segments + segment, row * segments + next_segment, (row + 1) * segments + next_segment, (row + 1) * segments + segment))
    faces.append(tuple(reversed(range(segments))))
    faces.append(tuple((len(profiles) - 1) * segments + segment for segment in range(segments)))
    mesh = bpy.data.meshes.new(f"Constructed shoe {side} mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.materials.append(leather)
    mesh.update()
    upper = bpy.data.objects.new(f"Leather shoe {side}", mesh)
    bpy.context.collection.objects.link(upper)
    attach_bone(upper, rig, f"foot.{side}")
    for face in mesh.polygons:
        face.use_smooth = True

    outline = [(0.0, -0.182), (0.055, -0.169), (0.087, -0.117), (0.091, -0.022), (0.083, 0.071), (0.058, 0.133), (0.0, 0.150), (-0.058, 0.133), (-0.083, 0.071), (-0.091, -0.022), (-0.087, -0.117), (-0.055, -0.169)]
    sole_vertices = [(center_x + x, y, z) for z in (0.012, 0.039) for x, y in outline]
    sole_faces = []
    count = len(outline)
    sole_faces.append(tuple(reversed(range(count))))
    sole_faces.append(tuple(range(count, count * 2)))
    for index in range(count):
        following = (index + 1) % count
        sole_faces.append((index, following, following + count, index + count))
    sole_mesh = bpy.data.meshes.new(f"Shoe sole {side} mesh")
    sole_mesh.from_pydata(sole_vertices, [], sole_faces)
    sole_mesh.materials.append(rubber)
    sole_mesh.update()
    sole = bpy.data.objects.new(f"Shoe sole {side}", sole_mesh)
    bpy.context.collection.objects.link(sole)
    bevel = sole.modifiers.new("Soft sole edge", "BEVEL")
    bevel.width = 0.006
    bevel.segments = 2
    sole.modifiers.new("Weighted sole normals", "WEIGHTED_NORMAL")
    attach_bone(sole, rig, f"foot.{side}")
    for index in range(4):
        y = -0.085 + index * 0.035
        bevelled_box(f"Lace {side} {index}", (center_x, y, 0.130 + index * 0.006), (0.080, 0.005, 0.003), 0.001, lace_surface, rig, f"foot.{side}")


def hair(rig, surface, style):
    sphere(f"Hair_{style}_cap", (0, -0.009, 1.726), (0.100, 0.113, 0.077), surface, rig, "head", 32)
    rng = random.Random({"sweep": 421, "short": 367, "curl": 829}[style])
    count = 1800 if style == "short" else 2600
    vertices = []
    faces = []
    for index in range(count):
        angle = math.tau * (index * 0.61803398875 + rng.uniform(-0.018, 0.018))
        polar = math.acos(1.0 - 0.91 * ((index + 0.5) / count))
        root = Vector((0.100 * math.sin(polar) * math.cos(angle), -0.009 + 0.113 * math.sin(polar) * math.sin(angle), 1.726 + 0.077 * math.cos(polar)))
        radial = Vector((math.cos(angle), math.sin(angle), -0.30)).normalized()
        length = rng.uniform(0.006, 0.013) if style == "short" else rng.uniform(0.010, 0.020)
        sweep = Vector((0.18, 0, 0.05)) if style == "sweep" else Vector((0, 0, 0))
        curl = Vector((0.34 * math.sin(index * 2.4), 0.34 * math.cos(index * 2.4), 0.12)) if style == "curl" else Vector((0, 0, 0))
        tangent = (radial + sweep + curl).normalized()
        side = tangent.cross(Vector((0, 0, 1))).normalized()
        if side.length_squared < 0.1:
            side = Vector((1, 0, 0))
        up = tangent.cross(side).normalized()
        radius = rng.uniform(0.00055, 0.00095)
        for step in range(4):
            fraction = step / 3.0
            center = root + tangent * length * fraction + Vector((0, 0, -0.008 * fraction * fraction))
            width = radius * max(0.04, 1.0 - fraction)
            for corner in range(3):
                direction = side * math.cos(math.tau * corner / 3) + up * math.sin(math.tau * corner / 3)
                vertices.append(tuple(center + direction * width))
        first = index * 12
        for step in range(3):
            for corner in range(3):
                following = (corner + 1) % 3
                faces.append((first + step * 3 + corner, first + step * 3 + following, first + (step + 1) * 3 + following, first + (step + 1) * 3 + corner))
    mesh = bpy.data.meshes.new(f"Hair_{style}_strands mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.materials.append(surface)
    mesh.update()
    strands = bpy.data.objects.new(f"Hair_{style}_strands", mesh)
    bpy.context.collection.objects.link(strands)
    attach_bone(strands, rig, "head")


def join_hair():
    pieces = [obj for obj in bpy.context.scene.objects if obj.name.startswith("Hair_")]
    bpy.ops.object.select_all(action="DESELECT")
    for obj in pieces:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = pieces[0]
    bpy.ops.object.join()
    pieces[0].name = "Groom"


def join_beard():
    pieces = [obj for obj in bpy.context.scene.objects if obj.name.startswith("Beard ")]
    bpy.ops.object.select_all(action="DESELECT")
    for obj in pieces:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = pieces[0]
    bpy.ops.object.join()
    pieces[0].name = "Beard"


def set_pose(rig, frame, phase, mode):
    bones = rig.pose.bones
    walking = mode == "Walk"
    running = mode == "Run"
    stride = 0.43 if walking else 0.62 if running else 0.0
    knee = 0.45 if walking else 0.77 if running else 0.0
    wave = math.sin(math.tau * phase)
    bones["root"].location.z = (0.014 if walking else 0.037 if running else 0.003) * (1 - math.cos(4 * math.pi * phase)) * 0.5
    bones["pelvis"].rotation_euler = (0, 0.025 * wave, 0.035 * wave)
    bones["spine"].rotation_euler = (-0.035 if running else 0.0, -0.012 * wave, -0.018 * wave)
    bones["chest"].rotation_euler = (0, 0, -0.018 * wave)
    bones["head"].rotation_euler = (0.012 * wave, 0, 0)
    for side, offset in (("L", 0), ("R", 0.5)):
        part = (phase + offset) % 1.0
        lead = math.cos(math.tau * part)
        lift = max(0.0, -math.sin(math.tau * part))
        bones[f"thigh.{side}"].rotation_euler = (stride * lead, 0, 0)
        bones[f"shin.{side}"].rotation_euler = (-0.04 - knee * lift, 0, 0)
        bones[f"foot.{side}"].rotation_euler = (-0.15 * lead + 0.11 * lift, 0, 0)
        bones[f"upper_arm.{side}"].rotation_euler = (-stride * 0.68 * lead, 0, 0)
        bones[f"forearm.{side}"].rotation_euler = (-0.12 - 0.25 * lift if running else -0.10, 0, 0)
    if mode in ("Jump", "Land"):
        bones["root"].location.z = 0.04 if mode == "Jump" else -0.035
        for side in ("L", "R"):
            bones[f"thigh.{side}"].rotation_euler.x = -0.28 if mode == "Jump" else 0.23
            bones[f"shin.{side}"].rotation_euler.x = -0.4
            bones[f"upper_arm.{side}"].rotation_euler.x = -0.75 if mode == "Jump" else 0.2
    for bone in bones:
        bone.keyframe_insert(data_path="location", frame=frame)
        bone.keyframe_insert(data_path="rotation_euler", frame=frame)


def make_actions(rig):
    bpy.context.scene.render.fps = 30
    for name, end in (("Idle", 60), ("Walk", 22), ("Run", 16), ("Jump", 12), ("Land", 9)):
        action = bpy.data.actions.new(name)
        rig.animation_data_create()
        rig.animation_data.action = action
        for frame in range(1, end + 1):
            set_pose(rig, frame, (frame - 1) / (end - 1), name)
        action.use_fake_user = True
        track = rig.animation_data.nla_tracks.new()
        track.name = name
        track.strips.new(name, 1, action)
        track.mute = True
    rig.animation_data.action = bpy.data.actions["Idle"]


def build_identity(name, spec):
    bpy.ops.wm.open_mainfile(filepath=str(FEMALE_BASE if name == "mara" else BASE))
    bpy.context.preferences.filepaths.save_version = 0
    keep = {"A001 gameplay topology proxy", "A001 eye.L", "A001 eye.R", "A001 iris 1", "A001 iris 2"}
    for obj in list(bpy.data.objects):
        if obj.name not in keep:
            bpy.data.objects.remove(obj, do_unlink=True)
    body = bpy.data.objects["A001 gameplay topology proxy"]
    body.hide_set(False)
    body.hide_render = False
    body.name = f"{name.title()} body"
    skin = material(f"{name.title()} skin", spec["skin"], 0.74)
    fabric = material(f"{name.title()} cotton", spec["shirt"], 0.91)
    denim = material(f"{name.title()} denim", spec["pants"], 0.92)
    hair_mat = material(f"{name.title()} hair", spec["hair"], 0.9)
    eye_white = material("Warm eye white", (0.43, 0.41, 0.37), 0.3)
    iris_mat = material("Brown iris", (0.040, 0.027, 0.021), 0.35)
    leather = material("Oxblood leather", (0.080, 0.046, 0.028), 0.70)
    rubber = material("Rubber sole", (0.045, 0.048, 0.05), 0.95)
    button = material("Horn button", (0.24, 0.18, 0.13), 0.55)
    body.data.materials.clear()
    body.data.materials.append(skin)
    modulate_body(body, spec)
    rig = make_rig(name)
    attach_auto(body, rig)
    for obj in list(bpy.data.objects):
        if obj.name.startswith("A001 eye") or obj.name.startswith("A001 iris"):
            obj.scale *= 0.73
            obj.location.y += 0.016
            obj.data.materials.clear()
            obj.data.materials.append(eye_white if obj.name.startswith("A001 eye") else iris_mat)
            attach_bone(obj, rig, "head")
    shell_from_body(body, "Cotton work shirt", fabric, lambda p: 0.99 < p.z < 1.49, 0.013)
    shell_from_body(body, "Denim trousers", denim, lambda p: 0.11 < p.z < 1.06 and abs(p.x) < 0.29, 0.012)
    ring("Cotton collar", (0, 0, 1.492), 0.074, 0.014, (1.20, 1.0, 1.0), fabric, rig, "neck")
    foot_x = 0.16 if name == "mara" else 0.215
    for side, sign in (("L", 1), ("R", -1)):
        constructed_shoe(side, sign * foot_x, rig, leather, rubber, button)
    for index, z in enumerate((1.12, 1.19, 1.26, 1.33)):
        sphere(f"Shirt button {index}", (0, -0.142, z), (0.009, 0.004, 0.009), button, rig, "spine" if z < 1.30 else "chest", 12)
    hair(rig, hair_mat, {"mara": "sweep", "dev": "short", "sol": "curl"}[name])
    join_hair()
    if name == "dev":
        for index in range(18):
            angle = math.pi * index / 17
            sphere(f"Beard {index}", (0.071 * math.cos(angle), -0.112, 1.565 - 0.019 * math.sin(angle)), (0.010, 0.010, 0.022), hair_mat, rig, "head", 8)
        join_beard()
    make_actions(rig)
    bpy.context.scene.frame_set(1)
    OUT_SOURCE.mkdir(parents=True, exist_ok=True)
    OUT_EXPORT.mkdir(parents=True, exist_ok=True)
    source = OUT_SOURCE / f"{name}.blend"
    export = OUT_EXPORT / f"{name}.glb"
    bpy.ops.wm.save_as_mainfile(filepath=str(source), compress=True)
    bpy.ops.object.select_all(action="DESELECT")
    for obj in bpy.context.scene.objects:
        if obj.type in {"MESH", "ARMATURE"}:
            obj.select_set(True)
    bpy.context.view_layer.objects.active = rig
    bpy.ops.export_scene.gltf(filepath=str(export), export_format="GLB", use_selection=True, export_animations=True, export_animation_mode="ACTIONS", export_force_sampling=False)
    print({"identity": name, "source_bytes": source.stat().st_size, "export_bytes": export.stat().st_size})


if __name__ == "__main__":
    requested = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else list(IDENTITIES)
    for identity in requested:
        build_identity(identity, IDENTITIES[identity])
