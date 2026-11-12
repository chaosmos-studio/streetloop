# First city block scene design

The first playable route begins at the harbor sidewalk, passes the repair shop, reaches a parked compact car, circles the block, and ends at the starting curb.

## Scene tree

```text
Main (Node3D)
├── HarborBlock (Node3D)
│   ├── Roads (Node3D)
│   ├── Sidewalks (Node3D)
│   ├── Buildings (Node3D)
│   └── StreetFurniture (Node3D)
├── Player (CharacterBody3D)
├── Car (RigidBody3D)
├── FollowCamera (Camera3D)
├── Sun (DirectionalLight3D)
└── Atmosphere (WorldEnvironment)
```

The block places reusable road, sidewalk, building, and prop scenes on a meter grid.
Each wrapper scene owns its visual glTF instance and simple gameplay collision.
The source Blender collection and exported glTF remain separate from Godot collision and behavior.

## Player and vehicle

The player owns on-foot acceleration, gravity, collision, and an interaction request signal.
The car owns steering, throttle, braking, four suspension contacts, body collision, and seat positions.
The main scene owns the transition between walking and driving so neither actor depends on the other's scene tree.
The current actor drives the camera target and continuous input.
The inactive actor remains in the world without processing movement input.

## Camera and input

Named Input Map actions cover movement, camera look, interact, brake, and pause.
Continuous movement is read during physics ticks and discrete interaction is received from unhandled input.
The camera follows an interpolated actor transform and rotates independently of the physics body.
The camera arm must avoid clipping through buildings and the car.

## Collision and scale

One Godot unit is one meter.
The road is 7 m wide, with a 2 m sidewalk on each side.
Collision bodies use primitive shapes with dimensions set on the shape resource.
Road and sidewalk collision follow the visible height so tires and feet meet their surfaces without a step.
The repair shop shell, doors, furnishings, and fixtures use separate collision and interaction nodes so the space can be entered and inspected.

## Review route

Walk the entire sidewalk and confirm curb and shop contacts.
Enter the repair shop, inspect its fixtures, leave through the doorway, enter the compact car, drive a full loop, brake, exit beside it, and return on foot.
Inspect the road, shop, and moving actors from the actual follow camera at 1280 x 720 and a wide phone crop.
Record frame time, draw calls, triangles, material count, and build size after the route works.
