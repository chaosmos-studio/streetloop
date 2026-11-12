# A005 harbor sidewalk

The model is 2 m wide and 32 m long, with an intended 0.17 m walking surface and a 0.19 m curb lip.
The origin is centered on the ground plane, with the street-facing edge at local X = -1 m.
Blender reports 252 triangles across 21 objects and five materials.
The exported GLB is 26,236 bytes.
The paving pattern is authored as separate shallow fields over a continuous base, so gameplay collision can use one simple shape.

## Pending review

- [ ] Inspect paving joints and curb height in the Godot gameplay camera.
- [ ] Verify the curb meets A003 without a gap or a sudden tire collision.
- [ ] Measure draw calls when the sidewalk repeats around the block.
- [ ] Capture front, side, rear, and gameplay views.
