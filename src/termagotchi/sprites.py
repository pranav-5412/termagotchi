"""Pixel-art sprite engine: a pet is a stack of parts, each posed per frame."""

from __future__ import annotations

import math
from dataclasses import dataclass, replace
from typing import Callable, Iterable

from PySide6.QtCore import QRectF
from PySide6.QtGui import QColor, QImage, QPainter

STATES = ("idle", "walk", "sleep", "eat", "special")
TRANSPARENT = "."


@dataclass(frozen=True)
class Pose:
    """Offset (in sprite cells), rotation (degrees), and scale of one part."""

    dx: float = 0.0
    dy: float = 0.0
    angle: float = 0.0
    sx: float = 1.0
    sy: float = 1.0
    visible: bool = True
    alpha: float = 1.0


@dataclass(frozen=True)
class Part:
    """A pixel grid placed at (x, y) on the canvas. Rotation pivots on `pivot`."""

    name: str
    x: int
    y: int
    rows: tuple[str, ...]
    pivot: tuple[float, float] | None = None
    z: int = 0

    @property
    def width(self) -> int:
        return len(self.rows[0])

    @property
    def height(self) -> int:
        return len(self.rows)

    @property
    def pivot_xy(self) -> tuple[float, float]:
        return self.pivot or (self.width / 2, self.height / 2)


PoseFn = Callable[[str, float], dict[str, Pose]]


@dataclass(frozen=True)
class PetSpec:
    """Everything the desktop needs to draw and move one species."""

    key: str
    palette: dict[str, str]
    parts: tuple[Part, ...]
    pose: PoseFn
    move: str = "walk"  # walk, hop, float, scurry, glide
    speed: float = 40.0  # pixels per second
    canvas: tuple[int, int] = (32, 32)
    special_name: str = "trick"


def grid(text: str) -> tuple[str, ...]:
    """Split pixel art into rows and right-pad them with transparent cells."""
    rows = text.strip("\n").split("\n")
    width = max(len(row) for row in rows)
    return tuple(row.ljust(width, TRANSPARENT) for row in rows)


