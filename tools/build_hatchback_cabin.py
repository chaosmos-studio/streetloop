"""Build the Tide hatchback's visible seats, controls, and interior hardware."""

import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
from car_geometry import box, cylinder, ellipsoid, export_collection, material, panel, tube


PROJECT = Path(__file__).resolve().parents[1]
NAME = "A138_tide_hatchback_cabin"
COLLECTION = "A138 Tide hatchback cabin"


def front_seat(name, x, collection, fabric, bolster, stitch, metal):
    box(f"{name} seat rail left", (x - 0.175, 0.04, 0.68), (0.028, 0.48, 0.06), metal, collection, 0.009)
    box(f"{name} seat rail right", (x + 0.175, 0.04, 0.68), (0.028, 0.48, 0.06), metal, collection, 0.009)
    box(f"{name} lower cushion", (x, 0.05, 0.8), (0.43, 0.51, 0.16), fabric, collection, 0.075)
    box(f"{name} cushion inlay", (x, 0.075, 0.884), (0.32, 0.36, 0.02), bolster, collection, 0.018)
    box(f"{name} backrest", (x, -0.235, 1.14), (0.43, 0.15, 0.64), fabric, collection, 0.073)
    box(f"{name} backrest inlay", (x, -0.152, 1.16), (0.31, 0.016, 0.44), bolster, collection, 0.018)
    box(f"{name} headrest", (x, -0.22, 1.56), (0.26, 0.16, 0.19), fabric, collection, 0.061)
    for offset in (-0.145, 0.145):
        cylinder(f"{name} headrest post {offset}", (x + offset * 0.4, -0.235, 1.435), 0.008, 0.18, metal, collection, 10)
    for offset in (-0.135, 0.135):
        tube(f"{name} seat piping {offset}", [(x + offset, 0.28, 0.84), (x + offset, 0.08, 0.88), (x + offset, -0.14, 0.84)], 0.006, stitch, collection)
    tube(f"{name} backrest piping", [(x - 0.17, -0.141, 0.87), (x - 0.17, -0.141, 1.38), (x + 0.17, -0.141, 1.38), (x + 0.17, -0.141, 0.87)], 0.005, stitch, collection)


def dashboard(collection, polymer, rubber, metal, instrument, signal):
    box("Dashboard crash pad", (0, 0.845, 1.05), (1.42, 0.31, 0.2), polymer, collection, 0.075)
    box("Dashboard lower fascia", (0, 0.79, 0.85), (1.46, 0.19, 0.21), polymer, collection, 0.035)
    box("Instrument binnacle", (-0.4, 0.662, 1.14), (0.44, 0.07, 0.23), rubber, collection, 0.035)
    for x in (-0.49, -0.31):
        cylinder(f"Analog dial bezel {x}", (x, 0.618, 1.155), 0.077, 0.012, metal, collection, 32, rotation=(math.pi / 2, 0, 0))
        cylinder(f"Analog dial face {x}", (x, 0.609, 1.155), 0.062, 0.013, instrument, collection, 32, rotation=(math.pi / 2, 0, 0))
        tube(f"Analog dial needle {x}", [(x, 0.601, 1.155), (x + 0.032, 0.601, 1.19)], 0.0035, signal, collection)
    box("Center console surround", (0.02, 0.659, 1.055), (0.3, 0.025, 0.25), rubber, collection, 0.023)
    box("Original small radio face", (0.02, 0.636, 1.1), (0.23, 0.01, 0.078), instrument, collection, 0.006)
    for x in (-0.087, 0.126):
        cylinder(f"Radio dial {x}", (x, 0.624, 1.1), 0.016, 0.013, metal, collection, 16, rotation=(math.pi / 2, 0, 0))
    for x in (-0.44, 0.4):
        box(f"Dash vent {x}", (x, 0.668, 1.035), (0.22, 0.012, 0.09), rubber, collection, 0.01)
        for row in range(3):
            box(f"Dash vent vane {x} {row}", (x, 0.658, 1.01 + row * 0.026), (0.18, 0.009, 0.006), metal, collection, 0.002)
    box("Passenger glovebox seam", (0.41, 0.664, 0.879), (0.39, 0.008, 0.009), rubber, collection, 0.003)
    box("Transmission tunnel", (0, 0.12, 0.72), (0.22, 1.33, 0.16), polymer, collection, 0.05)
    cylinder("Gear lever shaft", (0.015, 0.39, 0.85), 0.012, 0.2, metal, collection, 12)
    ellipsoid("Gear lever grip", (0.015, 0.39, 0.955), (0.065, 0.07, 0.1), rubber, collection, 16, 10)
    box("Handbrake boot", (0.01, -0.05, 0.82), (0.09, 0.22, 0.064), rubber, collection, 0.023)
    tube("Handbrake lever", [(0.01, -0.15, 0.83), (0.01, 0.03, 0.89)], 0.017, metal, collection)
    box("Accelerator pedal", (-0.33, 0.77, 0.59), (0.075, 0.018, 0.16), rubber, collection, 0.011)
    box("Brake pedal", (-0.51, 0.76, 0.62), (0.13, 0.018, 0.085), rubber, collection, 0.008)
    box("Clutch pedal", (-0.66, 0.76, 0.62), (0.12, 0.018, 0.085), rubber, collection, 0.008)


