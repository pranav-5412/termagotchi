"""Sugar glider: gray glider with big eyes that leaps and glides on its membrane."""

import math

from termagotchi.sprites import (
    FX_PALETTE, Part, PetSpec, Pose, blink, blob, fx_poses, grid, lift, overlay, sine,
    sleep_and_eat_parts,
)

PALETTE = {
    **FX_PALETTE,
    "o": "#2b2b36", "g": "#a9aebb", "l": "#cfd3dd", "d": "#7d8294", "k": "#3a3d4d",
    "c": "#f2f2f5", "p": "#e8a0b0", "e": "#0a0a0f", "w": "#ffffff",
    "m": "#b9a99a", "M": "#d4c7b8", "N": "#8f7f70",
}


def _tail() -> tuple[str, ...]:
    rows = blob(14, 6, "g", "o", "l", "d")
    return tuple(
        "".join("k" if x < 3 and char in "gld" else char for x, char in enumerate(row))
        for row in rows
    )


def _body() -> tuple[str, ...]:
    body = blob(13, 15, "g", "o", "l", "d")
    body = overlay(body, grid("kkkkkkkk"), 3, 1)
    return overlay(body, blob(9, 7, "c", "c", "c", "c"), 3, 8)


def _head() -> tuple[str, ...]:
    head = overlay(blob(13, 11, "g", "o", "l", "d"), blob(6, 4, "c", "c", "c", "c"), 6, 5)
    head = overlay(head, grid("k\nk\nk\nk"), 6, 1)
    return overlay(head, grid("ee"), 10, 5)


def _ear() -> tuple[str, ...]:
    return overlay(blob(5, 7, "g", "o", "l", "d"), blob(3, 4, "p", "p", "p", "p"), 1, 2)


def _eyes(closed: bool) -> tuple[str, ...]:
    base = tuple("." * 10 for _ in range(5))
    if closed:
        return overlay(overlay(base, grid("oooo"), 0, 3), grid("oooo"), 6, 3)
    eye = overlay(blob(4, 5, "e", "e"), grid("w"), 1, 1)
    return overlay(overlay(base, eye, 0, 0), eye, 6, 0)


def _limb(fill: str, h: int) -> tuple[str, ...]:
    return blob(3 if h == 8 else 4, h, fill, "o", "l" if fill == "g" else None, "d" if fill == "g" else None)


ZZZ, BOWL = sleep_and_eat_parts(27, 1, 26, 27)

PARTS = (
    Part("tail", 0, 19, _tail(), pivot=(13, 3), z=0),
    Part("wings", 1, 16, blob(30, 11, "m", "o", "M", "N"), z=1),
    Part("far_hind", 12, 23, _limb("d", 6), pivot=(2, 0), z=1),
    Part("far_front", 22, 20, _limb("d", 8), pivot=(1.5, 0), z=1),
    Part("body", 9, 14, _body(), z=2),
    Part("fold", 10, 19, blob(7, 8, "m", "N", "M", "N"), z=3),
    Part("near_hind", 9, 23, _limb("g", 6), pivot=(2, 0), z=3),
    Part("near_front", 19, 20, _limb("g", 8), pivot=(1.5, 0), z=3),
    Part("ear_l", 16, 0, _ear(), pivot=(2.5, 6), z=3),
    Part("ear_r", 24, 0, _ear(), pivot=(2.5, 6), z=3),
    Part("head", 16, 6, _head(), pivot=(6.5, 9), z=4),
    Part("eyes", 18, 9, _eyes(False), pivot=(5, 6), z=5),
    Part("eyes_closed", 18, 9, _eyes(True), pivot=(5, 6), z=5),
    ZZZ,
    BOWL,
)
FACE = ("head", "eyes", "eyes_closed", "ear_l", "ear_r")
LIMBS = ("far_hind", "far_front", "near_hind", "near_front")
ALL = tuple(p.name for p in PARTS if p.name not in ("zzz", "bowl"))


