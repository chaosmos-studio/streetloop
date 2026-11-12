# First harbor block review

Godot 4.7 loaded the road, sidewalks, repair shop, and workbench through separate scene wrappers without parse or import errors.
The exterior and interior were captured at 1280 x 720 using the GL Compatibility renderer on Intel Iris Xe graphics.
The exterior rendered 770 draw calls and 24,542 primitives in the measured frame.
The interior rendered 398 draw calls in the measured frame.
These numbers include scene lighting and shadow passes, and they describe one review camera frame rather than a gameplay performance profile.
Grouping only the repeated road and sidewalk exports by material lowered the same exterior view to 556 draw calls and the interior view to 369.
The grouped exports retain 14 road parts and 21 sidewalk parts in their editable Blender sources.
The images in this review show the grouped exports and were recaptured after the Godot reimport.

The road and sidewalk meet visually along the shop side in the exterior capture.
The shop's wall and floor meshes create an actual interior volume, and the workbench appears inside it at room scale.
The first interior capture was too dark, so two provisional task lights were added before the recorded view.
The exterior facade and the bench remain legible, while the interior is sparse and needs the individual furnishings listed in the catalog.

The garage shutter remains a visual mesh without synchronized collision or opening behavior.
The upper floor has no stair route yet.
The current camera is fixed for asset review, and no player or vehicle controller has been integrated.
Static export meshes must be grouped by material while retaining editable Blender parts and separate interactive components.
The next review must measure the draw-call change, prove doorway and furnishing clearance with the player capsule, and inspect the car from the driving camera.
The hinged A122 door replaced the shop's decorative leaf, and its closed close-up is in `art/review/repair_shop_door_closed.png`.
An open doorway ray was clear and the same ray hit `LeafBody` after closing, which checks the collider state along the intended entry path.
The exterior view measured 640 draw calls after the separate door was added.
The separate ceiling fan and wall switch were imported into the repair shop and connected locally.
The review capture measured fan speed at 0 before the switch, 6.52 rad/s after 120 rendered frames switched on, and 5.40 rad/s after 60 rendered frames switched off.
The captures in `art/review/workshop_fan_on.png` and `art/review/fan_switch_on.png` show the imported assets, but the room finishes remain flat and the switch has no player input path yet.
The latest exterior review frame measured 781 draw calls and 37,278 primitives, and the interior measured 452 draw calls with the fan and switch present.
The A149 ceramic module has 16 bevelled tiles and recessed grout across a 2 m square.
Its Blender source retains 17 separate objects and the GLB groups them into four material meshes.
Four modules cover the repair shop entrance, and the Godot capture is in `art/review/ceramic_floor_close.png`.
The corrected export imported without errors and the entrance view measured 460 draw calls, while the exterior measured 833 draw calls and 48,666 primitives.
The current grout is readable, but the tile glaze and surface variation are too subtle in the Compatibility renderer at player height.
The first player controller entered the repair shop from the sidewalk during a 72-tick forward input run.
The player moved from `(4.7, 0.17, 3.36)` to `(9.52, 0.16, 3.36)` and remained on the floor.
The gameplay camera captured both the entrance and interior in `art/review/first_player_spawn.png` and `art/review/first_player_shop.png`.
The character reads at the gameplay distance, but its shoulders, hands, and workwear need the material and form pass recorded in the A001 review.
The on-foot interaction ray closes and reopens the public door from the entry path.
The same input turns on the shop fan switch, and the fan reached 3.27 rad/s after 60 physics ticks in the focused interaction run.
The switch light and rocker show its state while the room stays loaded.
