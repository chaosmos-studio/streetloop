# A007 harbor twin-arm streetlamp review

The lamp has a 5.6 m tapering cast pole, two swept tubular arms, separate luminaire housings, opal lenses, a service door with hinges and latch, collars, a cable outlet, and anchor bolts.
The editable Blender source contains 50 objects. The grouped glTF contains 6 meshes, 6 materials, 3 images, and 5,728 triangles. It is 761,936 bytes. The first export had 10,816 triangles; simplifying the arm cross-section and small bevels brought the count down without changing the road-distance silhouette.

Four instances are placed along the harbor sidewalks with primitive base and pole collision. The imported result was inspected in Godot from the road, side, rear, and at service-panel distance. The door and fan interactions and the enter-drive-steer-brake-exit route still passed after placement.

The lamp is unlit in the current daylight scene. Its heads are separate in the Blender source but grouped in the static export. Night lighting, wiring behavior, material weathering, and collision checks during a direct vehicle impact remain open. The surrounding district still needs buildings and street furnishings to make these fixtures feel placed in a working city.
