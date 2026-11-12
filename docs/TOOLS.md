# Local editor tools

The project uses Godot 4.7 with the GL Compatibility renderer and Blender 5.2 for asset sources.
The Godot Editor MCP add-on is pinned at `2026.10.20.1` in `addons/godot_mcp/`.
Its matching Codex server is registered globally as `godot_editor` with `godot-editor-mcp==2026.10.20.1`.
The add-on archive was checked against the release SHA-256 `7173bb197eca2a8522b2173342ce474052d7746c3b36a9d404e554ae8cc1fbaf`.
Open this project in the Godot editor to let the add-on connect to the local MCP server at `127.0.0.1:9080`.
The Godot command line remains the verification path when the editor is closed.

Blender Lab MCP is registered globally as `blender`.
Open Blender with the MCP extension enabled and its bridge running to edit the live Blender scene.
Keep the source `.blend` for every asset independent of the exported GLB.
