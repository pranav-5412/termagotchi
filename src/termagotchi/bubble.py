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
