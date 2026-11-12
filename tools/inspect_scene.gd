extends SceneTree


func _initialize() -> void:
	var path: String = OS.get_cmdline_user_args()[0]
	var packed: PackedScene = load(path)
	var instance: Node = packed.instantiate()
	root.add_child(instance)
	_print_tree(instance, 0)
	quit()


func _print_tree(node: Node, depth: int) -> void:
	if node is Node3D:
		var spatial: Node3D = node as Node3D
		print("  ".repeat(depth), node.name, " ", node.get_class(), " ", spatial.position)
	else:
		print("  ".repeat(depth), node.name, " ", node.get_class())
	for child: Node in node.get_children():
		_print_tree(child, depth + 1)
