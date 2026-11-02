"""Speech bubbles: wrap a quote and draw it in a text box. No Qt or rich needed."""

from __future__ import annotations

import textwrap

DEFAULT_WIDTH = 28


def wrap_bubble(text: str, width: int = DEFAULT_WIDTH) -> list[str]:
    """Split text into lines of at most width characters, breaking at spaces."""
    if width < 4:
        raise ValueError("width must be at least 4")
    return textwrap.wrap(text, width=width) or [""]


def draw_bubble(text: str, width: int = DEFAULT_WIDTH) -> str:
    """Return the text inside a box with a small tail pointing down at the pet."""
    lines = wrap_bubble(text, width)
    inner = max(len(line) for line in lines)
    top = "." + "-" * (inner + 2) + "."
    body = [f"| {line:<{inner}} |" for line in lines]
    bottom = "'" + "-" * (inner + 2) + "'"
    tail = " " * 3 + "\\"
    return "\n".join([top, *body, bottom, tail])


class Bubble:
    """Tracks when a pet shows a quote: visible for a while, then quiet for a cooldown."""

    def __init__(self, show_seconds: float = 4.0, quiet_seconds: float = 20.0) -> None:
        self.show_seconds = show_seconds
        self.quiet_seconds = quiet_seconds
        self.text = ""
        self.age = 0.0
        self.quiet = quiet_seconds  # starts ready to speak

    @property
    def visible(self) -> bool:
        """True while a quote is on screen."""
        return bool(self.text)

    def can_speak(self) -> bool:
        """True when nothing is showing and the cooldown has passed."""
        return not self.visible and self.quiet >= self.quiet_seconds

    def say(self, text: str) -> bool:
        """Show text if allowed. Returns False when the pet is still quiet."""
        if not self.can_speak():
            return False
        self.text = text
        self.age = 0.0
        return True

    def update(self, dt: float) -> None:
        """Advance the clock by dt seconds: hide the quote when its time is up."""
        if self.visible:
            self.age += dt
            if self.age >= self.show_seconds:
                self.text = ""
                self.quiet = 0.0
        else:
            self.quiet += dt
