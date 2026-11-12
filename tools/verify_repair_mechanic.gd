extends SceneTree


func _initialize() -> void:
	call_deferred("_verify")


func _verify() -> void:
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	var shop: Node3D = scene.get_node("HarborBlock/Buildings/CornerRepairShop")
	var mechanic: RepairMechanic = shop.get_node("Mechanic")
	var start: Vector3 = mechanic.global_position
	var furthest: float = 0.0
	var grounded_frames: int = 0
	for frame: int in range(540):
		await physics_frame
		furthest = maxf(furthest, mechanic.global_position.distance_to(start))
		if mechanic.is_on_floor():
			grounded_frames += 1
		var local: Vector3 = shop.to_local(mechanic.global_position)
		if absf(local.x) > 4.55 or absf(local.z) > 3.5 or local.y < -0.1:
			push_error("Mechanic left the walkable shop floor: %s" % local)
			quit(1)
			return
	if furthest < 1.0 or grounded_frames < 500:
		push_error("Mechanic did not complete a grounded work-area route")
		quit(1)
		return
	print("Mechanic route: ", furthest, " m from start; grounded ", grounded_frames, "/540 frames; final ", shop.to_local(mechanic.global_position))
	quit()
