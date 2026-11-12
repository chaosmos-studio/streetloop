extends SceneTree


func _initialize() -> void:
	call_deferred("_capture")


func _capture() -> void:
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	var shop: Node3D = scene.get_node("HarborBlock/Buildings/CornerRepairShop")
	var mechanic: RepairMechanic = shop.get_node("Mechanic")
	var player: HarborPlayer = scene.get_node("Player")
	player.global_position = shop.to_global(Vector3(-1.55, 0.16, -1.55))
	player.camera_yaw.look_at(mechanic.global_position + Vector3.UP * 1.0, Vector3.UP)
	for frame: int in range(45):
		await physics_frame
	await RenderingServer.frame_post_draw
	var first: Error = root.get_texture().get_image().save_png("res://art/review/A085_repair_mechanic/in_game_first.png")
	for frame: int in range(140):
		await physics_frame
	await RenderingServer.frame_post_draw
	var second: Error = root.get_texture().get_image().save_png("res://art/review/A085_repair_mechanic/in_game_walking.png")
	print("Mechanic captures: ", first, " ", second)
	quit(first if first != OK else second)
