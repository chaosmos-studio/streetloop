extends SceneTree


func _initialize() -> void:
	call_deferred("_inspect")


func _inspect() -> void:
	for identity: CharacterIdentity in CharacterCatalog.IDENTITIES:
		var model: Node3D = identity.model.instantiate() as Node3D
		root.add_child(model)
		var player: AnimationPlayer = model.find_child("AnimationPlayer*", true, false) as AnimationPlayer
		var skeleton: Skeleton3D = model.find_child("Skeleton3D*", true, false) as Skeleton3D
		var triangles: int = 0
		var meshes: int = 0
		for node: Node in model.find_children("*", "MeshInstance3D", true, false):
			var mesh: MeshInstance3D = node as MeshInstance3D
			meshes += 1
			for surface: int in range(mesh.mesh.get_surface_count()):
				triangles += mesh.mesh.surface_get_array_index_len(surface) / 3
		print(identity.identity_id, ": ", meshes, " meshes, ", triangles, " triangles, ", skeleton.get_bone_count() if skeleton else 0, " bones, clips ", player.get_animation_list() if player else PackedStringArray())
		model.queue_free()
	quit()