def _face(t: float, asleep: bool = False, dy: float = 0.0, angle: float = 0.0, ears: float = 0.0):
    shut = asleep or blink(t, 3.0)
    poses = {name: Pose(dy=dy, angle=angle) for name in FACE}
    poses["ear_l"] = Pose(dy=dy, angle=angle + ears)
    poses["ear_r"] = Pose(dy=dy, angle=angle - ears)
    poses["eyes"] = Pose(dy=dy, angle=angle, visible=not shut)
    poses["eyes_closed"] = Pose(dy=dy, angle=angle, visible=shut)
    return poses


def _limbs(swing: float) -> dict[str, Pose]:
    return {
        "near_front": Pose(angle=swing),
        "far_front": Pose(angle=-swing),
        "near_hind": Pose(angle=-swing),
        "far_hind": Pose(angle=swing),
    }


def pose(state: str, t: float) -> dict[str, Pose]:
    poses = fx_poses(state, t)
    poses["wings"] = Pose(visible=False)
    if state == "idle":
        poses.update(_face(t, dy=sine(t, 2.8, 0.4), angle=sine(t, 5, 4), ears=sine(t, 1.7, 6)))
        poses["body"] = Pose(sy=1 + sine(t, 2.8, 0.02))
        poses["tail"] = Pose(angle=sine(t, 2.2, 10))
    elif state == "walk":
        poses.update(_limbs(sine(t, 0.3, 30)))
        bob = abs(sine(t, 0.3, 0.9)) - 0.5
        poses.update(_face(t, dy=bob, ears=sine(t, 0.3, 8)))
        poses["body"] = Pose(dy=bob)
        poses["fold"] = Pose(dy=bob)
        poses["tail"] = Pose(angle=-8 + sine(t, 0.6, 10))
    elif state == "eat":
        poses.update(_face(t, dy=3 + sine(t, 0.35, 1.0), angle=5, ears=sine(t, 0.35, 6)))
        poses["near_front"] = Pose(angle=-45)
        poses["far_front"] = Pose(angle=-50)
        poses["tail"] = Pose(angle=sine(t, 1.4, 12))
    elif state == "sleep":
        poses.update(_face(t, asleep=True, dy=5, angle=10, ears=-30))
        poses["body"] = Pose(sy=0.93 + sine(t, 3.3, 0.015), dy=1.5)
        poses["tail"] = Pose(angle=40, dx=4, dy=-1)
    else:  # special: crouch, leap, glide on the spread membrane, land
        p = (t % 3.6) / 3.6
        height = 0.0
        if p < 0.15:
            poses["body"] = Pose(sy=0.85, dy=2)
            poses.update(_face(t, dy=3))
            poses["tail"] = Pose(angle=sine(t, 0.3, 10))
        else:
            if p < 0.3:
                height = -8 * (p - 0.15) / 0.15
            elif p < 0.8:
                height = -8 + sine(t, 0.9, 1.4)
            elif p < 0.95:
                height = -8 * (0.95 - p) / 0.15
            spread = 1.0 if p < 0.95 else 0.0
            poses["wings"] = Pose(sy=1 + sine(t, 0.5, 0.08), visible=spread > 0)
            poses["fold"] = Pose(visible=False)
            poses.update(_face(t, angle=sine(t, 1.8, 3), ears=-20))
            poses["body"] = Pose(angle=sine(t, 1.8, 4))
            poses.update(_limbs(0))
            poses["near_front"] = Pose(angle=-70)
            poses["far_front"] = Pose(angle=-75)
            poses["near_hind"] = Pose(angle=70)
            poses["far_hind"] = Pose(angle=75)
            poses["tail"] = Pose(angle=-12 + sine(t, 0.7, 8))
            lift(poses, ALL, dy=height)
    return poses


SPEC = PetSpec(
    key="sugar_glider",
    palette=PALETTE,
    parts=PARTS,
    pose=pose,
    move="scurry",
    speed=50,
    special_name="glide",
)
