# A155 Fan wall switch

The switch plate is 0.115 m wide and 0.185 m high, with a recessed rocker, two mounting screws, back terminal, and a small amber indicator.
The rocker and its tactile ridge are children of `SwitchRockerPivot`, while the plate, screws, and terminal remain fixed.
The glTF has 11 nodes, four materials, and is about 55 KiB.
The source was inspected in the live Blender viewport from its front quarter.
The source origin is at the back of the wall plate near its lower edge.

## Pending review

- [ ] Check switch height, reach, and target size in the Godot shop.
- [ ] Link its visible rocker and indicator states to the fan motor state.
- [ ] Test repeated toggles during fan acceleration and coast-down.
- [ ] Inspect the wall contact, material, and close-range readability under room lighting.
