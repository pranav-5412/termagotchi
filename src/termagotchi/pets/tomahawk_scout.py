"""Tomahawk Scout: olive-coated explorer who tosses a tomahawk high and catches it."""

import math
from dataclasses import replace

from termagotchi.pets.biped import (
    ARM_PIVOT, ARM_SLOTS, HEAD_SLOT, LEG_PIVOT, LEG_SLOTS, RIGHT_SHOULDER, TORSO_SLOT, base_pose,
    hold, neck_pivot,
)
from termagotchi.sprites import (
    FX_PALETTE, Part, PetSpec, Pose, blob, grid, overlay, rect, sine, sleep_and_eat_parts,
)

PALETTE = {
    **FX_PALETTE,
    "o": "#1f2a12", "a": "#7c9a43", "l": "#a6c46a", "d": "#566f2a", "t": "#c9a56a",
    "T": "#e6c98f", "D": "#9a7a44", "b": "#6b4a2b", "B": "#8c6a42", "f": "#f0c8a0",
    "q": "#ffe0bf", "F": "#d9a77a", "e": "#1a1a1a", "w": "#ffffff", "r": "#d9573a",
    "R": "#a63d27", "s": "#b8c2cc", "S": "#e7eef5", "k": "#59626d", "h": "#7a4f2a",
    "Y": "#ffd23a",
}

HAND_REST = (24.0, 24.0)
HATCHET_X, HATCHET_Y = 21, 13
TOSS_HEIGHT = 19  # cells the tomahawk rises above the hand


def _hat() -> tuple[str, ...]:
    base = tuple("." * 20 for _ in range(9))
    base = overlay(base, blob(12, 7, "t", "o", "T", "D"), 4, 0)
    base = overlay(base, blob(20, 5, "t", "o", "T", "D"), 0, 4)
    return overlay(base, grid("RRRRRRRRRR"), 5, 4)


def _torso() -> tuple[str, ...]:
    torso = rect(12, 9, "a", "o", "l", "d")
    torso = overlay(torso, grid("b.....b\n.b...b."), 2, 1)
    return overlay(torso, grid("bbbbbbbbbb"), 1, 6)


def _arm() -> tuple[str, ...]:
    return overlay(rect(4, 9, "a", "o", "l", "d"), grid("bbbb\nbbbb"), 0, 7)


def _leg() -> tuple[str, ...]:
    return overlay(rect(5, 8, "d", "o", "a", "d"), grid("bbbbb\nbbbbb\nbbbbb"), 0, 5)


def _hatchet() -> tuple[str, ...]:
    rows = [".ooo...", "oSSSo..", "oSSSSo.", "oSkkSo.", ".oSSo..", *["..oho.."] * 8, "..ooo.."]
    return grid("\n".join(rows))


EYES = grid("""
we....we
ee....ee
ee....ee
""")
EYES_CLOSED = grid("""
........
ee....ee
........
""")

hx, hy = HEAD_SLOT
ZZZ, BOWL = sleep_and_eat_parts(27, 1, 25, 27)

PARTS = (
    Part("pack", 4, 17, rect(6, 9, "b", "o", "B", "b"), z=0),
    Part("leg_l", *LEG_SLOTS[0], _leg(), pivot=LEG_PIVOT, z=1),
    Part("leg_r", *LEG_SLOTS[1], _leg(), pivot=LEG_PIVOT, z=1),
    Part("torso", *TORSO_SLOT, _torso(), z=2),
    Part("hatchet", HATCHET_X, HATCHET_Y, _hatchet(), pivot=(3, 11), z=2),
    Part("arm_l", *ARM_SLOTS[0], _arm(), pivot=ARM_PIVOT, z=3),
    Part("arm_r", *ARM_SLOTS[1], _arm(), pivot=ARM_PIVOT, z=3),
    Part("scarf", 10, 15, blob(12, 4, "r", "o", "r", "R"), z=4),
    Part("scarf_tail", 19, 16, blob(4, 8, "r", "o", "r", "R"), pivot=(2, 0), z=4),
    Part("head", hx, hy, blob(16, 14, "f", "o", "q", "F"), pivot=neck_pivot(hx, hy), z=4),
    Part("eyes", 12, 10, EYES, pivot=neck_pivot(12, 10), z=5),
    Part("eyes_closed", 12, 10, EYES_CLOSED, pivot=neck_pivot(12, 10), z=5),
    Part("hat", 6, 0, _hat(), pivot=neck_pivot(6, 0), z=6),
    ZZZ,
    BOWL,
)
HEAD_EXTRA = ("hat",)
BODY_EXTRA = ("pack", "scarf", "scarf_tail")


def _hatchet_pose(arm: Pose, extra: float = 0.0) -> Pose:
    """Keep the tomahawk in the right hand, spun by extra degrees."""
    return hold(RIGHT_SHOULDER, HAND_REST, arm.angle, arm.dy, extra)


def pose(state: str, t: float) -> dict[str, Pose]:
    poses = base_pose(state, t, HEAD_EXTRA, BODY_EXTRA, blink_every=4.2)
    torso_dy = poses.get("torso", Pose()).dy
    poses["scarf_tail"] = Pose(angle=sine(t, 0.9, 12) - (16 if state == "walk" else 0), dy=torso_dy)
    poses["hatchet"] = _hatchet_pose(poses["arm_r"])
    if state == "special":  # toss the tomahawk high, catch it, then twirl it
        p = (t % 3.6) / 3.6
        up = Pose(angle=-150)
        if p < 0.15:
            arm = Pose(angle=-150 * p / 0.15)
            poses["arm_r"] = arm
            poses["hatchet"] = _hatchet_pose(arm)
        elif p < 0.6:
            k = (p - 0.15) / 0.45
            poses["arm_r"] = up
            base = _hatchet_pose(up)
            poses["hatchet"] = replace(
                base, dy=base.dy - TOSS_HEIGHT * math.sin(math.pi * k), angle=base.angle + 720 * k
            )
        elif p < 0.8:
            k = (p - 0.6) / 0.2
            arm = Pose(angle=-150 + 130 * k)
            poses["arm_r"] = arm
            poses["hatchet"] = _hatchet_pose(arm, extra=360 * k)
        else:
            k = (p - 0.8) / 0.2
            arm = Pose(angle=-20 * (1 - k))
            poses["arm_r"] = arm
            poses["hatchet"] = _hatchet_pose(arm)
    return poses


SPEC = PetSpec(
    key="tomahawk_scout",
    palette=PALETTE,
    parts=PARTS,
    pose=pose,
    move="walk",
    speed=40,
    special_name="tomahawk toss",
)
