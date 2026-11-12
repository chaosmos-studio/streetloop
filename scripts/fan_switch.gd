class_name FanSwitch
extends Node3D

signal toggled(enabled: bool)

@export var initially_on: bool = false

@onready var rocker: Node3D = $Art/SwitchRockerPivot
@onready var indicator: MeshInstance3D = $Art/PowerIndicator
@onready var indicator_light: OmniLight3D = $IndicatorLight

var _on: bool = false


func _ready() -> void:
	_on = initially_on
	_update_appearance()


func toggle() -> void:
	_on = not _on
	_update_appearance()
	toggled.emit(_on)


func is_on() -> bool:
	return _on


func _update_appearance() -> void:
	rocker.rotation.x = -0.12 if _on else 0.12
	indicator.visible = _on
	indicator_light.visible = _on
