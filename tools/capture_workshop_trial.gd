extends SceneTree


func _initialize() -> void:
	call_deferred("_capture")


func _capture() -> void:
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	var mechanic: RepairMechanic = scene.get_node("HarborBlock/Buildings/CornerRepairShop/Mechanic")
	mechanic.interaction.activate()
	if root.size.x < 1000:
		scene.get_node("TouchControls").show_preview()
		scene.get_node("VehicleHud").set_touch_mode(true)
	scene._enter_car()
	for frame: int in range(30):
		await physics_frame
	await RenderingServer.frame_post_draw
	var filename: String = "workshop_trial_mobile.png" if root.size.x < 1000 else "workshop_trial_desktop.png"
	var result: Error = root.get_texture().get_image().save_png("res://art/review/%s" % filename)
	print("Workshop trial capture: ", filename, " ", result)
	quit(result)
