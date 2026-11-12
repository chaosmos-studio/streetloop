"""Group an articulated Blender collection by pivot and material for glTF."""

import collections
from pathlib import Path

import bpy


def export_articulated_by_material(collection_name: str, output_path: str) -> dict[str, int]:
    source = bpy.data.collections[collection_name]
    originals = list(source.objects)
    previous_scene = bpy.context.window.scene
    previous_active = bpy.context.view_layer.objects.active
    previous_selection = [obj for obj in previous_scene.objects if obj.select_get()]
    for obj in previous_selection:
        obj.select_set(False)

    scene = bpy.data.scenes.new("Temporary articulated export")
    collection = bpy.data.collections.new("Articulated export parts")
    scene.collection.children.link(collection)
    clones = {}
    try:
        bpy.context.window.scene = scene
        for original in originals:
            clone = original.copy()
            if original.data:
                clone.data = original.data.copy()
            collection.objects.link(clone)
            clones[original] = clone
        for original, clone in clones.items():
            clone.parent = clones.get(original.parent)
            clone.matrix_parent_inverse = original.matrix_parent_inverse.copy()
            clone.matrix_basis = original.matrix_basis.copy()

        groups = collections.defaultdict(list)
        for original, clone in clones.items():
            if clone.type != "MESH":
                continue
            clone.select_set(True)
            bpy.context.view_layer.objects.active = clone
            for modifier in list(clone.modifiers):
                bpy.ops.object.modifier_apply(modifier=modifier.name)
            clone.select_set(False)
            material_name = clone.data.materials[0].name if clone.data.materials else "Unassigned"
            groups[(clone.parent, material_name)].append(clone)

        for (parent, material_name), members in groups.items():
            for obj in members:
                obj.select_set(True)
            active = members[0]
            bpy.context.view_layer.objects.active = active
            if len(members) > 1:
                bpy.ops.object.join()
            active.name = f"{parent.name if parent else 'Root'} {material_name}"
            active.select_set(False)

        for obj in collection.objects:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = next(obj for obj in collection.objects if obj.type == "EMPTY")
        bpy.ops.export_scene.gltf(
            filepath=str(Path(output_path).resolve()),
            export_format="GLB",
            use_selection=True,
            export_yup=True,
            export_materials="EXPORT",
            export_animations=False,
        )
        return {"source_meshes": sum(obj.type == "MESH" for obj in originals), "export_meshes": sum(obj.type == "MESH" for obj in collection.objects)}
    finally:
        bpy.context.window.scene = previous_scene
        for obj in previous_selection:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = previous_active
        for obj in list(collection.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(collection)
        bpy.data.scenes.remove(scene)
