"""Command line entry point for Termagotchi."""

from rich.console import Console
from rich.panel import Panel

from termagotchi.pet import Pet


def main() -> None:
    """Show the pet in the terminal."""
    console = Console()
    pet = Pet(name="Pixel")
    console.print(Panel(pet.describe(), title="Termagotchi", expand=False))


if __name__ == "__main__":
    main()
