extends SceneTree


func _initialize() -> void:
	call_deferred("_verify")


func _verify() -> void:
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	var player: HarborPlayer = scene.get_node("Player")
	var shop: Node3D = scene.get_node("HarborBlock/Buildings/CornerRepairShop")
	var terminal: ServiceTerminal = shop.get_node("ServiceTerminal")
	var view: ServiceTerminalView = scene.get_node("ServiceTerminalView")
	var fan_switch: FanSwitch = shop.get_node("FanSwitch")
	var fan: WorkshopFan = shop.get_node("CeilingFan")
	player.global_position = terminal.global_position + Vector3(-1.1, -0.916, 0)
	player.get_node("CameraYaw").rotation.y = -PI * 0.5
	player.get_node("CameraYaw/SpringArm3D").rotation.x = -0.15
	for frame: int in range(8):
		await physics_frame
	player.request_interaction()
	await physics_frame
	if not view.visible or player.controls_enabled:
		push_error("The player could not use the shop computer")
		quit(1)
		return
	view.run_diagnostic()
	if view.diagnostic_passed():
		push_error("The fan diagnostic passed with the wall switch off")
		quit(1)
		return
	view.close_view()
	if view.visible or not player.controls_enabled:
		push_error("Closing the terminal did not return player control")
		quit(1)
		return
	fan_switch.toggle()
	for frame: int in range(70):
		await physics_frame
	if fan.get_speed() < 2.0:
		push_error("Fan did not reach diagnostic speed")
		quit(1)
		return
	player.request_interaction()
	await physics_frame
	view.run_diagnostic()
	if not view.diagnostic_passed():
		push_error("The fan diagnostic did not pass after spin-up")
		quit(1)
		return
	view.close_view()
	print("Terminal opened, rejected an off fan, passed a spinning fan, and returned controls")
	print("Fan speed: ", fan.get_speed(), " rad/s")
	quit()
