# Streetloop plan

The first goal is a city block that is enjoyable to cross on foot and by car.
Each milestone ends with a playable build and a short review of movement, visual clarity, and measured cost.

## M0: A convincing block

- [x] Record the initial scope, scale, engine, and world assumptions.
- [x] Create the public repository and establish the Godot 4.7 project.
  Skills: `godot-prompter:godot-project-setup`, `godot-prompter:rendering-pipeline`.
- [ ] Make an editable material and measurement reference in Blender.
  Skills: `godot-prompter:assets-pipeline`, `godot-prompter:3d-essentials`.
- [ ] Build and review the road, sidewalk, walk-in repair shop, streetlamp, and compact car as separate catalog assets.
  Skills: `godot-prompter:assets-pipeline`, `godot-prompter:3d-essentials`.
- [ ] Complete one explorable shop interior with usable doors, reachable objects, and collision that matches every visible surface.
  Skills: `godot-prompter:scene-organization`, `godot-prompter:physics-system`, `godot-prompter:assets-pipeline`.
- [ ] Make the repair shop a realistic material and interaction benchmark with authored floor finishes, ceiling detail, a switched fan, a readable service manual, and a usable computer.
  Skills: `godot-prompter:assets-pipeline`, `godot-prompter:animation-system`, `godot-prompter:input-handling`, `godot-prompter:godot-ui`.
- [ ] Assemble the first harbor block from asset scenes with independent collisions and interaction points.
  Skills: `godot-prompter:scene-organization`, `godot-prompter:physics-system`, `godot-prompter:3d-essentials`.
- [ ] Add third-person on-foot movement with stable camera and gamepad input.
  Skills: `godot-prompter:player-controller`, `godot-prompter:input-handling`, `godot-prompter:camera-system`, `godot-prompter:animation-system`.
- [ ] Add one enterable compact car with a four-contact rigid-body suspension, steering, braking, exit clearance, and a readable camera transition.
  Skills: `godot-prompter:physics-system`, `godot-prompter:input-handling`, `godot-prompter:camera-system`, `godot-prompter:state-machine`.
- [ ] Test the car from front, rear, both sides, above, and inside while moving, braking, colliding, and opening each usable part.
  Skills: `godot-prompter:godot-testing`, `godot-prompter:animation-system`.
- [ ] Play a continuous route: walk to the car, enter, drive around the block, park, exit, and walk back.
  Skills: `godot-prompter:godot-testing`, `godot-prompter:godot-debugging`.
- [ ] Capture real game footage and profile the block at desktop and phone resolutions.
  Skills: `godot-prompter:godot-optimization`, `godot-prompter:web-export`, `godot-prompter:mobile-development`.

M0 passes when a player can complete that route without instructions, enter and inspect the shop, the vehicle can recover from a wall impact, the character never clips through the curb or furnishings, and the imported art reads at the actual camera distance.
Record vehicle acceleration, braking distance, minimum turning circle, suspension travel, and collision recovery during playtests.
Record frame time, draw calls, mesh triangles, texture memory, and compressed download size before setting hard budgets.

## M1: A living street

- [ ] Add pedestrian roles with sidewalk routes, idle stops, avoidance, and reactions to traffic.
  Skills: `godot-prompter:ai-navigation`, `godot-prompter:state-machine`, `godot-prompter:animation-system`.
- [ ] Add traffic lanes, signals, parked cars, and an emergency stop response.
  Skills: `godot-prompter:ai-navigation`, `godot-prompter:physics-system`.
- [ ] Add storefront interactions, doors, ambient voices, traffic audio, and weather cues.
  Skills: `godot-prompter:audio-system`, `godot-prompter:state-machine`.
- [ ] Add one short delivery job and one timed chase with distinct routes through the block.
  Skills: `godot-prompter:resource-pattern`, `godot-prompter:state-machine`, `godot-prompter:hud-system`.
- [ ] Test pedestrian, vehicle, and player contact together at normal play speed.
  Skills: `godot-prompter:godot-testing`, `godot-prompter:godot-optimization`.

## M2: Two connected districts

- [ ] Add the market quarter with different streets, density, landmarks, and jobs.
  Skills: `godot-prompter:scene-organization`, `godot-prompter:3d-essentials`.
- [ ] Stream district chunks around the player while preserving nearby simulation state.
  Skills: `godot-prompter:multithreading`, `godot-prompter:godot-optimization`, `godot-prompter:save-load`.
- [ ] Add garages, vehicle condition, money, inventory, and save/load.
  Skills: `godot-prompter:resource-pattern`, `godot-prompter:inventory-system`, `godot-prompter:save-load`.
- [ ] Add a readable heat and pursuit system tied to observed player actions.
  Skills: `godot-prompter:ai-navigation`, `godot-prompter:state-machine`, `godot-prompter:event-bus`.

## M3: City-wide game

- [ ] Expand districts only after each new area has a distinct traversal pattern, landmark, activity, and ambient identity.
- [ ] Build an authored mission chain, repeatable jobs, and free-roam events.
- [ ] Add day and night, rain, population density changes, and district-specific audio.
- [ ] Add controller remapping, accessibility options, graphics presets, and mobile touch controls.
- [ ] Test full-city travel, save migration, long sessions, and worst-case traffic density.

## Asset production rule

Every row in `ASSET_CATALOG.md` is a separate task.
Complete its model, materials, UVs, pivot, collision plan, source `.blend`, exported `.glb`, turntable, in-game screenshot, and measured cost before checking it off.
For buildings, include a traversable interior, doors with clearance, reachable furnishings, close-range materials, and purposeful object interactions in the asset specification.
For vehicles, include exterior and cabin views, separate mechanical assemblies, plausible dimensions and mass, and measured motion and contact behavior.
Shared modular pieces may repeat in the city, while hero buildings, vehicles, characters, and landmarks receive their own designs and source work.
The catalog can grow past a thousand items, but item count does not substitute for variation in architecture, gameplay, or motion.

## Review cadence

After each asset batch, walk and drive through the district from the gameplay camera.
Check silhouette, contact, navigation, collision, performance, and how the asset behaves beside moving traffic and pedestrians.
Keep the catalog, milestone checkboxes, and performance measurements current in separate one-line commits.
