"""Command line entry point for Termagotchi."""

from rich.console import Console
from rich.panel import Panel

from termagotchi.art import sprite
from termagotchi.pet import Pet


def main() -> None:
    """Show the pet in the terminal."""
    console = Console()
    pet = Pet(name="Pixel")
    body = f"{sprite()}\n\n{pet.describe()}"
    console.print(Panel(body, title="Termagotchi", expand=False))


if __name__ == "__main__":
    main()
