# First harbor block review

Godot 4.7 loaded the road, sidewalks, repair shop, and workbench through separate scene wrappers without parse or import errors.
The exterior and interior were captured at 1280 x 720 using the GL Compatibility renderer on Intel Iris Xe graphics.
The exterior rendered 770 draw calls and 24,542 primitives in the measured frame.
The interior rendered 398 draw calls in the measured frame.
These numbers include scene lighting and shadow passes, and they describe one review camera frame rather than a gameplay performance profile.

The road and sidewalk meet visually along the shop side in the exterior capture.
The shop's wall and floor meshes create an actual interior volume, and the workbench appears inside it at room scale.
The first interior capture was too dark, so two provisional task lights were added before the recorded view.
The exterior facade and the bench remain legible, while the interior is sparse and needs the individual furnishings listed in the catalog.

The closed door and shutter are currently visual meshes without synchronized collision or opening behavior.
The upper floor has no stair route yet.
The current camera is fixed for asset review, and no player or vehicle controller has been integrated.
Static export meshes must be grouped by material while retaining editable Blender parts and separate interactive components.
The next review must measure the draw-call change, prove doorway and furnishing clearance with the player capsule, and inspect the car from the driving camera.
