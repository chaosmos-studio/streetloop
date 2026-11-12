class_name WorkshopTrialHud
extends CanvasLayer

@onready var objective: Label = $Card/Content/Objective


func _ready() -> void:
	visible = false


func show_stage(message: String) -> void:
	visible = true
	objective.text = message


func set_objective(name: String, distance: float) -> void:
	objective.text = "%s   %d m" % [name, roundi(distance)]
