"""Dragon: green dragon that flaps its wings and breathes fire."""

import math

from termagotchi.sprites import (
    FX_PALETTE, Part, PetSpec, Pose, blink, blob, fx_poses, grid, overlay, sine, sleep_and_eat_parts,
)

PALETTE = {
    **FX_PALETTE,
    "o": "#1c2b1a", "g": "#4cae5b", "l": "#7ed67e", "d": "#2f7d3e", "Y": "#f1e08a",
    "y": "#ffd83a", "e": "#111111", "r": "#c94a3a", "h": "#e8d9a8", "W": "#e0705a",
    "V": "#b84d3c", "F": "#ff7a1a", "G": "#ffe45c", "R": "#e8431a",
}

HEAD_PIVOT = (19.0, 15.0)  # where the neck meets the body


def _pv(x: int, y: int) -> tuple[float, float]:
    return HEAD_PIVOT[0] - x, HEAD_PIVOT[1] - y


def _wing(w: int, h: int) -> tuple[str, ...]:
    wing = blob(w, h, "W", "o", "W", "V")
    bones = tuple("".join("o" if x == w - 2 - y // 2 else "." for x in range(w)) for y in range(h - 2))
    return overlay(wing, bones, 0, 1)


def _leg(top: str) -> tuple[str, ...]:
    return grid(f"""
o{top}{top}{top}o
o{top}{top}{top}o
o{top}{top}{top}o
o{top}{top}{top}o
o{top}{top}{top}o
o{top}{top}{top}o
ohohh
ooooo
""")


BODY = overlay(blob(18, 13, "g", "o", "l", "d"), blob(11, 6, "Y", "Y", "Y", "Y"), 5, 7)
SPIKES = grid("""
..r...r...r...r..
.rrr.rrr.rrr.rrr.
""")
HORN = grid("""
.h.
.hh
hh.
h..
""")
EYES = grid("""
yy
ye
""")
EYES_CLOSED = grid("""
..
oo
""")
FIRE = overlay(blob(7, 10, "R", "R", "F", "R"), blob(3, 6, "G", "G", "G", "G"), 2, 3)

ZZZ, BOWL = sleep_and_eat_parts(27, 1, 26, 27)

PARTS = (
    Part("tail", 0, 18, overlay(blob(14, 7, "g", "o", "l", "d"), grid("rr"), 0, 3), pivot=(13, 3.5), z=0),
    Part("wing_far", 6, 4, _wing(11, 12), pivot=(9, 11), z=0),
    Part("far_back", 8, 22, _leg("d"), pivot=(2.5, 0), z=1),
    Part("far_front", 19, 22, _leg("d"), pivot=(2.5, 0), z=1),
    Part("body", 7, 14, BODY, z=2),
    Part("spikes", 8, 12, SPIKES, z=3),
    Part("wing_near", 10, 3, _wing(13, 13), pivot=(10, 12), z=3),
    Part("near_back", 10, 22, _leg("g"), pivot=(2.5, 0), z=3),
    Part("near_front", 21, 22, _leg("g"), pivot=(2.5, 0), z=3),
    Part("neck", 16, 11, blob(8, 10, "g", "o", "l", "d"), z=3),
    Part("horn_l", 19, 3, HORN, pivot=_pv(19, 3), z=4),
    Part("horn_r", 23, 3, HORN, pivot=_pv(23, 3), z=4),
    Part("head", 19, 6, blob(11, 9, "g", "o", "l", "d"), pivot=_pv(19, 6), z=5),
    Part("snout", 25, 10, overlay(blob(7, 5, "g", "o", "l", "d"), grid("e"), 5, 1), pivot=_pv(25, 10), z=6),
    Part("jaw", 25, 13, blob(6, 3, "d", "o", "g", "d"), pivot=_pv(25, 13), z=5),
    Part("eyes", 24, 9, EYES, pivot=_pv(24, 9), z=7),
    Part("eyes_closed", 24, 9, EYES_CLOSED, pivot=_pv(24, 9), z=7),
    Part("fire", 25, 0, FIRE, pivot=(1, 9.5), z=8),
    ZZZ,
    BOWL,
)
HEAD = ("head", "snout", "jaw", "horn_l", "horn_r", "eyes", "eyes_closed")
LEGS = ("near_front", "far_front", "near_back", "far_back")


def _head(t: float, asleep: bool = False, dy: float = 0.0, angle: float = 0.0, jaw: float = 0.0):
    shut = asleep or blink(t, 4.2)
    poses = {name: Pose(dy=dy, angle=angle) for name in HEAD}
    poses["jaw"] = Pose(dy=dy, angle=angle + jaw)
    poses["eyes"] = Pose(dy=dy, angle=angle, visible=not shut)
    poses["eyes_closed"] = Pose(dy=dy, angle=angle, visible=shut)
    return poses


def _wings(angle: float, lag: float = 0.0) -> dict[str, Pose]:
    return {"wing_near": Pose(angle=angle), "wing_far": Pose(angle=angle + lag)}


def pose(state: str, t: float) -> dict[str, Pose]:
    poses = fx_poses(state, t)
    poses["fire"] = Pose(visible=False)
    if state == "idle":
        poses.update(_head(t, dy=sine(t, 3.2, 0.4), angle=sine(t, 4.5, 3)))
        poses.update(_wings(sine(t, 2.6, 5) - 8, 4))
        poses["body"] = Pose(sy=1 + sine(t, 3.2, 0.02))
        poses["tail"] = Pose(angle=sine(t, 2.4, 8))
    elif state == "walk":
        swing = sine(t, 0.8, 22)
        for name, sign in (("near_front", 1), ("far_front", -1), ("near_back", -1), ("far_back", 1)):
            poses[name] = Pose(angle=sign * swing)
        bob = abs(sine(t, 0.8, 0.7)) - 0.4
        poses.update(_head(t, dy=bob, angle=sine(t, 0.8, 3)))
        poses.update(_wings(-10 + sine(t, 0.8, 8), 4))
        poses["body"] = Pose(dy=bob)
        poses["tail"] = Pose(angle=-6 + sine(t, 1.6, 7))
    elif state == "eat":
        poses.update(_head(t, dy=3, angle=16 + sine(t, 0.5, 3), jaw=sine(t, 0.5, 8) + 6))
        poses.update(_wings(-14, 3))
        poses["tail"] = Pose(angle=sine(t, 1.5, 9))
    elif state == "sleep":
        poses.update(_head(t, asleep=True, dy=4, angle=22))
        poses.update(_wings(-35, 2))
        poses["body"] = Pose(sy=0.95 + sine(t, 3.6, 0.015), dy=1)
        poses["tail"] = Pose(angle=18, dx=2)
    else:  # special: inhale, breathe fire upward, exhale
        p = (t % 3.4) / 3.4
        if p < 0.2:  # inhale: chest swells, wings rise
            k = p / 0.2
            poses.update(_head(t, angle=-8 * k))
            poses.update(_wings(-8 - 30 * k, 4))
            poses["body"] = Pose(sy=1 + 0.08 * k)
        elif p < 0.72:  # fire
            flicker = sine(t, 0.14, 0.15)
            poses.update(_head(t, angle=-28, jaw=15))
            poses.update(_wings(-30 + sine(t, 0.45, 22), 6))
            poses["body"] = Pose(sy=1.08, dx=-0.5)
            poses["tail"] = Pose(angle=sine(t, 0.5, 6))
            poses["fire"] = Pose(visible=True, angle=6, sy=1.05 + flicker, sx=1 + flicker)
        else:  # exhale
            k = (p - 0.72) / 0.28
            poses.update(_head(t, angle=-28 * (1 - k) + sine(t, 0.8, 2)))
            poses.update(_wings(-30 * (1 - k) - 8, 4))
            poses["body"] = Pose(sy=1.08 - 0.08 * k)
    return poses


SPEC = PetSpec(
    key="dragon",
    palette=PALETTE,
    parts=PARTS,
    pose=pose,
    move="walk",
    speed=26,
    special_name="fire breath",
)
