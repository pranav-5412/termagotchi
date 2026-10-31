"""Shared four-legged template (not a species itself).

A `Look` describes shapes. `build` returns the parts and `make_pose` returns the pose function.
Palette letters every quadruped needs: o outline, a fill, l light, d dark, c belly, e eye, p accent.
Layout on the 32x32 canvas: legs end at y=29, the body sits on top of the legs, the head faces right
and ends at x=31.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass

from termagotchi.sprites import (
    Part, Pose, blink, blob, fx_poses, grid, lift, overlay, rect, sine, sleep_and_eat_parts,
)

GROUND = 29
LEG_TOP = 21


@dataclass(frozen=True)
class Look:
    """Shapes of one four-legged pet. Sizes are in sprite cells."""

    body: tuple[int, int] = (18, 9)
    head: tuple[int, int] = (12, 10)
    leg_w: int = 4
    ears: str = "round"  # round, point, long, floppy, none
    ear_size: tuple[int, int] = (4, 4)
    tail: str = "long"  # long, short, tuft, curl, none
    tail_size: tuple[int, int] = (3, 9)
    snout: tuple[int, int, str] | None = None  # width, height, fill letter
    belly: bool = True
    hoof: str | None = None  # letter for the bottom rows of the legs
    swing: float = 26.0


@dataclass(frozen=True)
class Layout:
    """Resolved positions for a Look."""

    look: Look
    bx: int
    by: int
    hx: int
    hy: int

    @property
    def neck(self) -> tuple[float, float]:
        """Point the head group tilts around."""
        return self.hx + 3.0, self.hy + self.look.head[1] - 1.0


def layout(look: Look) -> Layout:
    """Place body and head so the head ends at x=31 and the legs reach the ground."""
    bw, bh = look.body
    hw, hh = look.head
    hx = 32 - hw
    return Layout(look, max(0, hx + 3 - bw), LEG_TOP + 2 - bh, hx, LEG_TOP + 2 - bh + 4 - hh)


def _belly(rows: tuple[str, ...], letter: str) -> tuple[str, ...]:
    h, w = len(rows), len(rows[0])
    out = []
    for y, row in enumerate(rows):
        out.append("".join(
            letter if y >= h - 3 and 2 <= x <= w - 3 and ch not in ".o" else ch
            for x, ch in enumerate(row)
        ))
    return tuple(out)


def _ear(kind: str, w: int, h: int) -> tuple[str, ...]:
    if kind == "point":
        rows = []
        for y in range(h):
            n = max(1, round((y + 1) * w / h))
            row = "o" if n == 1 else "o" + "a" * (n - 2) + "o"
            rows.append(row.center(w, "."))
        return tuple(rows)
    if kind == "long":
        return rect(w, h, "a", "o", "l", "p")
    if kind == "floppy":
        return rect(w, h, "d", "o", "a", "d")
    return blob(w, h, "a", "o", "l", "d")


def _tail(kind: str, w: int, h: int) -> tuple[str, ...]:
    if kind == "tuft":
        return overlay(blob(w, h, "a", "o", "l", "d"), blob(w, max(3, h // 3), "p", "o"), 0, h - max(3, h // 3))
    if kind == "curl":
        return grid(".oo.\no..o\no.po\n.oo.")
    return blob(w, h, "a", "o", "l", "d")


def _leg(look: Look, h: int, far: bool) -> tuple[str, ...]:
    fill = "d" if far else "a"
    rows = list(rect(look.leg_w, h, fill, "o", None if far else "l", "d"))
    if look.hoof:
        for y in range(h - 2, h - 1):
            rows[y] = "o" + look.hoof * (look.leg_w - 2) + "o"
    return tuple(rows)


def _eyes(look: Look) -> tuple[tuple[str, ...], tuple[str, ...]]:
    w = max(5, look.head[0] - 5)
    mid = "." * (w - 2)
    return grid(f"e{mid}e\ne{mid}e"), grid(f"{'.' * w}\noo{'.' * (w - 4)}oo\n{'.' * w}")


def build(
    look: Look,
    head_parts: tuple[Part, ...] = (),
    body_parts: tuple[Part, ...] = (),
    ears_behind: bool = True,
) -> tuple[tuple[Part, ...], tuple[str, ...], tuple[str, ...]]:
    """Return (parts, head group names, body group names). Extra parts must keep unique names."""
    lay = layout(look)
    bw, bh = look.body
    hw, hh = look.head
    nx, ny = lay.neck
    leg_h = GROUND - LEG_TOP
    body = blob(bw, bh, "a", "o", "l", "d")
    if look.belly:
        body = _belly(body, "c")
    head = blob(hw, hh, "a", "o", "l", "d")
    eyes, closed = _eyes(look)
    ex, ey = lay.hx + 3, lay.hy + hh // 3 + 1
    back_x = lay.bx + 3
    front_x = lay.bx + bw - look.leg_w - 2
    parts: list[Part] = [
        Part("far_back", back_x - 3, LEG_TOP, _leg(look, leg_h, True), pivot=(look.leg_w / 2, 0), z=1),
        Part("far_front", front_x - 3, LEG_TOP, _leg(look, leg_h, True), pivot=(look.leg_w / 2, 0), z=1),
        Part("body", lay.bx, lay.by, body, z=2),
        Part("near_back", back_x, LEG_TOP, _leg(look, leg_h, False), pivot=(look.leg_w / 2, 0), z=3),
        Part("near_front", front_x, LEG_TOP, _leg(look, leg_h, False), pivot=(look.leg_w / 2, 0), z=3),
        Part("head", lay.hx, lay.hy, head, pivot=(nx - lay.hx, ny - lay.hy), z=4),
        Part("eyes", ex, ey, eyes, pivot=(nx - ex, ny - ey), z=5),
        Part("eyes_closed", ex, ey, closed, pivot=(nx - ex, ny - ey), z=5),
    ]
    head_names = ["head", "eyes", "eyes_closed"]
    if look.ears != "none":
        ew, eh = look.ear_size
        rows = _ear(look.ears, ew, eh)
        for name, x in (("ear_far", lay.hx + 1), ("ear_near", lay.hx + hw - ew - 1)):
            y = lay.hy - eh + (4 if look.ears == "floppy" else 2)
            if look.ears == "floppy":
                x += -1 if name == "ear_far" else 1
            parts.append(Part(name, x, max(0, y), rows, pivot=(nx - x, ny - max(0, y)), z=3 if ears_behind else 6))
            head_names.append(name)
    if look.snout:
        sw, sh, fill = look.snout
        sx, sy = 32 - sw, lay.hy + hh - sh - 1
        parts.append(Part("snout", sx, sy, blob(sw, sh, fill, "o", None, None), pivot=(nx - sx, ny - sy), z=5))
        head_names.append("snout")
    if look.tail != "none":
        tw, th = look.tail_size
        if look.tail == "curl":
            tw, th = 4, 4
        tx, ty = max(0, lay.bx - tw + 2), lay.by + 1
        parts.append(Part("tail", tx, ty, _tail(look.tail, tw, th), pivot=(tw - 1, 1), z=0))
    body_names = []
    for part in head_parts:
        parts.append(Part(part.name, part.x, part.y, part.rows, pivot=(nx - part.x, ny - part.y), z=part.z))
        head_names.append(part.name)
    for part in body_parts:
        parts.append(part)
        body_names.append(part.name)
    zzz, bowl = sleep_and_eat_parts(max(0, lay.hx - 2), 1, 26, 27)
    parts += [zzz, bowl]
    return tuple(parts), tuple(head_names), tuple(body_names)


LEGS = ("near_front", "far_front", "near_back", "far_back")
SpecialFn = Callable[[dict[str, Pose], float, "Rig"], None]


@dataclass(frozen=True)
class Rig:
    """Names of the parts that move together, handed to special moves."""

    head: tuple[str, ...]
    body: tuple[str, ...]
    look: Look
    has_tail: bool

    @property
    def everything(self) -> tuple[str, ...]:
        tail = ("tail",) if self.has_tail else ()
        return (*self.head, "body", *LEGS, *self.body, *tail)


def _face(rig: Rig, t: float, asleep: bool = False, dy: float = 0.0, angle: float = 0.0,
          dx: float = 0.0) -> dict[str, Pose]:
    shut = asleep or blink(t)
    poses = {name: Pose(dx=dx, dy=dy, angle=angle) for name in rig.head}
    poses["eyes"] = Pose(dx=dx, dy=dy, angle=angle, visible=not shut)
    poses["eyes_closed"] = Pose(dx=dx, dy=dy, angle=angle, visible=shut)
    return poses


def make_pose(head: tuple[str, ...], body: tuple[str, ...], look: Look, special: SpecialFn,
              wag: float = 12.0, bob: float = 0.6) -> Callable[[str, float], dict[str, Pose]]:
    """Build the pose function: shared idle, walk, eat and sleep plus the pet's own special."""
    rig = Rig(head, body, look, look.tail != "none")

    def pose(state: str, t: float) -> dict[str, Pose]:
        poses = fx_poses(state, t)
        tail = rig.has_tail
        if state == "walk":
            swing = sine(t, 0.6, look.swing)
            for leg, sign in zip(LEGS, (1, -1, -1, 1)):
                poses[leg] = Pose(angle=sign * swing)
            poses.update(_face(rig, t, dy=abs(sine(t, 0.6, bob)) - bob / 2))
            poses["body"] = Pose(dy=abs(sine(t, 0.6, bob)) - bob / 2)
            lift(poses, rig.body, dy=abs(sine(t, 0.6, bob)) - bob / 2)
            if tail:
                poses["tail"] = Pose(angle=-8 + sine(t, 0.6, wag / 2))
        elif state == "eat":
            poses.update(_face(rig, t, dy=3 + sine(t, 0.5, 1.2), angle=sine(t, 0.5, 5)))
            if tail:
                poses["tail"] = Pose(angle=sine(t, 1.6, wag))
        elif state == "sleep":
            poses.update(_face(rig, t, asleep=True, dy=3, angle=8))
            poses["body"] = Pose(sy=0.95 + sine(t, 3.5, 0.015), dy=1)
            lift(poses, rig.body, dy=1)
            if tail:
                poses["tail"] = Pose(angle=14)
        else:
            poses.update(_face(rig, t, dy=sine(t, 3, 0.4)))
            poses["body"] = Pose(sy=1 + sine(t, 3, 0.02))
            if tail:
                poses["tail"] = Pose(angle=sine(t, 2.4, wag))
            if state == "special":
                special(poses, t, rig)
        return poses

    return pose


def hop_all(poses: dict[str, Pose], rig: Rig, dy: float, dx: float = 0.0) -> None:
    """Lift every part together by dy (negative is up)."""
    lift(poses, rig.everything, dy=dy, dx=dx)


def arc(p: float) -> float:
    """0 to 1 to 0 over p in 0..1 (a jump arc)."""
    return math.sin(math.pi * min(max(p, 0.0), 1.0))
