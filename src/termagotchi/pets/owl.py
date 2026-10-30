"""Owl: brown owl that spins its head all the way around."""

import math

from termagotchi.sprites import (
    FX_PALETTE, Part, PetSpec, Pose, blink, blob, fx_poses, grid, lift, mirror, overlay, sine,
    sleep_and_eat_parts,
)

PALETTE = {
    **FX_PALETTE,
    "o": "#2d2118", "a": "#9b6b3e", "l": "#bd8d5a", "d": "#6e4a28", "D": "#573a1f",
    "c": "#f1e2c4", "y": "#ffcf3a", "e": "#111111", "f": "#f0a030", "t": "#d98a1c",
}

HEAD_X, HEAD_Y = 7, 3
PIVOT = (15.5, 15.0)  # absolute point the head turns around


def _pv(x: int, y: int) -> tuple[float, float]:
    """Pivot for a head part so the whole head turns around one point."""
    return PIVOT[0] - x, PIVOT[1] - y


def _eye() -> tuple[str, ...]:
    return overlay(blob(6, 6, "y", "o"), grid("ee\nee"), 2, 2)


def _eyes(closed: bool) -> tuple[str, ...]:
    base = tuple("." * 14 for _ in range(6))
    if closed:
        return overlay(overlay(base, grid("oooo"), 1, 3), grid("oooo"), 9, 3)
    return overlay(overlay(base, _eye(), 0, 0), _eye(), 8, 0)


BELLY = overlay(
    blob(12, 14, "c", "d", "c", "c"),
    grid("""
..d..d..d..
...d..d..d.
..d..d..d..
...d..d..d.
..d..d..d..
"""),
    0, 3,
)
TUFT_L = grid("""
oo..
oao.
oaao
.aao
""")
WING = blob(6, 16, "d", "o", "a", "D")
FOOT = grid("""
fffff
.f.f.
""")

ZZZ, BOWL = sleep_and_eat_parts(26, 2, 25, 27)

PARTS = (
    Part("body", 6, 10, blob(20, 20, "a", "o", "l", "d"), z=1),
    Part("belly", 10, 14, BELLY, z=2),
    Part("wing_l", 3, 13, WING, pivot=(3, 1), z=3),
    Part("wing_r", 23, 13, WING, pivot=(3, 1), z=3),
    Part("foot_l", 10, 29, FOOT, z=2),
    Part("foot_r", 17, 29, FOOT, z=2),
    Part("tuft_l", 7, 0, TUFT_L, pivot=_pv(7, 0), z=4),
    Part("tuft_r", 21, 0, mirror(TUFT_L), pivot=_pv(21, 0), z=4),
    Part("head", HEAD_X, HEAD_Y, blob(18, 14, "a", "o", "l", "d"), pivot=_pv(HEAD_X, HEAD_Y), z=4),
    Part("disc", 9, 5, blob(14, 10, "c", "d", "c", "c"), pivot=_pv(9, 5), z=5),
    Part("eyes", 9, 6, _eyes(False), pivot=_pv(9, 6), z=6),
    Part("eyes_closed", 9, 6, _eyes(True), pivot=_pv(9, 6), z=6),
    Part("beak", 14, 11, grid("oooo\nofto\n.oo."), pivot=_pv(14, 11), z=6),
    ZZZ,
    BOWL,
)
HEAD_GROUP = ("head", "tuft_l", "tuft_r", "disc", "eyes", "eyes_closed", "beak")
ALL = tuple(p.name for p in PARTS if p.name not in ("zzz", "bowl"))


def _head(t: float, asleep: bool = False, dy: float = 0.0, angle: float = 0.0, turn: float = 1.0):
    """Pose the head group. turn is the horizontal scale: negative shows the back of the head."""
    front = turn > 0.05
    shut = asleep or blink(t, 4.5, 0.2)
    poses = {name: Pose(dy=dy, angle=angle, sx=turn) for name in HEAD_GROUP}
    for name in ("disc", "beak"):
        poses[name] = Pose(dy=dy, angle=angle, sx=turn, visible=front)
    poses["eyes"] = Pose(dy=dy, angle=angle, sx=turn, visible=front and not shut)
    poses["eyes_closed"] = Pose(dy=dy, angle=angle, sx=turn, visible=front and shut)
    return poses


def pose(state: str, t: float) -> dict[str, Pose]:
    poses = fx_poses(state, t)
    if state == "idle":
        poses.update(_head(t, dy=sine(t, 3.4, 0.4), angle=sine(t, 6.5, 7)))
        poses["body"] = Pose(sy=1 + sine(t, 3.4, 0.015))
        poses["wing_l"] = Pose(angle=sine(t, 3.4, 2))
        poses["wing_r"] = Pose(angle=-sine(t, 3.4, 2))
    elif state == "walk":
        hop = abs(sine(t, 0.5, 1.0))
        poses.update(_head(t, dy=-hop * 0.5, angle=sine(t, 0.5, 4)))
        poses["body"] = Pose(angle=sine(t, 0.5, 5), dy=-hop * 0.6)
        poses["belly"] = Pose(angle=sine(t, 0.5, 5), dy=-hop * 0.6)
        poses["foot_l"] = Pose(dy=-max(0.0, sine(t, 0.5, 1.5)))
        poses["foot_r"] = Pose(dy=-max(0.0, -sine(t, 0.5, 1.5)))
        poses["wing_l"] = Pose(angle=sine(t, 0.5, 6))
        poses["wing_r"] = Pose(angle=-sine(t, 0.5, 6))
    elif state == "eat":
        poses.update(_head(t, dy=4 + sine(t, 0.45, 1.5), angle=8 + sine(t, 0.45, 4)))
        poses["body"] = Pose(angle=3)
    elif state == "sleep":
        poses.update(_head(t, asleep=True, dy=3, angle=-5))
        poses["body"] = Pose(sy=0.95 + sine(t, 3.6, 0.015), dy=1)
        poses["wing_l"] = Pose(angle=-6)
        poses["wing_r"] = Pose(angle=6)
    else:  # special: look around, spin the head fully, then wobble dizzily
        p = (t % 4.0) / 4.0
        flare = 0.0
        if p < 0.2:
            poses.update(_head(t, angle=-10 * math.sin(math.pi * p / 0.2)))
        elif p < 0.6:
            k = (p - 0.2) / 0.4
            flare = math.sin(math.pi * k)
            poses.update(_head(t, dy=-flare, turn=math.cos(2 * math.pi * k)))
        else:
            k = (p - 0.6) / 0.4
            poses.update(_head(t, angle=sine(t, 0.5, 14 * (1 - k))))
        poses["wing_l"] = Pose(angle=-35 * flare)
        poses["wing_r"] = Pose(angle=35 * flare)
        lift(poses, ("body", "belly"), dy=-0.5 * flare)
    return poses


SPEC = PetSpec(
    key="owl",
    palette=PALETTE,
    parts=PARTS,
    pose=pose,
    move="walk",
    speed=30,
    special_name="head spin",
)
