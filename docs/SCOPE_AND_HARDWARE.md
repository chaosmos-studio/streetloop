# LIFE scope and hardware estimates

These are planning ranges, not measured final build sizes or release commitments.
They assume original, detailed 3D assets, enterable hero buildings, authored careers, voiced or designed audio, multiple NPC schedules, and district streaming.

| Scope | Installed game | Editable source and build workspace | Team and time planning range |
|---|---:|---:|---|
| One polished neighborhood | 1-5 GiB | 50-250 GiB | 1-3 years for a small experienced team |
| Several connected districts | 8-30 GiB | 250 GiB-1 TiB | 3-6 years for a multidisciplinary team |
| Broad LIFE vision | 30-100+ GiB | 1-3+ TiB | 5-10+ years and dozens of specialists |

The upper range expands quickly if every home interior, vehicle, career activity, language, and cinematic is unique.
Streaming and shared materials reduce installed size, while unique texture sets, voice audio, animations, and retained source versions increase it.
Mobile and browser releases need a smaller content set or downloadable district packs.
The current Streetloop checkout is about 166 MiB, and its exported Web pack and engine total about 47 MiB before hosting compression.

## Current development machine

On 2026-11-13 the machine reported an Intel Core i5-12500H, Intel Iris Xe graphics, 15 GiB usable RAM, and 65 GiB free on the workspace volume.
This machine can build the first block and review small assets in Godot 4.7 and Blender 5.2.2.
Memory and storage are already tight for a realistic city asset library and parallel Blender, Godot, and texture work.

## Practical development hardware

| Work | RAM | Graphics memory | Fast local storage |
|---|---:|---:|---:|
| First playable district | 32 GiB | 8 GiB dedicated | 1 TiB SSD with at least 300 GiB free |
| Detailed city production | 64 GiB | 12-16 GiB dedicated | 2 TiB NVMe plus separate backup |
| Large asset baking and heavy rendering | 64-128 GiB | 16-24 GiB dedicated | 2-4 TiB NVMe plus backup or shared storage |

An 8-core modern CPU is a useful floor for concurrent editor, build, and content work.
The GPU and memory recommendations are project estimates, not Blender or Godot minimum requirements.
Blender lists 32 GB RAM and 8 GB VRAM as recommended hardware, while its minimum is 8 GB RAM and 2 GB VRAM.
Godot states that real project requirements depend on content, renderer, and resolution.

## Sources and recheck

- [Blender hardware requirements](https://www.blender.org/download/requirements/).
- [Godot 4.7 system requirements](https://docs.godotengine.org/en/4.7/about/system_requirements.html).
- [Godot 3D performance guidance](https://docs.godotengine.org/en/latest/tutorials/performance/optimizing_3d_performance.html).

Re-estimate each range after a representative home, street, vehicle, character set, and job have measured source, export, memory, and frame costs.
