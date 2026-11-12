# Current Streetloop work

LIFE is the long-term game vision and Streetloop is its playable harbor foundation.
The active area is H00 in `docs/areas/H00_harbor_block.md`.
The public preview is https://chaosmos.studio/streetloop/.

## Next focused slice

Build the original face and skin surface on the new A001 anatomy study, then rig it for contact-aware walking and running.
The full character breakdown is in `docs/CHARACTER_DETAIL_PLAN.md`.
The anatomy review is in `art/review/A001_anatomy_study/REVIEW.md`.
The earlier skinned candidate and its failed motion review remain in `art/review/A001_human_runner_lab/REVIEW.md`.
Keep the existing controller and car route working while the replacement is reviewed.

## Current evidence

The last committed route check drove the workshop trial south, north, and back under real Godot vehicle physics.
The A001 source and review identify round shoulders, mitten hands, a simple face, no deforming skeleton, and no foot IK.
The new Blender candidate imports with 18 bones and five clips, but its feet slide and its modeling is not yet acceptable.
The anatomical study imports at 1.77 m with 24,392 triangles and five meshes, but it has no production rig or clothing.
The current machine has an i5-12500H, Intel Iris Xe graphics, 16 GiB RAM, and about 65 GiB free on the workspace volume.

## Open risks

The visual standard, distinct careers, and complete city simulation in LIFE are far beyond the current one-block prototype.
The player model needs a new deformation rig before a natural human gait can be accepted.
The Web build is roughly 48 MiB before hosting compression and will need a loading and streaming plan as the city grows.
