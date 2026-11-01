"""Tests for pet speech quotes."""

import random

import pytest

from termagotchi.mood import MOODS
from termagotchi.quotes import QUOTES, pick


def test_every_mood_has_quotes_and_nothing_else_does():
    assert set(QUOTES) == set(MOODS)


@pytest.mark.parametrize("mood", MOODS)
def test_each_mood_has_several_distinct_quotes(mood):
    lines = QUOTES[mood]
    assert len(lines) >= 3
    assert len(set(lines)) == len(lines)


@pytest.mark.parametrize("mood", MOODS)
def test_pick_returns_a_line_for_that_mood(mood):
    assert pick(mood, random.Random(1)) in QUOTES[mood]


def test_pick_is_repeatable_with_a_seed():
    assert pick("happy", random.Random(7)) == pick("happy", random.Random(7))


def test_pick_rejects_an_unknown_mood():
    with pytest.raises(KeyError):
        pick("angry")
