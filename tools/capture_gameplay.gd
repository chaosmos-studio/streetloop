extends SceneTree


func _initialize() -> void:
	call_deferred("_capture")


func _capture() -> void:
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	var player: HarborPlayer = scene.get_node("Player")
	for frame: int in range(15):
		await physics_frame
	await RenderingServer.frame_post_draw
	var start: Vector3 = player.global_position
	var start_image: Image = root.get_texture().get_image()
	var start_result: Error = start_image.save_png("res://art/review/first_player_spawn.png")
	print("Player start: ", start, " floor=", player.is_on_floor(), " capture=", start_result)
	Input.action_press("move_forward")
	for frame: int in range(72):
		await physics_frame
	Input.action_release("move_forward")
	for frame: int in range(10):
		await physics_frame
	await RenderingServer.frame_post_draw
	var end: Vector3 = player.global_position
	var end_image: Image = root.get_texture().get_image()
	var end_result: Error = end_image.save_png("res://art/review/first_player_shop.png")
	print("Player end: ", end, " floor=", player.is_on_floor(), " moved=", end.distance_to(start), " capture=", end_result)
	quit(start_result if start_result != OK else end_result)
