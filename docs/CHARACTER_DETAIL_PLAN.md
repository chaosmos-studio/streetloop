# A001 realistic character work

The player character is built as a sequence of independently reviewed parts.
The anatomy source in `art/source/A001_anatomy_study.blend` is the shared measurement base.
The accepted character must fit the 1.77 m controller and be readable from the game camera and in close interaction shots.

## Work units

- [x] Establish a proportioned adult body study with individual fingers and toes and inspect it in Blender and Godot.
- [ ] Sculpt an original face and body identity, with asymmetry and age cues visible at close range.
- [ ] Paint skin color zones, lips, eyelids, palms, nails, scars, pores, and roughness at physically plausible scale.
- [ ] Build eyes with iris, pupil, cornea, tear line, eyelid thickness, and gaze controls.
- [ ] Build teeth, tongue, inner mouth, jaw, and a reviewed set of smile, laugh, speech, blink, and pain shapes.
- [ ] Groom scalp hair, eyebrows, eyelashes, and an optional beard in editable sources, then create game-ready cards or strands with measured overdraw.
- [ ] Rig spine, neck, shoulders, hips, knees, ankles, toes, wrists, all finger segments, jaw, eyes, and facial controls.
- [ ] Inspect deformation at crouch, full stride, overhead reach, grasp, seated driving, and facial extremes.
- [ ] Make the first cotton shirt with real thickness, seams, collar, cuffs, buttons, buttonholes, folds, and material maps.
- [ ] Make the first linen or denim trousers with waistband, pockets, fly, hems, and fabric-specific weave and motion.
- [ ] Make footwear with constructed upper, lining, laces or fastening, sole layers, tread, and foot contact pivots.
- [ ] Add optional glasses, jewellery, and bags as separate fitted assets with attachment points.
- [ ] Author and inspect walk, run, start, stop, turn, jump, land, crouch, climb, sit, and vehicle-entry motion with planted-foot checks.
- [ ] Make close, gameplay, and distant levels of detail with measured texture, skinning, hair, and frame costs.
- [ ] Replace the playable runner only after the harbor route, shop interactions, and car entry pass with the new character.

Each item receives its own source, export where relevant, front and side close views, a Godot camera view, a cost entry, and an acceptance note.
Clothing materials use distinct weave, weight, roughness, and fold behavior for cotton, linen, denim, leather, and metal.
The exported animation skeleton will contain every joint that affects visible motion, including finger segments and toes.
Internal anatomy guides can remain in the sculpt source without adding invisible game geometry.

The current body proxy is a measurement and shading reference, not a playable character.
The next unit is the character's original face and skin surface, followed by the deformation rig.

## Creator work units

### Configurable parts

| Part | Current creator | Acceptance before expanding it |
| --- | --- | --- |
| Face and body identity | Three complete adult bases | Review each face and silhouette in motion from front, profile, rear, and gameplay distance. |
| Skin | Five color choices | Paint undertones and roughness by body region, then check every tone in daylight, shade, and interior light. |
| Hair | Four colors on the chosen base groom | Fit independent scalp styles, brows, lashes, and facial hair to every head before exposing style switches. |
| Top and trousers | Separate color choices on one fitted outfit | Author interchangeable garment shapes, sizes, closures, fabric maps, and deformation for every body. |
| Eyes, glasses, jewellery, and bags | Fixed with the identity or absent | Add the separate geometry, attachment points, close views, and collision checks before exposing options. |
| Height, limb lengths, and body proportions | Fixed within each identity | Refit collision, camera, car seat, reach, and every motion clip before adding sliders. |

Expressions, finger joints, skin detail, fabric construction, and shoe contact are quality requirements for every identity rather than creator sliders.
Every visible choice must survive a save and show the same result in the preview, street, shop, and car scenes.

### Acceptance order

1. Finish one original face with reviewed skin, eyes, eyelids, mouth, brows, and expressions.
2. Build a fitted hairline and one groom for that face, then inspect it close and at gameplay scale.
3. Construct one complete outfit and footwear set with authored seams and measured material maps.
4. Correct the shared rig and gait using planted-foot and deformation review.
5. Repeat the same acceptance for the other identities before offering independent hair, facial hair, garment, or proportion choices.
6. Add close, gameplay, and distant LODs and profile frame time on the target laptop.

- [ ] Review multiple original adult face and body bases at front, profile, rear, and gameplay distances.
- [ ] Review skin tones under daylight, shade, and interior light without losing facial structure.
- [ ] Fit at least two hair silhouettes and one facial-hair option to each head shape.
- [ ] Fit clothing shapes and material variants without clipping at walking, crouching, and driving extremes.
- [ ] Rig every selectable body to the same skeleton and review walk, run, turn, jump, sit, and idle in motion.
- [x] Build a rotatable creator preview with clear identity and appearance choices.
- [x] Save and reload the choice, then use it for the live player in the harbor route.
- [ ] Measure draw calls, triangles, texture memory, and frame cost for each combination.

Do not expose a choice until its art changes visibly in both the preview and the live player.
Keep the authoring source, exports, camera review, and acceptance notes for every identity.
The initial creator is a playable character lab. Its models have shared motion clips and visible material choices, but the facial, garment, skin, and gait work above remains open before A001 is accepted.
