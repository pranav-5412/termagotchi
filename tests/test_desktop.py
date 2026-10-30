"""Tests for the desktop window's care actions."""

import random

import pytest
from PySide6.QtCore import QRect
from PySide6.QtWidgets import QApplication

from termagotchi.desktop import CARE_SECONDS, PetWindow
from termagotchi.pet import Pet
from termagotchi.sprites import Part, PetSpec, Pose


@pytest.fixture(scope="module")
def app():
    return QApplication.instance() or QApplication([])


def make_window(app) -> PetWindow:
    spec = PetSpec(
        "cat", {"#": "#ff8800"}, (Part("body", 4, 4, ("##", "##")),),
        lambda state, t: {"body": Pose()}, canvas=(16, 16),
    )
    pet = Pet(name="Tom", hunger=50, happiness=50, energy=50)
    return PetWindow(spec, QRect(0, 0, 800, 600), random.Random(1), pet)


def test_feed_lowers_hunger_and_shows_eating(app) -> None:
    window = make_window(app)
    window.care(window.pet.feed, "eat")
    assert window.pet.hunger == 20
    assert window.brain.state == "eat"
    assert window.brain.duration == CARE_SECONDS


def test_play_triggers_special_and_sleep_restores_energy(app) -> None:
    window = make_window(app)
    window.care(window.pet.play, "special")
    assert window.brain.state == "special"
    window.care(window.pet.sleep, "sleep")
    assert window.pet.energy == 85 and window.brain.state == "sleep"


def test_decay_ticks_stats(app) -> None:
    window = make_window(app)
    window.decay()
    assert window.pet.hunger == 54
