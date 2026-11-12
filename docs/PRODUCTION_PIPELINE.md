# LIFE production pipeline

The project advances through small playable slices.
One slice joins a place, an action, a consequence, and a review in the actual game.

## Source of truth

| File | Purpose | Update when |
|---|---|---|
| `docs/LIFE_VISION.md` | Player promise and long-term scope | The game direction changes |
| `PLAN.md` | Current playable milestones | A gate passes or the next gate changes |
| `docs/MAP_INDEX.md` | Area IDs and dependencies | An area is planned, started, or accepted |
| `docs/areas/<ID>_<name>.md` | One area's routes, interiors, people, jobs, and budget | Work in that area changes |
| `ASSET_CATALOG.md` | One row per authored asset | An asset begins or passes acceptance |
| `docs/decisions/` | Stable technical and design choices | A choice with future impact is made |
| `docs/reviews/` and `art/review/` | Measured play and art evidence | A slice is tested |
| `docs/NOW.md` | Current branch, working set, next action, and blockers | Every work session ends |

## Work units

An asset has its own editable source, export, scale and pivot, material list, collision plan, game-camera review, cost, and acceptance result.
A gameplay system has a decision record, a small interface, an in-world use case, a player route, and a regression check.
A district starts with travel and one usable interior before its asset roster grows.
One issue or checklist line represents one testable result, not an entire career or neighborhood.

## Gates

1. Make a representative asset and movement scene for the new visual or mechanical rule.
2. Inspect the source from all sides and inspect the export in Godot 4.7 GL Compatibility.
3. Play the relevant route with keyboard, controller, and touch where they apply.
4. Measure draw calls, triangles, texture memory, frame time, and build size on target hardware.
5. Record the result and keep a catalog or milestone box open when a quality condition fails.
6. Commit each logical change with the workspace's one-line subject rule.
7. Update the public build after the slice passes its gate.

## Simulation boundaries

The visible area runs high-detail physics and animation.
Offscreen residents and businesses run a lower-frequency schedule and transaction model.
Offline catch-up uses elapsed time, capped obligations, and a reviewable event log.
The cap and recovery rules must be playtested before an offline economy is enabled.
The save schema will version residents, households, assets, debts, ownership, and events separately, with migration tests before release.

## Context handoff

Start from `docs/NOW.md`, then read only the active area file, relevant system decision, asset rows, and recent review.
At the end of a session, record the tested commit, active branch, exact next work, measured result, and any unresolved risk.
Keep exploratory notes out of permanent design documents until they survive a playtest.
