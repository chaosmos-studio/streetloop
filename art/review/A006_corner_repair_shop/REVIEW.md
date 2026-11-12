# A006 corner repair shop

The building footprint is 10 m by 8 m and its roof details reach about 8.2 m above ground.
The street-facing facade is local positive Y in Blender, which exports toward Godot negative Z.
The entrance door, garage shutter, roof tank, awning, and windows are separate source objects.
The GLB contains 63 intended objects, 10 materials, 1,844 triangles with bevel modifiers applied, and 110,476 bytes.

## Pending review

- [ ] Inspect the facade and roof from the gameplay camera in Godot.
- [ ] Replace visual facade overlays with recessed openings where the player can enter.
- [ ] Merge static export geometry by material after measuring draw calls in the block.
- [ ] Add front, side, rear, and gameplay review images.
- [ ] Verify door and shutter pivots, collision, and clearance before enabling interaction.
