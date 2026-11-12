"""Export static collection meshes grouped by material without changing the source."""

import collections
from pathlib import Path

import bpy


def export_static_by_material(collection_name: str, output_path: str) -> dict[str, int]:
    source = bpy.data.collections[collection_name]
    source_objects = [obj for obj in source.objects if obj.type == "MESH"]
    if not source_objects:
        raise ValueError(f"No mesh objects in {collection_name}")

    previous_scene = bpy.context.window.scene
    previous_selection = [obj for obj in previous_scene.objects if obj.select_get()]
    previous_active = bpy.context.view_layer.objects.active
    for obj in previous_selection:
        obj.select_set(False)

    export_scene = bpy.data.scenes.new("Temporary material export")
    export_collection = bpy.data.collections.new("Export meshes")
    export_scene.collection.children.link(export_collection)

    try:
        bpy.context.window.scene = export_scene
        groups = collections.defaultdict(list)
        for original in source_objects:
            clone = original.copy()
            clone.data = original.data.copy()
            export_collection.objects.link(clone)
            clone.select_set(True)
            bpy.context.view_layer.objects.active = clone
            for modifier in list(clone.modifiers):
                bpy.ops.object.modifier_apply(modifier=modifier.name)
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            clone.select_set(False)
            material_name = clone.data.materials[0].name if clone.data.materials else "Unassigned"
            groups[material_name].append(clone)

        for material_name, members in groups.items():
            for obj in members:
                obj.select_set(True)
            bpy.context.view_layer.objects.active = members[0]
            if len(members) > 1:
                bpy.ops.object.join()
            members[0].name = f"Static {material_name}"
            members[0].select_set(False)

        for obj in export_collection.objects:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = next(iter(export_collection.objects))
        bpy.ops.export_scene.gltf(
            filepath=str(Path(output_path).resolve()),
            export_format="GLB",
            use_selection=True,
            export_apply=True,
            export_yup=True,
            export_materials="EXPORT",
        )
        return {"source_objects": len(source_objects), "export_meshes": len(export_collection.objects)}
    finally:
        bpy.context.window.scene = previous_scene
        for obj in previous_selection:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = previous_active
        for obj in list(export_collection.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(export_collection)
        bpy.data.scenes.remove(export_scene)
