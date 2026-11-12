class_name ServiceManual
extends Node3D

signal opened

@onready var interaction: WorldInteractable = $Interaction


func _ready() -> void:
	interaction.activated.connect(func() -> void: opened.emit())