def steering(collection, rubber, metal, stitch):
    cylinder("Steering column", (-0.4, 0.62, 0.94), 0.04, 0.31, rubber, collection, 18, rotation=(math.pi / 2, 0, 0))
    points = []
    for index in range(49):
        angle = math.tau * index / 48
        points.append((-0.4 + 0.19 * math.cos(angle), 0.45, 1.1 + 0.19 * math.sin(angle)))
    tube("Textured steering wheel rim", points, 0.02, rubber, collection, True)
    cylinder("Steering wheel center", (-0.4, 0.45, 1.1), 0.07, 0.035, rubber, collection, 24, rotation=(math.pi / 2, 0, 0))
    for angle in (math.pi * 0.5, math.pi * 1.17, math.pi * 1.83):
        end = (-0.4 + 0.175 * math.cos(angle), 0.45, 1.1 + 0.175 * math.sin(angle))
        tube(f"Steering wheel spoke {angle:.2f}", [(-0.4, 0.45, 1.1), end], 0.012, metal, collection)
    tube("Steering wheel top stitch", [(-0.41, 0.426, 1.289), (-0.4, 0.426, 1.29), (-0.39, 0.426, 1.289)], 0.002, stitch, collection)


def rear_cabin(collection, fabric, bolster, polymer, rubber, metal, stitch):
    box("Rear bench cushion", (0, -0.82, 0.78), (1.37, 0.52, 0.18), fabric, collection, 0.073)
    box("Rear bench backrest", (0, -1.12, 1.08), (1.35, 0.17, 0.62), fabric, collection, 0.066)
    for x in (-0.44, 0.44):
        box(f"Rear headrest {x}", (x, -1.12, 1.45), (0.25, 0.17, 0.15), fabric, collection, 0.047)
    for x in (-0.24, 0.24):
        tube(f"Rear seat division {x}", [(x, -1.025, 0.85), (x, -1.025, 1.34)], 0.005, stitch, collection)
    box("Cabin carpet", (0, -0.1, 0.62), (1.51, 2.53, 0.018), rubber, collection, 0.005)
    for side in (-1, 1):
        x = side
        box(f"Door card front {side}", (x * 0.737, 0.12, 0.97), (0.036, 1.01, 0.37), polymer, collection, 0.027)
        box(f"Door card rear {side}", (x * 0.737, -0.93, 0.97), (0.036, 0.9, 0.37), polymer, collection, 0.027)
        box(f"Door pull front {side}", (x * 0.709, 0.12, 1.05), (0.025, 0.22, 0.045), metal, collection, 0.012)
        box(f"Door pull rear {side}", (x * 0.709, -0.92, 1.05), (0.025, 0.2, 0.045), metal, collection, 0.012)
        tube(f"Front seat belt {side}", [(x * 0.7, -0.28, 1.57), (x * 0.57, -0.25, 1.21), (x * 0.33, 0.04, 0.79)], 0.012, rubber, collection)
        box(f"Seat belt buckle {side}", (x * 0.21, -0.02, 0.85), (0.045, 0.035, 0.075), metal, collection, 0.009)
    box("Cabin rear parcel shelf", (0, -1.51, 1.065), (1.37, 0.48, 0.055), polymer, collection, 0.019)
    box("Interior rearview mirror", (0, 0.73, 1.56), (0.25, 0.045, 0.07), metal, collection, 0.016)


def build():
    previous = bpy.data.collections.get(COLLECTION)
    if previous:
        for obj in list(previous.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(previous)
    collection = bpy.data.collections.new(COLLECTION)
    bpy.context.scene.collection.children.link(collection)
    fabric = material("SL Tide woven grey seat cloth", (0.22, 0.26, 0.255), 0.88)
    bolster = material("SL Tide blue seat inlay", (0.105, 0.21, 0.23), 0.84)
    polymer = material("SL Tide graphite cabin polymer", (0.12, 0.145, 0.145), 0.79)
    rubber = material("SL Tide deep rubber", (0.035, 0.04, 0.041), 0.94)
    metal = material("SL Tide interior satin metal", (0.42, 0.45, 0.44), 0.48, 0.69)
    instrument = material("SL Tide instrument face", (0.08, 0.17, 0.18), 0.44)
    signal = material("SL Tide instrument amber", (0.75, 0.35, 0.1), 0.42)
    stitch = material("SL Tide ivory seat piping", (0.51, 0.54, 0.48), 0.86)
    for name, x in (("Driver", -0.39), ("Passenger", 0.39)):
        front_seat(name, x, collection, fabric, bolster, stitch, metal)
    dashboard(collection, polymer, rubber, metal, instrument, signal)
    steering(collection, rubber, metal, stitch)
    rear_cabin(collection, fabric, bolster, polymer, rubber, metal, stitch)
    return export_collection(NAME, collection, PROJECT)


if __name__ == "__main__":
    print(build())
