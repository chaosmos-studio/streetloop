extends SceneTree


func _initialize() -> void:
	call_deferred("_capture")


func _capture() -> void:
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	var car: TideHatchback = scene.get_node("TideHatchback")
	var player: HarborPlayer = scene.get_node("Player")
	for frame: int in range(30):
		await physics_frame
	var review_camera: Camera3D = scene.get_node("ReviewCamera")
	review_camera.current = true
	review_camera.global_position = car.global_position + Vector3(-5.8, 3.1, -6.4)
	review_camera.look_at(car.global_position)
	await RenderingServer.frame_post_draw
	var suffix: String = "mobile" if root.size.x < 1000 else "desktop"
	var parked_result: Error = root.get_texture().get_image().save_png("res://art/review/tide_hatchback_parked_%s.png" % suffix)
	car.get_node("DriverDoorInteraction").activate()
	await physics_frame
	await process_frame
	player.visible = false
	Input.action_press("move_forward")
	for frame: int in range(110):
		await physics_frame
	Input.action_release("move_forward")
	for frame: int in range(3):
		await process_frame
	await RenderingServer.frame_post_draw
	var driving_result: Error = root.get_texture().get_image().save_png("res://art/review/tide_hatchback_driving_%s.png" % suffix)
	print("Parked capture: ", parked_result, " driving capture: ", driving_result)
	quit(parked_result if parked_result != OK else driving_result)
