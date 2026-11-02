"""Tests for terminal animations."""

import pytest

from termagotchi.animations import (
    ACTIONS,
    compose,
    eat_frames,
    frames_for,
    play_frames,
    sleep_frames,
)


@pytest.mark.parametrize("make", [eat_frames, play_frames, sleep_frames])
def test_each_animation_has_several_distinct_frames(make):
    frames = make()
    assert len(frames) >= 3
    assert len(set(frames)) >= 3


def test_every_action_has_frames():
    for action in ACTIONS:
        assert frames_for(action)


def test_frames_for_matches_the_makers():
    assert frames_for("feed") == eat_frames()
    assert frames_for("play") == play_frames()
    assert frames_for("sleep") == sleep_frames()


def test_unknown_action_raises():
    with pytest.raises(KeyError):
        frames_for("dance")


def test_compose_puts_the_header_above_the_art():
    assert compose("zZ", "(^_^)") == "zZ\n(^_^)"
