# Workshop driving trial decisions

| Decision | Choice | Why | Revisit when |
|---|---|---|---|
| Scope | One authored trial in the harbor block | It proves a complete activity before a reusable mission system exists | A second job needs shared rules |
| World | Single player, 3D, GDScript | This matches Streetloop's running project | Multiplayer is planned |
| State | A small enum owned by one trial node | The route has few states and no independent transitions | Jobs need branching or persistence |
| Feedback | A compact objective HUD and the existing interaction prompt | The player needs a clear next action at street scale | A map and navigation system exist |

## Assumptions

- The mechanic offers a repeatable car trial with south and north road turns and a return to the shop.
- Progress lasts for the current session.
- The trial uses the existing hatchback and does not award money yet.
