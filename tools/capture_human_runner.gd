extends SceneTree


func _initialize() -> void:
	call_deferred("_capture")


func _capture() -> void:
	var stage: Node3D = Node3D.new()
	root.add_child(stage)
	var model: Node3D = load("res://assets/models/A001_human_runner.glb").instantiate()
	stage.add_child(model)
	var player: AnimationPlayer = model.find_child("AnimationPlayer*", true, false) as AnimationPlayer
	var camera: Camera3D = Camera3D.new()
	stage.add_child(camera)
	camera.current = true
	camera.fov = 42.0
	var sun: DirectionalLight3D = DirectionalLight3D.new()
	stage.add_child(sun)
	sun.rotation_degrees = Vector3(-35, -30, 0)
	sun.light_energy = 1.4
	var ambient: WorldEnvironment = WorldEnvironment.new()
	stage.add_child(ambient)
	ambient.environment = Environment.new()
	ambient.environment.background_mode = Environment.BG_COLOR
	ambient.environment.background_color = Color(0.84, 0.88, 0.88)
	ambient.environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	ambient.environment.ambient_light_color = Color(0.9, 0.9, 0.9)
	ambient.environment.ambient_light_energy = 0.8
	player.stop(true)
	camera.position = Vector3(3.2, 1.15, 0)
	camera.look_at(Vector3(0, 0.89, 0))
	await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://art/review/human_runner_rest.png")
	await _save(player, camera, "Idle", 0.0, Vector3(0, 1.15, -3.2), "front")
	await _save(player, camera, "Idle", 0.0, Vector3(3.2, 1.15, 0), "side")
	await _save(player, camera, "Idle", 0.0, Vector3(0, 1.15, 3.2), "rear")
	await _save(player, camera, "Walk", 0.14, Vector3(3.2, 1.15, 0), "walk_contact")
	await _save(player, camera, "Walk", 0.55, Vector3(3.2, 1.15, 0), "walk_swing")
	await _save(player, camera, "Run", 0.1, Vector3(3.2, 1.15, 0), "run_contact")
	await _save(player, camera, "Run", 0.35, Vector3(3.2, 1.15, 0), "run_air")
	quit()


func _save(player: AnimationPlayer, camera: Camera3D, clip: String, at: float, position: Vector3, name: String) -> void:
	player.play(clip)
	player.seek(at, true)
	camera.position = position
	camera.look_at(Vector3(0, 0.89, 0))
	await process_frame
	await RenderingServer.frame_post_draw
	var result: Error = root.get_texture().get_image().save_png("res://art/review/human_runner_%s.png" % name)
	if result != OK:
		push_error("Failed to save runner view: %s" % result)
		quit(1)
