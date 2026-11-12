class_name ServiceManualView
extends CanvasLayer

signal closed

const PAGES: Array[Dictionary] = [
	{
		"heading": "Harbor workshop",
		"body": "SERVICE BOOK 04\n\nThis bench belongs to the night crew. Every repair starts with a walk around the vehicle. Note the damage before touching a tool."
	},
	{
		"heading": "South curb hatchback",
		"body": "WORK ORDER 04\n\nThe courier reports a squeal after rain. Bring the blue hatchback into the service bay. Check the belt and its tension before replacing parts."
	},
	{
		"heading": "Under the bonnet",
		"body": "INSPECTION\n\nLet the engine cool. Release the bonnet catch and support the panel. Check the belt for cracks, glazing and loose tension. Keep hands clear of moving pulleys."
	},
	{
		"heading": "Bench notes",
		"body": "RETURN TO SERVICE\n\nFit the correct belt, set its tension and turn the pulley by hand. Start the engine only after the tools are clear. Listen again with the bonnet open."
	},
]

@onready var panel: PanelContainer = $Shade/Margin/Center/Page
@onready var page_margin: MarginContainer = $Shade/Margin/Center/Page/Padding
@onready var heading: Label = $Shade/Margin/Center/Page/Padding/Content/Heading
@onready var body: Label = $Shade/Margin/Center/Page/Padding/Content/Body
@onready var count: Label = $Shade/Margin/Center/Page/Padding/Content/Navigation/Count
@onready var previous_button: Button = $Shade/Margin/Center/Page/Padding/Content/Navigation/Previous
@onready var next_button: Button = $Shade/Margin/Center/Page/Padding/Content/Navigation/Next
@onready var close_button: Button = $Shade/Margin/Center/Page/Padding/Content/Navigation/Close

var _page_index: int = 0


func _ready() -> void:
	visible = false
	previous_button.pressed.connect(previous_page)
	next_button.pressed.connect(next_page)
	close_button.pressed.connect(close_view)
	get_viewport().size_changed.connect(_resize)
	_resize()
	_refresh()


func open() -> void:
	_page_index = 0
	_refresh()
	visible = true
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	next_button.grab_focus()


func close_view() -> void:
	if not visible:
		return
	visible = false
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	closed.emit()


func next_page() -> void:
	_page_index = mini(_page_index + 1, PAGES.size() - 1)
	_refresh()


func previous_page() -> void:
	_page_index = maxi(_page_index - 1, 0)
	_refresh()


func current_page() -> int:
	return _page_index


func _unhandled_input(event: InputEvent) -> void:
	if not visible or not event.is_pressed():
		return
	if event.is_action_pressed("ui_cancel"):
		close_view()
	elif event.is_action_pressed("ui_right"):
		next_page()
	elif event.is_action_pressed("ui_left"):
		previous_page()
	else:
		return
	get_viewport().set_input_as_handled()


func _refresh() -> void:
	heading.text = PAGES[_page_index]["heading"]
	body.text = PAGES[_page_index]["body"]
	count.text = "%02d / %02d" % [_page_index + 1, PAGES.size()]
	previous_button.disabled = _page_index == 0
	next_button.disabled = _page_index == PAGES.size() - 1


func _resize() -> void:
	var size: Vector2 = get_viewport().get_visible_rect().size
	var compact: bool = size.y < 520.0
	panel.custom_minimum_size = Vector2(minf(720.0, size.x - 48.0), minf(500.0, size.y - 36.0))
	var inset: int = 16 if compact else 32
	for side: String in ["left", "right", "top", "bottom"]:
		page_margin.add_theme_constant_override("margin_" + side, inset)
	heading.add_theme_font_size_override("font_size", 27 if compact else 36)
	body.add_theme_font_size_override("font_size", 18 if compact else 24)
