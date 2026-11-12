extends SceneTree


func _initialize() -> void:
	call_deferred("_verify")


func _verify() -> void:
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	var player: HarborPlayer = scene.get_node("Player")
	var shop: Node3D = scene.get_node("HarborBlock/Buildings/CornerRepairShop")
	var door: Node3D = shop.get_node("PublicDoor")
	var fan_switch: FanSwitch = shop.get_node("FanSwitch")
	var fan: WorkshopFan = shop.get_node("CeilingFan")
	for frame: int in range(4):
		await physics_frame
	player.request_interaction()
	await physics_frame
	if door.call("is_open"):
		push_error("Door interaction did not close the door")
		quit(1)
		return
	player.request_interaction()
	await physics_frame
	if not door.call("is_open"):
		push_error("Door interaction did not reopen the door")
		quit(1)
		return

	player.global_position = Vector3(fan_switch.global_position.x + 1.0, 0.16, fan_switch.global_position.z)
	player.get_node("CameraYaw").rotation.y = PI * 0.5
	player.get_node("CameraYaw/SpringArm3D").rotation.x = -0.15
	for frame: int in range(3):
		await physics_frame
	player.request_interaction()
	await physics_frame
	if not fan_switch.is_on() or not fan.is_enabled():
		push_error("Player interaction did not turn on the ceiling fan")
		quit(1)
		return
	for frame: int in range(60):
		await physics_frame
	print("Door reopens: ", door.call("is_open"))
	print("Fan switch on: ", fan_switch.is_on(), " speed: ", fan.get_speed())
	quit()
