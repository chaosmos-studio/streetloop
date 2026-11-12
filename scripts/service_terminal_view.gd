class_name ServiceTerminalView
extends CanvasLayer

signal closed

@onready var panel: PanelContainer = $Shade/Margin/Center/Terminal
@onready var content_margin: MarginContainer = $Shade/Margin/Center/Terminal/Padding
@onready var heading: Label = $Shade/Margin/Center/Terminal/Padding/Content/Heading
@onready var switch_state: Label = $Shade/Margin/Center/Terminal/Padding/Content/Status/Switch
@onready var rotor_state: Label = $Shade/Margin/Center/Terminal/Padding/Content/Status/Rotor
@onready var instructions: Label = $Shade/Margin/Center/Terminal/Padding/Content/Instructions
@onready var result_label: Label = $Shade/Margin/Center/Terminal/Padding/Content/Result
@onready var run_button: Button = $Shade/Margin/Center/Terminal/Padding/Content/Actions/Run
@onready var close_button: Button = $Shade/Margin/Center/Terminal/Padding/Content/Actions/Close

var _switch: FanSwitch
var _fan: WorkshopFan
var _passed: bool = false


func _ready() -> void:
	visible = false
	run_button.pressed.connect(run_diagnostic)
	close_button.pressed.connect(close_view)
	get_viewport().size_changed.connect(_resize)
	_resize()


func bind(fan_switch: FanSwitch, fan: WorkshopFan) -> void:
	_switch = fan_switch
	_fan = fan


func open() -> void:
	visible = true
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	_refresh()
	run_button.grab_focus()


func close_view() -> void:
	if not visible:
		return
	visible = false
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	closed.emit()


func run_diagnostic() -> void:
	if not _switch.is_on():
		result_label.text = "SWITCH OFF. Turn on the wall switch, then retry."
		result_label.add_theme_color_override("font_color", Color(0.97, 0.68, 0.38))
	elif _fan.get_speed() < 2.0:
		result_label.text = "ROTOR BELOW TEST SPEED. Wait for it to spin up."
		result_label.add_theme_color_override("font_color", Color(0.97, 0.68, 0.38))
	else:
		_passed = true
		result_label.text = "PASS. Fan circuit and rotor speed verified."
		result_label.add_theme_color_override("font_color", Color(0.55, 0.85, 0.64))


func diagnostic_passed() -> bool:
	return _passed


func _process(_delta: float) -> void:
	if visible and _switch and _fan:
		_refresh()


func _unhandled_input(event: InputEvent) -> void:
	if visible and event.is_action_pressed("ui_cancel"):
		close_view()
		get_viewport().set_input_as_handled()


func _refresh() -> void:
	switch_state.text = "SWITCH   " + ("ON" if _switch.is_on() else "OFF")
	rotor_state.text = "ROTOR    %02d RPM" % roundi(_fan.get_speed() * 60.0 / TAU)
	if _passed:
		instructions.text = "The last fan diagnostic passed. The wall switch still controls the fan."
	else:
		instructions.text = "Turn on the wall switch, let the fan spin up, then run the check."


func _resize() -> void:
	var size: Vector2 = get_viewport().get_visible_rect().size
	var compact: bool = size.y < 520.0
	panel.custom_minimum_size = Vector2(minf(760.0, size.x - 40.0), minf(500.0, size.y - 30.0))
	var inset: int = 15 if compact else 30
	for side: String in ["left", "right", "top", "bottom"]:
		content_margin.add_theme_constant_override("margin_" + side, inset)
	heading.add_theme_font_size_override("font_size", 24 if compact else 34)
	instructions.add_theme_font_size_override("font_size", 16 if compact else 21)
