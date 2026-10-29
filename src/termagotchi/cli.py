"""Command line entry point for Termagotchi."""

import argparse

from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
from rich.table import Table

from termagotchi.art import display_name, species_keys, sprite
from termagotchi.pet import Pet


def choose_species(console: Console) -> str:
    """Show a numbered menu and return the chosen species key."""
    keys = species_keys()
    table = Table(title="Choose your pet", show_header=False, box=None)
    for number, key in enumerate(keys, start=1):
        table.add_row(f"[bold cyan]{number}[/]", display_name(key))
    console.print(table)
    choice = IntPrompt.ask(
        "Pick a number",
        choices=[str(n) for n in range(1, len(keys) + 1)],
        show_choices=False,
    )
    return keys[choice - 1]


def build_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(prog="termagotchi", description="A pet in your terminal.")
    parser.add_argument(
        "--pet",
        choices=species_keys(),
        help="skip the menu and use this species",
    )
    parser.add_argument("--name", help="skip the name prompt and use this name")
    return parser


def main() -> None:
    """Pick a pet, then show it in the terminal."""
    args = build_parser().parse_args()
    console = Console()
    species = args.pet or choose_species(console)
    name = args.name or Prompt.ask("Name your pet", default=display_name(species).split(" (")[0])
    pet = Pet(name=name, species=species)
    body = f"{sprite(species)}\n\n{pet.describe()}"
    console.print(Panel(body, title="Termagotchi", expand=False))


if __name__ == "__main__":
    main()
