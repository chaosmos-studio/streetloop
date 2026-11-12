extends SceneTree


func _initialize() -> void:
	call_deferred("_inspect")


func _inspect() -> void:
	var model: Node3D = load("res://assets/models/A001_human_runner.glb").instantiate()
	root.add_child(model)
	var skeleton: Skeleton3D = model.find_child("Skeleton3D*", true, false) as Skeleton3D
	var player: AnimationPlayer = model.find_child("AnimationPlayer*", true, false) as AnimationPlayer
	if skeleton == null or player == null:
		push_error("Imported runner lacks a skeleton or animation player")
		quit(1)
		return
	print("Runner skeleton bones: %d" % skeleton.get_bone_count())
	print("Runner animations: %s" % [player.get_animation_list()])
	for clip: StringName in player.get_animation_list():
		var animation: Animation = player.get_animation(clip)
		print("%s: %.3f s, %d tracks" % [clip, animation.length, animation.get_track_count()])
	player.play("Walk")
	player.seek(0.14, true)
	for name: String in ["thigh.L", "shin.L", "foot.L", "upper_arm.L"]:
		var index: int = skeleton.find_bone(name)
		print("%s bone %d pose %s global %s" % [name, index, skeleton.get_bone_pose_rotation(index) if index >= 0 else Quaternion.IDENTITY, skeleton.get_bone_global_pose(index).origin if index >= 0 else Vector3.ZERO])
	var mesh_count: int = 0
	var triangles: int = 0
	for node: Node in model.find_children("*", "MeshInstance3D", true, false):
		var instance: MeshInstance3D = node as MeshInstance3D
		mesh_count += 1
		if mesh_count <= 4:
			print("Mesh %s: skeleton %s, skin %s" % [instance.name, instance.skeleton, instance.skin != null])
		for surface: int in range(instance.mesh.get_surface_count()):
			triangles += instance.mesh.surface_get_array_index_len(surface) / 3
	print("Runner meshes: %d, triangles: %d" % [mesh_count, triangles])
	quit()
