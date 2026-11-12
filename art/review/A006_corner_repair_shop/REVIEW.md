# A006 corner repair shop

The building footprint is 10 m by 8 m and its roof details reach about 8.2 m above ground.
The street-facing facade is local positive Y in Blender, which exports toward Godot negative Z.
The entrance door, garage shutter, roof tank, awning, and windows are separate source objects.
The second-pass GLB contains 82 intended mesh nodes, 10 materials, and is 220 KiB.
The solid placeholder shell was replaced with separate floor slabs, rear and side walls, front piers, lintels, and upper window openings.
The front pedestrian opening is about 1.6 m wide and the service bay opening is about 5.05 m wide.
The door and shutter remain separate meshes for later opening animation.
The exterior was inspected again in the live Blender viewport after the structural change.

## Pending review

- [ ] Inspect the facade and roof from the gameplay camera in Godot.
- [x] Replace the solid shell with structural openings for the pedestrian door and service bay.
- [ ] Test the actual player route through the door after Godot collision and opening behavior are wired.
- [ ] Build and inspect the interior furnishing assets from every reachable camera angle.
- [ ] Merge static export geometry by material after measuring draw calls in the block.
- [ ] Add front, side, rear, and gameplay review images.
- [ ] Verify door and shutter pivots, collision, and clearance before enabling interaction.
