extends Control

var speed_kmh: float = 0.0


func _draw() -> void:
	var center: Vector2 = size * 0.5
	var radius: float = minf(size.x, size.y) * 0.45
	draw_circle(center, radius, Color(0.06, 0.12, 0.13, 0.91))
	draw_arc(center, radius - 3.0, deg_to_rad(0), deg_to_rad(360), 72, Color(0.58, 0.62, 0.57, 0.83), 3.0, true)
	draw_arc(center, radius - 14.0, deg_to_rad(135), deg_to_rad(405), 48, Color(0.21, 0.4, 0.4, 1), 5.0, true)
	for index: int in range(9):
		var angle: float = deg_to_rad(135.0 + index * 33.75)
		var direction: Vector2 = Vector2(cos(angle), sin(angle))
		draw_line(center + direction * (radius - 24.0), center + direction * (radius - 15.0), Color(0.91, 0.84, 0.67, 1), 2.0, true)
	var needle_angle: float = deg_to_rad(135.0 + clampf(speed_kmh / 160.0, 0.0, 1.0) * 270.0)
	var needle: Vector2 = Vector2(cos(needle_angle), sin(needle_angle))
	draw_line(center - needle * 8.0, center + needle * (radius - 29.0), Color(0.89, 0.43, 0.33, 1), 3.0, true)
	draw_circle(center, 5.0, Color(0.88, 0.78, 0.59, 1))
