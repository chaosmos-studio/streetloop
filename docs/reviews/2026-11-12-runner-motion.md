# Harbor runner movement review

The on-foot walk and sprint targets are now 1.7 m/s and 3.8 m/s.
The existing articulated model uses a speed-linked gait with separate stance and swing phases, knee lift, counter-moving arms, a small pelvis weight shift, and different rising and falling poses.
The gait advances from actual horizontal travel speed, so starting, stopping, and sprinting change its timing.

In the running harbor block, the runner traveled 1.286 m over 50 walking physics ticks including acceleration, then 2.203 m over 38 sprinting ticks including the speed change.
The sampled jump frame was 0.894 m above the sidewalk.
Idle, two walking phases, sprint, and jump were inspected at 1280 x 720.
The door, fan, manual, terminal, and car routes still passed after the movement change.

The current model is an articulated first pass without a deforming skeleton or foot IK.
The sampled frames show clearer leg separation and weight shift, but a complete motion review and uneven-ground foot contact remain open.
