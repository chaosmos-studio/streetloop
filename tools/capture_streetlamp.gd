extends SceneTree


func _initialize() -> void:
	call_deferred("_capture")


func _capture() -> void:
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	scene.get_node("InteractionHint").visible = false
	var lamp: Node3D = scene.get_node("HarborBlock/Streetlamps/EastSouthLamp")
	var camera: Camera3D = scene.get_node("ReviewCamera")
	camera.current = true
	camera.fov = 58.0
	var positions: Array[Vector3] = [
		Vector3(-8.0, 4.2, -8.0),
		Vector3(8.0, 4.2, 8.0),
		Vector3(0, 4.2, -11.0),
	]
	var names: Array[String] = ["road", "rear", "side"]
	for index: int in range(positions.size()):
		camera.global_position = lamp.global_position + positions[index]
		camera.look_at(lamp.global_position + Vector3(0, 2.8, 0))
		for frame: int in range(2):
			await process_frame
		await RenderingServer.frame_post_draw
		var output: String = "res://art/review/harbor_streetlamp_%s.png" % names[index]
		var result: Error = root.get_texture().get_image().save_png(output)
		print("Capture: ", output, " result=", result)
		if result != OK:
			quit(result)
			return
	camera.fov = 43.0
	camera.global_position = lamp.global_position + Vector3(-0.8, 1.55, 1.8)
	camera.look_at(lamp.global_position + Vector3(0, 1.15, 0.14))
	await process_frame
	await RenderingServer.frame_post_draw
	var detail_output: String = "res://art/review/harbor_streetlamp_service_panel.png"
	var detail_result: Error = root.get_texture().get_image().save_png(detail_output)
	print("Capture: ", detail_output, " result=", detail_result)
	quit(detail_result)
