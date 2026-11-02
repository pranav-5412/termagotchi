"""Tests for speech bubbles."""

import pytest

from termagotchi.bubble import wrap_bubble


def test_short_text_stays_on_one_line():
    assert wrap_bubble("Hi there") == ["Hi there"]


def test_long_text_wraps_within_the_width():
    lines = wrap_bubble("I could do this all day and then some more", width=16)
    assert len(lines) > 1
    assert all(len(line) <= 16 for line in lines)
    assert " ".join(lines) == "I could do this all day and then some more"


def test_empty_text_gives_one_empty_line():
    assert wrap_bubble("") == [""]


def test_tiny_width_is_rejected():
    with pytest.raises(ValueError):
        wrap_bubble("hello", width=2)
