"""Render a contact sheet of one pet's animation frames to a PNG, for checking by eye."""

import argparse

from PySide6.QtGui import QImage, QPainter

from termagotchi.pets import load_all
from termagotchi.sprites import STATES, Renderer

TIMES = (0.0, 0.25, 0.5, 0.75)


def contact_sheet(key: str, scale: int = 6) -> QImage:
    """Return a grid image: one row per state, one column per sample time."""
    renderer = Renderer(load_all()[key], scale)
    width, height = renderer.size
    sheet = QImage(width * len(TIMES), height * len(STATES), QImage.Format.Format_ARGB32)
    sheet.fill(0xFFE8E8E8)
    painter = QPainter(sheet)
    for row, state in enumerate(STATES):
        for col, t in enumerate(TIMES):
            painter.drawImage(col * width, row * height, renderer.snapshot(state, t))
    painter.end()
    return sheet


def main() -> None:
    parser = argparse.ArgumentParser(description="Save a pet animation contact sheet.")
    parser.add_argument("key")
    parser.add_argument("out")
    args = parser.parse_args()
    contact_sheet(args.key).save(args.out)


if __name__ == "__main__":
    main()
