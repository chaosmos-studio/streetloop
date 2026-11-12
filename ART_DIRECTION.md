# Streetloop art direction

## Place

Streetloop takes place in a fictional working port city after a warm rain.
Its first harbor block mixes repair shops, tiled storefronts, concrete walkups, painted metal, wet asphalt, and harbor equipment.
The city should feel inhabited and practical, with shop renovations, patched pavement, hand-lettered local signs made for this world, and objects placed for a reason.

## Shape and scale

Buildings use strong rooflines, recessed doors, deep window frames, and visible structural thickness.
Vehicles use distinct cabin, wheelbase, and cargo silhouettes rather than colour swaps.
Characters use readable posture and clothing shapes before facial detail.
A standing adult is 1.75 m, a compact car is about 4.1 m long, a lane is 3.5 m, and a sidewalk is 2 m.
The third-person camera must keep doors, curbs, wheels, hands, and mission objects readable during motion.

## Palette and materials

The base palette is warm concrete, faded teal, brick, petrol blue, oxidized copper, charcoal asphalt, and amber light.
Wet surfaces should be darker and slightly glossier, without becoming mirrors.
Use rough painted plaster, glazed tile, honed and polished stone, matte wood, woven awnings, rubber, cloth, glass, and worn metal as a small shared material library.
Give every close-range material authored base color, roughness, and normal detail that survives glTF export and the Godot GL Compatibility renderer.
Keep material variation tied to construction, weather, contact, and use instead of random noise.
Wood needs grain that follows its cut and a dry matte finish where hands and tools touch it.
Stone and marble need distinct veining, edge treatment, and finish rather than the same pattern with a different tint.
Tile needs physical grout depth, alignment, and sensible transitions to thresholds and floor mats.
Plaster of Paris ceiling work needs shaped coves and fixtures that belong to the building's construction.

## Visual priority

The player and active vehicles have the clearest silhouette and highest local contrast.
Interactable doors, job objects, and hazards receive a consistent amber or teal accent and a motion cue when relevant.
Background buildings remain legible as architecture but use quieter saturation and fewer sharp details.
Walk-in interiors receive close-range construction detail, individually placed furnishings, readable surfaces, and working objects.
Signals, crosswalks, lanes, and curbs must remain readable in rain and low light.

## Motion and contact

Footsteps should show weight transfer, planted feet, and turns that react to input promptly.
Vehicles should show suspension compression, wheel rotation, braking pitch, and contact with road irregularities.
Loose cloth, hanging cables, puddles, and signs can respond subtly to motion and wind, but should never hide the driving path.
Impact animation must communicate cause and recover into control without a long lockout.

## Lighting

Build the first block for soft late-afternoon sun after rain.
Use one shadowed directional light and broad sky fill in Godot Compatibility.
Blender lights are for asset review, while Godot owns the final look.
Night and storm lighting wait until the day block's materials survive import and gameplay.

## Asset review

Inspect each asset from front, side, rear, and the gameplay camera distance.
Check the source and exported model for scale, pivots, normals, UVs, texture colour space, alpha, separate moving parts, and collision boundaries.
Review movement in motion where the asset animates.
Record triangles, materials, textures, and on-screen instances after import before claiming a performance cost.
The current first-pass car, shop, road, and bench are structure and scale studies until their close-range material and interaction reviews pass.
