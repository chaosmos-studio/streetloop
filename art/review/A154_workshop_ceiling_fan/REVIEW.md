# A154 Workshop ceiling fan

The first fan is 1.34 m across and drops about 0.51 m below its ceiling mount.
Its 39 source objects include a fixed canopy, downrod, coupling, motor housing, cooling vents, and lower bearing bands.
Three formed blades, brackets, fasteners, hub, and lower cap are children of `FanRotorPivot`.
The glTF preserves that pivot and contains five materials in about 207 KiB.
The source was inspected in the live Blender viewport from the motor side and as a whole assembly.
The mount origin is at the ceiling contact point, and the rotor axis is local Z in Blender.

## Pending review

- [ ] Inspect the blade pitch, clearance, and balance from below, side, and above.
- [ ] Place the fan below the shop ceiling and check the view at the player camera.
- [ ] Verify the imported rotor axis and spin direction in Godot.
- [ ] Check acceleration, steady rotation, coast-down, and switch response in motion.
- [ ] Add close-range wear and material variation after the mechanical silhouette passes.
