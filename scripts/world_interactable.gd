class_name WorldInteractable
extends Area3D

signal activated


func activate() -> void:
	activated.emit()
