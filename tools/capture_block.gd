extends SceneTree


func _initialize() -> void:
	call_deferred("_capture")


func _capture() -> void:
	var block: PackedScene = load("res://scenes/main.tscn")
	var scene: Node3D = block.instantiate()
	root.add_child(scene)
	await process_frame
	await process_frame
	await RenderingServer.frame_post_draw
	var image: Image = root.get_texture().get_image()
	var output: String = "res://art/review/harbor_block.png"
	var result: Error = image.save_png(output)
	print("Capture: ", output, " ", image.get_width(), "x", image.get_height(), " result=", result)
	print("Exterior draw calls: ", Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME))
	print("Exterior rendered primitives: ", Performance.get_monitor(Performance.RENDER_TOTAL_PRIMITIVES_IN_FRAME))
	var camera: Camera3D = scene.get_node("ReviewCamera")
	camera.position = Vector3(7.2, 1.7, 1.4)
	camera.look_at(Vector3(11.4, 1.1, -1.8))
	await process_frame
	await RenderingServer.frame_post_draw
	var interior: Image = root.get_texture().get_image()
	var interior_output: String = "res://art/review/repair_shop_interior.png"
	var interior_result: Error = interior.save_png(interior_output)
	print("Capture: ", interior_output, " ", interior.get_width(), "x", interior.get_height(), " result=", interior_result)
	print("Interior draw calls: ", Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME))
	if result == OK:
		result = interior_result
	quit(result)
