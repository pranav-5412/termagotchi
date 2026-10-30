"""Ghost: floating sheet ghost that spins and vanishes."""

import math

from termagotchi.sprites import (
    FX_PALETTE, Part, PetSpec, Pose, TRANSPARENT, blink, blob, fx_poses, grid, overlay, sine,
    sleep_and_eat_parts,
)

PALETTE = {
    **FX_PALETTE,
    "o": "#4a5575", "W": "#f6f8ff", "l": "#ffffff", "d": "#c9d3ee", "e": "#1a1d2b",
    "p": "#ffb0c8", "M": "#6b2238",
}

BODY_W, BODY_H, BODY_X, BODY_Y = 20, 26, 6, 4
CENTER_X = BODY_X + BODY_W / 2


def _body(phase: int) -> tuple[str, ...]:
    """Dome on top, scalloped hem below. phase slides the scallops sideways."""
    w, h = BODY_W, BODY_H
    radius = w / 2

    def bottom(x: int) -> int:
        return h - 5 + round(3.5 * abs(math.sin(math.pi * (x + phase + 0.5) / 5)))

    def inside(x: int, y: int) -> bool:
        if not 0 <= x < w or y < 0:
            return False
        if y < radius:
            return ((x - (w - 1) / 2) / radius) ** 2 + ((y - (radius - 1)) / radius) ** 2 <= 1.0
        return y <= bottom(x)

    rows = []
    for y in range(h):
        row = ""
        for x in range(w):
            if not inside(x, y):
                row += TRANSPARENT
            elif any(not inside(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                row += "o"
            else:
                v = -0.6 * (x - w / 2) / (w / 2) - 0.8 * (y - h / 2) / (h / 2)
                row += "l" if v > 0.5 else "d" if v < -0.35 else "W"
        rows.append(row)
    return tuple(rows)


def _eyes(closed: bool) -> tuple[str, ...]:
    base = tuple("." * 12 for _ in range(7))
    if closed:
        base = overlay(overlay(base, grid(".ee.\ne..e"), 1, 2), grid(".ee.\ne..e"), 7, 2)
    else:
        eye = overlay(blob(4, 6, "e", "e"), grid("l"), 1, 1)
        base = overlay(overlay(base, eye, 1, 0), eye, 7, 0)
    return overlay(overlay(base, grid("pp"), 0, 5), grid("pp"), 10, 5)


def _pv(x: int, y: int, py: float) -> tuple[float, float]:
    """Pivot on the ghost's vertical centerline so spins look like turning."""
    return CENTER_X - x, py - y


MOUTH_OPEN = blob(4, 5, "M", "e")
MOUTH_SHUT = grid("ee")
ARM = blob(5, 4, "W", "o", "l", "d")

ZZZ, BOWL = sleep_and_eat_parts(27, 1, 25, 27)

PARTS = (
    *(Part(f"body_{i}", BODY_X, BODY_Y, _body(i), pivot=_pv(BODY_X, BODY_Y, 13), z=1) for i in range(3)),
    Part("arm_l", 3, 17, ARM, pivot=(4, 1), z=2),
    Part("arm_r", 24, 17, ARM, pivot=(1, 1), z=2),
    Part("eyes", 10, 11, _eyes(False), pivot=_pv(10, 11, 13), z=3),
    Part("eyes_closed", 10, 11, _eyes(True), pivot=_pv(10, 11, 13), z=3),
    Part("mouth_open", 14, 19, MOUTH_OPEN, pivot=_pv(14, 19, 13), z=3),
    Part("mouth_shut", 15, 20, MOUTH_SHUT, pivot=_pv(15, 20, 13), z=3),
    ZZZ,
    BOWL,
)
BODIES = ("body_0", "body_1", "body_2")
FACE = ("eyes", "eyes_closed", "mouth_open", "mouth_shut")
SKIN = BODIES + FACE + ("arm_l", "arm_r")


def _ghost(
    t: float, hem_speed: float = 4.0, dy: float = 0.0, sx: float = 1.0, sy: float = 1.0,
    angle: float = 0.0, alpha: float = 1.0, asleep: bool = False, mouth_open: bool = False,
    arm_l: float = 0.0, arm_r: float = 0.0,
) -> dict[str, Pose]:
    """Pose the whole ghost: hem frame, face (hidden when turned away), arms."""
    frame = int(t * hem_speed) % 3
    front = sx > 0.05
    shut = asleep or blink(t, 4.0, 0.2)
    base = dict(dy=dy, sx=sx, sy=sy, angle=angle, alpha=alpha)
    poses = {name: Pose(visible=(i == frame), **base) for i, name in enumerate(BODIES)}
    poses["eyes"] = Pose(visible=front and not shut, **base)
    poses["eyes_closed"] = Pose(visible=front and shut, **base)
    poses["mouth_open"] = Pose(visible=front and mouth_open, **base)
    poses["mouth_shut"] = Pose(visible=front and not mouth_open, **base)
    poses["arm_l"] = Pose(dy=dy, angle=arm_l, alpha=alpha, sy=sy)
    poses["arm_r"] = Pose(dy=dy, angle=arm_r, alpha=alpha, sy=sy)
    return poses


def pose(state: str, t: float) -> dict[str, Pose]:
    poses = fx_poses(state, t)
    if state == "idle":
        poses.update(_ghost(t, dy=sine(t, 2.2, 0.8), arm_l=sine(t, 2.2, 10), arm_r=-sine(t, 2.2, 10)))
    elif state == "walk":
        poses.update(_ghost(t, hem_speed=8, dy=sine(t, 1.0, 0.6), angle=8, arm_l=-25, arm_r=-25))
    elif state == "eat":
        chew = (t % 0.5) < 0.25
        poses.update(_ghost(t, sy=1 + sine(t, 0.5, 0.05), mouth_open=chew, arm_l=20, arm_r=-20))
    elif state == "sleep":
        poses.update(_ghost(t, dy=sine(t, 3.2, 0.8), alpha=0.75 + sine(t, 3.2, 0.1), asleep=True,
                            arm_l=6, arm_r=-6))
    else:  # special: boo, spin twice while fading out, reappear
        p = (t % 3.2) / 3.2
        if p < 0.15:  # boo
            poses.update(_ghost(t, sx=1.06, sy=1.06, mouth_open=True, arm_l=125, arm_r=-125))
        elif p < 0.55:  # spin and fade out
            k = (p - 0.15) / 0.4
            poses.update(_ghost(t, hem_speed=10, dy=-3 * k, sx=math.cos(4 * math.pi * k),
                                alpha=max(0.0, 1 - k * 1.1), arm_l=60, arm_r=-60))
        elif p < 0.7:  # gone
            poses.update(_ghost(t, alpha=0.0))
        elif p < 0.9:  # fade back in
            k = (p - 0.7) / 0.2
            poses.update(_ghost(t, dy=-3 * (1 - k), alpha=k, mouth_open=k > 0.7,
                                arm_l=125 * k, arm_r=-125 * k))
        else:
            poses.update(_ghost(t, mouth_open=True, arm_l=125, arm_r=-125))
    return poses


SPEC = PetSpec(
    key="ghost",
    palette=PALETTE,
    parts=PARTS,
    pose=pose,
    move="float",
    speed=30,
    special_name="vanish",
)
