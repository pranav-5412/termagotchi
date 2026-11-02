"""Mood: a pure function from the three stats to one word."""

MOODS = ("happy", "hungry", "sleepy", "sad")

HUNGRY_AT = 70  # hunger at or above this value
SLEEPY_AT = 25  # energy at or below this value
SAD_AT = 30  # happiness at or below this value


def mood(hunger: int, happiness: int, energy: int) -> str:
    """Return the pet's mood. The most urgent need wins: hungry, then sleepy, then sad."""
    if hunger >= HUNGRY_AT:
        return "hungry"
    if energy <= SLEEPY_AT:
        return "sleepy"
    if happiness <= SAD_AT:
        return "sad"
    return "happy"


MOOD_LABELS = {
    "happy": "feeling great",
    "hungry": "hungry",
    "sleepy": "sleepy",
    "sad": "sad",
}

# Rich style used to color the mood line on the terminal card.
MOOD_STYLES = {
    "happy": "green",
    "hungry": "yellow",
    "sleepy": "blue",
    "sad": "magenta",
}
