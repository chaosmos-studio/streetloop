class_name WorldInteractable
extends Area3D

signal activated

@export var prompt_text: String = "Use"


func activate() -> void:
	activated.emit()
