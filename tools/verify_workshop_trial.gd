extends SceneTree


func _initialize() -> void:
	call_deferred("_verify")


func _verify() -> void:
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	var trial: WorkshopTrial = scene.get_node("WorkshopTrial")
	var hud: WorkshopTrialHud = scene.get_node("WorkshopTrialHud")
	var mechanic: RepairMechanic = scene.get_node("HarborBlock/Buildings/CornerRepairShop/Mechanic")
	var car: TideHatchback = scene.get_node("TideHatchback")
	await physics_frame
	if trial.stage != WorkshopTrial.Stage.IDLE or hud.visible:
		_fail("Road trial was active before talking to the mechanic")
		return
	mechanic.interaction.activate()
	if trial.stage != WorkshopTrial.Stage.SOUTH or not hud.visible:
		_fail("Talking to the mechanic did not start the road trial")
		return
	car.freeze = true
	car.controls_enabled = true
	car.global_position = Vector3(0.0, 0.85, 26.0)
	await physics_frame
	if trial.stage != WorkshopTrial.Stage.NORTH:
		_fail("South road end did not advance the trial")
		return
	car.global_position = Vector3(0.0, 0.85, -26.0)
	await physics_frame
	if trial.stage != WorkshopTrial.Stage.RETURN:
		_fail("North road end did not advance the trial")
		return
	car.controls_enabled = false
	car.global_position = Vector3(2.25, 0.85, 8.0)
	mechanic.interaction.activate()
	if trial.stage != WorkshopTrial.Stage.COMPLETE or mechanic.interaction.prompt_text != "Run the road trial again":
		_fail("Parked return did not complete the trial")
		return
	print("Workshop road trial: start, south, north, parked return, completion")
	quit()


func _fail(message: String) -> void:
	push_error(message)
	quit(1)
