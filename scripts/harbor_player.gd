class_name HarborPlayer
extends CharacterBody3D

signal focused_interactable_changed(text: String)

@export var walk_speed: float = 4.2
@export var sprint_speed: float = 6.2
@export var acceleration: float = 16.0
@export var braking: float = 21.0
@export var jump_velocity: float = 5.1
@export var turn_speed: float = 12.0
@export var mouse_sensitivity: float = 0.0024
@export var gamepad_look_speed: float = 2.5

@onready var visual: HarborRunnerVisual = $Visual
@onready var camera_yaw: Node3D = $CameraYaw
@onready var spring_arm: SpringArm3D = $CameraYaw/SpringArm3D
@onready var camera: Camera3D = $CameraYaw/SpringArm3D/Camera3D

var controls_enabled: bool = true
var _gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")
var _jump_buffer: float = 0.0
var _coyote_time: float = 0.0
var _interact_requested: bool = false
var _focused_interactable: WorldInteractable
var _focused_text: String = ""


func _ready() -> void:
	spring_arm.add_excluded_object(get_rid())
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED


func _input(event: InputEvent) -> void:
	if not controls_enabled:
		return
	if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		camera_yaw.rotation.y -= event.relative.x * mouse_sensitivity
		spring_arm.rotation.x = clampf(spring_arm.rotation.x - event.relative.y * mouse_sensitivity, -0.62, 0.3)
	if event is InputEventMouseButton and event.pressed and Input.mouse_mode == Input.MOUSE_MODE_VISIBLE:
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	if event is InputEventKey and event.pressed and event.keycode == KEY_ESCAPE:
		Input.mouse_mode = Input.MOUSE_MODE_VISIBLE


func _unhandled_input(event: InputEvent) -> void:
	if controls_enabled and event.is_action_pressed("jump"):
		_jump_buffer = 0.12
		get_viewport().set_input_as_handled()
	if controls_enabled and event.is_action_pressed("interact"):
		request_interaction()
		get_viewport().set_input_as_handled()


func _process(delta: float) -> void:
	if not controls_enabled:
		return
	var look: Vector2 = Input.get_vector("look_left", "look_right", "look_up", "look_down")
	camera_yaw.rotation.y -= look.x * gamepad_look_speed * delta
	spring_arm.rotation.x = clampf(spring_arm.rotation.x - look.y * gamepad_look_speed * delta, -0.62, 0.3)


func _physics_process(delta: float) -> void:
	_coyote_time = 0.1 if is_on_floor() else maxf(0.0, _coyote_time - delta)
	_jump_buffer = maxf(0.0, _jump_buffer - delta)
	var input_vector: Vector2 = Input.get_vector("move_left", "move_right", "move_forward", "move_back") if controls_enabled else Vector2.ZERO
	var direction: Vector3 = camera.global_transform.basis * Vector3(input_vector.x, 0.0, input_vector.y)
	direction.y = 0.0
	direction = direction.normalized()
	var speed: float = sprint_speed if controls_enabled and Input.is_action_pressed("sprint") else walk_speed
	var target: Vector2 = Vector2(direction.x, direction.z) * speed * input_vector.length()
	var horizontal: Vector2 = Vector2(velocity.x, velocity.z)
	horizontal = horizontal.move_toward(target, (acceleration if target.length_squared() > 0.0 else braking) * delta)
	velocity.x = horizontal.x
	velocity.z = horizontal.y
	if _jump_buffer > 0.0 and _coyote_time > 0.0:
		velocity.y = jump_velocity
		_jump_buffer = 0.0
		_coyote_time = 0.0
	elif not is_on_floor():
		velocity.y -= _gravity * delta
	else:
		velocity.y = -0.05
	move_and_slide()
	_update_look_target()
	if _interact_requested:
		_interact_requested = false
		if _focused_interactable:
			_focused_interactable.activate()
	if direction.length_squared() > 0.001:
		visual.rotation.y = lerp_angle(visual.rotation.y, atan2(direction.x, direction.z), minf(1.0, turn_speed * delta))
	visual.set_motion(horizontal.length(), is_on_floor())


func request_interaction() -> void:
	_interact_requested = true


func _update_look_target() -> void:
	var origin: Vector3 = global_position + Vector3.UP * 1.4
	var target: Vector3 = origin - camera.global_transform.basis.z * 2.3
	var query: PhysicsRayQueryParameters3D = PhysicsRayQueryParameters3D.create(origin, target, 4)
	query.collide_with_areas = true
	query.collide_with_bodies = false
	var hit: Dictionary = get_world_3d().direct_space_state.intersect_ray(query)
	var interactable: WorldInteractable = null
	if not hit.is_empty():
		interactable = hit["collider"] as WorldInteractable
	var prompt: String = interactable.prompt_text if interactable else ""
	if interactable == _focused_interactable and prompt == _focused_text:
		return
	_focused_interactable = interactable
	_focused_text = prompt
	focused_interactable_changed.emit(prompt)
