# A003 straight harbor road

The model is 7 m wide and 32 m long, with a 0.14 m structural slab and a top surface at ground level.
The asset origin is at the road center, at ground level.
Blender reports 168 triangles across 14 objects and four materials.
The exported GLB now groups the 14 editable source objects into four static meshes by material.
The grouped export is about 12 KiB and contains no unrelated scene objects.
The road is designed to join at its two lengthwise ends, with curbs supplied by A005.

## Pending review

- [ ] Inspect paint contrast and patch depth in the Godot gameplay camera.
- [ ] Verify the road meets the sidewalk without gaps or vehicle bumps.
- [ ] Measure draw calls and instances in the assembled block.
- [ ] Capture front, side, rear, and gameplay views.
