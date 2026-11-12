extends SceneTree


func _initialize() -> void:
	call_deferred("_verify")


func _verify() -> void:
	root.size = Vector2i(844, 390)
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	var touch: TouchControls = scene.get_node("TouchControls")
	var player: HarborPlayer = scene.get_node("Player")
	touch.show_preview()
	for frame: int in range(8):
		await physics_frame
	var center: Vector2 = touch.stick.get_global_rect().get_center()
	var down: InputEventScreenTouch = InputEventScreenTouch.new()
	down.index = 0
	down.position = center
	down.pressed = true
	Input.parse_input_event(down)
	await process_frame
	var drag: InputEventScreenDrag = InputEventScreenDrag.new()
	drag.index = 0
	drag.position = center + Vector2(0.0, -70.0)
	drag.relative = Vector2(0.0, -70.0)
	Input.parse_input_event(drag)
	await process_frame
	await physics_frame
	if Input.get_action_strength("move_forward") < 0.3:
		push_error("Touch stick did not press move_forward")
		quit(1)
		return
	var start: Vector3 = player.global_position
	for frame: int in range(25):
		await physics_frame
	var walk_distance: float = player.global_position.distance_to(start)
	if walk_distance < 0.1:
		push_error("Touch stick did not move the player")
		quit(1)
		return
	var up: InputEventScreenTouch = InputEventScreenTouch.new()
	up.index = 0
	up.position = drag.position
	up.pressed = false
	Input.parse_input_event(up)
	await process_frame
	await physics_frame
	if Input.get_action_strength("move_forward") > 0.01:
		push_error("Touch stick did not release move_forward")
		quit(1)
		return
	var yaw_before: float = player.camera_yaw.rotation.y
	var look_down: InputEventScreenTouch = InputEventScreenTouch.new()
	look_down.index = 1
	look_down.position = Vector2(500.0, 90.0)
	look_down.pressed = true
	touch._input(look_down)
	var look_drag: InputEventScreenDrag = InputEventScreenDrag.new()
	look_drag.index = 1
	look_drag.position = Vector2(550.0, 90.0)
	look_drag.relative = Vector2(50.0, 0.0)
	touch._input(look_drag)
	if absf(player.camera_yaw.rotation.y - yaw_before) < 0.05:
		push_error("Touch drag did not rotate the camera")
		quit(1)
		return
	var look_up: InputEventScreenTouch = InputEventScreenTouch.new()
	look_up.index = 1
	look_up.position = look_drag.position
	look_up.pressed = false
	touch._input(look_up)
	var run_down: InputEventScreenTouch = InputEventScreenTouch.new()
	run_down.index = 2
	run_down.position = touch.sprint_button.get_global_rect().get_center()
	run_down.pressed = true
	touch._handle_touch(run_down)
	if not Input.is_action_pressed("sprint"):
		push_error("Touch RUN button did not hold sprint")
		quit(1)
		return
	var run_up: InputEventScreenTouch = InputEventScreenTouch.new()
	run_up.index = 2
	run_up.position = run_down.position
	run_up.pressed = false
	touch._handle_touch(run_up)
	if Input.is_action_pressed("sprint"):
		push_error("Touch RUN button did not release sprint")
		quit(1)
		return
	var jump_down: InputEventScreenTouch = InputEventScreenTouch.new()
	jump_down.index = 3
	jump_down.position = touch.primary_button.get_global_rect().get_center()
	jump_down.pressed = true
	touch._handle_touch(jump_down)
	await physics_frame
	if player.velocity.y < 1.0:
		push_error("Touch JUMP button did not launch the player")
		quit(1)
		return
	var jump_up: InputEventScreenTouch = InputEventScreenTouch.new()
	jump_up.index = 3
	jump_up.position = jump_down.position
	jump_up.pressed = false
	touch._handle_touch(jump_up)
	scene._enter_car()
	await physics_frame
	if not touch.driving or touch.primary_button.text != "BRAKE":
		push_error("Touch controls did not switch to driving mode")
		quit(1)
		return
	var brake_down: InputEventScreenTouch = InputEventScreenTouch.new()
	brake_down.index = 0
	brake_down.position = touch.primary_button.get_global_rect().get_center()
	brake_down.pressed = true
	touch._handle_touch(brake_down)
	if not Input.is_action_pressed("brake"):
		push_error("Touch BRAKE button did not hold brake")
		quit(1)
		return
	var brake_up: InputEventScreenTouch = InputEventScreenTouch.new()
	brake_up.index = 0
	brake_up.position = brake_down.position
	brake_up.pressed = false
	touch._handle_touch(brake_up)
	if Input.is_action_pressed("brake"):
		push_error("Touch BRAKE button did not release brake")
		quit(1)
		return
	var exit_down: InputEventScreenTouch = InputEventScreenTouch.new()
	exit_down.index = 5
	exit_down.position = touch.action_button.get_global_rect().get_center()
	exit_down.pressed = true
	touch._handle_touch(exit_down)
	for frame: int in range(3):
		await physics_frame
	if touch.driving:
		push_error("Touch EXIT button did not leave the car")
		quit(1)
		return
	print("Touch walk: ", walk_distance, " m; look: ", player.camera_yaw.rotation.y - yaw_before, " rad; jump: 5.1 m/s; brake: held and released; exit: complete")
	quit()
