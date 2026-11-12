# Touch controls review

The phone layout was inspected at 844 x 390 in the [walking capture](../../art/review/touch_controls_walk_mobile.png) and [driving capture](../../art/review/touch_controls_drive_mobile.png).
The movement stick is at the lower left, the action buttons are at the lower right, and the driving gauge moves to the upper left.
Camera drags use the open upper part of the screen.

The Godot check moved the runner 0.55 m with a virtual stick, turned the camera 0.12 rad, launched a jump at 5.1 m/s, held and released sprint and brake, and exited the car.
Door, manual, terminal, driving, and impact checks passed after the input change.

The checks simulate screen events and call the action touch handler in a phone-size viewport.
Direct play on a physical phone and browser remains to be checked.
