# A164 Bench surface material

The first material pass supplies original 1024 x 512 base-color, packed occlusion-roughness-metallic, and tangent-space normal PNGs.
The generated roughness stays in the matte range of about 0.60 to 0.91, and the metallic channel is zero for wood.
The images are packed in the editable material source and embedded in the A125 glTF export.
Godot 4.7 imported the three image textures through the GL Compatibility renderer, and the workbench close view shows the grain under its interior lights.
The three source PNGs total about 1.2 MiB and the updated A125 glTF is about 1.5 MiB.
The texture recipe is in `tools/generate_bench_wood.py`.

The first generated maps were black because Blender's color-space change reset their pixels.
The recipe now sets color space before pixel data, and the saved maps were inspected after regeneration.

## Pending review

- [ ] Replace the regular grain rhythm with more natural board-to-board variation and knots.
- [ ] Inspect UV direction and scale on the top, edge, and lower shelf independently.
- [ ] Check the material under grazing daylight and a moving task light.
- [ ] Measure texture memory and import compression on the intended desktop and phone targets.
