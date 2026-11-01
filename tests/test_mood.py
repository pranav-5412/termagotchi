"""Tests for the mood function."""

import pytest

from termagotchi.mood import HUNGRY_AT, MOODS, SAD_AT, SLEEPY_AT, mood


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
