extends Node3D

@export var initially_open: bool = false
@export var open_angle: float = -1.55
@export var angular_speed: float = 2.4

@onready var art_pivot: Node3D = $Art/DoorLeafPivot
@onready var leaf_body: AnimatableBody3D = $LeafBody

var _target_angle: float = 0.0
var _angle: float = 0.0


func _ready() -> void:
	_target_angle = open_angle if initially_open else 0.0
	_angle = _target_angle
	_set_leaf_angle(_angle)
	$Interaction.activated.connect(_toggle)


func _physics_process(delta: float) -> void:
	_angle = move_toward(_angle, _target_angle, angular_speed * delta)
	_set_leaf_angle(_angle)


func set_open(value: bool) -> void:
	_target_angle = open_angle if value else 0.0


func is_open() -> bool:
	return is_equal_approx(_target_angle, open_angle)


func _toggle() -> void:
	set_open(not is_open())


func _set_leaf_angle(value: float) -> void:
	art_pivot.rotation.y = value
	leaf_body.rotation.y = value
