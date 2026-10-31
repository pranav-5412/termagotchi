"""Tests for saving and loading the pet."""

import json
from pathlib import Path

from termagotchi import storage
from termagotchi.pet import DECAY_HUNGER, Pet


def test_save_path_uses_env_override(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv(storage.SAVE_ENV, str(tmp_path / "x.json"))
    assert storage.save_path() == tmp_path / "x.json"


def test_save_writes_pet_and_desktop_state(tmp_path: Path) -> None:
    pet = Pet(name="Zed", species="dog", age=3, hunger=40, happiness=60, energy=70)
    path = storage.save(pet, {"x": 123.5}, tmp_path / "sub" / "save.json", now=1000.0)
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["saved_at"] == 1000.0
    assert data["pet"] == {
        "name": "Zed", "species": "dog", "age": 3, "hunger": 40, "happiness": 60, "energy": 70,
    }
    assert data["desktop"] == {"x": 123.5}


def test_save_leaves_no_temp_file(tmp_path: Path) -> None:
    storage.save(Pet(name="Zed"), path=tmp_path / "save.json")
    assert [p.name for p in tmp_path.iterdir()] == ["save.json"]


def test_load_returns_none_without_a_save(tmp_path: Path) -> None:
    assert storage.load(tmp_path / "missing.json") is None


def test_load_round_trips_a_save(tmp_path: Path) -> None:
    pet = Pet(name="Zed", species="fox", age=2, hunger=10, happiness=80, energy=55)
    path = storage.save(pet, {"x": 42.0}, tmp_path / "save.json", now=500.0)
    saved = storage.load(path, now=500.0)
    assert saved is not None
    assert saved.pet == pet
    assert saved.desktop == {"x": 42.0}
    assert saved.saved_at == 500.0


def test_load_catches_the_pet_up_on_time_away(tmp_path: Path) -> None:
    pet = Pet(name="Zed", hunger=0)
    path = storage.save(pet, path=tmp_path / "save.json", now=1000.0)
    saved = storage.load(path, now=1000.0 + 60)  # 4 ticks of 15 seconds
    assert saved is not None
    assert saved.pet.hunger == 4 * DECAY_HUNGER
