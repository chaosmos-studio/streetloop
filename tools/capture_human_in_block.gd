extends SceneTree


func _initialize() -> void:
	call_deferred("_capture")


func _capture() -> void:
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	var player: HarborPlayer = scene.get_node("Player")
	player.visual.hide()
	var rigged: Node3D = load("res://assets/models/A001_human_runner.glb").instantiate()
	player.add_child(rigged)
	rigged.rotation.y = PI * 0.5
	var animation: AnimationPlayer = rigged.find_child("AnimationPlayer*", true, false) as AnimationPlayer
	var camera: Camera3D = player.camera
	camera.current = true
	player.global_position = Vector3(-4.45, 0.17, 7.0)
	player.camera_yaw.rotation.y = 0.0
	for frame: int in range(25):
		await physics_frame
	animation.play("Idle")
	await _save("idle")
	Input.action_press("move_forward")
	animation.play("Walk")
	for frame: int in range(38):
		await physics_frame
	await _save("walk")
	Input.action_press("sprint")
	animation.play("Run")
	for frame: int in range(30):
		await physics_frame
	await _save("run")
	Input.action_release("move_forward")
	Input.action_release("sprint")
	quit()


func _save(name: String) -> void:
	await RenderingServer.frame_post_draw
	var result: Error = root.get_texture().get_image().save_png("res://art/review/human_runner_block_%s.png" % name)
	if result != OK:
		push_error("Could not save human runner gameplay view: %s" % result)
		quit(1)
