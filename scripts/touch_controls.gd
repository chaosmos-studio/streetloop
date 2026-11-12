class_name TouchControls
extends CanvasLayer

@onready var stick: VirtualJoystick = $Overlay/MoveStick
@onready var sprint_button: Button = $Overlay/Sprint
@onready var action_button: Button = $Overlay/Action
@onready var primary_button: Button = $Overlay/Primary

var player: HarborPlayer
var car: TideHatchback
var driving: bool = false
var _look_index: int = -1
var _button_touches: Dictionary[int, StringName] = {}


func _ready() -> void:
	visible = DisplayServer.is_touchscreen_available() or OS.has_feature("web_android") or OS.has_feature("web_ios")
	stick.action_left = &"move_left"
	stick.action_right = &"move_right"
	stick.action_up = &"move_forward"
	stick.action_down = &"move_back"
	stick.joystick_mode = VirtualJoystick.JOYSTICK_DYNAMIC
	stick.joystick_size = 156.0
	stick.tip_size = 66.0
	_style_stick()
	for button: Button in [sprint_button, action_button, primary_button]:
		_style_button(button)
		button.mouse_filter = Control.MOUSE_FILTER_IGNORE
		button.toggle_mode = true


func bind(actor: HarborPlayer, vehicle: TideHatchback) -> void:
	player = actor
	car = vehicle


func set_driving(active: bool) -> void:
	_release_buttons()
	driving = active
	primary_button.text = "BRAKE" if active else "JUMP"
	action_button.text = "EXIT" if active else "USE"
	sprint_button.visible = not active
	Input.action_release("sprint")
	Input.action_release("brake")
	_look_index = -1


func set_action_prompt(value: String) -> void:
	if driving:
		return
	var lower: String = value.to_lower()
	if "door" in lower:
		action_button.text = "DOOR"
	elif "drive" in lower:
		action_button.text = "DRIVE"
	elif "manual" in lower:
		action_button.text = "READ"
	elif "terminal" in lower:
		action_button.text = "OPEN"
	else:
		action_button.text = "USE"


func set_inspecting(active: bool) -> void:
	$Overlay.visible = not active
	if active:
		_release_buttons()
		_look_index = -1


func show_preview() -> void:
	visible = true


func _input(event: InputEvent) -> void:
	if not visible or not $Overlay.visible:
		return
	if event is InputEventScreenTouch:
		_handle_touch(event)
	if event is InputEventScreenDrag and event.index == _look_index:
		if driving:
			car.add_look_delta(event.relative)
		else:
			player.add_look_delta(event.relative)
		get_viewport().set_input_as_handled()


func _can_start_look(point: Vector2) -> bool:
	var viewport_size: Vector2 = get_viewport().get_visible_rect().size
	return point.x > viewport_size.x * 0.28 and point.y < viewport_size.y - 202.0


func _handle_touch(event: InputEventScreenTouch) -> void:
	if not event.pressed:
		if _button_touches.has(event.index):
			var action: StringName = _button_touches[event.index]
			_button_touches.erase(event.index)
			if action == &"sprint":
				Input.action_release("sprint")
				sprint_button.set_pressed_no_signal(false)
			elif action == &"primary":
				_primary_up()
				primary_button.set_pressed_no_signal(false)
			else:
				action_button.set_pressed_no_signal(false)
		if event.index == _look_index:
			_look_index = -1
		return
	if not driving and sprint_button.get_global_rect().has_point(event.position):
		_button_touches[event.index] = &"sprint"
		sprint_button.set_pressed_no_signal(true)
		Input.action_press("sprint")
	elif action_button.get_global_rect().has_point(event.position):
		_button_touches[event.index] = &"action"
		action_button.set_pressed_no_signal(true)
		_use_action()
	elif primary_button.get_global_rect().has_point(event.position):
		_button_touches[event.index] = &"primary"
		primary_button.set_pressed_no_signal(true)
		_primary_down()
	elif _look_index == -1 and _can_start_look(event.position):
		_look_index = event.index


func _release_buttons() -> void:
	_button_touches.clear()
	sprint_button.set_pressed_no_signal(false)
	action_button.set_pressed_no_signal(false)
	primary_button.set_pressed_no_signal(false)
	Input.action_release("sprint")
	Input.action_release("brake")


func _use_action() -> void:
	if driving:
		car.request_exit()
	else:
		player.request_interaction()


func _primary_down() -> void:
	if driving:
		Input.action_press("brake")
	else:
		player.request_jump()


func _primary_up() -> void:
	Input.action_release("brake")


func _style_stick() -> void:
	var ring: StyleBoxFlat = StyleBoxFlat.new()
	ring.bg_color = Color(0.035, 0.15, 0.17, 0.48)
	ring.border_color = Color(0.68, 0.83, 0.78, 0.76)
	ring.set_border_width_all(2)
	ring.set_corner_radius_all(90)
	stick.add_theme_stylebox_override("normal_joystick", ring)
	stick.add_theme_stylebox_override("pressed_joystick", ring)
	var thumb: StyleBoxFlat = StyleBoxFlat.new()
	thumb.bg_color = Color(0.12, 0.38, 0.41, 0.84)
	thumb.border_color = Color(0.91, 0.85, 0.69, 0.9)
	thumb.set_border_width_all(2)
	thumb.set_corner_radius_all(40)
	stick.add_theme_stylebox_override("normal_tip", thumb)
	stick.add_theme_stylebox_override("pressed_tip", thumb)


func _style_button(button: Button) -> void:
	var normal: StyleBoxFlat = StyleBoxFlat.new()
	normal.bg_color = Color(0.035, 0.15, 0.17, 0.72)
	normal.border_color = Color(0.78, 0.82, 0.73, 0.86)
	normal.set_border_width_all(2)
	normal.set_corner_radius_all(28)
	var pressed: StyleBoxFlat = normal.duplicate()
	pressed.bg_color = Color(0.2, 0.49, 0.48, 0.91)
	button.add_theme_stylebox_override("normal", normal)
	button.add_theme_stylebox_override("hover", normal)
	button.add_theme_stylebox_override("pressed", pressed)
	button.add_theme_color_override("font_color", Color(0.98, 0.94, 0.82))
	button.add_theme_font_size_override("font_size", 16)
