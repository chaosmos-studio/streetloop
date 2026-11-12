extends SceneTree


func _initialize() -> void:
	call_deferred("_capture")


func _capture() -> void:
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	var car: TideHatchback = scene.get_node("TideHatchback")
	var player: HarborPlayer = scene.get_node("Player")
	player.visible = false
	var camera: Camera3D = scene.get_node("ReviewCamera")
	camera.current = true
	for frame: int in range(35):
		await physics_frame
	var poses: Dictionary = {
		"front": Vector3(-2.3, 2.25, -5.5),
		"rear": Vector3(2.7, 2.25, 5.5),
		"side": Vector3(-5.2, 2.0, -0.3),
		"cabin": Vector3(-2.25, 1.65, -0.1),
	}
	var viewport: String = "mobile" if root.size.x < 1000 else "desktop"
	for name: String in poses:
		var offset: Vector3 = poses[name]
		camera.global_position = car.global_transform * offset
		camera.look_at(car.global_transform * Vector3(0, 0.85, 0))
		await RenderingServer.frame_post_draw
		var path: String = "res://art/review/tide_revision_%s_%s.png" % [name, viewport]
		var error: Error = root.get_texture().get_image().save_png(path)
		if error != OK:
			push_error("Could not save %s: %s" % [path, error])
			quit(1)
			return
	print("Captured revised hatchback front, rear, side, and cabin views")
	quit()
