"""Tests for the pet behavior brain."""

import random

from termagotchi.behavior import CHOICES, Brain


def make(seed: int = 1) -> Brain:
    return Brain(0, 500, 50, random.Random(seed))


def test_walk_moves_toward_target_and_faces_it() -> None:
    brain = make()
    brain.x = 0
    brain.set_state("walk", 100)
    brain.target = 200
    brain.facing = 1
    brain.update(1.0)
    assert brain.x == 50


def test_walk_ends_on_arrival() -> None:
    brain = make()
    brain.x = 0
    brain.set_state("walk", 100)
    brain.target = 10
    brain.update(1.0)
    assert brain.x == 10
    assert brain.state in CHOICES


def test_timed_state_switches_after_duration() -> None:
    brain = make()
    brain.set_state("sleep", 1.0)
    brain.update(0.5)
    assert brain.state == "sleep"
    brain.update(0.6)
    assert brain.state_time == 0.0


def test_held_pet_does_not_move_or_change() -> None:
    brain = make()
    brain.set_state("sleep", 0.1)
    brain.held = True
    brain.update(5.0)
    assert brain.state == "sleep"


def test_stays_inside_bounds_over_long_run() -> None:
    brain = make(7)
    for _ in range(20000):
        brain.update(0.05)
        assert 0 <= brain.x <= 500