def blob(
    w: int, h: int, fill: str, outline: str = "o", light: str | None = None, dark: str | None = None
) -> tuple[str, ...]:
    """Draw a shaded ellipse with a 1-pixel outline, lit from the upper left."""
    cx, cy = (w - 1) / 2, (h - 1) / 2

    def inside(x: int, y: int) -> bool:
        return ((x - cx) / (w / 2)) ** 2 + ((y - cy) / (h / 2)) ** 2 <= 1.0

    rows = []
    for y in range(h):
        row = ""
        for x in range(w):
            if not inside(x, y):
                row += TRANSPARENT
            elif any(not inside(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                row += outline
            else:
                v = -0.6 * (x - cx) / (w / 2) - 0.8 * (y - cy) / (h / 2)
                row += light if light and v > 0.45 else dark if dark and v < -0.45 else fill
        rows.append(row)
    return tuple(rows)


def overlay(base: tuple[str, ...], detail: tuple[str, ...], x: int, y: int) -> tuple[str, ...]:
    """Stamp detail onto base at (x, y). Transparent detail cells keep the base."""
    canvas = [list(row) for row in base]
    for dy, row in enumerate(detail):
        for dx, char in enumerate(row):
            if char != TRANSPARENT and 0 <= y + dy < len(canvas) and 0 <= x + dx < len(canvas[0]):
                canvas[y + dy][x + dx] = char
    return tuple("".join(row) for row in canvas)


def mirror(rows: tuple[str, ...]) -> tuple[str, ...]:
    """Flip a grid left to right."""
    return tuple(row[::-1] for row in rows)


# Shared effect colors: Z = sleep letters, B = bowl, K = kibble.
FX_PALETTE = {"Z": "#8fb8ff", "B": "#c0504d", "K": "#8a5a2b", "H": "#ffffff"}


def sleep_and_eat_parts(zx: int, zy: int, bx: int, by: int) -> tuple[Part, Part]:
    """Return the floating 'z' and the food bowl, placed at the given cells."""
    zzz = Part("zzz", zx, zy, grid("""
ZZZ
..Z
.Z.
ZZZ
"""), z=9)
    bowl = Part("bowl", bx, by, grid("""
.KKK.
BBBBB
.BBB.
"""), z=9)
    return zzz, bowl


def fx_poses(state: str, t: float) -> dict[str, Pose]:
    """Poses for the shared 'zzz' and 'bowl' parts."""
    return {
        "zzz": Pose(dy=-((t * 2) % 4), alpha=1 - ((t * 2) % 4) / 5, visible=state == "sleep"),
        "bowl": Pose(visible=state == "eat"),
    }


def sine(t: float, period: float, amp: float = 1.0, phase: float = 0.0) -> float:
    """Return amp * sin over a period given in seconds."""
    return amp * math.sin(2 * math.pi * (t / period + phase))


def blink(t: float, every: float = 3.2, length: float = 0.15) -> bool:
    """True while the eyes should be closed."""
    return (t % every) < length


def validate(spec: PetSpec) -> list[str]:
    """Return a list of problems with a spec (empty when it is sound)."""
    errors: list[str] = []
    width, height = spec.canvas
    names = {part.name for part in spec.parts}
    if len(names) != len(spec.parts):
        errors.append("duplicate part names")
    for part in spec.parts:
        if len({len(row) for row in part.rows}) != 1:
            errors.append(f"{part.name}: rows differ in length")
            continue
        bad = {c for row in part.rows for c in row} - set(spec.palette) - {TRANSPARENT}
        if bad:
            errors.append(f"{part.name}: colors not in palette {sorted(bad)}")
        if part.x < 0 or part.y < 0 or part.x + part.width > width or part.y + part.height > height:
            errors.append(f"{part.name}: outside the {width}x{height} canvas")
    for state in STATES:
        for t in (0.0, 0.4, 1.7):
            unknown = set(spec.pose(state, t)) - names
            if unknown:
                errors.append(f"{state}: poses for unknown parts {sorted(unknown)}")
    return errors


class Renderer:
    """Draws a PetSpec at an integer pixel scale."""

    def __init__(self, spec: PetSpec, scale: int = 4) -> None:
        self.spec = spec
        self.scale = scale
        self._images = {part.name: self._build(part) for part in spec.parts}
        self._order = sorted(spec.parts, key=lambda part: part.z)

    @property
    def size(self) -> tuple[int, int]:
        return self.spec.canvas[0] * self.scale, self.spec.canvas[1] * self.scale

    def _build(self, part: Part) -> QImage:
        image = QImage(part.width, part.height, QImage.Format.Format_ARGB32)
        image.fill(0)
        for y, row in enumerate(part.rows):
            for x, char in enumerate(row):
                if char != TRANSPARENT:
                    image.setPixelColor(x, y, QColor(self.spec.palette[char]))
        return image

    def draw(self, painter: QPainter, state: str, t: float, facing: int = 1) -> None:
        """Paint one frame. facing is 1 for right, -1 for left."""
        s = self.scale
        poses = self.spec.pose(state, t)
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, False)
        if facing < 0:
            painter.translate(self.size[0], 0)
            painter.scale(-1, 1)
        for part in self._order:
            pose = poses.get(part.name, Pose())
            if not pose.visible:
                continue
            px, py = part.pivot_xy
            painter.save()
            painter.translate((part.x + px + pose.dx) * s, (part.y + py + pose.dy) * s)
            painter.setOpacity(pose.alpha)
            painter.rotate(pose.angle)
            painter.scale(pose.sx, pose.sy)
            target = QRectF(-px * s, -py * s, part.width * s, part.height * s)
            painter.drawImage(target, self._images[part.name])
            painter.restore()
        painter.restore()

    def snapshot(self, state: str, t: float, facing: int = 1) -> QImage:
        """Render one frame to an image (used by tests and previews)."""
        width, height = self.size
        image = QImage(width, height, QImage.Format.Format_ARGB32)
        image.fill(0)
        painter = QPainter(image)
        self.draw(painter, state, t, facing)
        painter.end()
        return image


def lift(poses: dict[str, Pose], names: Iterable[str], dy: float = 0.0, dx: float = 0.0) -> None:
    """Shift the named parts by (dx, dy) cells on top of their current pose."""
    for name in names:
        pose = poses.get(name, Pose())
        poses[name] = replace(pose, dx=pose.dx + dx, dy=pose.dy + dy)
