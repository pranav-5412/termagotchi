"""Speech bubbles: wrap a quote and draw it in a text box. No Qt or rich needed."""

from __future__ import annotations

import textwrap

DEFAULT_WIDTH = 28


def wrap_bubble(text: str, width: int = DEFAULT_WIDTH) -> list[str]:
    """Split text into lines of at most width characters, breaking at spaces."""
    if width < 4:
        raise ValueError("width must be at least 4")
    return textwrap.wrap(text, width=width) or [""]
