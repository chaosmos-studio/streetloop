extends Node3D

@onready var player: HarborPlayer = $Player
@onready var interaction_hint: InteractionHint = $InteractionHint


func _ready() -> void:
	player.focused_interactable_changed.connect(interaction_hint.set_target_text)
