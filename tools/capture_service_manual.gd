extends SceneTree


func _initialize() -> void:
	call_deferred("_capture")


func _capture() -> void:
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	var player: HarborPlayer = scene.get_node("Player")
	var manual: ServiceManual = scene.get_node("HarborBlock/Buildings/CornerRepairShop/ServiceManual")
	player.global_position = manual.global_position + Vector3(-1.13, -0.916, 0)
	player.get_node("CameraYaw").rotation.y = -PI * 0.5
	player.get_node("CameraYaw/SpringArm3D").rotation.x = -0.18
	for frame: int in range(8):
		await physics_frame
	player.request_interaction()
	await physics_frame
	for frame: int in range(3):
		await process_frame
	await RenderingServer.frame_post_draw
	var output: String = "res://art/review/service_manual_mobile.png" if root.size.x < 1000 else "res://art/review/service_manual_desktop.png"
	var image: Image = root.get_texture().get_image()
	var result: Error = image.save_png(output)
	print("Capture: ", output, " ", image.get_width(), "x", image.get_height(), " result=", result)
	quit(result)
