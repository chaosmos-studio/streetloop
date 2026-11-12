"""Shared Blender construction helpers for the Tide hatchback."""

import math

import bpy


def material(name, color, roughness, metallic=0.0, alpha=1.0):
    result = bpy.data.materials.new(name)
    result.use_nodes = True
    result.diffuse_color = (*color, alpha)
    surface = result.node_tree.nodes.get("Principled BSDF")
    surface.inputs["Base Color"].default_value = (*color, alpha)
    surface.inputs["Roughness"].default_value = roughness
    surface.inputs["Metallic"].default_value = metallic
    surface.inputs["Alpha"].default_value = alpha
    if alpha < 1.0:
        result.surface_render_method = "BLENDED"
        result.use_transparency_overlap = False
    return result


def move(obj, collection):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


def box(name, position, dimensions, surface, collection, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=position)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(surface)
    if bevel:
        modifier = obj.modifiers.new("Formed edge", "BEVEL")
        modifier.width = bevel
        modifier.segments = 2
        obj.modifiers.new("Weighted normals", "WEIGHTED_NORMAL")
    return move(obj, collection)


def cylinder(name, position, radius, depth, surface, collection, vertices=20, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=position, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(surface)
    for polygon in obj.data.polygons:
        polygon.use_smooth = True
    return move(obj, collection)


def ellipsoid(name, position, dimensions, surface, collection, segments=20, rings=12):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, radius=1, location=position)
    obj = bpy.context.object
    obj.name = name
    obj.scale = tuple(d * 0.5 for d in dimensions)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(surface)
    for polygon in obj.data.polygons:
        polygon.use_smooth = True
    return move(obj, collection)


def tube(name, points, radius, surface, collection, cyclic=False):
    curve = bpy.data.curves.new(name, "CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = radius
    curve.bevel_resolution = 2
    spline = curve.splines.new("POLY")
    spline.points.add(len(points) - 1)
    for control, point in zip(spline.points, points):
        control.co = (*point, 1.0)
    spline.use_cyclic_u = cyclic
    obj = bpy.data.objects.new(name, curve)
    collection.objects.link(obj)
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.convert(target="MESH")
    obj.data.materials.append(surface)
    return obj


def panel(name, vertices, faces, surface, collection, smooth=True):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    obj.data.materials.append(surface)
    mesh.uv_layers.new(name="Car panel UV")
    for polygon in mesh.polygons:
        normal = polygon.normal
        for loop_index in polygon.loop_indices:
            vertex = mesh.vertices[mesh.loops[loop_index].vertex_index].co
            uv = mesh.uv_layers.active.data[loop_index].uv
            if abs(normal.x) > abs(normal.z):
                uv[:] = ((vertex.y + 2.1) / 4.2, vertex.z / 1.8)
            else:
                uv[:] = ((vertex.x + 1.0) / 2.0, (vertex.y + 2.1) / 4.2)
        polygon.use_smooth = smooth
    return obj


def export_collection(name, collection, project, images=()):
    from export_static_by_material import export_static_by_material

    bpy.context.view_layer.update()
    source = project / "art" / "source" / f"{name}.blend"
    bpy.data.libraries.write(str(source), {collection, *images}, compress=True)
    output = project / "assets" / "models" / f"{name}.glb"
    result = export_static_by_material(collection.name, str(output))
    collection.hide_viewport = True
    return {"source": str(source), "export": str(output), "objects": result["source_objects"], "meshes": result["export_meshes"]}


def arc(center_y, center_z, radius, start, end, count):
    return [(center_y + radius * math.cos(start + (end - start) * index / count), center_z + radius * math.sin(start + (end - start) * index / count)) for index in range(count + 1)]
