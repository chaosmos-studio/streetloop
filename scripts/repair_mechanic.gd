class_name RepairMechanic
extends CharacterBody3D

@export var walk_speed: float = 1.1
@export var wait_seconds: float = 2.4
@export var route_path: NodePath = ^"../MechanicRoute"

@onready var visual: HarborRunnerVisual = $Visual
@onready var route: Node3D = get_node(route_path)

var _waypoints: Array[Marker3D] = []
var _next_waypoint: int = 1
var _wait: float = 1.0
var _gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")


func _ready() -> void:
	for marker: Node in route.get_children():
		_waypoints.append(marker as Marker3D)


func _physics_process(delta: float) -> void:
	if not is_on_floor():
		velocity.y -= _gravity * delta
	else:
		velocity.y = -0.05
	var desired: Vector3 = Vector3.ZERO
	if _wait > 0.0:
		_wait = maxf(0.0, _wait - delta)
	elif not _waypoints.is_empty():
		var offset: Vector3 = _waypoints[_next_waypoint].global_position - global_position
		offset.y = 0.0
		if offset.length() < 0.28:
			_next_waypoint = (_next_waypoint + 1) % _waypoints.size()
			_wait = wait_seconds
		else:
			desired = offset.normalized() * walk_speed
	var horizontal: Vector2 = Vector2(velocity.x, velocity.z).move_toward(Vector2(desired.x, desired.z), delta * 4.0)
	velocity.x = horizontal.x
	velocity.z = horizontal.y
	move_and_slide()
	if horizontal.length() > 0.08:
		var local_direction: Vector3 = get_parent().global_transform.basis.inverse() * Vector3(horizontal.x, 0.0, horizontal.y).normalized()
		visual.rotation.y = lerp_angle(visual.rotation.y, atan2(local_direction.x, local_direction.z), minf(1.0, delta * 7.0))
	visual.set_motion(horizontal.length(), is_on_floor(), velocity.y)
