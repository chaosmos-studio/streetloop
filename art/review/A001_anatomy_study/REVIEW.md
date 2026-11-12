# A001 anatomy study review

The [source](../../source/A001_anatomy_study.blend) holds a 1.77 m anatomical sculpt with three multiresolution levels, a complete UV layout, a packed skin color image, and separate eyes and irises.
The [Godot proxy](../../../assets/models/A001_anatomy_proxy.glb) uses the base topology.
The source comes from the official CC0 Blender Human Base Meshes v1.4.1 bundle recorded in `CREDITS.md`.

## Measured cost

- The body base has 10,582 vertices.
- Godot imports five mesh instances, 24,392 triangles, and five material surfaces.
- The imported body bounds are 0.922 m wide, 1.770 m tall, and 0.304 m deep.
- The Blender source is 15,175,971 bytes, the glTF export is 2,272,632 bytes, and the 2048 px skin image is 1,435,425 bytes.
- Five Blender review views and the skin bake completed under a 3 GiB process memory cap on this laptop.
- Blender's color management installation fell back to Standard because its OpenColorIO config and library versions differ.

## Visual inspection

`front.png`, `side.png`, `rear.png`, `face.png`, and `hand.png` show the sculpt in Blender.
`godot_import.png` shows the textured base topology in Godot 4.7 with the GL Compatibility renderer.
The first bake exposed unpainted UV regions, which were fixed by re-unwrapping the body.
The first Godot import exposed inherited eye transforms, which were fixed before the final export.

## Acceptance

The anatomy foundation has distinct fingers and toes and a plausible adult silhouette.
The base face needs an original identity, and the skin needs refined color zones, roughness, pore normals, and close-range lighting review.
The study has no production skeleton, facial shapes, hair, beard, garments, shoes, or movement.
The A001 catalog row remains open, and the playable character has not changed.
