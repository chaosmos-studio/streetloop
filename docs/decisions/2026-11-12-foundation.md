# Streetloop foundation decisions

| Decision | Choice | Why | Revisit when |
| --- | --- | --- | --- |
| Scope | Grow a full game through playable district slices | A city needs tested movement, driving, and interaction before asset volume | The first block is played end to end |
| Dimension | Third-person 3D | Walking and driving need shared streets and readable spatial contact | Camera tests show a clearer alternative |
| Language | Statically typed GDScript | It matches the workspace and keeps iteration fast | A measured subsystem requires native code |
| Authority | Local single-player | The requested sandbox does not depend on other players | Multiplayer becomes a defined feature |
| Renderer | Godot 4.7 GL Compatibility | One material and light strategy can be checked in web previews and on modest devices | Target hardware measurements justify another path |
| World | Original fictional coastal port city | It gives a distinct visual vocabulary without copying a real city or another game | Playtests reveal a stronger setting |
| World structure | Separate district scenes on a shared meter grid | Roads and interactions stay independent and later streaming stays possible | The first district performance is measured |
| Asset source | One editable Blender source and one reviewed Godot export per catalog item | Each item can be revised, inspected, and tracked alone | A proven shared source is better for a related set |

## Assumptions to validate

- The first district is a compact harbor block with one street loop, a corner shop, a sidewalk, and a vehicle spawn.
- A standing adult reference is 1.75 m tall, a lane is 3.5 m wide, and a sidewalk is 2 m wide.
- The first character is a city runner with no prescribed story or criminal role.
- The first playable loop tests on-foot movement, entering a compact car, driving, exiting, and returning to the start.
- Missions, traffic, pedestrians, pursuit, economy, and persistence join only after that loop feels good.
