extends SceneTree


func _initialize() -> void:
	call_deferred("_verify")


func _verify() -> void:
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	var car: TideHatchback = scene.get_node("TideHatchback")
	var wall: StaticBody3D = StaticBody3D.new()
	wall.collision_layer = 1
	wall.position = Vector3(2.25, 1.05, 22.0)
	var collision: CollisionShape3D = CollisionShape3D.new()
	var shape: BoxShape3D = BoxShape3D.new()
	shape.size = Vector3(5.0, 2.1, 0.38)
	collision.shape = shape
	wall.add_child(collision)
	scene.add_child(wall)
	for frame: int in range(35):
		await physics_frame
	car.controls_enabled = true
	Input.action_press("move_forward")
	for frame: int in range(270):
		await physics_frame
	Input.action_release("move_forward")
	var impact_position: Vector3 = car.global_position
	var impact_speed: float = car.speed_kmh()
	if impact_position.z > 20.4 or impact_speed > 3.0 or impact_position.y < 0.4:
		push_error("Car crossed or failed to settle against the wall: %s, %.2f km/h" % [impact_position, impact_speed])
		quit(1)
		return
	Input.action_press("move_back")
	for frame: int in range(150):
		await physics_frame
	Input.action_release("move_back")
	var reverse_position: Vector3 = car.global_position
	if reverse_position.z > impact_position.z - 2.0:
		push_error("Car could not reverse after impact: %s -> %s" % [impact_position, reverse_position])
		quit(1)
		return
	print("Impact stop: ", impact_position, " at ", impact_speed, " km/h")
	print("Reverse recovery: ", reverse_position, " distance ", impact_position.distance_to(reverse_position), " m")
	quit()
