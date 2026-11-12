extends SceneTree


func _initialize() -> void:
	call_deferred("_capture")


func _capture() -> void:
	var stage: Node3D = Node3D.new()
	root.add_child(stage)
	var model: Node3D = load("res://assets/models/A001_anatomy_proxy.glb").instantiate()
	stage.add_child(model)
	var camera: Camera3D = Camera3D.new()
	stage.add_child(camera)
	camera.current = true
	camera.position = Vector3(0, 1.3, 3.4)
	camera.look_at(Vector3(0, 0.9, 0))
	camera.fov = 38.0
	var sun: DirectionalLight3D = DirectionalLight3D.new()
	stage.add_child(sun)
	sun.rotation_degrees = Vector3(-38, -25, 0)
	sun.light_energy = 1.5
	var ambient: WorldEnvironment = WorldEnvironment.new()
	stage.add_child(ambient)
	ambient.environment = Environment.new()
	ambient.environment.background_mode = Environment.BG_COLOR
	ambient.environment.background_color = Color(0.32, 0.34, 0.35)
	ambient.environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	ambient.environment.ambient_light_color = Color(0.7, 0.7, 0.7)
	ambient.environment.ambient_light_energy = 0.7
	for frame: int in range(5):
		await process_frame
	await RenderingServer.frame_post_draw
	var result: Error = root.get_texture().get_image().save_png("res://art/review/A001_anatomy_study/godot_import.png")
	if result != OK:
		push_error("Could not save anatomy proxy view: %s" % result)
		quit(1)
		return
	quit()
