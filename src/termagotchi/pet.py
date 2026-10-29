"""The Pet model: a name plus four stats."""

from dataclasses import dataclass

from termagotchi.art import species_label


@dataclass
class Pet:
    """A virtual pet. Stats run from 0 to 100."""

    name: str
    species: str = "cat"
    age: int = 0
    hunger: int = 0  # 0 = full, 100 = starving
    happiness: int = 50
    energy: int = 100

    @property
    def title(self) -> str:
        """Return the name with the species, such as 'Zed the Star Knight'."""
        return f"{self.name} the {species_label(self.species)}"

    def stats_line(self) -> str:
        """Return the stats as one line."""
        return (
            f"age {self.age} | hunger {self.hunger} | "
            f"happiness {self.happiness} | energy {self.energy}"
        )

    def describe(self) -> str:
        """Return a one-line summary of the pet."""
        return f"{self.title} | {self.stats_line()}"
