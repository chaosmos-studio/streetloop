# H00 Harbor block

## Current playable route

Enter the repair shop, inspect its manual and terminal, ask the mechanic for a driving trial, drive to both road ends, return the car, and report completion.
This is the first continuous place-action-consequence slice for LIFE.

## Existing assets and spaces

The current asset catalog includes the road, sidewalk, repair shop, lamp, player, mechanic, car, door, workbench, fan, manual, and terminal.
The shop has a public doorway and working interior interactions.
The surrounding street is a prototype strip with open edges and no junction or neighboring homes.

## Next work in order

- [ ] Replace A001 with a proportioned, deforming human character and validated locomotion.
- [ ] Give A085 the same rig standard with distinct workwear and a usable work gesture.
- [ ] Add a traversable junction and physically legible north and south destinations.
- [ ] Furnish the shop with reachable drawers, tools, storage, sink, and a service bay.
- [ ] Add a second resident and a delivery activity with a visible handoff.
- [ ] Measure the area at desktop and phone resolutions during driving and on-foot play.
- [ ] Walk and drive the full route without debug input and record failures in `docs/reviews/`.

## Acceptance

The area passes when players can finish the route without instructions, identify the mechanic and destinations, park and exit reliably, inspect and use the shop, and see stable foot and wheel contact.
The art must read at gameplay distance and survive close inspection inside the shop.
The performance budget is set from measured target-device runs, not an assumed asset count.
