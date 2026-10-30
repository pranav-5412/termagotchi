"""Fox: sleek red fox that stalks and pounces nose-first."""

import math

from termagotchi.sprites import (
    FX_PALETTE, Part, PetSpec, Pose, blink, blob, fx_poses, grid, lift, overlay, sine,
    sleep_and_eat_parts,
)

PALETTE = {
    **FX_PALETTE,
    "o": "#3b1d10", "a": "#e86f1f", "l": "#f79a4a", "d": "#bd4f12", "c": "#fff4e6",
    "K": "#2a1a14", "k": "#141414", "y": "#ffc83d", "e": "#1a1a1a",
}


def _tail() -> tuple[str, ...]:
    rows = blob(12, 8, "a", "o", "l", "d")
    # White tip on the left three columns.
    return tuple(
        "".join("c" if x < 4 and char in "ald" else char for x, char in enumerate(row))
        for row in rows
    )


def _leg(top: str) -> tuple[str, ...]:
    return grid(f"""
o{top}{top}o
o{top}{top}o
o{top}{top}o
oKKo
oKKo
oKKo
oKKo
oKKo
oooo
""")


EAR = grid("""
..o..
.oao.
.oKo.
oaKao
oaaao
oaaao
""")
HEAD = blob(11, 10, "a", "o", "l", "d")
SNOUT = overlay(overlay(blob(8, 5, "a", "o", "l", "d"), grid("ccccc"), 2, 3), grid("kk"), 6, 1)
EYES = grid("""
.yy...yy.
yee...eey
""")
EYES_CLOSED = grid("""
.........
.oo...oo.
""")
PUFF = blob(7, 4, "H", "H")
CHEST = grid("""
....cccc
..cccccc
..cccccc
""")

ZZZ, BOWL = sleep_and_eat_parts(27, 3, 26, 27)

PARTS = (
    Part("tail", 0, 14, _tail(), pivot=(10, 4), z=0),
    Part("far_back", 8, 22, _leg("d"), pivot=(2, 0), z=1),
    Part("far_front", 20, 22, _leg("d"), pivot=(2, 0), z=1),
    Part("body", 6, 15, overlay(blob(18, 10, "a", "o", "l", "d"), CHEST, 9, 5), z=2),
    Part("near_back", 10, 22, _leg("a"), pivot=(2, 0), z=3),
    Part("near_front", 22, 22, _leg("a"), pivot=(2, 0), z=3),
    Part("ear_l", 17, 3, EAR, pivot=(5.5, 14), z=3),
    Part("ear_r", 23, 3, EAR, pivot=(-0.5, 14), z=3),
    Part("head", 17, 8, HEAD, pivot=(5.5, 9), z=4),
    Part("snout", 23, 12, SNOUT, pivot=(-0.5, 5), z=5),
    Part("eyes", 18, 11, EYES, pivot=(4.5, 6), z=5),
    Part("eyes_closed", 18, 11, EYES_CLOSED, pivot=(4.5, 6), z=5),
    Part("puff", 25, 27, PUFF, z=8),
    ZZZ,
    BOWL,
)
FACE = ("head", "snout", "eyes", "eyes_closed", "ear_l", "ear_r")
ALL = tuple(part.name for part in PARTS if part.name not in ("zzz", "bowl", "puff"))
LEGS = ("near_front", "far_front", "near_back", "far_back")


def _face(t: float, asleep: bool = False, dy: float = 0.0, angle: float = 0.0) -> dict[str, Pose]:
    """Move the whole head group together; eyes close on blink or sleep."""
    shut = asleep or blink(t, 4.1)
    poses = {name: Pose(dy=dy, angle=angle) for name in FACE}
    poses["eyes"] = Pose(dy=dy, angle=angle, visible=not shut)
    poses["eyes_closed"] = Pose(dy=dy, angle=angle, visible=shut)
    return poses


def _legs(swing: float) -> dict[str, Pose]:
    return {
        "near_front": Pose(angle=swing),
        "far_front": Pose(angle=-swing),
        "near_back": Pose(angle=-swing),
        "far_back": Pose(angle=swing),
    }


def pose(state: str, t: float) -> dict[str, Pose]:
    poses = fx_poses(state, t)
    poses["puff"] = Pose(visible=False)
    if state == "idle":
        poses.update(_face(t, dy=sine(t, 3, 0.4), angle=sine(t, 6, 3)))
        poses["ear_l"] = Pose(dy=sine(t, 3, 0.4), angle=sine(t, 1.9, 7))
        poses["body"] = Pose(sy=1 + sine(t, 3, 0.02))
        poses["tail"] = Pose(angle=sine(t, 2.2, 9))
    elif state == "walk":
        poses.update(_legs(sine(t, 0.5, 26)))
        bob = abs(sine(t, 0.5, 0.7)) - 0.4
        poses.update(_face(t, dy=bob))
        poses["body"] = Pose(dy=bob)
        poses["tail"] = Pose(angle=-6 + sine(t, 1.0, 7))
    elif state == "eat":
        poses.update(_face(t, dy=4 + sine(t, 0.45, 1.3), angle=sine(t, 0.45, 5)))
        poses["tail"] = Pose(angle=sine(t, 1.2, 9))
    elif state == "sleep":
        poses.update(_face(t, asleep=True, dy=4, angle=10))
        poses["body"] = Pose(sy=0.95 + sine(t, 3.4, 0.015), dy=1)
        poses["tail"] = Pose(angle=24, dx=3, dy=1)
    else:  # special: stalk, leap, nose-first pounce, shake off
        p = (t % 3.2) / 3.2
        if p < 0.35:  # stalk low, tail tip twitching
            poses["body"] = Pose(sy=0.84, dy=2.2)
            poses.update(_face(t, dy=3.5, angle=4))
            poses["tail"] = Pose(angle=sine(t, 0.3, 12), dy=1)
            poses.update(_legs(sine(t, 0.4, 3)))
        elif p < 0.6:  # high leap, tipping nose down
            k = (p - 0.35) / 0.25
            height = -12 * math.sin(math.pi * k)
            tilt = -22 + 55 * k
            poses["body"] = Pose(angle=tilt * 0.6, sy=1.04)
            poses.update(_face(t, dy=-1, angle=tilt * 0.8))
            poses["tail"] = Pose(angle=28)
            poses.update(_legs(-30 + 60 * k))
            lift(poses, ALL, dy=height)
        elif p < 0.76:  # nose in the snow, tail up
            k = (p - 0.6) / 0.16
            poses["body"] = Pose(angle=24, dy=1.5, sy=0.95)
            poses.update(_face(t, dy=5, angle=30))
            poses["tail"] = Pose(angle=-30, dy=-2)
            poses.update(_legs(-12))
            poses["puff"] = Pose(visible=True, dy=-3 * k, alpha=1 - 0.6 * k, sx=1 + 0.5 * k)
        else:  # shake the snow off
            k = (p - 0.76) / 0.24
            poses["body"] = Pose(angle=8 * (1 - k))
            poses.update(_face(t, dy=3 * (1 - k), angle=sine(t, 0.2, 14 * (1 - k))))
            poses["tail"] = Pose(angle=sine(t, 0.3, 14))
    return poses


SPEC = PetSpec(
    key="fox",
    palette=PALETTE,
    parts=PARTS,
    pose=pose,
    move="walk",
    speed=58,
    special_name="snow pounce",
)
