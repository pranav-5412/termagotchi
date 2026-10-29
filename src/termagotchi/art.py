"""ASCII sprites for the pet."""

HAPPY = r"""
   /\_/\
  ( o.o )
   > ^ <
"""


def sprite() -> str:
    """Return the default sprite (more moods come on Day 4)."""
    return HAPPY.strip("\n")
