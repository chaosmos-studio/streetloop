# Character creator decisions

| Decision | Choice | Why | Revisit when |
| --- | --- | --- | --- |
| Scope | A durable creator inside the current playable neighborhood | The LIFE character will be reused across later districts | The life-stage system needs different bodies |
| Identity | Several original adult face and body bases | A palette swap alone does not create a distinct person | New identities are sculpted and rigged |
| Configuration | Identity and material colors first. Add hair style, facial hair, and outfit choices when fitted assets exist | Every choice must make a visible change | A new garment or groom is reviewed |
| Scene ownership | One controller with a replaceable character visual | Movement and interactions should behave identically for every identity | Body size changes collision or reach |
| Data | Authored definitions in project resources and one validated selection in `user://` JSON | Designers need editable options and the player needs a safe persistent choice | Save slots join the LIFE game |
| Preview | A live 3D preview inside a responsive Control overlay | Players need to inspect the face and outfit from different angles | A full creator room becomes useful |
| Motion | Shared skeleton and named clips for every identity | Character changes must not change control response | A measured locomotion system needs retargeting |

## Open / deferred

- Facial sculpt sliders, ancestry labels, age stages, tattoos, and jewellery are deferred until their own reviewed models and deformation checks exist.
- The first saved character is assumed to be one local profile.
- The first identity set is assumed to be adult and compatible with the current 1.77 m controller.
