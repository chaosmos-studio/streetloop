# Tide hatchback exterior and cabin review

The first Tide hatchback body was a scale and driving study with an opaque upper shell.
The revised body has formed bonnet and roof surfaces, wheel opening lips, separate glass, door shutlines, mirrors, lamps, a hatch outline, and a textured petrol blue enamel finish.
The cabin has front and rear seats, rails, headrests, belts, door cards, a dashboard, analog dials, steering wheel, pedals, handbrake, gear lever, and parcel shelf.
Both assets retain the wheelbase and origin used by the tested four-contact suspension.

The exterior glTF contains 7 meshes, 7 materials, 6,060 triangles, three 512 x 512 textures, and 685,676 bytes.
The cabin glTF contains 8 meshes, 8 materials, 7,868 triangles, no textures, and 359,820 bytes.
The existing wheel assemblies remain separate and animated by the driving wrapper.

Front, rear, side, and close cabin views were inspected in Godot Compatibility at 1280 x 720 and 844 x 390.
The enter, drive, steer, brake, and exit route passed after the swap with the same measured suspension position and travel as the first drive.

The exterior still reads too angular at normal camera distance, and the transparent windscreen shows visible striping in the close view.
The cabin controls are modeled but static, and the driving camera does not enter the cabin.
The doors and hatch need separate pivots and working collision, and the car has not yet passed an impact recovery test.
The body and cabin need another proportion, finish, and lighting pass before they meet the catalog's final asset standard.
