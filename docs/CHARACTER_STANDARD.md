# Human character and gait standard

A001 is a temporary articulated runner with rigid shoulders, hands, knees, and boots.
The replacement keeps the 1.77 m gameplay scale and the current `CharacterBody3D` controller while its visual body changes to a deforming armature.

## Anatomy and deformation

- Keep the head, shoulder girdle, ribcage, pelvis, legs, hands, and feet in believable human proportion from front, side, and rear.
- Keep joints inside the body volume and preserve elbow, knee, shoulder, and hip silhouettes at extreme poses.
- Use one deforming skeleton with continuous weighted skin or clothing surfaces that hide intentional seams.
- Separate the character's style and identity from the rig so age, clothing, and other residents can reuse a reviewed motion basis.
- Match the current floor origin, Godot forward direction, collision capsule, camera scale, and car entry points.

## Gait reference

A walking cycle runs from one foot's contact to its next contact.
At a typical pace the same foot supports weight for about 60 percent of the cycle and swings for about 40 percent.
The stance foot should remain near its contact point while the body travels, then roll from heel through midfoot to forefoot before toe-off.
The pelvis rises near single support, lowers during double support, and rotates modestly as the opposite arm counters leg motion.
Running uses shorter ground contact, airborne phases, stronger arm motion, and a separate cycle rather than a sped-up walk.
The numbers guide first animation keys and are adjusted against reference footage and the actual controller speed.

## Review gate

- [ ] Show front, side, rear, and close hand, foot, face, and shoulder views.
- [ ] Inspect skin weights at hip flexion, knee bend, shoulder raise, elbow flexion, and torso twist.
- [ ] Show synchronized walk and run clips at the game's actual speeds from side and gameplay camera.
- [ ] Check heel contact, planted foot drift, toe-off, both support transitions, stops, turns, stairs, jumps, and car entry.
- [ ] Measure stride length, cycle frequency, frame cost, triangle count, material count, texture memory, and export size.
- [ ] Test keyboard, gamepad, and touch movement and verify the shop and car routes still pass.

The review must compare moving footage, not selected still poses alone.
An "exact human walk" is not a single universal loop because gait varies with person, speed, footwear, terrain, and load.
The target is a believable, reference-led performance that stays responsive to play.

## References

- [Human gait phases and events](https://pmc.ncbi.nlm.nih.gov/articles/PMC8595292/).
- [Ankle and foot rollover during walking](https://pmc.ncbi.nlm.nih.gov/articles/PMC3918177/).
- [Pelvis motion during gait](https://pmc.ncbi.nlm.nih.gov/articles/PMC5545133/).
- [Arm swing and whole-body balance](https://pmc.ncbi.nlm.nih.gov/articles/PMC2817299/).
- [Godot 4.7 AnimationTree and root motion](https://docs.godotengine.org/en/4.7/tutorials/animation/animation_tree.html).
- [Godot 4.7 humanoid retargeting](https://docs.godotengine.org/en/4.7/tutorials/assets_pipeline/retargeting_3d_skeletons.html).
