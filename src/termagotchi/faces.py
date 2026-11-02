"""Little text faces for each mood, shown on the terminal card."""

from __future__ import annotations

from termagotchi.mood import MOOD_LABELS

FACES: dict[str, str] = {
    "happy": "(^_^)",
    "hungry": "(O_O)",
    "sleepy": "(-_-)",
    "sad": "(T_T)",
}


def face(mood: str) -> str:
    """Return the face for a mood (KeyError for an unknown mood)."""
    return FACES[mood]


def mood_text(name: str, mood: str) -> str:
    """Return the card line for a mood, such as '(O_O) Rex is hungry'."""
    return f"{face(mood)} {name} is {MOOD_LABELS[mood]}"
