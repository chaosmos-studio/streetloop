class_name CharacterCatalog
extends RefCounted

const IDENTITIES: Array[CharacterIdentity] = [
	preload("res://assets/characters/mara.tres"),
	preload("res://assets/characters/dev.tres"),
	preload("res://assets/characters/sol.tres"),
]
const SKIN_NAMES: PackedStringArray = ["Umber", "Sienna", "Copper", "Olive", "Honey", "Sand"]
const SKIN_COLORS: Array[Color] = [
	Color("68402e"), Color("895238"), Color("ad6a48"),
	Color("94704d"), Color("bd8961"), Color("d2aa82"),
]
const HAIR_NAMES: PackedStringArray = ["Ink", "Chestnut", "Copper", "Ash"]
const HAIR_COLORS: Array[Color] = [Color("211c1b"), Color("493024"), Color("784633"), Color("66605a")]
const SHIRT_NAMES: PackedStringArray = ["Sea glass", "Indigo", "Clay", "Linen"]
const SHIRT_COLORS: Array[Color] = [Color("607c78"), Color("455f77"), Color("9a6651"), Color("c2b39b")]
const TROUSER_NAMES: PackedStringArray = ["Blue denim", "Charcoal", "Olive", "Sand"]
const TROUSER_COLORS: Array[Color] = [Color("354e68"), Color("3f4144"), Color("5c6550"), Color("9a866c")]


static func identity_index(identity_id: String) -> int:
	for index: int in range(IDENTITIES.size()):
		if IDENTITIES[index].identity_id == identity_id:
			return index
	return 0
