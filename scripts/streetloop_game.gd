extends Node3D

@onready var player: HarborPlayer = $Player
@onready var interaction_hint: InteractionHint = $InteractionHint
@onready var service_manual: ServiceManual = $HarborBlock/Buildings/CornerRepairShop/ServiceManual
@onready var service_manual_view: ServiceManualView = $ServiceManualView
@onready var service_terminal: ServiceTerminal = $HarborBlock/Buildings/CornerRepairShop/ServiceTerminal
@onready var service_terminal_view: ServiceTerminalView = $ServiceTerminalView
@onready var fan_switch: FanSwitch = $HarborBlock/Buildings/CornerRepairShop/FanSwitch
@onready var ceiling_fan: WorkshopFan = $HarborBlock/Buildings/CornerRepairShop/CeilingFan
@onready var tide_hatchback: TideHatchback = $TideHatchback
@onready var vehicle_hud: VehicleHud = $VehicleHud

var _driving: bool = false


func _ready() -> void:
	player.focused_interactable_changed.connect(interaction_hint.set_target_text)
	service_manual.opened.connect(_open_service_manual)
	service_manual_view.closed.connect(_close_service_manual)
	service_terminal.opened.connect(_open_service_terminal)
	service_terminal_view.closed.connect(_close_service_terminal)
	service_terminal_view.bind(fan_switch, ceiling_fan)
	tide_hatchback.enter_requested.connect(func() -> void: call_deferred("_enter_car"))
	tide_hatchback.exit_requested.connect(func() -> void: call_deferred("_exit_car"))
	vehicle_hud.bind(tide_hatchback)


func _open_service_manual() -> void:
	_set_inspection(true)
	service_manual_view.open()


func _close_service_manual() -> void:
	_set_inspection(false)


func _open_service_terminal() -> void:
	_set_inspection(true)
	service_terminal_view.open()


func _close_service_terminal() -> void:
	_set_inspection(false)


func _set_inspection(active: bool) -> void:
	player.controls_enabled = not active
	interaction_hint.visible = not active


func _enter_car() -> void:
	if _driving or service_manual_view.visible or service_terminal_view.visible:
		return
	_driving = true
	player.controls_enabled = false
	player.set_physics_process(false)
	player.get_node("Collision").disabled = true
	player.visible = false
	interaction_hint.visible = false
	tide_hatchback.controls_enabled = true
	tide_hatchback.driving_camera.make_current()
	vehicle_hud.set_driving(true)


func _exit_car() -> void:
	if not _driving or tide_hatchback.speed_kmh() > 7.0:
		return
	var exit_position: Vector3 = tide_hatchback.driver_exit_position()
	var query: PhysicsShapeQueryParameters3D = PhysicsShapeQueryParameters3D.new()
	query.shape = (player.get_node("Collision") as CollisionShape3D).shape
	query.transform = Transform3D(Basis.IDENTITY, exit_position + Vector3.UP * 0.875)
	query.collision_mask = 9
	query.exclude = [player.get_rid()]
	if not player.get_world_3d().direct_space_state.intersect_shape(query).is_empty():
		return
	_driving = false
	tide_hatchback.controls_enabled = false
	vehicle_hud.set_driving(false)
	player.global_position = exit_position
	player.velocity = Vector3.ZERO
	player.get_node("Collision").disabled = false
	player.set_physics_process(true)
	player.visible = true
	player.controls_enabled = true
	interaction_hint.visible = true
	player.camera.make_current()
