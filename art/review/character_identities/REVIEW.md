# First character identity review

Mara, Dev, and Sol are distinct adult character studies at the current 1.77 m player scale.
Mara uses the realistic female anatomical base. Dev and Sol use the realistic male base with different face and body proportions.
Each source is editable in `art/source/character_identities/` and exports to `assets/models/characters/`.
The feet sit at the model origin and the face points toward positive Z in Godot.

| Identity | Imported meshes | Triangles | Skeleton bones | GLB size |
| --- | ---: | ---: | ---: | ---: |
| Mara | 25 | 80,150 | 43 | 7.46 MB |
| Dev | 26 | 67,606 | 43 | 5.84 MB |
| Sol | 25 | 80,000 | 43 | 7.62 MB |

Each export contains Idle, Walk, Run, Jump, and Land clips.
Front, profile, rear, and face views were rendered from the editable source at 720 by 960 pixels.
The 1280 by 720 creator screenshot shows the actual Godot GL Compatibility render at 1,021 draw calls and 261,790 rendered primitives for the whole scene and preview.
The 450 by 900 portrait view was inspected with the same character assets and its Save button visible without scrolling.
The live-player capture followed a 2.78 m walk into the repair shop, ended grounded, and recorded 748 draw calls and 184,020 rendered primitives for the visible scene.
The creator save, reload, model swap, and clip availability were exercised in Godot.
The existing workshop, driving, and touch control checks passed after the first-visit creator screen was accounted for in the touch harness.

## Next acceptance work

- Replace the current close-range hair cap with a groom that has an authored hairline and varied flow.
- Improve the constructed shoes with a fitted last, heel, tongue, eyelets, and foot roll.
- Add skin zones, pores, lips, eyelids, teeth, nail beds, and facial expression controls.
- Fit shirts and trousers with authored seams, cuffs, folds, and close-range fabric maps.
- Inspect deformation, foot placement, starts, stops, turns, crouches, and driving at normal game speed.
- Measure the frame-time cost of each identity on the target laptop and add a distant LOD.

The models are playable studies. They have not passed the realistic A001 character acceptance bar.
