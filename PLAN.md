# 10-Day Plan

Five commit-sized tasks per day. Mark a day done when its tasks are pushed.

Progress: Days 1 to 4 done (Oct 29 to Nov 2).

## Day 1: Foundation (done, Oct 29)

1. Project skeleton, `pyproject.toml`, `.gitignore`
2. README with the pet concept
3. `Pet` class
4. CLI entry point
5. First ASCII art

Also done that day: 16 original characters, a pet selection menu, a colored pet card, `CLAUDE.md` and this plan.

## Day 2: Core stats and actions (done, Oct 30)

1. `feed`, `play`, `sleep` commands
2. Stats clamp between 0 and 100
3. Stats decay over time
4. Status bars rendered with `rich`
5. Unit tests for the stats logic

## Extras done (Oct 30 and Oct 31)

- Desktop mode: a layered pixel-art sprite engine (`sprites.py`), a behavior `Brain` (`behavior.py`), transparent always-on-top pet windows (`desktop.py`) with drag, a right-click care menu, and stat decay every 15 seconds.
- A desktop pet with its own special move for every species, one module per species in `pets/`.
- Shared quadruped template (`pets/quad.py`) and the horse as the 17th species, in both ASCII and pixel art.
- `--desktop` flag, a sprite preview sheet tool (`preview.py`), and per-species render tests.

## Day 3: Persistence (done, Oct 31)

1. Save the pet to `~/.termagotchi/save.json`
2. Load on startup
3. Offline time catch-up (the pet gets hungry while you are away, capped at 8 hours)
4. First-run flow (menu only when no save exists)
5. Handle a corrupted save file (moved aside as `save.bad`)

## Day 4: Moods and animation (done, Nov 1 to Nov 2)

Revised: desktop pets already animate idle, walk, sleep, eat, and a special move, so this day adds moods on top.

1. Mood system: a pure function that turns stats into happy, hungry, sleepy, or sad (done: `mood.py` and `Pet.mood`)
2. A different face per mood in the terminal card (done: `faces.py`)
3. Desktop pets react to mood (done: `MOOD_WEIGHTS` in `behavior.py`)
4. Eating, playing, and sleeping animations in the terminal card (done: `animations.py`)
5. Speech bubbles with random quotes, in terminal and desktop mode (done: `bubble.py`, used by the CLI and the desktop windows)

## Day 5: Life and growth

1. Life stages (egg, baby, teen, adult)
2. XP and leveling
3. Evolution sprites per stage
4. Gentle runaway logic with a revive option
5. Tests for evolution

## Day 6: Git integration

1. Read recent commits with `git log`
2. Commits feed the pet and give XP
3. Streak bonus for daily commits
4. Pet reacts to commit messages (`fix:` worried, `feat:` excited)
5. Shell hook so the pet greets you on `git commit`

## Day 7: Mini-games and items

1. Number-guessing game for happiness
2. Rock-paper-scissors with the pet
3. Inventory (snacks, toys)
4. Coins from games and streaks
5. Simple shop command

## Day 8: Achievements and stats

1. Achievement definitions
2. Unlock detection with a toast message
3. `stats` dashboard
4. Pet diary
5. Daily summary on launch

## Day 9: Polish and UX

1. Color themes
2. Interactive menu mode (arrow keys)
3. Config file and settings command
4. Better error messages and `--help`
5. Refactor and raise test coverage

## Day 10: Ship it

1. Package for `pip install` and test in a fresh venv
2. GitHub Actions to run tests
3. Demo GIF for the README
4. Full README
5. Tag `v1.0.0` and write release notes
