class_name InteractionHint
extends CanvasLayer

@onready var panel: PanelContainer = $Anchor/Panel
@onready var key_label: Label = $Anchor/Panel/Content/Key
@onready var prompt_label: Label = $Anchor/Panel/Content/Prompt


func _ready() -> void:
	panel.visible = false


func set_target_text(value: String) -> void:
	panel.visible = not value.is_empty()
	if value.is_empty():
		return
	key_label.text = "X" if not Input.get_connected_joypads().is_empty() else "E"
	prompt_label.text = value
