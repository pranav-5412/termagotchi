"""Alien: little green alien that gets beamed up by a UFO."""

import math

from termagotchi.sprites import (
    FX_PALETTE, Part, PetSpec, Pose, blink, blob, fx_poses, grid, lift, overlay, sine,
    sleep_and_eat_parts,
)

PALETTE = {
    **FX_PALETTE,
    "o": "#10351c", "g": "#58d36e", "l": "#9cf0a8", "d": "#2f9a4a", "e": "#06100a",
    "w": "#ffffff", "Y": "#ffe45c", "U": "#9aa7b8", "V": "#5c6878", "G": "#7be0ff",
    "B": "#66f6ffb0",
}


def _almond(rows: tuple[str, ...], shift_sign: int, x: int, width: int) -> list[str]:
    """Place a blob into rows of the given width, slanting it like an alien eye."""
    out = []
    for y, row in enumerate(rows):
        shift = shift_sign * round((y - 4) / 2.5)
        cells = ["."] * width
        for dx, char in enumerate(row):
            if char != "." and 0 <= x + shift + dx < width:
                cells[x + shift + dx] = char
        out.append("".join(cells))
    return out


def _eyes() -> tuple[str, ...]:
    eye = overlay(blob(7, 9, "e", "e"), grid("ww\nww"), 1, 1)
    left = _almond(eye, 1, 2, 20)
    right = _almond(eye, -1, 11, 20)
    return tuple("".join(b if b != "." else a for a, b in zip(l_row, r_row)) for l_row, r_row in zip(left, right))


def _eyes_closed() -> tuple[str, ...]:
    base = tuple("." * 20 for _ in range(9))
    return overlay(overlay(base, grid("eeeeeee"), 2, 5), grid("eeeeeee"), 11, 5)


ANTENNA = grid("""
YY
YY
dd
d.
d.
dd
""")
BEAM = tuple(
    "".join("B" if abs(x - 9.5) <= 5 + 5 * y / 30 else "." for x in range(20)) for y in range(31)
)
UFO = overlay(blob(24, 6, "U", "V", "U", "V"), blob(10, 4, "G", "V", "w", "G"), 7, 0)

ZZZ, BOWL = sleep_and_eat_parts(27, 2, 25, 27)

PARTS = (
    Part("beam", 6, 0, BEAM, pivot=(10, 0), z=0),
    Part("ufo", 4, 0, UFO, z=9),
    Part("antenna_l", 10, 1, ANTENNA, pivot=(1, 5), z=1),
    Part("antenna_r", 20, 1, ANTENNA, pivot=(1, 5), z=1),
    Part("leg_l", 12, 27, blob(4, 5, "g", "o", "l", "d"), pivot=(2, 0), z=1),
    Part("leg_r", 16, 27, blob(4, 5, "g", "o", "l", "d"), pivot=(2, 0), z=1),
    Part("body", 11, 19, overlay(blob(10, 10, "g", "o", "l", "d"), grid("Y"), 4, 4), z=2),
    Part("arm_l", 8, 20, blob(3, 8, "g", "o", "l", "d"), pivot=(1.5, 1), z=3),
    Part("arm_r", 21, 20, blob(3, 8, "g", "o", "l", "d"), pivot=(1.5, 1), z=3),
    Part("head", 6, 4, blob(20, 17, "g", "o", "l", "d"), pivot=(10, 14), z=4),
    Part("eyes", 6, 9, _eyes(), pivot=(10, 9), z=5),
    Part("eyes_closed", 6, 9, _eyes_closed(), pivot=(10, 9), z=5),
    Part("mouth", 14, 18, grid("ee"), pivot=(2, -3), z=5),
    ZZZ,
    BOWL,
)
HEAD = ("head", "eyes", "eyes_closed", "mouth", "antenna_l", "antenna_r")
BODY = ("body", "arm_l", "arm_r", "leg_l", "leg_r")
CREATURE = HEAD + BODY


