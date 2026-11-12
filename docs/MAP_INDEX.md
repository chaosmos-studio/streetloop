# LIFE area index

Each area has a fixed identifier, map bounds, one playable route, an interior roster, active work, resident behavior, and an acceptance review.
The coordinates below describe intended neighborhoods, not placed world geometry.
An area remains planned until its own file records measured bounds and a playable build.

| Area | Role | First distinctive activity | Required spaces | Status |
|---|---|---|---|---|
| H00 Harbor block | First playable street | Repair shop driving trial | Repair shop, road, parking | In prototype |
| H01 Home row | First daily-life loop | Morning preparation and rent | Starter home, grocery, bus stop | Planned |
| H02 Market quarter | Work and prices | Stock and sell goods | Market hall, food stall, storage | Planned |
| H03 Civic center | Education and services | Enroll and apply for work | School, clinic, bank, municipal office | Planned |
| H04 Dock yards | Logistics and industry | Load and deliver cargo | Warehouse, pier, garage | Planned |
| H05 Waterfront | Leisure and tourism | Guide or service visitors | Promenade, cafe, ferry landing | Planned |
| H06 Campus | Skill progression | Attend practical training | Classrooms, library, workshop | Planned |
| H07 Outer homes | Ownership and family | Maintain a purchased home | Several house types, park, local shops | Planned |

## Area file contract

Create `docs/areas/<ID>_<name>.md` before building an area.
The file records boundaries, elevation, street and pedestrian connections, enterable interiors, residents, jobs, asset IDs, dependencies, budgets, and an ordered acceptance checklist.
The world scene uses the same ID in its folder name, so a map task can be traced to source, export, scene, and review.
Each area has a playable route before adjoining scenery expands.

## H00 immediate route

The harbor block currently has two road segments, sidewalks, a walk-in repair shop, a car, lamps, and one mechanic.
Its next acceptance work is a human-quality runner, believable shop furnishing and materials, a road with a real junction, physical job landmarks, traffic behavior, and a recorded desktop and phone profile.
