extends SceneTree


func _initialize() -> void:
	call_deferred("_capture")


func _capture() -> void:
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	var manual: ServiceManual = scene.get_node("HarborBlock/Buildings/CornerRepairShop/ServiceManual")
	var camera: Camera3D = scene.get_node("ReviewCamera")
	camera.current = true
	camera.fov = 35.0
	camera.global_position = manual.global_position + Vector3(-0.42, 0.48, 0.42)
	camera.look_at(manual.global_position + Vector3(0, 0.02, 0))
	for frame: int in range(3):
		await process_frame
	await RenderingServer.frame_post_draw
	var output: String = "res://art/review/service_manual_model.png"
	var image: Image = root.get_texture().get_image()
	var result: Error = image.save_png(output)
	print("Capture: ", output, " ", image.get_width(), "x", image.get_height(), " result=", result)
	quit(result)