def _head(t: float, asleep: bool = False, dy: float = 0.0, angle: float = 0.0, sway: float = 0.0):
    shut = asleep or blink(t, 3.4, 0.2)
    poses = {name: Pose(dy=dy, angle=angle) for name in ("head", "mouth")}
    poses["eyes"] = Pose(dy=dy, angle=angle, visible=not shut)
    poses["eyes_closed"] = Pose(dy=dy, angle=angle, visible=shut)
    poses["antenna_l"] = Pose(dy=dy, angle=angle + sway)
    poses["antenna_r"] = Pose(dy=dy, angle=angle - sway * 0.8)
    return poses


def pose(state: str, t: float) -> dict[str, Pose]:
    poses = fx_poses(state, t)
    poses["beam"] = Pose(visible=False)
    poses["ufo"] = Pose(visible=False)
    if state == "idle":
        poses.update(_head(t, dy=sine(t, 2.8, 0.5), angle=sine(t, 5, 3), sway=sine(t, 1.8, 10)))
        poses["arm_l"] = Pose(angle=sine(t, 2.8, 5))
        poses["arm_r"] = Pose(angle=-sine(t, 2.8, 5))
        poses["body"] = Pose(sy=1 + sine(t, 2.8, 0.02))
    elif state == "walk":
        step = sine(t, 0.6, 1.0)
        bob = -abs(step) * 0.8
        poses.update(_head(t, dy=bob, angle=8 * step, sway=sine(t, 0.6, 20, 0.25)))
        poses["leg_l"] = Pose(dy=-max(0.0, step) * 1.5)
        poses["leg_r"] = Pose(dy=-max(0.0, -step) * 1.5)
        poses["arm_l"] = Pose(angle=-20 * step, dy=bob)
        poses["arm_r"] = Pose(angle=20 * step, dy=bob)
        lift(poses, ("body",), dy=bob)
    elif state == "eat":
        poses.update(_head(t, dy=3 + sine(t, 0.4, 0.8), angle=6, sway=-18))
        poses["arm_l"] = Pose(angle=25)
        poses["arm_r"] = Pose(angle=-25)
    elif state == "sleep":
        poses.update(_head(t, asleep=True, dy=3, angle=7, sway=-30))
        poses["arm_l"] = Pose(angle=5)
        poses["arm_r"] = Pose(angle=-5)
        lift(poses, ("body",), dy=1)
    else:  # special: UFO arrives, beam lifts the alien, alien dangles, set back down
        p = (t % 4.5) / 4.5
        rise = 0.0
        ufo_dy = -10.0
        beam_alpha = 0.0
        if p < 0.12:  # UFO descends into place
            ufo_dy = -10 - 12 * (1 - p / 0.12)
        elif p < 0.2:
            beam_alpha = (p - 0.12) / 0.08
        elif p < 0.8:
            beam_alpha = 1.0
            rise = min(1.0, (p - 0.2) / 0.1) if p < 0.7 else (0.8 - p) / 0.1
        elif p < 0.88:
            beam_alpha = (0.88 - p) / 0.08
        else:
            ufo_dy = -10 - 12 * ((p - 0.88) / 0.12)
        poses["ufo"] = Pose(dy=ufo_dy)
        if beam_alpha > 0:
            flicker = 0.75 + sine(t, 0.15, 0.25)
            poses["beam"] = Pose(dy=-5, sy=1.19, alpha=beam_alpha * flicker)
        floating = -6 * rise + sine(t, 1.2, 0.8) * rise
        poses.update(_head(t, dy=floating, angle=0, sway=sine(t, 0.8, 18)))
        poses["arm_l"] = Pose(angle=40 + sine(t, 0.7, 20) * rise, dy=floating)
        poses["arm_r"] = Pose(angle=-40 - sine(t, 0.7, 20) * rise, dy=floating)
        poses["leg_l"] = Pose(angle=sine(t, 0.9, 18) * rise, dy=floating)
        poses["leg_r"] = Pose(angle=-sine(t, 0.9, 18) * rise, dy=floating)
        lift(poses, ("body",), dy=floating)
    return poses


SPEC = PetSpec(
    key="alien",
    palette=PALETTE,
    parts=PARTS,
    pose=pose,
    move="walk",
    speed=36,
    special_name="abduction",
)
