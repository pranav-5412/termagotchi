"""The Pet model: a name plus four stats."""

from dataclasses import dataclass


@dataclass
class Pet:
    """A virtual pet. Stats run from 0 to 100."""

    name: str
    age: int = 0
    hunger: int = 0  # 0 = full, 100 = starving
    happiness: int = 50
    energy: int = 100

    def describe(self) -> str:
        """Return a one-line summary of the pet's stats."""
        return (
            f"{self.name} | age {self.age} | hunger {self.hunger} | "
            f"happiness {self.happiness} | energy {self.energy}"
        )
