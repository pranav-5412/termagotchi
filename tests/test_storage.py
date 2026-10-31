"""Tests for saving and loading the pet."""

import json
from pathlib import Path

from termagotchi import storage
from termagotchi.pet import Pet


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
