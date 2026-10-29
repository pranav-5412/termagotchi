# Termagotchi

A terminal pet in Python with `rich`. Goal: finish a 10-day build with a commit streak (5+ real commits a day). Full plan: see `PLAN.md`.

## Rules

- Commit small and often with conventional messages (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`).
- One task per commit. Run the code before committing. Add a test when the logic is testable.
- Characters are original only. No Marvel, DC, Disney, or other existing characters, and no real people.
- Keep sprites in `src/termagotchi/art.py`. Every species has a name, a rich color, and ASCII art. Add new species by adding one entry to `SPECIES`.
- Python 3.10+ code, type hints, short docstrings.

## Layout

- `src/termagotchi/pet.py`: `Pet` dataclass (name, species, age, hunger, happiness, energy).
- `src/termagotchi/art.py`: `SPECIES` registry and sprite helpers.
- `src/termagotchi/cli.py`: pet menu, name prompt, colored pet card. Flags: `--pet KEY`, `--name NAME`.

## Run

```bash
pip install -e .
python -m termagotchi.cli
```

On Windows, `python` may be the Microsoft Store shortcut. Use `py -m termagotchi.cli` or the full path to `python.exe`.

## Status

- Day 1 done: skeleton, Pet class, CLI, ASCII art.
- Extra done: 16 characters, selection menu, colored layout.
- Next: Day 2 (feed, play, sleep commands, stat limits, decay, status bars, tests).

## Open work

- Sprites still look rough in places (fox, dragon, hero characters). Improve detail and symmetry. Print each sprite in a terminal and check it by eye.
- Add moods per species on Day 4 (happy, hungry, sleepy, sad sprites).
