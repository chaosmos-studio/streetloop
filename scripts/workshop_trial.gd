class_name WorkshopTrial
extends Node

enum Stage { IDLE, SOUTH, NORTH, RETURN, COMPLETE }

const SOUTH_TURN: Vector3 = Vector3(0.0, 0.0, 26.0)
const NORTH_TURN: Vector3 = Vector3(0.0, 0.0, -26.0)
const PARKING_POSITION: Vector3 = Vector3(2.25, 0.0, 8.0)

@onready var mechanic: RepairMechanic = $"../HarborBlock/Buildings/CornerRepairShop/Mechanic"
@onready var car: TideHatchback = $"../TideHatchback"
@onready var hud: WorkshopTrialHud = $"../WorkshopTrialHud"

var stage: Stage = Stage.IDLE


func _ready() -> void:
	mechanic.consulted.connect(_on_mechanic_consulted)


func _physics_process(_delta: float) -> void:
	if not car.controls_enabled:
		return
	var position: Vector3 = car.global_position
	if stage == Stage.SOUTH and absf(position.x) < 4.2 and position.z > 24.0:
		_set_stage(Stage.NORTH)
	elif stage == Stage.NORTH and absf(position.x) < 4.2 and position.z < -24.0:
		_set_stage(Stage.RETURN)
	if stage == Stage.SOUTH:
		hud.set_objective("South road end", position.distance_to(SOUTH_TURN))
	elif stage == Stage.NORTH:
		hud.set_objective("North road end", position.distance_to(NORTH_TURN))
	elif stage == Stage.RETURN:
		hud.set_objective("Park by the shop", position.distance_to(PARKING_POSITION))


func _on_mechanic_consulted() -> void:
	match stage:
		Stage.IDLE, Stage.COMPLETE:
			_set_stage(Stage.SOUTH)
		Stage.SOUTH:
			hud.show_stage("Drive to the south road end")
		Stage.NORTH:
			hud.show_stage("Turn and drive to the north end")
		Stage.RETURN:
			var parking_distance: float = car.global_position.distance_to(PARKING_POSITION)
			if parking_distance < 6.0 and car.speed_kmh() < 3.0:
				_set_stage(Stage.COMPLETE)
			else:
				hud.set_objective("Bring the car back", parking_distance)


func _set_stage(value: Stage) -> void:
	stage = value
	match stage:
		Stage.SOUTH:
			mechanic.interaction.prompt_text = "Check road trial"
			hud.show_stage("Drive to the south road end")
		Stage.NORTH:
			mechanic.interaction.prompt_text = "Check road trial"
			hud.show_stage("Turn and drive to the north end")
		Stage.RETURN:
			mechanic.interaction.prompt_text = "Report road trial"
			hud.show_stage("Return and park by the shop")
		Stage.COMPLETE:
			mechanic.interaction.prompt_text = "Run the road trial again"
			hud.show_stage("Trial complete")
