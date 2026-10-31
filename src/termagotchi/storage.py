"""Save the pet to ~/.termagotchi/save.json."""

from __future__ import annotations

import json
import os
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

from termagotchi.pet import Pet

SAVE_ENV = "TERMAGOTCHI_SAVE"  # overrides the save path (used by tests)


def save_path() -> Path:
    """Return the save file path: $TERMAGOTCHI_SAVE or ~/.termagotchi/save.json."""
    override = os.environ.get(SAVE_ENV)
    return Path(override) if override else Path.home() / ".termagotchi" / "save.json"


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
