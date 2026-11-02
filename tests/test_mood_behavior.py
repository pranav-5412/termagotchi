"""Tests for mood-driven pet behavior."""

import random
from collections import Counter

import pytest

from termagotchi.behavior import CHOICES, MOOD_WEIGHTS, Brain, weights_for
from termagotchi.mood import MOODS


def test_every_mood_has_weights_for_known_states():
    assert set(MOOD_WEIGHTS) == set(MOODS)
    for boosts in MOOD_WEIGHTS.values():
        assert set(boosts) <= set(CHOICES)


@pytest.mark.parametrize("mood", MOODS)
def test_weights_cover_every_state_and_stay_positive(mood):
    weights = weights_for(mood)
    assert set(weights) == set(CHOICES)
    assert all(value > 0 for value in weights.values())


def test_hungry_pets_favor_eating_over_the_default():
    assert weights_for("hungry")["eat"] > weights_for("happy")["eat"]


def test_sleepy_pets_favor_sleeping():
    assert weights_for("sleepy")["sleep"] > weights_for("happy")["sleep"]


def test_sad_pets_rarely_do_tricks():
    assert weights_for("sad")["special"] < CHOICES["special"][0]
