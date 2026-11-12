extends SceneTree


func _initialize() -> void:
	call_deferred("_benchmark")


func _benchmark() -> void:
	var scene: Node3D = load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	var player: HarborPlayer = scene.get_node("Player")
	player.global_position = Vector3(-4.45, 0.17, 7.0)
	player.camera.current = true
	Input.action_press("move_forward")
	var intervals: PackedFloat64Array = PackedFloat64Array()
	var draws: float = 0.0
	var primitives: float = 0.0
	var previous: int = Time.get_ticks_usec()
	for frame: int in range(180):
		await RenderingServer.frame_post_draw
		var now: int = Time.get_ticks_usec()
		if frame >= 60:
			intervals.append(float(now - previous) / 1000.0)
			draws += float(Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME))
			primitives += float(Performance.get_monitor(Performance.RENDER_TOTAL_PRIMITIVES_IN_FRAME))
		previous = now
	Input.action_release("move_forward")
	intervals.sort()
	var total: float = 0.0
	for interval: float in intervals:
		total += interval
	var count: float = float(intervals.size())
	var mean_ms: float = total / count
	print("Block benchmark 1280x720, 120 sampled walking frames")
	print("Frame mean %.2f ms, p95 %.2f ms, measured %.1f fps" % [mean_ms, intervals[int(count * 0.95)], 1000.0 / mean_ms])
	print("Draw calls mean %.0f, primitives mean %.0f" % [draws / count, primitives / count])
	quit()
