# A141 Hatchback wheel and tire

The wheel is a separate assembly with a 0.373 m rolling radius and a 0.224 m overall tire width.
Its editable source has a watertight profiled rubber casing, fine three-lane road tread, alloy rim and bead, five spokes and lug bolts, hub, brake disc, caliper, and valve stem.
The brake caliper is separate so it can stay fixed while the wheel, hub, and disc rotate.
The source has 21 objects and six materials, and the glTF has 6,216 triangles and is about 347 KiB.
The pivot is at the wheel center and the axle is local X.

The first tread render looked like an off-road tire, so the blocks were made shallower and closer together.
The revised wheel was inspected in the live Blender viewport from the outer front quarter.

## Pending review

- [ ] Inspect the inner side, face, tread, and brake hardware from dedicated views.
- [ ] Fit four instances to the hatchback and check clearance through full suspension and steering travel.
- [ ] Separate the rotating assembly from stationary brake hardware in the Godot wrapper.
- [ ] Test wheel rotation, tire contact, brake response, and curb impact in motion.
- [ ] Measure draw calls and any needed mesh grouping after the moving assembly works.
