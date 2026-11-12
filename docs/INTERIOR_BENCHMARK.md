# Repair shop interior benchmark

The repair shop is the first complete close-range space and sets the standard for later homes and businesses.
The player must be able to enter, move around every furnishing, examine each authored object, operate the fan, read the service manual, use the computer, and leave without a camera or collision jump.

## Construction pass

- [ ] Set the ground floor plan from a 1.75 m person and a 0.64 m wide player collider.
- [ ] Fit the public doorway, service bay, stairs, upper landing, windows, and roof route with actual clearance.
- [ ] Build ceramic tile, honed marble, rubber mat, plaster cove, and skirting as distinct construction layers.
- [ ] Check that floor changes preserve a continuous walkable surface and do not snag a wheel or foot.
- [ ] Place fixtures according to structural supports, electrical routes, sightlines, and plausible use.

## Material pass

- [ ] Make original base-color, roughness, and normal textures for close-range wood, tile, stone, rubber, and plaster.
- [ ] Give the bench a dry matte finish, shaped edges, fasteners, worn grips, and scratches where tools contact it.
- [ ] Make marble and tile patterns distinct in geometry, vein scale, grout, and reflectance.
- [ ] Bake Blender-only procedural details and verify the exported material inside Godot Compatibility.
- [ ] Inspect each material in daylight, interior task light, grazing light, and from normal player distance.

## Function pass

- [ ] Open and close the public door with aligned art, collision, latch, and sound.
- [ ] Give each furnishing a collision shape and a close inspection position that the camera can reach.
- [x] Animate the fan blades with acceleration and coast-down tied to the wall switch.
- [x] Make the switch state visible and the fan state persistent while the room remains loaded.
- [x] Let the service manual open, turn pages, and show original legible content.
- [ ] Let the computer gain input focus, accept player input, and return control cleanly to movement.
- [ ] Give drawers, cabinets, and loose items individual inspect or use states where their construction suggests one.

## Review pass

- [ ] Walk the room as a player and inspect every reachable item from its intended distance.
- [ ] Check door, stair, workbench, desk, and ceiling-fan clearances during motion.
- [ ] Check the fan and switch from all directions and at several speeds.
- [ ] Read the book and computer text at 1280 x 720 and a wide phone viewport.
- [ ] Record imported triangles, materials, texture memory, draw calls, frame time, and compressed build size.
- [ ] Capture exterior, room-wide, close material, interaction, and moving-object evidence.

One object is accepted only after its Blender source, glTF export, Godot scene, behavior, and review record agree.
The current screenshots show a structural room, a first-pass bench, an operated fan and switch, one ceramic entrance section, and the service manual at desktop and landscape phone sizes.
The floor finish still needs material and lighting refinement before this benchmark is complete.
