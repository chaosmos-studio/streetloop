extends SceneTree


func _initialize() -> void:
	call_deferred("_verify")


func _verify() -> void:
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	var mechanic: RepairMechanic = scene.get_node("HarborBlock/Buildings/CornerRepairShop/Mechanic")
	var trial: WorkshopTrial = scene.get_node("WorkshopTrial")
	var car: TideHatchback = scene.get_node("TideHatchback")
	await physics_frame
	mechanic.interaction.activate()
	scene._enter_car()
	Input.action_press("move_forward")
	if not await _reach_stage(trial, WorkshopTrial.Stage.NORTH, 500):
		_fail("Driving south did not reach the road end")
		return
	Input.action_release("move_forward")
	Input.action_press("move_back")
	if not await _reach_stage(trial, WorkshopTrial.Stage.RETURN, 1100):
		_fail("Driving north did not reach the road end")
		return
	Input.action_release("move_back")
	Input.action_press("move_forward")
	var returned: bool = false
	for frame: int in range(700):
		await physics_frame
		if car.global_position.z > 3.0:
			returned = true
			break
	Input.action_release("move_forward")
	Input.action_press("brake")
	for frame: int in range(180):
		await physics_frame
		if car.speed_kmh() < 2.0:
			break
	Input.action_release("brake")
	if not returned or car.global_position.distance_to(WorkshopTrial.PARKING_POSITION) > 6.0:
		_fail("The car could not return to the shop parking area: %s" % car.global_position)
		return
	scene._exit_car()
	mechanic.interaction.activate()
	if trial.stage != WorkshopTrial.Stage.COMPLETE:
		_fail("The mechanic did not accept the driven return")
		return
	print("Workshop drive: completed south, north, and parked return; car ", car.global_position)
	quit()


func _reach_stage(trial: WorkshopTrial, target: WorkshopTrial.Stage, limit: int) -> bool:
	for frame: int in range(limit):
		await physics_frame
		if trial.stage == target:
			return true
	return false


func _fail(message: String) -> void:
	Input.action_release("move_forward")
	Input.action_release("move_back")
	Input.action_release("brake")
	push_error(message)
	quit(1)
