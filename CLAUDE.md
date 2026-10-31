# Termagotchi

A pet that lives in your terminal and on your desktop. Python with `rich` for the terminal card and PySide6 for the desktop pets. Goal: finish a 10-day build with a commit streak (5+ real commits a day). Full plan: see `PLAN.md`.

## Rules

- Commit small and often with conventional messages (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`).
- One task per commit. Run the code before committing. Add a test when the logic is testable.
- Characters are original only. No Marvel, DC, Disney, or other existing characters, and no real people.
- Every species has two drawings. Add both when adding a species:
  1. Terminal ASCII art in `src/termagotchi/art.py`: one entry in `SPECIES` (display name, rich color, art).
  2. Desktop pixel pet in `src/termagotchi/pets/<key>.py`: exports one `SPEC`, then add the key to `PET_MODULES` in `src/termagotchi/pets/__init__.py`.
- Four-legged pets (horse) build on `pets/quad.py`. Hero pets build on `pets/biped.py`.
- Python 3.10+ code, type hints, short docstrings.
- Tests run Qt headless (`tests/conftest.py`). Point the app at a throwaway save with the `TERMAGOTCHI_SAVE` environment variable so tests and experiments do not overwrite the real pet.

## Layout

- `src/termagotchi/pet.py`: `Pet` dataclass (name, species, age, hunger, happiness, energy). `feed`, `play`, `sleep`, `tick` (decay), `catch_up` (decay for time away, capped at 8 hours), `adjust` (clamps every stat to 0 to 100).
- `src/termagotchi/storage.py`: `save` and `load` for `~/.termagotchi/save.json` (atomic write, stores the pet, desktop x position, and timestamp). A corrupt save moves to `save.bad` and the app starts fresh.
- `src/termagotchi/art.py`: `SPECIES` registry (17 species, horse included) and ASCII sprite helpers.
- `src/termagotchi/cli.py`: first-run pet menu, name prompt, colored pet card with stat bars, command loop (`feed`, `play`, `sleep`, `quit`), `--desktop` hand-off.
- `src/termagotchi/sprites.py`: layered pixel-art engine (`Part`, `Pose`, `PetSpec`, `Renderer`, helpers like `grid`, `blob`, `rect`, `mirror`, `validate`). States: idle, walk, sleep, eat, special.
- `src/termagotchi/pets/`: one module per species, plus `quad.py` and `biped.py` templates and the `load_all` registry.
- `src/termagotchi/behavior.py`: `Brain` picks what a desktop pet does next (no Qt, so it is testable).
- `src/termagotchi/desktop.py`: transparent always-on-top pet windows, drag to move, right-click menu (Feed, Play, Sleep, Hide, Quit all), decay timer every 15 seconds, saves on quit.
- `src/termagotchi/preview.py`: renders a contact sheet PNG of one pet's animation frames, for checking sprites by eye.
- `tests/`: pytest suite for pet logic, storage, CLI, behavior, sprites, and every species' desktop pet.

## Run

```bash
pip install -e ".[dev]"          # dev adds pytest and PySide6
py -m termagotchi.cli            # terminal pet (loads the save, or shows the menu on first run)
py -m termagotchi.cli --pet dragon --name Ember   # skip the menu (starts a new pet)
py -m termagotchi.cli --new      # ignore the save and start over
py -m termagotchi.cli --desktop            # every pet walks on the desktop
py -m termagotchi.cli --desktop fox owl    # chosen pets only
py -m termagotchi.preview fox fox.png      # contact sheet of one pet's frames
py -m pytest
```

On Windows, `python` may be the Microsoft Store shortcut, so use `py -m ...` or the full path to `python.exe`.

## Status

- Day 1 done (Oct 29): skeleton, Pet class, CLI, ASCII art, 16-character menu, colored layout.
- Day 2 done (Oct 30): feed, play, sleep, stat clamping, decay with `Pet.tick`, colored stat bars, tests.
- Extra done (Oct 30): desktop mode with a layered sprite engine, a `Brain` for behavior, a right-click care menu, and an animated desktop pet with its own special move for each of the 16 species. Includes the `--desktop` flag and a preview tool.
- Day 3 done (Oct 31): save file, load on startup, offline catch-up, first-run flow, corrupt-save recovery.
- Horse (17th species) done: ASCII entry, pixel pet, and the shared quadruped template.
- Next: Day 4 (moods and animation). See `PLAN.md`.

## Open work

- Desktop pets already animate per state. Day 4 still needs mood-driven behavior: sprites that react to hunger, happiness, and energy (happy, hungry, sleepy, sad), speech bubbles, and eating and playing animations in the terminal card.
- The terminal ASCII art is rougher than the desktop pixel art (fox, dragon, hero characters, horse). Print each sprite in a terminal and fix symmetry and detail by eye.
- The save file holds one pet: the first desktop window. Saving all desktop pets needs a format change.
- Decay runs in the CLI (one tick per command) and in desktop mode (every 15 seconds). Keep both on `Pet.tick` so the stats stay consistent.
