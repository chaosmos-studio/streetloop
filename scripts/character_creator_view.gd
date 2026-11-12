class_name CharacterCreatorView
extends CanvasLayer

signal opened
signal saved(choice: CharacterChoice)
signal closed

@onready var open_button: Button = $OpenButton
@onready var overlay: Control = $Overlay
@onready var grid: GridContainer = $Overlay/Grid
@onready var preview: CharacterAppearance = $Overlay/Grid/PreviewPanel/Preview/ViewportContainer/Viewport/Stage/Visual
@onready var preview_camera: Camera3D = $Overlay/Grid/PreviewPanel/Preview/ViewportContainer/Viewport/Stage/Camera
@onready var description: Label = $Overlay/Grid/ChoicesPanel/Layout/Scroll/Form/Description
@onready var identity: OptionButton = $Overlay/Grid/ChoicesPanel/Layout/Scroll/Form/Identity
@onready var skin: OptionButton = $Overlay/Grid/ChoicesPanel/Layout/Scroll/Form/Skin
@onready var hair: OptionButton = $Overlay/Grid/ChoicesPanel/Layout/Scroll/Form/Hair
@onready var shirt: OptionButton = $Overlay/Grid/ChoicesPanel/Layout/Scroll/Form/Shirt
@onready var trousers: OptionButton = $Overlay/Grid/ChoicesPanel/Layout/Scroll/Form/Trousers
@onready var back: Button = $Overlay/Grid/ChoicesPanel/Layout/Actions/Back
@onready var save_button: Button = $Overlay/Grid/ChoicesPanel/Layout/Actions/Save
@onready var view_toggle: Button = $Overlay/Grid/PreviewPanel/Preview/ViewToggle

var choice: CharacterChoice = CharacterChoice.new()
var _first_visit: bool = false
var _face_view: bool = false
var _dragging: bool = false


func _ready() -> void:
	_populate(identity, CharacterCatalog.IDENTITIES.map(func(item: CharacterIdentity) -> String: return item.display_name))
	_populate(skin, CharacterCatalog.SKIN_NAMES)
	_populate(hair, CharacterCatalog.HAIR_NAMES)
	_populate(shirt, CharacterCatalog.SHIRT_NAMES)
	_populate(trousers, CharacterCatalog.TROUSER_NAMES)
	for option: OptionButton in [identity, skin, hair, shirt, trousers]:
		option.item_selected.connect(_refresh)
	open_button.pressed.connect(func() -> void: open(CharacterChoice.read_saved(), false))
	back.pressed.connect(close)
	save_button.pressed.connect(_save)
	$Overlay/Grid/PreviewPanel/Preview/TurnLeft.pressed.connect(func() -> void: preview.rotation.y -= PI / 4.0)
	$Overlay/Grid/PreviewPanel/Preview/TurnRight.pressed.connect(func() -> void: preview.rotation.y += PI / 4.0)
	view_toggle.pressed.connect(_toggle_view)
	$Overlay/Grid/PreviewPanel/Preview.gui_input.connect(_preview_input)
	get_viewport().size_changed.connect(_resize)
	_resize()
	_style()


func _populate(option: OptionButton, names: Variant) -> void:
	for label: String in names:
		option.add_item(label)


func open(saved_choice: CharacterChoice, first_visit: bool) -> void:
	choice = saved_choice.copy()
	_first_visit = first_visit
	identity.select(choice.identity)
	skin.select(choice.skin)
	hair.select(choice.hair)
	shirt.select(choice.shirt)
	trousers.select(choice.trousers)
	_face_view = false
	_update_camera()
	_refresh(0)
	overlay.visible = true
	open_button.visible = false
	back.visible = not first_visit
	identity.grab_focus()
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	opened.emit()


func close() -> void:
	if _first_visit:
		return
	overlay.visible = false
	open_button.visible = true
	closed.emit()


func _save() -> void:
	if not choice.save():
		return
	overlay.visible = false
	open_button.visible = true
	_first_visit = false
	saved.emit(choice.copy())


func set_available(value: bool) -> void:
	open_button.visible = value and not overlay.visible


func _refresh(_selected: int) -> void:
	choice.identity = identity.selected
	choice.skin = skin.selected
	choice.hair = hair.selected
	choice.shirt = shirt.selected
	choice.trousers = trousers.selected
	description.text = CharacterCatalog.IDENTITIES[choice.identity].description
	preview.apply_choice(choice)


func _toggle_view() -> void:
	_face_view = not _face_view
	_update_camera()


func _update_camera() -> void:
	preview_camera.position = Vector3(0, 1.62, 1.05) if _face_view else Vector3(0, 1.2, 3.1)
	preview_camera.look_at(Vector3(0, 1.62 if _face_view else 0.95, 0))
	view_toggle.text = "BODY" if _face_view else "FACE"


func _preview_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		_dragging = event.pressed
	elif event is InputEventMouseMotion and _dragging:
		preview.rotation.y += event.relative.x * 0.012
	elif event is InputEventScreenDrag:
		preview.rotation.y += event.relative.x * 0.012


func _unhandled_input(event: InputEvent) -> void:
	if not overlay.visible:
		return
	if event.is_action_pressed("ui_cancel"):
		close()
		get_viewport().set_input_as_handled()


func _resize() -> void:
	var size: Vector2 = get_viewport().get_visible_rect().size
	grid.columns = 1 if size.x < 760.0 else 2
	var margin: float = 12.0 if size.y < 600.0 else 36.0
	grid.offset_left = margin
	grid.offset_top = margin
	grid.offset_right = -margin
	grid.offset_bottom = -margin
	var viewport_panel: Control = $Overlay/Grid/PreviewPanel
	viewport_panel.custom_minimum_size.y = 180.0 if grid.columns == 1 else 330.0


func _style() -> void:
	var panel_style: StyleBoxFlat = StyleBoxFlat.new()
	panel_style.bg_color = Color("203039")
	panel_style.border_color = Color("5b7478")
	panel_style.set_border_width_all(1)
	panel_style.set_corner_radius_all(14)
	for panel: PanelContainer in [$Overlay/Grid/PreviewPanel, $Overlay/Grid/ChoicesPanel]:
		panel.add_theme_stylebox_override("panel", panel_style)
	for button: Button in [open_button, back, save_button]:
		button.add_theme_font_size_override("font_size", 17)
