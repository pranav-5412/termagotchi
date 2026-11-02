"""Little text faces for each mood, shown on the terminal card."""

from __future__ import annotations

FACES: dict[str, str] = {
    "happy": "(^_^)",
    "hungry": "(O_O)",
    "sleepy": "(-_-)",
    "sad": "(T_T)",
}


def face(mood: str) -> str:
    """Return the face for a mood (KeyError for an unknown mood)."""
    return FACES[mood]
