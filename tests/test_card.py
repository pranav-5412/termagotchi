"""Tests for the terminal pet card."""

import pytest

pytest.importorskip("rich")

from rich.console import Console  # noqa: E402

from termagotchi import cli  # noqa: E402
from termagotchi.faces import face  # noqa: E402
from termagotchi.pet import Pet  # noqa: E402


def _card_text(pet: Pet) -> str:
    console = Console(record=True, width=80)
    console.print(cli.render_pet(pet))
    return console.export_text()


def test_card_shows_the_happy_face():
    assert face("happy") in _card_text(Pet("Zed"))


def test_card_shows_the_hungry_face():
    text = _card_text(Pet("Zed", hunger=90))
    assert face("hungry") in text
    assert "Zed is hungry" in text


def test_speak_prints_a_quote_for_the_mood():
    from termagotchi.quotes import QUOTES

    console = Console(record=True, width=80)
    quote = cli.speak(console, Pet("Zed", hunger=90))
    assert quote in QUOTES["hungry"]
    assert quote.split()[0] in console.export_text()


def test_animate_skips_when_not_a_terminal():
    console = Console(record=True, width=80)  # not a terminal under pytest
    assert cli.animate(console, Pet("Zed"), "feed") == 0
