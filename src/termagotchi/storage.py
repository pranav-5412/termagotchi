"""Save the pet to ~/.termagotchi/save.json."""

from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

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


def load(path: Path | None = None) -> Saved | None:
    """Read the save file. Returns None when there is no save."""
    path = path or save_path()
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return Saved(
        pet=Pet(**data["pet"]),
        desktop=dict(data.get("desktop", {})),
        saved_at=float(data.get("saved_at", 0.0)),
    )
