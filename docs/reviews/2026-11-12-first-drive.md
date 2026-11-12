# First Tide hatchback drive

The existing A002 hatchback body and four A141 wheel assemblies now have a Godot wrapper. A 1,220 kg rigid body receives force through four suspension contacts. Each wheel steers or spins independently, while its brake caliper stays fixed to the steering mount.

The player entered by focusing the driver door, exited while parked, re-entered, drove, steered, braked, and exited again. The drive used the actual harbor road and a chase camera. The instrument dial was inspected at 1280 x 720 and 844 x 390.

After two seconds at rest, the body origin was 0.822 m high. The four suspension lengths were 0.227, 0.227, 0.231, and 0.231 m. After three seconds of throttle, the car had traveled 12.35 m and reached 24.7 km/h. A 65-frame left steer moved it 3.36 m sideways by the next sample. Braking brought it to about 0.06 km/h. These are prototype measurements from one route, not final handling targets.

The rendered review shows that the car remains too boxy, its cabin is too dark to inspect, and the road is sparse. The body and wheel sources need a closer design pass. Engine and tire audio, wheel-ground collision recovery, tuned steering, headlamps, door animation, and a smooth camera handoff remain open. Desktop input was exercised. Gamepad mappings are present but untested, and touch driving controls are still needed for an Android build.
