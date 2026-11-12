extends Node3D

@onready var ceiling_fan: WorkshopFan = $CeilingFan
@onready var fan_switch: FanSwitch = $FanSwitch


func _ready() -> void:
	fan_switch.toggled.connect(ceiling_fan.set_enabled)
	ceiling_fan.set_enabled(fan_switch.is_on())
