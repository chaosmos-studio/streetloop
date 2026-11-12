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
	camera.position = Vector3(10.6, 1.55, -0.3)
	camera.look_at(Vector3(12.1, 0.9, -1.8))
	await process_frame
	await RenderingServer.frame_post_draw
	var bench_image: Image = root.get_texture().get_image()
	var bench_output: String = "res://art/review/workbench_material_close.png"
	var bench_result: Error = bench_image.save_png(bench_output)
	print("Capture: ", bench_output, " ", bench_image.get_width(), "x", bench_image.get_height(), " result=", bench_result)
	camera.position = Vector3(9.25, 1.75, 2.0)
	camera.look_at(Vector3(7.25, 0.16, 2.0))
	await process_frame
	await RenderingServer.frame_post_draw
	var tile_image: Image = root.get_texture().get_image()
	var tile_output: String = "res://art/review/ceramic_floor_close.png"
	var tile_result: Error = tile_image.save_png(tile_output)
	print("Capture: ", tile_output, " ", tile_image.get_width(), "x", tile_image.get_height(), " result=", tile_result)
	var shop: Node3D = scene.get_node("HarborBlock/Buildings/CornerRepairShop")
	var fan: WorkshopFan = shop.get_node("CeilingFan")
	var fan_switch: FanSwitch = shop.get_node("FanSwitch")
	print("Fan speed before switch: ", fan.get_speed())
	fan_switch.toggle()
	for frame in 120:
		await process_frame
	print("Fan speed after switch on: ", fan.get_speed())
	camera.position = Vector3(9.5, 1.75, 1.2)
	camera.look_at(Vector3(9.5, 3.16, 0))
	await process_frame
	await RenderingServer.frame_post_draw
	var fan_image: Image = root.get_texture().get_image()
	var fan_output: String = "res://art/review/workshop_fan_on.png"
	var fan_result: Error = fan_image.save_png(fan_output)
	print("Capture: ", fan_output, " ", fan_image.get_width(), "x", fan_image.get_height(), " result=", fan_result)
	camera.position = Vector3(7, 1.42, 1.8)
	camera.look_at(Vector3(5.78, 1.31, 1.8))
	await process_frame
	await RenderingServer.frame_post_draw
	var switch_image: Image = root.get_texture().get_image()
	var switch_output: String = "res://art/review/fan_switch_on.png"
	var switch_result: Error = switch_image.save_png(switch_output)
	print("Capture: ", switch_output, " ", switch_image.get_width(), "x", switch_image.get_height(), " result=", switch_result)
	fan_switch.toggle()
	for frame in 60:
		await process_frame
	print("Fan speed during coast-down: ", fan.get_speed())
	var door: Node3D = scene.get_node("HarborBlock/Buildings/CornerRepairShop/PublicDoor")
	print("Open doorway ray: ", _door_ray(scene.get_world_3d()))
	door.call("set_open", false)
	for frame in 50:
		await physics_frame
	var art_angle: float = door.get_node("Art/DoorLeafPivot").rotation.y
	var collider_angle: float = door.get_node("LeafBody").rotation.y
	print("Closed door art and collider angles: ", art_angle, " ", collider_angle)
	print("Closed doorway ray: ", _door_ray(scene.get_world_3d()))
	camera.position = Vector3(3.2, 1.9, 3.36)
	camera.look_at(Vector3(5.6, 1.45, 3.36))
	await process_frame
	await RenderingServer.frame_post_draw
	var door_image: Image = root.get_texture().get_image()
	var door_output: String = "res://art/review/repair_shop_door_closed.png"
	var door_result: Error = door_image.save_png(door_output)
	print("Capture: ", door_output, " ", door_image.get_width(), "x", door_image.get_height(), " result=", door_result)
	if result == OK:
		result = interior_result
	if result == OK:
		result = bench_result
	if result == OK:
		result = tile_result
	if result == OK:
		result = fan_result
	if result == OK:
		result = switch_result
	if result == OK:
		result = door_result
	quit(result)


func _door_ray(world: World3D) -> String:
	var query: PhysicsRayQueryParameters3D = PhysicsRayQueryParameters3D.create(
		Vector3(4.8, 1.4, 3.36), Vector3(6.6, 1.4, 3.36)
	)
	var hit: Dictionary = world.direct_space_state.intersect_ray(query)
	return "clear" if hit.is_empty() else str((hit["collider"] as Node).name)
