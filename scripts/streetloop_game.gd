extends Node3D

@onready var player: HarborPlayer = $Player
@onready var interaction_hint: InteractionHint = $InteractionHint
@onready var service_manual: ServiceManual = $HarborBlock/Buildings/CornerRepairShop/ServiceManual
@onready var service_manual_view: ServiceManualView = $ServiceManualView


func _ready() -> void:
	player.focused_interactable_changed.connect(interaction_hint.set_target_text)
	service_manual.opened.connect(_open_service_manual)
	service_manual_view.closed.connect(_close_service_manual)


func _open_service_manual() -> void:
	player.controls_enabled = false
	interaction_hint.visible = false
	service_manual_view.open()


func _close_service_manual() -> void:
	player.controls_enabled = true
	interaction_hint.visible = true
