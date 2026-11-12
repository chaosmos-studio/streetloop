# A125 Mechanic workbench

The first interior prop is 2.4 m wide, 0.78 m deep, and approximately 1.26 m high including the vise.
It has a worn hardwood top with separate board seams, a steel frame with four rubber feet, a lower shelf, three drawer fronts with pulls, and a vise with separate fixed jaw, moving jaw, screw, handle, and end knobs.
The editable Blender source contains 50 separate objects and six materials.
The model was inspected in the live Blender viewport from the front quarter and the working surface remains legible at room scale.
The source origin is on the ground below the center of the top, with local positive Y facing the user.
The worktop and lower shelf now use the original A164 color, roughness, and normal maps packed into the editable source and embedded in the glTF.
The material was inspected from the bench's usable side in Godot at 1280 x 720 in `art/review/workbench_material_close.png`.
The surface reads as dry wood with visible grain and retains its color under the interior lights.
The grain is still too regular for final close inspection and needs another authored variation pass.

## Pending review

- [ ] Verify all surfaces and the handle from the Godot gameplay camera.
- [ ] Place the bench in the repair shop and test approach, collision, and drawer reach.
- [ ] Measure imported triangles and draw calls before deciding which static pieces to merge.
- [ ] Animate the vise and drawers when they have gameplay interactions.
- [ ] Capture front, side, rear, detail, and in-game views.
