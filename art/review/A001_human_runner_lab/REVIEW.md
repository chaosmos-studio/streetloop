# A001 human runner lab review

This is a candidate rig and motion basis, not the accepted player character.
The playable scene still uses `A001_harbor_runner.glb`.

## Measured import

- Blender source: `art/source/A001_human_runner.blend`, 284,057 bytes.
- Godot export: `assets/models/A001_human_runner.glb`, 627,656 bytes.
- Imported Godot scene: 18 bones, 50 mesh instances, 9,188 triangles, and five clips named Idle, Walk, Run, Jump, and Land.
- The walk loop is 0.800 seconds and the run loop is 0.533 seconds at 30 fps.
- The skeleton and all five clips imported without an error in Godot 4.7 Compatibility.

The source and export sizes should be remeasured after later model changes.
The inspection script prints the current imported geometry and clip counts.

## Visual evidence

The files `art/review/human_runner_front.png`, `human_runner_side.png`, and `human_runner_rear.png` show the rest silhouette.
The walk and run captures show key poses, and `human_runner_block_idle.png`, `human_runner_block_walk.png`, and `human_runner_block_run.png` show the candidate in the harbor scene at the game camera distance.
The first Godot capture caught disconnected mesh pieces caused by duplicate Blender vertex groups.
The final captured images have continuous jacket sleeves and trouser legs after that correction.

## Acceptance decision

The candidate fails the character standard.
The face, shoulders, hands, shoe size, clothing construction, and surface finish still look simplified.
The stance foot does not stay planted, the run lacks a convincing airborne phase, and the cycle does not cover stops, turns, slopes, stairs, or vehicle entry.
The current screenshots are isolated frames rather than a full moving review.
Do not replace the playable runner until the model, contact-aware clips, game-camera motion, and collision alignment pass `docs/CHARACTER_STANDARD.md`.

## Next focused work

1. Refine continuous anatomical surfaces and clothing from front, side, and rear reference.
2. Author heel, midfoot, and toe contact using foot targets and bake the result into walk and run clips.
3. Blend animation from controller speed and add starts, stops, turns, jump, landing, and car entry.
4. Capture continuous motion at 1.7 m/s and 3.8 m/s and measure planted-foot drift.
5. Test the whole harbor route with the replacement scene before changing the default player.
