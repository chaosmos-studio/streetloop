class_name TideHatchback
extends RigidBody3D

signal enter_requested
signal exit_requested

const WHEEL_POSITIONS: Array[Vector3] = [
	Vector3(-0.85, -0.22, -1.2),
	Vector3(0.85, -0.22, -1.2),
	Vector3(-0.85, -0.22, 1.26),
	Vector3(0.85, -0.22, 1.26),
]

@export var wheel_radius: float = 0.373
@export var suspension_rest: float = 0.30
@export var spring_stiffness: float = 42000.0
@export var spring_damping: float = 4200.0
@export var drive_force: float = 5100.0
@export var brake_force: float = 9200.0
@export var grip: float = 1.05

@onready var body_art: Node3D = $BodyArt
@onready var interaction: WorldInteractable = $DriverDoorInteraction
@onready var camera_rig: Node3D = $CameraRig
@onready var driving_camera: Camera3D = $CameraRig/SpringArm3D/Camera3D

var controls_enabled: bool = false
var _throttle: float = 0.0
var _steering: float = 0.0
var _braking: bool = false
var _wheel_steers: Array[Node3D] = []
var _wheel_spins: Array[Node3D] = []
var _wheel_lengths: Array[float] = [0.3, 0.3, 0.3, 0.3]


func _ready() -> void:
	interaction.activated.connect(func() -> void: enter_requested.emit())
	for node: Node in body_art.find_children("*", "MeshInstance3D", true, false):
		var part: String = node.name.to_lower()
		if "tire" in part or "rim" in part or "hub" in part or "spoke" in part:
			(node as MeshInstance3D).visible = false
	for index: int in range(4):
		var steer: Node3D = get_node("Wheels/Wheel%d/Steer" % index)
		var mount: Node3D = steer.get_node("Mount")
		var spin: Node3D = mount.get_node("Spin")
		_wheel_steers.append(steer)
		_wheel_spins.append(spin)
		for name: String in ["Stationary brake caliper", "Caliper bridge"]:
			var brake_part: Node3D = spin.find_child(name, true, false) as Node3D
			if brake_part:
				brake_part.reparent(mount, true)
	camera_rig.top_level = true
	camera_rig.global_position = global_position + Vector3.UP * 1.1
	camera_rig.global_rotation = Vector3(0, global_rotation.y, 0)


func _physics_process(_delta: float) -> void:
	_throttle = Input.get_axis("move_back", "move_forward") if controls_enabled else 0.0
	_steering = Input.get_axis("move_left", "move_right") if controls_enabled else 0.0
	_braking = Input.is_action_pressed("brake") or not controls_enabled


func _unhandled_input(event: InputEvent) -> void:
	if controls_enabled and event.is_action_pressed("interact"):
		exit_requested.emit()
		get_viewport().set_input_as_handled()


func _process(delta: float) -> void:
	var forward_speed: float = -linear_velocity.dot(global_transform.basis.z)
	var steer_angle: float = _steering * lerpf(0.42, 0.16, clampf(absf(forward_speed) / 20.0, 0.0, 1.0))
	for index: int in range(4):
		_wheel_steers[index].rotation.y = steer_angle if index < 2 else 0.0
		_wheel_steers[index].position.y = -0.22 - _wheel_lengths[index]
		var wheel_side: float = -1.0 if index % 2 == 0 else 1.0
		_wheel_spins[index].rotation.x += forward_speed / wheel_radius * wheel_side * delta
	var desired_position: Vector3 = global_position + Vector3.UP * 1.1
	camera_rig.global_position = camera_rig.global_position.lerp(desired_position, minf(1.0, delta * 10.0))
	camera_rig.global_rotation.y = lerp_angle(camera_rig.global_rotation.y, global_rotation.y, minf(1.0, delta * 7.0))


func _integrate_forces(state: PhysicsDirectBodyState3D) -> void:
	var basis: Basis = state.transform.basis
	var up: Vector3 = basis.y.normalized()
	var forward: Vector3 = -basis.z.normalized()
	for index: int in range(4):
		var mount: Vector3 = state.transform * WHEEL_POSITIONS[index]
		var endpoint: Vector3 = mount - up * (suspension_rest + wheel_radius + 0.16)
		var query: PhysicsRayQueryParameters3D = PhysicsRayQueryParameters3D.create(mount, endpoint, 1, [get_rid()])
		var hit: Dictionary = state.get_space_state().intersect_ray(query)
		if hit.is_empty():
			_wheel_lengths[index] = suspension_rest
			continue
		var length: float = clampf(mount.distance_to(hit["position"]) - wheel_radius, 0.0, suspension_rest)
		_wheel_lengths[index] = length
		var offset: Vector3 = hit["position"] - state.transform.origin
		var contact_velocity: Vector3 = state.linear_velocity + state.angular_velocity.cross(offset)
		var compression: float = suspension_rest - length
		var normal_force: float = maxf(0.0, compression * spring_stiffness - contact_velocity.dot(up) * spring_damping)
		state.apply_force(up * normal_force, offset)
		var wheel_forward: Vector3 = forward.rotated(up, _steering * 0.42 if index < 2 else 0.0)
		wheel_forward = wheel_forward.slide(hit["normal"]).normalized()
		var sideways: Vector3 = hit["normal"].cross(wheel_forward).normalized()
		var lateral_force: float = clampf(-contact_velocity.dot(sideways) * mass * 2.0, -normal_force * grip, normal_force * grip)
		var forward_speed: float = contact_velocity.dot(wheel_forward)
		var engine: float = _throttle * drive_force * 0.5 if index < 2 else 0.0
		var braking: float = -signf(forward_speed) * brake_force * 0.25 if _braking and absf(forward_speed) > 0.08 else 0.0
		var rolling: float = -forward_speed * 90.0
		var longitudinal: float = clampf(engine + braking + rolling, -normal_force * grip, normal_force * grip)
		state.apply_force(wheel_forward * longitudinal + sideways * lateral_force, offset)


func driver_exit_position() -> Vector3:
	return global_transform * Vector3(-1.65, -0.65, -0.2)


func speed_kmh() -> float:
	return linear_velocity.length() * 3.6
