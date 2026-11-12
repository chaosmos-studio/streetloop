extends SceneTree


func _initialize() -> void:
	call_deferred("_capture")


func _capture() -> void:
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	var player: HarborPlayer = scene.get_node("Player")
	var creator: CharacterCreatorView = scene.get_node("CharacterCreatorView")
	creator.overlay.visible = false
	player.controls_enabled = true
	for frame: int in range(20):
		await physics_frame
	var start: Vector3 = player.global_position
	Input.action_press("move_forward")
	for frame: int in range(100):
		await physics_frame
	Input.action_release("move_forward")
	for frame: int in range(6):
		await process_frame
	await RenderingServer.frame_post_draw
	var end: Vector3 = player.global_position
	var result: Error = root.get_texture().get_image().save_png("res://art/review/character_identities/live_player.png")
	print("Character route: moved ", end.distance_to(start), " m, floor=", player.is_on_floor(), " screenshot=", result)
	print("Gameplay draw calls: ", Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME))
	print("Gameplay primitives: ", Performance.get_monitor(Performance.RENDER_TOTAL_PRIMITIVES_IN_FRAME))
	quit(result if end.distance_to(start) > 0.5 else 1)
