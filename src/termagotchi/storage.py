"""Save the pet to ~/.termagotchi/save.json."""

from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from termagotchi.art import SPECIES
from termagotchi.pet import Pet

SAVE_ENV = "TERMAGOTCHI_SAVE"  # overrides the save path (used by tests)


def save_path() -> Path:
    """Return the save file path: $TERMAGOTCHI_SAVE or ~/.termagotchi/save.json."""
    override = os.environ.get(SAVE_ENV)
    return Path(override) if override else Path.home() / ".termagotchi" / "save.json"


@dataclass
class Saved:
    """What a save file holds: the pet, desktop state, and when it was written."""

    pet: Pet
    desktop: dict[str, Any] = field(default_factory=dict)
    saved_at: float = 0.0


def save(
    pet: Pet,
    desktop: dict[str, Any] | None = None,
    path: Path | None = None,
    now: float | None = None,
) -> Path:
    """Write the pet, its desktop state (such as x position), and a timestamp as JSON."""
    path = path or save_path()
    data = {
        "version": 1,
        "saved_at": time.time() if now is None else now,
        "pet": asdict(pet),
        "desktop": desktop or {},
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    tmp.replace(path)  # atomic, so a crash never leaves half a file
    return path


def load(path: Path | None = None, now: float | None = None) -> Saved | None:
    """Read the save file and catch the pet up on time away.

    Returns None when there is no save or the file is corrupt (a corrupt file moves to .bad).
    """
    path = path or save_path()
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        saved_at = float(data.get("saved_at", 0.0))
        pet = Pet(**data["pet"])
        desktop = dict(data.get("desktop", {}))
        if pet.species not in SPECIES:
            raise ValueError(f"unknown species {pet.species!r}")
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        backup = path.with_suffix(".bad")
        path.replace(backup)  # keep the broken file for inspection, start fresh
        return None
    if saved_at:
        pet.catch_up((time.time() if now is None else now) - saved_at)
    return Saved(pet=pet, desktop=desktop, saved_at=saved_at)
