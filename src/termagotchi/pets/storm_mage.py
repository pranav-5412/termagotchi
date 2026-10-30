"""Storm Mage: purple wizard whose staff calls a thundercloud and lightning."""

import math

from termagotchi.pets.biped import (
    ARM_PIVOT, ARM_SLOTS, HEAD_SLOT, LEG_PIVOT, LEG_SLOTS, RIGHT_SHOULDER, base_pose, hold,
    neck_pivot,
)
from termagotchi.sprites import (
    FX_PALETTE, TRANSPARENT, Part, PetSpec, Pose, blob, grid, lift, overlay, rect, sine,
    sleep_and_eat_parts,
)

PALETTE = {
    **FX_PALETTE,
    "o": "#1f0f33", "M": "#6b3fc4", "m": "#9a6bff", "n": "#442488", "Y": "#ffd23a",
    "f": "#f2c9a0", "q": "#ffe0bf", "F": "#d9a77a", "W": "#f5f5fa", "h": "#c4c8d8",
    "b": "#5a3a1e", "e": "#1a1a1a", "w": "#ffffff", "C": "#8a5a2b", "c": "#7be0ff",
    "g": "#8a90ad", "G": "#555b78", "L": "#fff7a8", "y": "#ffe45c", "R": "#7bb8ff",
}

HAND_REST = (24.0, 24.0)


def _hat() -> tuple[str, ...]:
    """Pointed hat: a cone tapering to the tip, over a wide brim."""
    w, h = 18, 9

    def inside(x: int, y: int) -> bool:
        if not 0 <= x < w or not 0 <= y < h:
            return False
        if y >= 7:
            return abs(x - 8.5) <= 8.5 - (y - 7) * 0.5
        return abs(x - 8.5) <= 1.0 + y * 0.9

    rows = []
    for y in range(h):
        row = ""
        for x in range(w):
            if not inside(x, y):
                row += TRANSPARENT
            elif any(not inside(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                row += "o"
            else:
                row += "m" if x < 6 else "n" if x > 12 else "M"
        rows.append(row)
    return overlay(tuple(rows), grid(".Y.\nYYY\n.Y."), 7, 2)


def _cloud() -> tuple[str, ...]:
    base = tuple("." * 20 for _ in range(8))
    for x, y, w, h in ((0, 3, 9, 5), (5, 0, 10, 7), (11, 2, 9, 6)):
        base = overlay(base, blob(w, h, "g", "G", "w", "G"), x, y)
    return base


def _bolt() -> tuple[str, ...]:
    rows = []
    for y in range(9):
        c = 3 + round(2 * math.sin(y * 1.1))
        rows.append("".join("y" if x == c else "L" if abs(x - c) == 1 else "." for x in range(7)))
    return tuple(rows)


def _rain() -> tuple[str, ...]:
    return tuple("".join("R" if (x * 2 + y) % 6 == 0 else "." for x in range(20)) for y in range(22))


def _staff() -> tuple[str, ...]:
    crystal = overlay(blob(5, 5, "c", "o", "w", "c"), grid("."), 0, 0)
    return tuple(crystal) + tuple(".oCo." for _ in range(17))


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
    Part("leg_l", *LEG_SLOTS[0], rect(5, 8, "b", "o", "b", "b"), pivot=LEG_PIVOT, z=1),
    Part("leg_r", *LEG_SLOTS[1], rect(5, 8, "b", "o", "b", "b"), pivot=LEG_PIVOT, z=1),
    Part("torso", 9, 16, overlay(rect(14, 13, "M", "o", "m", "n"), grid("YYYYYYYYYYYY"), 1, 4), z=2),
    Part("staff", 22, 6, _staff(), pivot=(HAND_REST[0] - 22, HAND_REST[1] - 6), z=2),
    Part("arm_l", *ARM_SLOTS[0], overlay(rect(4, 9, "M", "o", "m", "n"), grid("ffff\nffff"), 0, 7),
         pivot=ARM_PIVOT, z=3),
    Part("arm_r", *ARM_SLOTS[1], overlay(rect(4, 9, "M", "o", "m", "n"), grid("ffff\nffff"), 0, 7),
         pivot=ARM_PIVOT, z=3),
    Part("head", hx, hy, blob(16, 14, "f", "o", "q", "F"), pivot=neck_pivot(hx, hy), z=4),
    Part("eyes", 12, 10, EYES, pivot=neck_pivot(12, 10), z=5),
    Part("eyes_closed", 12, 10, EYES_CLOSED, pivot=neck_pivot(12, 10), z=5),
    Part("beard", 11, 13, blob(10, 7, "W", "o", "W", "h"), pivot=neck_pivot(11, 13), z=5),
    Part("hat", 7, 0, _hat(), pivot=neck_pivot(7, 0), z=6),
    Part("rain", 6, 0, _rain(), z=7),
    Part("cloud", 6, 0, _cloud(), z=8),
    Part("bolt", 22, 0, _bolt(), z=8),
    ZZZ,
    BOWL,
)
HEAD_EXTRA = ("beard", "hat")
RAISE = ("head", "eyes", "eyes_closed", "beard", "hat")


def _staff_pose(arm: Pose) -> Pose:
    """Hold the staff upright in the right hand however the arm turns."""
    return hold(RIGHT_SHOULDER, HAND_REST, arm.angle, arm.dy, extra=-arm.angle)


def pose(state: str, t: float) -> dict[str, Pose]:
    poses = base_pose(state, t, HEAD_EXTRA, blink_every=4.0)
    for name in ("rain", "cloud", "bolt"):
        poses[name] = Pose(visible=False)
    poses["staff"] = _staff_pose(poses["arm_r"])
    if state == "special":  # raise the staff, call a storm, strike the crystal
        p = (t % 4.0) / 4.0
        k = min(1.0, p / 0.15) if p < 0.8 else max(0.0, (1 - p) / 0.2)
        arm = Pose(angle=-150 * k)
        poses["arm_r"] = arm
        poses["staff"] = _staff_pose(arm)
        poses["arm_l"] = Pose(angle=35 * k)
        lift(poses, RAISE, dy=-0.5 * k)
        if p > 0.12:
            fade = min(1.0, (p - 0.12) / 0.1) * (1.0 if p < 0.82 else max(0.0, (0.92 - p) / 0.1))
            poses["cloud"] = Pose(dy=-8, alpha=fade, dx=sine(t, 1.6, 0.5))
            poses["rain"] = Pose(dy=(t * 20) % 6, alpha=0.7 * fade)
            strike = (t % 0.9) < 0.12 or 0.3 < (t % 0.9) < 0.4
            poses["bolt"] = Pose(visible=strike and fade > 0.5, dy=0)
    return poses


SPEC = PetSpec(
    key="storm_mage",
    palette=PALETTE,
    parts=PARTS,
    pose=pose,
    move="walk",
    speed=28,
    special_name="thunderstorm",
)
