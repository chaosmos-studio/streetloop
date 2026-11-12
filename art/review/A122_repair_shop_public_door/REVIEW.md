# A122 Repair shop public door

The door is a 1.46 m wide frame with a 1.29 m leaf, a 2.89 m frame height, and a threshold at 0.18 m.
Its 28 source objects include fixed jambs and threshold, rubber seals, glazed leaf, mullions, kick plate, inside and outside pulls, latch, strike, and three visible hinges.
The leaf parts are children of `DoorLeafPivot`, whose origin sits on the left hinge axis at local X = -0.635 m.
The frame and latch strike remain stationary.
The glTF preserves the hinge pivot and its 19 child meshes, and contains no unrelated objects.
The source was inspected in the live Blender viewport from the exterior front quarter.
The Godot wrapper drives the glTF pivot and an `AnimatableBody3D` leaf with the same angle.
At the tested frame, an exterior-to-interior ray through the open doorway was clear, while the closed doorway hit `LeafBody`.
The closed door art and collider angles both reached zero, and the close-up render is in `art/review/repair_shop_door_closed.png`.

## Pending review

- [ ] Inspect the door from inside and outside in Godot while opening and closing.
- [ ] Check the player capsule's clearance through the fully open leaf.
- [ ] Verify the leaf never clips into the adjacent pier or workbench.
- [ ] Add handle input and latch sound after the player interaction system exists.
