extends SceneTree


func _initialize() -> void:
	call_deferred("_verify")


func _verify() -> void:
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	var player: HarborPlayer = scene.get_node("Player")
	var shop: Node3D = scene.get_node("HarborBlock/Buildings/CornerRepairShop")
	var manual: ServiceManual = shop.get_node("ServiceManual")
	var view: ServiceManualView = scene.get_node("ServiceManualView")
	player.global_position = manual.global_position + Vector3(-1.13, -0.916, 0)
	player.get_node("CameraYaw").rotation.y = -PI * 0.5
	player.get_node("CameraYaw/SpringArm3D").rotation.x = -0.18
	for frame: int in range(8):
		await physics_frame
	player.request_interaction()
	await physics_frame
	if not view.visible or player.controls_enabled:
		push_error("The player could not read the service manual")
		quit(1)
		return
	view.next_page()
	view.next_page()
	view.next_page()
	if view.current_page() != 3:
		push_error("Manual page navigation did not reach the last page")
		quit(1)
		return
	view.previous_page()
	if view.current_page() != 2:
		push_error("Manual did not turn back")
		quit(1)
		return
	view.close_view()
	if view.visible or not player.controls_enabled:
		push_error("Closing the manual did not return movement controls")
		quit(1)
		return
	print("Manual opened through player interaction, turned pages, and restored controls")
	quit()
