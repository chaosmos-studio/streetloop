class_name WorkshopFan
extends Node3D

@export var maximum_speed: float = 12.57
@export var acceleration: float = 3.2
@export var coast_down: float = 1.5

@onready var rotor: Node3D = $Art/FanRotorPivot

var _enabled: bool = false
var _speed: float = 0.0


func _process(delta: float) -> void:
	var target_speed: float = maximum_speed if _enabled else 0.0
	var change_rate: float = acceleration if _enabled else coast_down
	_speed = move_toward(_speed, target_speed, change_rate * delta)
	rotor.rotate_y(_speed * delta)


func set_enabled(value: bool) -> void:
	_enabled = value


func is_enabled() -> bool:
	return _enabled


func get_speed() -> float:
	return _speed
