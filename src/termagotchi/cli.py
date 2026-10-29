"""Command line entry point for Termagotchi."""

import argparse

from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
from rich.table import Table
from rich.text import Text

from termagotchi.art import color, display_name, species_keys, species_label, sprite
from termagotchi.pet import Pet


def choose_species(console: Console) -> str:
    """Show a numbered, colored menu and return the chosen species key."""
    keys = species_keys()
    table = Table(title="Choose your pet", show_header=False, box=box.ROUNDED, padding=(0, 2))
    table.add_column(justify="right", style="bold")
    table.add_column()
    for number, key in enumerate(keys, start=1):
        table.add_row(str(number), Text(display_name(key), style=color(key)))
    console.print(Align.center(table))
    choice = IntPrompt.ask(
        "Pick a number",
        choices=[str(n) for n in range(1, len(keys) + 1)],
        show_choices=False,
    )
    return keys[choice - 1]


def render_pet(pet: Pet) -> Panel:
    """Build the pet card: sprite, name, and stats."""
    style = color(pet.species)
    body = Group(
        Align.center(Text(sprite(pet.species), style=style, no_wrap=True)),
        Text(""),
        Align.center(Text(pet.title, style=f"bold {style}")),
        Align.center(Text(pet.stats_line(), style="dim")),
    )
    return Panel(
        body,
        title="Termagotchi",
        border_style=style,
        box=box.ROUNDED,
        padding=(1, 4),
        expand=False,
    )


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
    name = args.name or Prompt.ask("Name your pet", default=species_label(species))
    console.print(render_pet(Pet(name=name, species=species)))


if __name__ == "__main__":
    main()
