class_name CharacterChoice
extends RefCounted

const SAVE_PATH: String = "user://character.json"
const VERSION: int = 1

var identity: int = 0
var skin: int = 2
var hair: int = 0
var shirt: int = 0
var trousers: int = 0


func copy() -> CharacterChoice:
	var result: CharacterChoice = CharacterChoice.new()
	result.identity = identity
	result.skin = skin
	result.hair = hair
	result.shirt = shirt
	result.trousers = trousers
	return result


func validate() -> void:
	identity = clampi(identity, 0, CharacterCatalog.IDENTITIES.size() - 1)
	skin = clampi(skin, 0, CharacterCatalog.SKIN_COLORS.size() - 1)
	hair = clampi(hair, 0, CharacterCatalog.HAIR_COLORS.size() - 1)
	shirt = clampi(shirt, 0, CharacterCatalog.SHIRT_COLORS.size() - 1)
	trousers = clampi(trousers, 0, CharacterCatalog.TROUSER_COLORS.size() - 1)


func save(path: String = SAVE_PATH) -> bool:
	validate()
	var file: FileAccess = FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		push_error("Could not save character: %s" % FileAccess.get_open_error())
		return false
	var data: Dictionary = {
		"version": VERSION,
		"identity": CharacterCatalog.IDENTITIES[identity].identity_id,
		"skin": skin,
		"hair": hair,
		"shirt": shirt,
		"trousers": trousers,
	}
	file.store_string(JSON.stringify(data))
	file.close()
	return true


static func read_saved(path: String = SAVE_PATH) -> CharacterChoice:
	var choice: CharacterChoice = CharacterChoice.new()
	if not FileAccess.file_exists(path):
		return choice
	var file: FileAccess = FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_error("Could not read character: %s" % FileAccess.get_open_error())
		return choice
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	file.close()
	if not parsed is Dictionary:
		return choice
	var data: Dictionary = parsed as Dictionary
	if data.get("version", 0) != VERSION:
		return choice
	choice.identity = CharacterCatalog.identity_index(str(data.get("identity", "")))
	choice.skin = int(data.get("skin", 2))
	choice.hair = int(data.get("hair", 0))
	choice.shirt = int(data.get("shirt", 0))
	choice.trousers = int(data.get("trousers", 0))
	choice.validate()
	return choice
