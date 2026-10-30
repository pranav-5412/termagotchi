"""Rabbit: white lop-eared bunny that hops and does a binky."""

import math

from termagotchi.sprites import (
    FX_PALETTE, Part, PetSpec, Pose, blink, blob, fx_poses, grid, lift, overlay, sine,
    sleep_and_eat_parts,
)

PALETTE = {
    **FX_PALETTE,
    "o": "#4a3340", "a": "#f2e6ea", "l": "#ffffff", "d": "#cfbcc5", "p": "#f3a3b5",
    "n": "#e8607f", "e": "#2a1a24", "w": "#ffffff",
}


def _ear() -> tuple[str, ...]:
    ear = blob(5, 13, "a", "o", "l", "d")
    return overlay(ear, tuple("..p.." for _ in range(8)), 0, 3)


def _head() -> tuple[str, ...]:
    head = blob(13, 11, "a", "o", "l", "d")
    head = overlay(head, grid("n"), 6, 6)
    head = overlay(head, grid("o.o"), 5, 7)
    return overlay(head, grid("p.....p"), 3, 6)


EYES = grid("""
we.....ew
ee.....ee
""")
EYES_CLOSED = grid("""
oo.....oo
.........
""")

ZZZ, BOWL = sleep_and_eat_parts(27, 2, 26, 27)

PARTS = (
    Part("tail", 3, 20, blob(6, 6, "l", "o", "l", "d"), z=0),
    Part("ear_far", 18, 0, _ear(), pivot=(2.5, 12), z=1),
    Part("ear_near", 23, 0, _ear(), pivot=(2.5, 12), z=1),
    Part("body", 7, 16, blob(17, 13, "a", "o", "l", "d"), z=2),
    Part("haunch", 6, 19, blob(9, 9, "a", "o", "l", "d"), z=3),
    Part("foot", 4, 28, blob(10, 4, "a", "o", "l", "d"), pivot=(8, 0), z=3),
    Part("paw", 21, 27, blob(6, 5, "a", "o", "l", "d"), pivot=(3, 0), z=3),
    Part("head", 18, 10, _head(), pivot=(6.5, 9), z=4),
    Part("eyes", 20, 13, EYES, pivot=(4.5, 0), z=5),
    Part("eyes_closed", 20, 13, EYES_CLOSED, pivot=(4.5, 0), z=5),
    ZZZ,
    BOWL,
)
UPPER = ("ear_far", "ear_near", "head", "eyes", "eyes_closed")
ALL = tuple(part.name for part in PARTS if part.name not in ("zzz", "bowl"))


def _face(t: float, asleep: bool = False, dy: float = 0.0, angle: float = 0.0) -> dict[str, Pose]:
    shut = asleep or blink(t, 3.5)
    return {
        "head": Pose(dy=dy, angle=angle),
        "eyes": Pose(dy=dy, angle=angle, visible=not shut),
        "eyes_closed": Pose(dy=dy, angle=angle, visible=shut),
    }


def _ears(dy: float, near: float, far: float) -> dict[str, Pose]:
    return {"ear_near": Pose(dy=dy, angle=near), "ear_far": Pose(dy=dy, angle=far)}


def pose(state: str, t: float) -> dict[str, Pose]:
    poses = fx_poses(state, t)
    if state == "idle":
        flick = 14 if (t % 4.0) < 0.2 else 0
        poses.update(_face(t, dy=sine(t, 2.6, 0.4)))
        poses.update(_ears(sine(t, 2.6, 0.4), sine(t, 3.1, 3) + flick, sine(t, 3.1, 3, 0.2)))
        poses["body"] = Pose(sy=1 + sine(t, 2.6, 0.02))
        poses["tail"] = Pose(dy=sine(t, 0.4, 0.3))
    elif state == "walk":
        p = abs(math.sin(t * 7))  # 0 on the ground, 1 at the top of the hop
        poses.update(_face(t, dy=-0.5 * p))
        poses.update(_ears(-0.5 * p, -24 * p, -28 * p))
        poses["body"] = Pose(sy=0.9 + 0.2 * p, sx=1.05 - 0.1 * p, dy=0.6 * (1 - p))
        poses["foot"] = Pose(angle=-30 * p)
        poses["haunch"] = Pose(angle=-12 * p)
        poses["paw"] = Pose(angle=24 * p)
    elif state == "eat":
        poses.update(_face(t, dy=4 + sine(t, 0.3, 0.8), angle=6 + sine(t, 0.3, 3)))
        poses.update(_ears(4, 10, 8))
    elif state == "sleep":
        poses.update(_face(t, asleep=True, dy=5, angle=8))
        poses.update(_ears(5, -50, -55))
        poses["body"] = Pose(sy=0.92 + sine(t, 3.4, 0.015), dy=1.5)
    else:  # special: binky, a joyful jump with a twist
        p = (t % 2.2) / 2.2
        if p < 0.2:  # crouch
            poses["body"] = Pose(sy=0.82, dy=2.5)
            poses.update(_face(t, dy=3))
            poses.update(_ears(3, 6, 8))
        elif p < 0.75:  # airborne
            k = (p - 0.2) / 0.55
            height = -9 * math.sin(math.pi * k)
            twist = 22 * math.sin(2 * math.pi * k)
            poses["body"] = Pose(angle=twist, sy=1.12)
            poses.update(_face(t, angle=twist * 0.6))
            poses.update(_ears(0, sine(t, 0.25, 32), sine(t, 0.25, 32, 0.25)))
            poses["foot"] = Pose(angle=sine(t, 0.3, 35))
            poses["paw"] = Pose(angle=-20)
            lift(poses, ALL, dy=height)
        else:  # landing wobble
            poses["body"] = Pose(sy=0.88, dy=1.5)
            poses.update(_face(t, dy=2))
            poses.update(_ears(2, sine(t, 0.3, 8), sine(t, 0.3, 8, 0.2)))
    return poses


SPEC = PetSpec(
    key="rabbit",
    palette=PALETTE,
    parts=PARTS,
    pose=pose,
    move="hop",
    speed=52,
    special_name="binky",
)
