extends SceneTree


func _initialize() -> void:
	call_deferred("_capture")


func _capture() -> void:
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	var creator: CharacterCreatorView = scene.get_node("CharacterCreatorView")
	for index: int in range(15):
		await process_frame
	creator.open(CharacterChoice.new(), false)
	for index: int in range(12):
		await process_frame
	await RenderingServer.frame_post_draw
	var label: String = "portrait" if root.size.x < 760 else "desktop"
	var result: Error = root.get_texture().get_image().save_png("res://art/review/character_identities/creator_%s.png" % label)
	print("Creator screenshot: ", result)
	print("Creator draw calls: ", Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME))
	print("Creator primitives: ", Performance.get_monitor(Performance.RENDER_TOTAL_PRIMITIVES_IN_FRAME))
	creator.view_toggle.emit_signal("pressed")
	for index: int in range(4):
		await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://art/review/character_identities/creator_face.png")
	quit(result)
