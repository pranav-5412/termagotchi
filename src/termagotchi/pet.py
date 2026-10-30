"""The Pet model: a name plus four stats."""

from dataclasses import dataclass

from termagotchi.art import species_label


STAT_MIN = 0
STAT_MAX = 100


def clamp(value: int) -> int:
    """Limit a stat value to the range 0 to 100."""
    return max(STAT_MIN, min(STAT_MAX, value))


@dataclass
class Pet:
    """A virtual pet. Stats run from 0 to 100."""

    name: str
    species: str = "cat"
    age: int = 0
    hunger: int = 0  # 0 = full, 100 = starving
    happiness: int = 50
    energy: int = 100

    def __post_init__(self) -> None:
        """Clamp the starting stats."""
        self.adjust()

    def adjust(self, hunger: int = 0, happiness: int = 0, energy: int = 0) -> None:
        """Add deltas to the stats, then clamp each to 0 to 100."""
        self.hunger = clamp(self.hunger + hunger)
        self.happiness = clamp(self.happiness + happiness)
        self.energy = clamp(self.energy + energy)

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

    def feed(self) -> str:
        """Feed the pet: less hunger, a little more happiness."""
        self.adjust(hunger=-30, happiness=5)
        return f"{self.name} eats happily."

    def play(self) -> str:
        """Play with the pet: more happiness, more hunger, less energy."""
        self.adjust(hunger=10, happiness=20, energy=-15)
        return f"{self.name} plays with you."

    def sleep(self) -> str:
        """Let the pet sleep: restore energy, add a little hunger."""
        self.adjust(hunger=10, energy=50)
        return f"{self.name} takes a nap."

    def describe(self) -> str:
        """Return a one-line summary of the pet."""
        return f"{self.title} | {self.stats_line()}"
