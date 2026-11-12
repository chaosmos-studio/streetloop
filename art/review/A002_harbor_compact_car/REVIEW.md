# A002 Harbor compact car

The first asset pass is a four-door harbor utility car with a 4.2 m body length, 1.82 m width, and 1.72 m overall height.
It has a faded petrol-blue painted body, separate tire and rim meshes, visible doors, lamps, bumpers, mirrors, and a simple cabin.
The editable Blender collection contains 74 objects and eight materials.
The exported glTF contains 74 mesh nodes and no unrelated scene objects.
The current export is 416 KiB.

The silhouette was inspected in the live Blender viewport from the front quarter.
The cabin roof and nose are deliberately broad so the car reads from a third-person camera.
This is the first-pass art for steering and contact tests, and the proportions and cabin glazing need review in motion inside Godot.
The body, wheels, and doors are separate editable objects, but a gameplay wrapper and wheel animation are pending.
The collision plan is one vehicle body box with narrow wheel contact handled by the controller, with entry points beside the front doors.
The source collection pivot is at ground level at the center of the wheelbase and local +Y is the front.
