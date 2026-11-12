extends SceneTree


func _initialize() -> void:
	call_deferred("_verify")


func _verify() -> void:
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	var player: HarborPlayer = scene.get_node("Player")
	var car: TideHatchback = scene.get_node("TideHatchback")
	var wheel_mount: Node3D = car.get_node("Wheels/Wheel0/Steer/Mount")
	var brake_caliper: Node3D = wheel_mount.find_child("Stationary brake caliper", true, false) as Node3D
	if not brake_caliper or brake_caliper.get_parent() != wheel_mount:
		push_error("Brake caliper is not fixed outside the spinning wheel group")
		quit(1)
		return
	for frame: int in range(120):
		await physics_frame
	var rest_position: Vector3 = car.global_position
	print("Rest position: ", rest_position, " wheel lengths: ", car.get("_wheel_lengths"))
	player.global_position = car.global_transform * Vector3(-1.95, -0.65, -0.35)
	player.get_node("CameraYaw").rotation.y = PI * 0.5
	player.get_node("CameraYaw/SpringArm3D").rotation.x = -0.13
	for frame: int in range(6):
		await physics_frame
	player.request_interaction()
	await physics_frame
	await process_frame
	if player.visible or not car.controls_enabled:
		push_error("The player could not enter the car from its door")
		quit(1)
		return
	car.exit_requested.emit()
	await physics_frame
	await process_frame
	if not player.visible or car.controls_enabled:
		push_error("The player could not leave the parked car")
		quit(1)
		return
	player.request_interaction()
	await physics_frame
	await process_frame
	if player.visible or not car.controls_enabled:
		push_error("The player could not re-enter the car after exiting")
		quit(1)
		return
	Input.action_press("move_forward")
	for frame: int in range(180):
		await physics_frame
	Input.action_release("move_forward")
	var driven_position: Vector3 = car.global_position
	var driven_speed: float = car.speed_kmh()
	print("Driven position: ", driven_position, " speed km/h: ", driven_speed)
	var wheel_spin: float = car.get_node("Wheels/Wheel1/Steer/Mount/Spin").rotation.x
	if absf(wheel_spin) < 1.0:
		push_error("Wheel art did not rotate with the car")
		quit(1)
		return
	if driven_position.distance_to(rest_position) < 2.0 or driven_speed < 5.0:
		push_error("Car did not accelerate along the road")
		quit(1)
		return
	Input.action_press("move_forward")
	Input.action_press("move_left")
	for frame: int in range(65):
		await physics_frame
	Input.action_release("move_left")
	Input.action_release("move_forward")
	var steered_position: Vector3 = car.global_position
	print("Steered position: ", steered_position, " heading: ", car.rotation.y)
	if absf(steered_position.x - driven_position.x) < 0.4:
		push_error("Steering did not change the car's route")
		quit(1)
		return
	Input.action_press("brake")
	for frame: int in range(180):
		await physics_frame
	Input.action_release("brake")
	print("Braked speed km/h: ", car.speed_kmh(), " position: ", car.global_position)
	if car.speed_kmh() > 7.0:
		push_error("Car did not come to exit speed under braking")
		quit(1)
		return
	car.exit_requested.emit()
	await physics_frame
	await process_frame
	if not player.visible or car.controls_enabled:
		push_error("Exiting the car did not return on-foot control")
		quit(1)
		return
	print("Drive, brake, exit route passed")
	quit()
