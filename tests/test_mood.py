"""Tests for the mood function."""

from dataclasses import asdict

import pytest

from termagotchi.mood import HUNGRY_AT, MOODS, SAD_AT, SLEEPY_AT, mood
from termagotchi.pet import Pet


def test_fresh_pet_is_happy():
    assert mood(0, 50, 100) == "happy"


@pytest.mark.parametrize(
    ("hunger", "happiness", "energy", "expected"),
    [
        (HUNGRY_AT, 50, 100, "hungry"),
        (HUNGRY_AT - 1, 50, 100, "happy"),
        (0, 50, SLEEPY_AT, "sleepy"),
        (0, 50, SLEEPY_AT + 1, "happy"),
        (0, SAD_AT, 100, "sad"),
        (0, SAD_AT + 1, 100, "happy"),
    ],
)
def test_thresholds(hunger, happiness, energy, expected):
    assert mood(hunger, happiness, energy) == expected


def test_hungry_beats_sleepy_and_sad():
    assert mood(100, 0, 0) == "hungry"


def test_sleepy_beats_sad():
    assert mood(0, 0, 0) == "sleepy"


def test_every_mood_can_happen_and_nothing_else_does():
    seen = {
        mood(hunger, happiness, energy)
        for hunger in range(0, 101, 5)
        for happiness in range(0, 101, 5)
        for energy in range(0, 101, 5)
    }
    assert seen == set(MOODS)


def test_pet_mood_follows_its_stats():
    pet = Pet("Zed")
    assert pet.mood == "happy"
    pet.adjust(hunger=100)
    assert pet.mood == "hungry"
    pet.feed()
    pet.feed()
    assert pet.mood == "happy"


def test_pet_mood_sleepy_and_sad():
    assert Pet("Zed", energy=10).mood == "sleepy"
    assert Pet("Zed", happiness=10).mood == "sad"


def test_mood_is_not_saved_as_a_field():
    assert "mood" not in asdict(Pet("Zed"))
