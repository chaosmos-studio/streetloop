class_name CharacterAppearance
extends Node3D

var _model: Node3D
var _animation: AnimationPlayer
var _speed: float = 0.0
var _grounded: bool = true
var _vertical_speed: float = 0.0


func apply_choice(choice: CharacterChoice) -> void:
	choice.validate()
	if _model != null:
		remove_child(_model)
		_model.queue_free()
		_model = null
	var identity: CharacterIdentity = CharacterCatalog.IDENTITIES[choice.identity]
	_model = identity.model.instantiate() as Node3D
	add_child(_model)
	_animation = _model.find_child("AnimationPlayer*", true, false) as AnimationPlayer
	for node: Node in _model.find_children("*", "MeshInstance3D", true, false):
		var mesh: MeshInstance3D = node as MeshInstance3D
		var color: Color = Color.WHITE
		var name_lower: String = mesh.name.to_lower()
		if name_lower.ends_with(" body"):
			color = CharacterCatalog.SKIN_COLORS[choice.skin]
		elif name_lower == "groom":
			color = CharacterCatalog.HAIR_COLORS[choice.hair]
		elif name_lower.begins_with("cotton "):
			color = CharacterCatalog.SHIRT_COLORS[choice.shirt]
		elif name_lower == "denim trousers" or name_lower.begins_with("trouser "):
			color = CharacterCatalog.TROUSER_COLORS[choice.trousers]
		else:
			continue
		var surface: StandardMaterial3D = StandardMaterial3D.new()
		surface.albedo_color = color
		surface.roughness = 0.88 if name_lower != "groom" else 0.95
		if name_lower.begins_with("cotton "):
			surface.albedo_texture = preload("res://assets/textures/characters/cotton_weave.png")
			surface.normal_enabled = true
			surface.normal_texture = preload("res://assets/textures/A001_runner_cloth_normal.png")
			surface.normal_scale = 0.12
			surface.uv1_scale = Vector3(3, 3, 1)
		elif name_lower == "denim trousers" or name_lower.begins_with("trouser "):
			surface.albedo_texture = preload("res://assets/textures/characters/denim_weave.png")
			surface.normal_enabled = true
			surface.normal_texture = preload("res://assets/textures/A001_runner_cloth_normal.png")
			surface.normal_scale = 0.18
			surface.uv1_scale = Vector3(4, 4, 1)
		mesh.material_override = surface
	if _animation != null:
		for name: String in ["Idle", "Walk", "Run"]:
			var clip: Animation = _animation.get_animation(name)
			if clip != null:
				clip.loop_mode = Animation.LOOP_LINEAR
		_animation.play("Idle")


func set_motion(speed: float, grounded: bool, vertical_speed: float) -> void:
	_speed = speed
	_grounded = grounded
	_vertical_speed = vertical_speed


func _process(_delta: float) -> void:
	if _animation == null:
		return
	var wanted: String = "Idle"
	if not _grounded:
		wanted = "Jump" if _vertical_speed > 0.0 else "Land"
	elif _speed > 2.45:
		wanted = "Run"
	elif _speed > 0.15:
		wanted = "Walk"
	if _animation.current_animation != wanted:
		_animation.play(wanted, 0.12)
	_animation.speed_scale = clampf(_speed / (3.8 if wanted == "Run" else 1.7), 0.75, 1.3) if wanted in ["Walk", "Run"] else 1.0
