"""Terminal animations: a header line that changes each frame above the sprite. No rich needed."""

from __future__ import annotations

EAT_FRAMES = (
    "        o",
    "       o",
    "      o",
    "    *nom*",
    "   *nom nom*",
)
PLAY_FRAMES = (
    "o",
    "  o",
    "    o",
    "  o",
    "o",
)
SLEEP_FRAMES = (
    "z",
    "z Z",
    "z Z z",
    "z Z z Z",
)

ACTIONS = ("feed", "play", "sleep")


def eat_frames() -> tuple[str, ...]:
    """Food drops toward the pet, then the pet chews."""
    return EAT_FRAMES


def play_frames() -> tuple[str, ...]:
    """A ball bounces back and forth."""
    return PLAY_FRAMES


def sleep_frames() -> tuple[str, ...]:
    """Zs pile up above a sleeping pet."""
    return SLEEP_FRAMES


def frames_for(action: str) -> tuple[str, ...]:
    """Return the header frames for feed, play, or sleep (KeyError otherwise)."""
    return {"feed": eat_frames, "play": play_frames, "sleep": sleep_frames}[action]()


def compose(header: str, art: str) -> str:
    """Put a header line above the sprite art."""
    return f"{header}\n{art}"
