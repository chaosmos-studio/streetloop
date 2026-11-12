extends SceneTree


func _initialize() -> void:
	call_deferred("_capture")


func _capture() -> void:
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	var touch: TouchControls = scene.get_node("TouchControls")
	touch.show_preview()
	scene.get_node("VehicleHud").set_touch_mode(true)
	scene.get_node("InteractionHint").visible = false
	for frame: int in range(25):
		await physics_frame
	await RenderingServer.frame_post_draw
	var walk_result: Error = root.get_texture().get_image().save_png("res://art/review/touch_controls_walk_mobile.png")
	scene._enter_car()
	for frame: int in range(12):
		await physics_frame
	await RenderingServer.frame_post_draw
	var drive_result: Error = root.get_texture().get_image().save_png("res://art/review/touch_controls_drive_mobile.png")
	print("Touch layout capture: ", walk_result, " ", drive_result)
	quit(walk_result if walk_result != OK else drive_result)
