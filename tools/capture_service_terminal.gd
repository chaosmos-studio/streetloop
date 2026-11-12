extends SceneTree


func _initialize() -> void:
	call_deferred("_capture")


func _capture() -> void:
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	var shop: Node3D = scene.get_node("HarborBlock/Buildings/CornerRepairShop")
	var terminal: ServiceTerminal = shop.get_node("ServiceTerminal")
	var view: ServiceTerminalView = scene.get_node("ServiceTerminalView")
	var fan_switch: FanSwitch = shop.get_node("FanSwitch")
	var player: HarborPlayer = scene.get_node("Player")
	var suffix: String = "mobile" if root.size.x < 1000 else "desktop"
	var camera: Camera3D = scene.get_node("ReviewCamera")
	camera.current = true
	camera.fov = 48.0
	camera.global_position = terminal.global_position + Vector3(-1.05, 0.79, 0.65)
	camera.look_at(terminal.global_position + Vector3(0, 0.28, -0.15))
	for frame: int in range(3):
		await process_frame
	await RenderingServer.frame_post_draw
	var model_result: Error = root.get_texture().get_image().save_png("res://art/review/service_terminal_model_%s.png" % suffix)
	player.global_position = terminal.global_position + Vector3(-1.1, -0.916, 0)
	player.get_node("CameraYaw").rotation.y = -PI * 0.5
	player.get_node("CameraYaw/SpringArm3D").rotation.x = -0.15
	player.camera.make_current()
	for frame: int in range(8):
		await physics_frame
	player.request_interaction()
	await physics_frame
	view.run_diagnostic()
	await RenderingServer.frame_post_draw
	var off_result: Error = root.get_texture().get_image().save_png("res://art/review/service_terminal_off_%s.png" % suffix)
	fan_switch.toggle()
	for frame: int in range(70):
		await physics_frame
	view.run_diagnostic()
	await RenderingServer.frame_post_draw
	var pass_result: Error = root.get_texture().get_image().save_png("res://art/review/service_terminal_pass_%s.png" % suffix)
	print("Terminal captures: ", suffix, " ", model_result, " ", off_result, " ", pass_result)
	quit(model_result if model_result != OK else off_result if off_result != OK else pass_result)
