extends SceneTree


func _initialize() -> void:
	call_deferred("_capture")


func _capture() -> void:
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	var player: HarborPlayer = scene.get_node("Player")
	var review_camera: Camera3D = scene.get_node("ReviewCamera")
	player.global_position = Vector3(-4.45, 0.17, 7.0)
	player.camera_yaw.rotation.y = 0.0
	review_camera.current = true
	for frame: int in range(20):
		await physics_frame
	await _save(player, review_camera, "idle")
	var walk_start: Vector3 = player.global_position
	Input.action_press("move_forward")
	for frame: int in range(38):
		await physics_frame
	await _save(player, review_camera, "walk_contact")
	for frame: int in range(12):
		await physics_frame
	await _save(player, review_camera, "walk_swing")
	var walk_distance: float = walk_start.distance_to(player.global_position)
	var sprint_start: Vector3 = player.global_position
	Input.action_press("sprint")
	for frame: int in range(38):
		await physics_frame
	await _save(player, review_camera, "sprint")
	var sprint_distance: float = sprint_start.distance_to(player.global_position)
	var jump_event: InputEventAction = InputEventAction.new()
	jump_event.action = "jump"
	jump_event.pressed = true
	Input.parse_input_event(jump_event)
	await physics_frame
	jump_event.pressed = false
	Input.parse_input_event(jump_event)
	for frame: int in range(12):
		await physics_frame
	await _save(player, review_camera, "jump")
	Input.action_release("move_forward")
	Input.action_release("sprint")
	print("Captured runner gait. Walk distance: %.3f m over 50 ticks. Sprint distance: %.3f m over 38 ticks. Jump height: %.3f m" % [walk_distance, sprint_distance, player.global_position.y - 0.17])
	quit()


func _save(player: HarborPlayer, camera: Camera3D, name: String) -> void:
	camera.global_position = player.global_position + Vector3(-4.2, 1.8, 1.9)
	camera.look_at(player.global_position + Vector3.UP * 0.9)
	await RenderingServer.frame_post_draw
	var error: Error = root.get_texture().get_image().save_png("res://art/review/runner_gait_%s.png" % name)
	if error != OK:
		push_error("Could not capture runner gait: %s" % error)
		quit(1)
