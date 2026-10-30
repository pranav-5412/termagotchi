"""Shadow Ninja: charcoal ninja that throws a shuriken, then vanishes in a smoke bomb."""

import math
from dataclasses import replace

from termagotchi.pets.biped import (
    ARM_PIVOT, ARM_SLOTS, HEAD_SLOT, LEG_PIVOT, LEG_SLOTS, TORSO_SLOT, base_pose, neck_pivot,
)
from termagotchi.sprites import (
    FX_PALETTE, Part, PetSpec, Pose, blob, grid, lift, overlay, rect, sine, sleep_and_eat_parts,
)

PALETTE = {
    **FX_PALETTE,
    "o": "#0a0b10", "k": "#2b2f3a", "K": "#454b5c", "d": "#1a1d26", "g": "#6a7186",
    "f": "#e8c4a0", "R": "#d94a4a", "r": "#a83232", "e": "#0a0b10", "S": "#c9cfdd",
    "W": "#eef1f8",
}


def _head() -> tuple[str, ...]:
    hood = blob(16, 14, "k", "o", "K", "d")
    hood = overlay(hood, grid("ffffffffffff\nffffffffffff\nffffffffffff"), 2, 5)
    return overlay(hood, grid("RRRRRRRRRRRRRR"), 1, 3)


def _torso() -> tuple[str, ...]:
    torso = rect(12, 9, "k", "o", "K", "d")
    torso = overlay(torso, grid("g.......g\n.g.....g.\n..g...g.."), 1, 1)
    return overlay(torso, grid("gggggggggg\nrrrrrrrrrr"), 1, 6)


def _arm() -> tuple[str, ...]:
    return overlay(rect(4, 9, "k", "o", "K", "d"), grid("gggg\nffff"), 0, 6)


def _leg() -> tuple[str, ...]:
    return overlay(rect(5, 8, "k", "o", "K", "d"), grid("ggggg\nggggg\nkkkkk"), 0, 5)


def _smoke() -> tuple[str, ...]:
    base = tuple("." * 22 for _ in range(20))
    for x, y, w, h in ((0, 6, 11, 11), (11, 6, 11, 11), (5, 0, 12, 12), (4, 9, 14, 11)):
        base = overlay(base, blob(w, h, "S", "S", "W", "S"), x, y)
    return base


SHURIKEN = grid("""
...o...
..ogo..
.ogggo.
ogg.ggo
.ogggo.
..ogo..
...o...
""")
TAILS = grid("""
RR....
.RRR..
..RRRR
""")
EYES = grid("""
oo....oo
ee....ee
ee....ee
""")
EYES_CLOSED = grid("""
........
oo....oo
........
""")

hx, hy = HEAD_SLOT
ZZZ, BOWL = sleep_and_eat_parts(27, 1, 25, 27)

PARTS = (
    Part("scarf", 1, 16, blob(11, 4, "g", "o", "g", "d"), pivot=(10, 2), z=0),
    Part("leg_l", *LEG_SLOTS[0], _leg(), pivot=LEG_PIVOT, z=1),
    Part("leg_r", *LEG_SLOTS[1], _leg(), pivot=LEG_PIVOT, z=1),
    Part("torso", *TORSO_SLOT, _torso(), z=2),
    Part("arm_l", *ARM_SLOTS[0], _arm(), pivot=ARM_PIVOT, z=3),
    Part("arm_r", *ARM_SLOTS[1], _arm(), pivot=ARM_PIVOT, z=3),
    Part("tails", 2, 7, TAILS, pivot=neck_pivot(2, 7), z=3),
    Part("head", hx, hy, _head(), pivot=neck_pivot(hx, hy), z=4),
    Part("eyes", 12, 8, EYES, pivot=neck_pivot(12, 8), z=5),
    Part("eyes_closed", 12, 8, EYES_CLOSED, pivot=neck_pivot(12, 8), z=5),
    Part("shuriken", 23, 2, SHURIKEN, pivot=(3.5, 3.5), z=6),
    Part("smoke", 5, 12, _smoke(), pivot=(11, 10), z=7),
    ZZZ,
    BOWL,
)
HEAD_EXTRA = ("tails",)
NINJA = ("scarf", "leg_l", "leg_r", "torso", "arm_l", "arm_r", "tails", "head", "eyes", "eyes_closed")


def _alpha(poses: dict[str, Pose], value: float) -> None:
    """Set the same opacity on every part of the ninja."""
    for name in NINJA:
        poses[name] = replace(poses.get(name, Pose()), alpha=value)


def pose(state: str, t: float) -> dict[str, Pose]:
    poses = base_pose(state, t, HEAD_EXTRA, ("scarf",), blink_every=4.4)
    poses["shuriken"] = Pose(visible=False)
    poses["smoke"] = Pose(visible=False)
    flutter = sine(t, 0.9, 8)
    poses["tails"] = replace(poses["tails"], angle=poses["tails"].angle + flutter)
    poses["scarf"] = Pose(angle=sine(t, 1.1, 8) - (14 if state == "walk" else 0),
                          dy=poses.get("torso", Pose()).dy)
    if state == "special":
        p = (t % 3.6) / 3.6
        if p < 0.2:  # crouch, shuriken spinning over the raised hand
            k = p / 0.2
            poses["arm_r"] = Pose(angle=-150 * k, dy=1)
            poses["torso"] = Pose(sy=0.9, dy=1.5)
            lift(poses, ("head", "eyes", "eyes_closed", "tails", "scarf"), dy=1.5)
            poses["shuriken"] = Pose(visible=k > 0.3, angle=t * 900, dy=-1 + 2 * (1 - k))
        elif p < 0.35:  # throw: the star flies out, arm snaps forward
            k = (p - 0.2) / 0.15
            poses["arm_r"] = Pose(angle=-150 + 120 * k)
            poses["shuriken"] = Pose(visible=k < 0.95, dx=1 + 5 * k, dy=-1 - 5 * math.sin(math.pi * k),
                                     angle=t * 1200, alpha=1 - 0.4 * k)
        elif p < 0.45:  # smoke bomb: puff grows as the ninja fades
            k = (p - 0.35) / 0.1
            poses["smoke"] = Pose(visible=True, sx=0.3 + 0.7 * k, sy=0.3 + 0.7 * k)
            _alpha(poses, max(0.0, 1 - k * 1.3))
        elif p < 0.65:  # hidden while the smoke thins out
            k = (p - 0.45) / 0.2
            poses["smoke"] = Pose(visible=True, sx=1.0 + 0.1 * k, sy=1.0 + 0.2 * k, alpha=1 - k, dy=-2 * k)
            _alpha(poses, 0.0)
        elif p < 0.8:  # reappear arms crossed
            k = (p - 0.65) / 0.15
            poses["arm_l"] = Pose(angle=55 * k, dy=-1 * k)
            poses["arm_r"] = Pose(angle=-55 * k, dy=-1 * k)
            _alpha(poses, k)
    return poses


SPEC = PetSpec(
    key="shadow_ninja",
    palette=PALETTE,
    parts=PARTS,
    pose=pose,
    move="scurry",
    speed=46,
    special_name="smoke bomb",
)
