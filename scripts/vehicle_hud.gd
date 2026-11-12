class_name VehicleHud
extends CanvasLayer

@onready var panel: Control = $Instrument
@onready var gauge: Control = $Instrument/Gauge
@onready var speed: Label = $Instrument/Speed
@onready var gear: Label = $Instrument/Gear
@onready var exit_hint: Label = $Instrument/ExitHint

var _car: TideHatchback


func _ready() -> void:
	visible = false
	get_viewport().size_changed.connect(_resize)
	_resize()


func bind(car: TideHatchback) -> void:
	_car = car


func set_driving(value: bool) -> void:
	visible = value


func _process(_delta: float) -> void:
	if not visible or not _car:
		return
	var current_speed: float = _car.speed_kmh()
	gauge.set("speed_kmh", current_speed)
	gauge.queue_redraw()
	speed.text = str(roundi(current_speed))
	gear.text = "R" if Input.is_action_pressed("move_back") else "D"
	exit_hint.text = "X  EXIT" if not Input.get_connected_joypads().is_empty() else "E  EXIT"


func _resize() -> void:
	var compact: bool = get_viewport().get_visible_rect().size.y < 520.0
	var dimension: float = 155.0 if compact else 204.0
	panel.offset_left = -dimension - 18.0
	panel.offset_top = -dimension - 16.0
	panel.offset_right = -18.0
	panel.offset_bottom = -16.0
	speed.add_theme_font_size_override("font_size", 30 if compact else 38)
