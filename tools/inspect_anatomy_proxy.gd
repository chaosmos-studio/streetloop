extends SceneTree


func _initialize() -> void:
	call_deferred("_inspect")


func _inspect() -> void:
	var model: Node3D = load("res://assets/models/A001_anatomy_proxy.glb").instantiate()
	root.add_child(model)
	var mesh_count: int = 0
	var triangle_count: int = 0
	var material_count: int = 0
	var bounds: AABB = AABB()
	for node: Node in model.find_children("*", "MeshInstance3D", true, false):
		var instance: MeshInstance3D = node as MeshInstance3D
		mesh_count += 1
		var instance_bounds: AABB = instance.global_transform * instance.get_aabb()
		print("%s origin %s bounds %s" % [instance.name, instance.global_position, instance_bounds])
		bounds = instance_bounds if mesh_count == 1 else bounds.merge(instance_bounds)
		for surface: int in range(instance.mesh.get_surface_count()):
			triangle_count += instance.mesh.surface_get_array_index_len(surface) / 3
			if instance.mesh.surface_get_material(surface) != null:
				material_count += 1
	print("Anatomy proxy: %d meshes, %d triangles, %d material surfaces" % [mesh_count, triangle_count, material_count])
	print("World bounds: %s" % bounds)
	quit()
