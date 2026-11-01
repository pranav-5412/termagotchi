"""Short lines a pet says, grouped by mood."""

from __future__ import annotations

import random

QUOTES: dict[str, tuple[str, ...]] = {
    "happy": (
        "Life is good!",
        "Best day ever!",
        "Thanks for coding with me!",
        "I could do this all day.",
    ),
    "hungry": (
        "Feed me, please?",
        "My tummy is rumbling.",
        "Is it snack time yet?",
        "I smell commits and I want some.",
    ),
    "sleepy": (
        "So sleepy...",
        "Five more minutes?",
        "Time for a nap.",
        "My eyes are closing...",
    ),
    "sad": (
        "Play with me?",
        "I feel a little lonely.",
        "Did you forget about me?",
        "A hug would help.",
    ),
}


def pick(mood: str, rng: random.Random | None = None) -> str:
    """Return a random line for a mood. Raises KeyError for an unknown mood."""
    return (rng or random.Random()).choice(QUOTES[mood])
