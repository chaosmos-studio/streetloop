class_name HarborRunnerVisual
extends Node3D

@onready var model: Node3D = $Model
@onready var hips: Node3D = model.find_child("HipsPivot*", true, false) as Node3D
@onready var left_hip: Node3D = model.find_child("LeftHipPivot*", true, false) as Node3D
@onready var right_hip: Node3D = model.find_child("RightHipPivot*", true, false) as Node3D
@onready var left_knee: Node3D = model.find_child("LeftKneePivot*", true, false) as Node3D
@onready var right_knee: Node3D = model.find_child("RightKneePivot*", true, false) as Node3D
@onready var left_shoulder: Node3D = model.find_child("LeftShoulderPivot*", true, false) as Node3D
@onready var right_shoulder: Node3D = model.find_child("RightShoulderPivot*", true, false) as Node3D
@onready var left_elbow: Node3D = model.find_child("LeftElbowPivot*", true, false) as Node3D
@onready var right_elbow: Node3D = model.find_child("RightElbowPivot*", true, false) as Node3D

var _speed: float = 0.0
var _grounded: bool = true
var _phase: float = 0.0
var _rest_height: float = 0.0


func _ready() -> void:
	_rest_height = hips.position.y


func _process(delta: float) -> void:
	var blend: float = clampf(_speed / 4.2, 0.0, 1.0) if _grounded else 0.0
	_phase = fmod(_phase + delta * lerpf(3.0, 10.0, blend), TAU)
	var stride: float = sin(_phase) * 0.58 * blend
	left_hip.rotation.x = stride
	right_hip.rotation.x = -stride
	left_knee.rotation.x = maxf(0.0, -sin(_phase)) * 0.46 * blend
	right_knee.rotation.x = maxf(0.0, sin(_phase)) * 0.46 * blend
	left_shoulder.rotation.x = -stride * 0.68
	right_shoulder.rotation.x = stride * 0.68
	left_elbow.rotation.x = -0.12 - maxf(0.0, sin(_phase)) * 0.23 * blend
	right_elbow.rotation.x = -0.12 - maxf(0.0, -sin(_phase)) * 0.23 * blend
	hips.position.y = _rest_height + absf(sin(_phase)) * 0.018 * blend + sin(Time.get_ticks_msec() * 0.002) * 0.003
	if not _grounded:
		left_hip.rotation.x = -0.22
		right_hip.rotation.x = 0.12
		left_shoulder.rotation.x = -0.25
		right_shoulder.rotation.x = -0.25


func set_motion(speed: float, grounded: bool) -> void:
	_speed = speed
	_grounded = grounded
