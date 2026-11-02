"""Tests for speech bubbles."""

import pytest

from termagotchi.bubble import Bubble, draw_bubble, wrap_bubble


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


def test_bubble_box_has_equal_width_rows():
    rows = draw_bubble("Thanks for coding with me!", width=16).splitlines()
    box = rows[:-1]
    assert len({len(row) for row in box}) == 1
    assert box[0].startswith(".") and box[-1].startswith("'")


def test_bubble_ends_with_a_tail():
    assert draw_bubble("Hi").splitlines()[-1].strip() == "\\"


def test_new_bubble_can_speak_at_once():
    bubble = Bubble()
    assert bubble.say("Hello") is True
    assert bubble.visible and bubble.text == "Hello"


def test_bubble_hides_after_its_show_time():
    bubble = Bubble(show_seconds=2, quiet_seconds=5)
    bubble.say("Hello")
    bubble.update(1.9)
    assert bubble.visible
    bubble.update(0.2)
    assert not bubble.visible


def test_bubble_stays_quiet_during_the_cooldown():
    bubble = Bubble(show_seconds=2, quiet_seconds=5)
    bubble.say("Hello")
    bubble.update(2)
    assert bubble.say("Again") is False
    bubble.update(4.9)
    assert bubble.say("Again") is False
    bubble.update(0.2)
    assert bubble.say("Again") is True


def test_bubble_cannot_be_replaced_while_visible():
    bubble = Bubble()
    bubble.say("One")
    assert bubble.say("Two") is False
    assert bubble.text == "One"
