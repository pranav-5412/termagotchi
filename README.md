# Termagotchi 🐣

A tiny pet that lives in your terminal and on your desktop. Feed it, play with it, and keep it alive by committing code every day.

Think Tamagotchi, but for developers: your git commits are its food, and your coding streak keeps it happy.

## Concept

- The pet has four stats: age, hunger, happiness, and energy.
- Stats change over time, even while you are away (catch-up is capped at 8 hours).
- Actions (`feed`, `play`, `sleep`) raise or lower stats.
- Your pet is saved to `~/.termagotchi/save.json` and loaded on the next launch.
- Coming next: moods, life stages, and git commits that feed the pet.

## Install

Not released yet. For now, from a clone of this repo:

```bash
pip install -e .
termagotchi
```

On Windows, if `termagotchi` is not found, run `py -m termagotchi.cli` instead.

## Pick your pet

The first launch shows a menu of 17 original characters: cat, dog, rabbit, fox, owl, penguin, sugar glider, dragon, robot, ghost, alien, horse, and five heroes (Captain Comet, Star Knight, Storm Mage, Shadow Ninja, Tomahawk Scout). Later launches load your saved pet.

```bash
termagotchi                             # load your pet, or choose from the menu
termagotchi --pet dragon --name Ember   # skip the menu and start a new pet
termagotchi --new                       # ignore the save and start over
```

In the terminal, type `feed`, `play`, `sleep`, or `quit`. Each command moves the clock one tick and shows colored stat bars.

## Desktop mode

Pets walk, sleep, eat, and do a species trick in small transparent windows at the bottom of your screen. Drag a pet to move it. Right-click for Feed, Play, Sleep, Hide, and Quit.

```bash
pip install -e ".[desktop]"
termagotchi --desktop              # every pet
termagotchi --desktop fox owl      # chosen pets
```

## Development

```bash
pip install -e ".[dev]"
py -m pytest
py -m termagotchi.preview fox fox.png   # contact sheet of one pet's animation frames
```

## Roadmap

Built in 10 days.

| Day | Focus | Status |
| --- | --- | --- |
| 1 | Foundation: Pet class, CLI, first ASCII art | Done |
| 2 | Stats and actions | Done |
| 3 | Saving and offline catch-up | Done |
| 4 | Moods and animation | Next |
| 5 | Life stages and evolution | |
| 6 | Git integration | |
| 7 | Mini-games and items | |
| 8 | Achievements and stats | |
| 9 | Polish and UX | |
| 10 | Packaging and v1.0.0 | |

Extras built along the way: desktop mode with an animated pixel-art pet for every species.

## License

MIT (to be added).
