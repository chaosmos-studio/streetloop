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
var _vertical_speed: float = 0.0
var _phase: float = 0.0
var _blend: float = 0.0
var _rest_height: float = 0.0


func _ready() -> void:
	_rest_height = hips.position.y


func _process(delta: float) -> void:
	_blend = move_toward(_blend, clampf(_speed / 0.7, 0.0, 1.0) if _grounded else 0.0, delta * 6.0)
	var sprint: float = clampf((_speed - 1.7) / 2.1, 0.0, 1.0)
	var stance: float = lerpf(0.58, 0.46, sprint)
	var stride: float = lerpf(0.65, 0.94, sprint)
	if _speed > 0.08 and _grounded:
		var frequency: float = _speed * stance / stride
		_phase = wrapf(_phase + delta * frequency, 0.0, 1.0)
	var left: Vector2 = _leg_pose(_phase, stance, stride, sprint)
	var right: Vector2 = _leg_pose(wrapf(_phase + 0.5, 0.0, 1.0), stance, stride, sprint)
	left_hip.rotation.x = left.x * _blend
	right_hip.rotation.x = right.x * _blend
	left_knee.rotation.x = left.y * _blend
	right_knee.rotation.x = right.y * _blend
	left_shoulder.rotation.x = -left.x * 0.82 * _blend
	right_shoulder.rotation.x = -right.x * 0.82 * _blend
	left_elbow.rotation.x = (-0.1 - maxf(0.0, -left.x) * 0.35) * _blend
	right_elbow.rotation.x = (-0.1 - maxf(0.0, -right.x) * 0.35) * _blend
	hips.position.y = _rest_height + absf(sin(TAU * _phase)) * 0.025 * _blend
	hips.rotation.x = 0.045 * sprint * _blend
	hips.rotation.y = sin(TAU * _phase) * 0.04 * _blend
	hips.rotation.z = cos(TAU * _phase) * 0.018 * _blend
	if not _grounded:
		_pose_airborne()


func _leg_pose(phase: float, stance: float, stride: float, sprint: float) -> Vector2:
	if phase < stance:
		var progress: float = phase / stance
		var reach: float = lerpf(stride * 0.5, -stride * 0.5, progress)
		return Vector2(asin(clampf(reach / 0.89, -0.92, 0.92)), 0.06)
	var swing: float = (phase - stance) / (1.0 - stance)
	var reach: float = lerpf(-stride * 0.5, stride * 0.5, smoothstep(0.0, 1.0, swing))
	var knee: float = 0.1 + sin(PI * swing) * lerpf(0.52, 0.7, sprint)
	return Vector2(asin(clampf(reach / 0.89, -0.92, 0.92)), knee)


func _pose_airborne() -> void:
	var rising: bool = _vertical_speed > 0.0
	left_hip.rotation.x = -0.24 if rising else 0.12
	right_hip.rotation.x = 0.16 if rising else -0.1
	left_knee.rotation.x = 0.44 if rising else 0.1
	right_knee.rotation.x = 0.37 if rising else 0.1
	left_shoulder.rotation.x = -1.05 if rising else -0.25
	right_shoulder.rotation.x = -0.88 if rising else -0.25
	left_elbow.rotation.x = -0.31
	right_elbow.rotation.x = -0.31
	hips.position.y = _rest_height
	hips.rotation.x = -0.05 if rising else 0.04
	hips.rotation.y = 0.0
	hips.rotation.z = 0.0


func set_motion(speed: float, grounded: bool, vertical_speed: float) -> void:
	_speed = speed
	_grounded = grounded
	_vertical_speed = vertical_speed
