"""Tests for the Pet stats logic."""

from termagotchi.pet import DECAY_ENERGY, DECAY_HAPPINESS, DECAY_HUNGER, Pet, clamp


def test_clamp_limits_range() -> None:
    assert clamp(-5) == 0
    assert clamp(50) == 50
    assert clamp(150) == 100


def test_starting_stats_are_clamped() -> None:
    pet = Pet(name="Tom", hunger=-10, happiness=500, energy=101)
    assert (pet.hunger, pet.happiness, pet.energy) == (0, 100, 100)


def test_feed_lowers_hunger_and_stops_at_zero() -> None:
    pet = Pet(name="Tom", hunger=20)
    pet.feed()
    assert pet.hunger == 0
    assert pet.happiness == 55


def test_play_changes_stats() -> None:
    pet = Pet(name="Tom", hunger=0, happiness=50, energy=100)
    pet.play()
    assert (pet.hunger, pet.happiness, pet.energy) == (10, 70, 85)


def test_play_caps_happiness_and_floors_energy() -> None:
    pet = Pet(name="Tom", happiness=95, energy=5)
    pet.play()
    assert pet.happiness == 100
    assert pet.energy == 0


def test_sleep_restores_energy_up_to_100() -> None:
    pet = Pet(name="Tom", energy=70)
    pet.sleep()
    assert pet.energy == 100
    assert pet.hunger == 10


def test_tick_decays_stats() -> None:
    pet = Pet(name="Tom", hunger=0, happiness=50, energy=100)
    pet.tick()
    assert pet.hunger == DECAY_HUNGER
    assert pet.happiness == 50 - DECAY_HAPPINESS
    assert pet.energy == 100 - DECAY_ENERGY


def test_tick_multiple_steps_stays_in_range() -> None:
    pet = Pet(name="Tom")
    pet.tick(steps=1000)
    assert (pet.hunger, pet.happiness, pet.energy) == (100, 0, 0)
