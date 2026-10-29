# 10-Day Plan

Five commit-sized tasks per day. Mark a day done when its tasks are pushed.

## Day 1: Foundation (done)

1. Project skeleton, `pyproject.toml`, `.gitignore`
2. README with the pet concept
3. `Pet` class
4. CLI entry point
5. First ASCII art

## Day 2: Core stats and actions

1. `feed`, `play`, `sleep` commands
2. Stats clamp between 0 and 100
3. Stats decay over time
4. Status bars rendered with `rich`
5. Unit tests for the stats logic

## Day 3: Persistence

1. Save the pet to `~/.termagotchi/save.json`
2. Load on startup
3. Offline time catch-up (the pet gets hungry while you are away)
4. First-run flow (menu only when no save exists)
5. Handle a corrupted save file

## Day 4: Moods and animation

1. Mood system (happy, hungry, sleepy, sad)
2. A different sprite per mood
3. Idle animation loop (blinking)
4. Eating and playing animations
5. Speech bubbles with random quotes

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
