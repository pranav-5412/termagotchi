"""Desktop mode: pets walk around the bottom of the screen in transparent windows."""

from __future__ import annotations

import math
import random
import sys
import time
from typing import Callable

from PySide6.QtCore import QPoint, Qt, QTimer
from PySide6.QtGui import QContextMenuEvent, QMouseEvent, QPainter
from PySide6.QtWidgets import QApplication, QMenu, QWidget

from termagotchi.art import species_label
from termagotchi.behavior import Brain
from termagotchi.pet import Pet
from termagotchi.pets import load_all
from termagotchi.sprites import PetSpec, Renderer

SCALE = 4
HEADROOM = 40  # extra window height so hopping and floating pets are not clipped
FRAME_MS = 33
DECAY_MS = 15_000  # one stat tick every 15 seconds
CARE_SECONDS = 3.0  # how long a pet shows a care animation


def vertical_offset(spec: PetSpec, state: str, t: float) -> float:
    """Extra window lift in pixels for the species' movement style."""
    if spec.move == "hop" and state == "walk":
        return abs(math.sin(t * 7)) * 24
    if spec.move == "float":
        return 18 + math.sin(t * 2) * 8
    return 0.0


class PetWindow(QWidget):
    """A small frameless, transparent, always-on-top window holding one pet."""

    def __init__(
        self,
        spec: PetSpec,
        screen_rect,
        rng: random.Random | None = None,
        pet: Pet | None = None,
    ) -> None:
        super().__init__(
            None,
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool,
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.spec = spec
        self.pet = pet or Pet(name=species_label(spec.key), species=spec.key)
        self.renderer = Renderer(spec, SCALE)
        width, height = self.renderer.size
        self.setFixedSize(width, height + HEADROOM)
        self.ground = screen_rect.bottom() - height + 2
        self.brain = Brain(screen_rect.left(), screen_rect.right() - width, spec.speed, rng)
        if spec.move == "scurry":
            self.brain.speed *= 1.8
        self.clock = 0.0
        self._last = time.monotonic()
        self._grab: QPoint | None = None
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.tick)
        self._timer.start(FRAME_MS)
        self._decay_timer = QTimer(self)
        self._decay_timer.timeout.connect(self.decay)
        self._decay_timer.start(DECAY_MS)
        self.tick()

    def tick(self) -> None:
        """Advance the brain and move the window."""
        now = time.monotonic()
        dt = min(now - self._last, 0.25)
        self._last = now
        self.clock += dt
        self.brain.update(dt)
        if self._grab is None:
            lift = vertical_offset(self.spec, self.brain.state, self.clock)
            self.move(round(self.brain.x), round(self.ground - lift - HEADROOM))
        self.update()

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:  # noqa: N802
        """Right-click menu: stats, care actions, and quit."""
        menu = QMenu(self)
        menu.addAction(self.pet.title).setEnabled(False)
        menu.addAction(self.pet.stats_line()).setEnabled(False)
        menu.addSeparator()
        for label, act, state in (
            ("Feed", self.pet.feed, "eat"),
            (f"Play ({self.spec.special_name})", self.pet.play, "special"),
            ("Sleep", self.pet.sleep, "sleep"),
        ):
            menu.addAction(label, lambda act=act, state=state: self.care(act, state))
        menu.addSeparator()
        menu.addAction("Hide this pet", self.close)
        menu.addAction("Quit all", QApplication.quit)
        menu.exec(event.globalPos())

    def care(self, action: Callable[[], str], state: str) -> None:
        """Apply a care action to the stats and show it on screen."""
        action()
        self.brain.set_state(state, CARE_SECONDS)

    def decay(self) -> None:
        """Slowly age the stats while the pet lives on the desktop."""
        self.pet.tick()

    def paintEvent(self, event) -> None:  # noqa: N802 (Qt API name)
        painter = QPainter(self)
        painter.translate(0, HEADROOM)
        self.renderer.draw(painter, self.brain.state, self.clock, self.brain.facing)
        painter.end()

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            self._grab = event.position().toPoint()
            self.brain.held = True

    def mouseMoveEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if self._grab is not None:
            self.move(event.globalPosition().toPoint() - self._grab)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton and self._grab is not None:
            self._grab = None
            self.brain.x = min(max(self.x(), self.brain.left), self.brain.right)
            self.brain.held = False
            self.brain.set_state("idle", 1.0)


def run(keys: list[str] | None = None) -> int:
    """Open one window per pet key (all registered pets when keys is empty)."""
    specs = load_all()
    keys = keys or list(specs)
    unknown = [key for key in keys if key not in specs]
    if unknown:
        print(f"No desktop sprite yet for: {', '.join(unknown)}. Available: {', '.join(specs)}")
        return 2
    app = QApplication.instance() or QApplication(sys.argv)
    rect = app.primaryScreen().availableGeometry()
    windows = [PetWindow(specs[key], rect) for key in keys]
    for window in windows:
        window.show()
    return app.exec()


def main() -> None:
    sys.exit(run(sys.argv[1:]))


if __name__ == "__main__":
    main()
