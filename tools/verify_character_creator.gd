extends SceneTree


func _initialize() -> void:
	call_deferred("_verify")


func _verify() -> void:
	var path: String = "user://character_verification.json"
	var choice: CharacterChoice = CharacterChoice.new()
	choice.identity = 2
	choice.skin = 5
	choice.hair = 3
	choice.shirt = 2
	choice.trousers = 1
	if not choice.save(path):
		quit(1)
		return
	var restored: CharacterChoice = CharacterChoice.read_saved(path)
	DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
	if [restored.identity, restored.skin, restored.hair, restored.shirt, restored.trousers] != [2, 5, 3, 2, 1]:
		push_error("Character selection did not survive a save and load")
		quit(1)
		return
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	var player: HarborPlayer = scene.get_node("Player")
	var creator: CharacterCreatorView = scene.get_node("CharacterCreatorView")
	creator.open(restored, false)
	if creator.description.text != CharacterCatalog.IDENTITIES[2].description:
		push_error("Creator did not load the saved identity")
		quit(1)
		return
	player.visual.apply_choice(restored)
	var model: Node3D = player.visual.get_child(0) as Node3D
	if model == null or model.name.to_lower().find("sol") < 0:
		push_error("Selected identity did not replace the live player")
		quit(1)
		return
	var animation: AnimationPlayer = model.find_child("AnimationPlayer*", true, false) as AnimationPlayer
	if animation == null or not animation.has_animation("Walk"):
		push_error("Selected identity lost its locomotion clips")
		quit(1)
		return
	print("Character creator save, load, preview, live model, and clips verified")
	quit()
