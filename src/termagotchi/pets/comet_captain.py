"""Captain Comet: visor-helmet space hero with an orange scarf who leaps in a comet trail."""

import math

from termagotchi.pets.biped import (
    ARM_PIVOT, ARM_SLOTS, HEAD_SLOT, LEG_PIVOT, LEG_SLOTS, TORSO_SLOT, base_pose, neck_pivot,
)
from termagotchi.sprites import (
    FX_PALETTE, Part, PetSpec, Pose, blob, grid, lift, overlay, rect, sine, sleep_and_eat_parts,
)

PALETTE = {
    **FX_PALETTE,
    "o": "#0b1f3a", "b": "#2f6fe0", "l": "#6fa3ff", "d": "#1c4aa8", "w": "#e9f0fb",
    "W": "#ffffff", "h": "#aebbd6", "V": "#17426b", "g": "#9ff2ff", "O": "#ff8a1f",
    "Y": "#ffd23a",
}


def _head() -> tuple[str, ...]:
    helmet = blob(16, 14, "w", "o", "W", "h")
    return overlay(helmet, blob(12, 7, "V", "o"), 2, 4)


def _torso() -> tuple[str, ...]:
    torso = rect(12, 9, "b", "o", "l", "d")
    torso = overlay(torso, grid("OOOOOOOOOO"), 1, 6)
    torso = overlay(torso, grid("YY"), 5, 6)
    return overlay(torso, grid(".YY.\nYOOY\n.YY."), 4, 2)


def _arm() -> tuple[str, ...]:
    return overlay(rect(4, 9, "b", "o", "l", "d"), grid("WWWW\nWWWW"), 0, 7)


def _leg() -> tuple[str, ...]:
    return overlay(rect(5, 8, "b", "o", "l", "d"), grid("OOOOO\nOOOOO\nOOOOO"), 0, 5)


def _trail() -> tuple[str, ...]:
    rows = []
    for y in range(10):
        half = 1 + y * 0.35
        rows.append("".join(
            "Y" if abs(x - 3.5) < half * 0.45 else "O" if abs(x - 3.5) < half else "."
            for x in range(8)
        ))
    return tuple(rows)


EYES = grid("""
gg....gg
gg....gg
""")
EYES_CLOSED = grid("""
........
gg....gg
""")
FIN = grid("""
.OO.
OYYO
OYYO
""")
BURST = grid("""
...Y....Y...
.Y..YYYY..Y.
YYYYYYYYYYYY
""")

hx, hy = HEAD_SLOT
ZZZ, BOWL = sleep_and_eat_parts(27, 1, 25, 27)

PARTS = (
    Part("trail", 12, 21, _trail(), pivot=(4, 0), z=0),
    Part("scarf", 2, 16, blob(10, 4, "O", "o", "Y", "O"), pivot=(9, 2), z=0),
    Part("leg_l", *LEG_SLOTS[0], _leg(), pivot=LEG_PIVOT, z=1),
    Part("leg_r", *LEG_SLOTS[1], _leg(), pivot=LEG_PIVOT, z=1),
    Part("torso", *TORSO_SLOT, _torso(), z=2),
    Part("arm_l", *ARM_SLOTS[0], _arm(), pivot=ARM_PIVOT, z=3),
    Part("arm_r", *ARM_SLOTS[1], _arm(), pivot=ARM_PIVOT, z=3),
    Part("head", hx, hy, _head(), pivot=neck_pivot(hx, hy), z=4),
    Part("fin", 14, 0, FIN, pivot=neck_pivot(14, 0), z=4),
    Part("eyes", 12, 9, EYES, pivot=neck_pivot(12, 9), z=5),
    Part("eyes_closed", 12, 9, EYES_CLOSED, pivot=neck_pivot(12, 9), z=5),
    Part("burst", 10, 27, BURST, z=6),
    ZZZ,
    BOWL,
)
HEAD_EXTRA = ("fin",)
BODY_EXTRA = ("scarf",)
RISER = ("head", "fin", "eyes", "eyes_closed", "torso", "scarf", "arm_l", "arm_r", "leg_l", "leg_r")


def pose(state: str, t: float) -> dict[str, Pose]:
    poses = base_pose(state, t, HEAD_EXTRA, BODY_EXTRA)
    poses["trail"] = Pose(visible=False)
    poses["burst"] = Pose(visible=False)
    if state in ("idle", "eat", "sleep"):
        poses["scarf"] = Pose(angle=sine(t, 1.4, 8), dy=poses.get("torso", Pose()).dy)
    elif state == "walk":
        poses["scarf"] = Pose(angle=-12 + sine(t, 0.6, 10), dy=poses["torso"].dy)
    else:  # special: crouch, launch in a comet trail with a raised fist, land with a burst
        p = (t % 3.4) / 3.4
        height = 0.0
        if p < 0.15:  # crouch
            poses["torso"] = Pose(sy=0.88, dy=1.5)
            lift(poses, ("head", "fin", "eyes", "eyes_closed", "scarf"), dy=2)
            poses["arm_l"] = Pose(angle=20, dy=2)
            poses["arm_r"] = Pose(angle=-20, dy=2)
        elif p < 0.75:
            if p < 0.3:
                k = (p - 0.15) / 0.15
                height = -9 * math.sin(k * math.pi / 2)
            elif p < 0.62:
                height = -9 + sine(t, 1.0, 0.8)
            else:
                k = (p - 0.62) / 0.13
                height = -9 * (1 - k * k)
            poses["arm_r"] = Pose(angle=-165)
            poses["arm_l"] = Pose(angle=18)
            poses["leg_l"] = Pose(angle=14)
            poses["leg_r"] = Pose(angle=-10)
            poses["scarf"] = Pose(angle=-70 + sine(t, 0.25, 10))
            lift(poses, RISER, dy=height)
            poses["trail"] = Pose(dy=height, sy=1.0 + min(1.0, -height / 9) * 2.2, alpha=0.8)
        else:  # land: burst of light, then settle
            k = (p - 0.75) / 0.25
            poses["torso"] = Pose(sy=0.92 + 0.08 * k, dy=1 - k)
            lift(poses, ("head", "fin", "eyes", "eyes_closed", "scarf"), dy=1 - k)
            poses["arm_l"] = Pose(angle=12)
            poses["arm_r"] = Pose(angle=-12)
            poses["burst"] = Pose(visible=k < 0.5, alpha=1 - 2 * k, sx=1 + k)
    return poses


SPEC = PetSpec(
    key="comet_captain",
    palette=PALETTE,
    parts=PARTS,
    pose=pose,
    move="walk",
    speed=44,
    special_name="comet leap",
)
