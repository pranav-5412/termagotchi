"""Penguin: waddles, and flops onto its belly to slide."""

from termagotchi.sprites import (
    FX_PALETTE, Part, PetSpec, Pose, blink, blob, fx_poses, grid, sine, sleep_and_eat_parts,
)

PALETTE = {
    **FX_PALETTE,
    "o": "#0d1a2b", "K": "#243b5a", "k": "#1a2b44", "L": "#3d5b82", "c": "#f4f7fb",
    "s": "#d6e0ee", "f": "#ff9f1c", "O": "#c97410", "e": "#0a0a0a", "w": "#ffffff",
}

BASE = (15.5, 29.0)  # waddle pivot, between the feet


def _pv(x: int, y: int) -> tuple[float, float]:
    """Pivot that puts a part's rotation at the shared waddle point."""
    return BASE[0] - x, BASE[1] - y


EYES = grid("""
.ee....ee.
.ew....we.
""")
EYES_CLOSED = grid("""
..........
.oo....oo.
""")
BEAK = grid("""
ffffff
.ffff.
..ff..
""")

ZZZ, BOWL = sleep_and_eat_parts(26, 2, 25, 27)

PARTS = (
    Part("flipper_l", 4, 13, blob(4, 12, "K", "o", "L", "k"), pivot=(3, 1), z=0),
    Part("flipper_r", 24, 13, blob(4, 12, "K", "o", "L", "k"), pivot=(1, 1), z=0),
    Part("body", 7, 8, blob(18, 22, "K", "o", "L", "k"), pivot=_pv(7, 8), z=1),
    Part("belly", 10, 12, blob(11, 16, "c", "s", "c", "c"), pivot=_pv(10, 12), z=2),
    Part("foot_l", 8, 29, blob(7, 3, "f", "O"), pivot=_pv(8, 29), z=3),
    Part("foot_r", 16, 29, blob(7, 3, "f", "O"), pivot=_pv(16, 29), z=3),
    Part("head", 9, 1, blob(14, 11, "K", "o", "L", "k"), pivot=_pv(9, 1), z=4),
    Part("mask", 11, 4, blob(10, 6, "c", "s", "c", "c"), pivot=_pv(11, 4), z=5),
    Part("eyes", 11, 5, EYES, pivot=_pv(11, 5), z=6),
    Part("eyes_closed", 11, 5, EYES_CLOSED, pivot=_pv(11, 5), z=6),
    Part("beak", 13, 8, BEAK, pivot=_pv(13, 8), z=6),
    ZZZ,
    BOWL,
)
HEAD = ("head", "mask", "eyes", "eyes_closed", "beak")
GROUP = ("body", "belly", "foot_l", "foot_r") + HEAD


def _group(
    t: float, angle: float = 0.0, dx: float = 0.0, dy: float = 0.0,
    head_dy: float = 0.0, asleep: bool = False,
) -> dict[str, Pose]:
    """Rotate the rigid body group about the feet; the head can also dip."""
    shut = asleep or blink(t, 3.9)
    poses = {name: Pose(angle=angle, dx=dx, dy=dy) for name in GROUP}
    for name in HEAD:
        poses[name] = Pose(angle=angle, dx=dx, dy=dy + head_dy)
    poses["eyes"] = Pose(angle=angle, dx=dx, dy=dy + head_dy, visible=not shut)
    poses["eyes_closed"] = Pose(angle=angle, dx=dx, dy=dy + head_dy, visible=shut)
    return poses


def pose(state: str, t: float) -> dict[str, Pose]:
    poses = fx_poses(state, t)
    if state == "idle":
        poses.update(_group(t, angle=sine(t, 4, 1.5), head_dy=sine(t, 3, 0.4)))
        poses["flipper_l"] = Pose(angle=sine(t, 2.6, 4))
        poses["flipper_r"] = Pose(angle=-sine(t, 2.6, 4))
    elif state == "walk":
        poses.update(_group(t, angle=sine(t, 0.6, 7), dy=-abs(sine(t, 0.6, 0.6))))
        poses["flipper_l"] = Pose(angle=-18 + sine(t, 0.6, 16))
        poses["flipper_r"] = Pose(angle=18 - sine(t, 0.6, 16))
        poses["foot_l"] = Pose(angle=poses["foot_l"].angle, dy=-max(0.0, sine(t, 0.6, 1.6)))
        poses["foot_r"] = Pose(angle=poses["foot_r"].angle, dy=-max(0.0, -sine(t, 0.6, 1.6)))
    elif state == "eat":
        poses.update(_group(t, angle=3, head_dy=3 + sine(t, 0.45, 1.4)))
        poses["flipper_l"] = Pose(angle=-20 + sine(t, 0.9, 6))
        poses["flipper_r"] = Pose(angle=20 - sine(t, 0.9, 6))
    elif state == "sleep":
        poses.update(_group(t, angle=2, head_dy=3, asleep=True))
        poses["flipper_l"] = Pose(angle=6)
        poses["flipper_r"] = Pose(angle=-6)
    else:  # special: lean, flop onto the belly, slide, pop back up and cheer
        p = (t % 3.6) / 3.6
        if p < 0.18:  # lean forward
            a = p / 0.18
            poses.update(_group(t, angle=22 * a))
        elif p < 0.3:  # flop down
            a = (p - 0.18) / 0.12
            lie = 0.25 + 0.75 * a
            poses.update(_group(t, angle=90 * lie, dx=-10 * lie, dy=-7 * lie))
        elif p < 0.82:  # slide
            poses.update(_group(t, angle=90 + sine(t, 0.35, 2), dx=-10, dy=-7))
            for name in ("flipper_l", "flipper_r"):
                poses[name] = Pose(visible=False)
        elif p < 0.92:  # pop up
            a = 1 - (p - 0.82) / 0.1
            poses.update(_group(t, angle=90 * a, dx=-10 * a, dy=-7 * a))
        else:  # cheer
            poses.update(_group(t))
            poses["flipper_l"] = Pose(angle=-70 + sine(t, 0.25, 12))
            poses["flipper_r"] = Pose(angle=70 - sine(t, 0.25, 12))
        if p < 0.3 or p >= 0.82:
            poses.setdefault("flipper_l", Pose(angle=-10))
            poses.setdefault("flipper_r", Pose(angle=10))
    return poses


SPEC = PetSpec(
    key="penguin",
    palette=PALETTE,
    parts=PARTS,
    pose=pose,
    move="walk",
    speed=28,
    special_name="belly slide",
)
