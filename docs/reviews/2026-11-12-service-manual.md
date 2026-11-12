# Service manual review

The 0.30 m clothbound book sits on the repair shop workbench. Its Blender source has a separate cover pivot, a cream paper block, visible leaf edges, an inset title, and tarnished corner guards.
Godot imports the 579,252-byte glTF as 9 meshes, 7 materials, and 7,292 triangles. The cover uses three 512 x 512 textures. The reading page uses a separate original 1024 x 768 paper texture.

The player opened the manual with the same focus interaction as the door and fan switch. All four authored pages turned forward and backward, and closing the view returned movement control. The imported book and the reading page were captured in Godot at 1280 x 720, with the reading page also captured at 844 x 390.

The physical cover pivot is present but does not yet move. The game room still lacks the lighting and material detail needed for a final close-range benchmark.
