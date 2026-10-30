"""Checks that every registered desktop pet is sound and distinct."""

import pytest

from termagotchi.art import species_keys
from termagotchi.pets import PET_MODULES, load_all
from termagotchi.sprites import STATES, validate

SPECS = load_all()


def test_module_count_matches_specs() -> None:
    assert len(SPECS) == len(PET_MODULES)


@pytest.mark.parametrize("key", sorted(SPECS))
def test_spec_is_valid(key: str) -> None:
    assert validate(SPECS[key]) == []


@pytest.mark.parametrize("key", sorted(SPECS))
def test_key_is_a_known_species(key: str) -> None:
    assert key in species_keys()


@pytest.mark.parametrize("key", sorted(SPECS))
def test_special_animation_differs_from_idle(key: str) -> None:
    spec = SPECS[key]
    times = [i * 0.1 for i in range(40)]
    assert [spec.pose("special", t) for t in times] != [spec.pose("idle", t) for t in times]


@pytest.mark.parametrize("key", sorted(SPECS))
def test_every_state_animates(key: str) -> None:
    spec = SPECS[key]
    for state in STATES:
        frames = {tuple(sorted(spec.pose(state, i * 0.1).items(), key=str)) for i in range(40)}
        assert len(frames) > 1 or state == "sleep", state


def test_special_animations_are_unique_per_species() -> None:
    times = [i * 0.1 for i in range(40)]
    seen = {tuple(str(spec.pose("special", t)) for t in times) for spec in SPECS.values()}
    assert len(seen) == len(SPECS)


def test_every_species_has_a_desktop_pet() -> None:
    assert set(SPECS) == set(species_keys())


@pytest.mark.parametrize("key", sorted(SPECS))
def test_every_state_renders_pixels(key: str) -> None:
    from termagotchi.sprites import Renderer

    renderer = Renderer(SPECS[key], scale=2)
    for state in STATES:
        image = renderer.snapshot(state, 0.7)
        assert any(
            image.pixelColor(x, y).alpha() > 0
            for x in range(0, image.width(), 2)
            for y in range(0, image.height(), 2)
        ), state
