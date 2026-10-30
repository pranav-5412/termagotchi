# Termagotchi 🐣

A tiny pet that lives in your terminal. Feed it, play with it, and keep it alive by committing code every day.

Think Tamagotchi, but for developers: your git commits are its food, and your coding streak keeps it happy.

## Concept

- The pet has four stats: age, hunger, happiness, and energy.
- Stats change over time, even while you are away.
- Actions (`feed`, `play`, `sleep`) raise or lower stats.
- Your git commits give the pet XP and a streak bonus.

## Install

Not released yet. For now, from a clone of this repo:

```bash
pip install -e .
termagotchi
```

## Pick your pet

Each launch shows a menu of 16 original characters: cat, dog, rabbit, fox, owl, penguin, sugar glider, dragon, robot, ghost, alien, and five heroes (Captain Comet, Star Knight, Storm Mage, Shadow Ninja, Tomahawk Scout).

```bash
termagotchi                        # choose from the menu
termagotchi --pet dragon --name Ember   # skip the menu
```

## Desktop mode

Pets walk, sleep, eat, and do a species trick in small transparent windows at the bottom of your screen. Drag a pet to move it. Right-click for Feed, Play, Sleep, and Quit.

```bash
pip install -e ".[desktop]"
termagotchi --desktop              # every pet
termagotchi --desktop fox owl      # chosen pets
```

## Roadmap

Built in 10 days.

| Day | Focus |
| --- | --- |
| 1 | Foundation: Pet class, CLI, first ASCII art |
| 2 | Stats and actions |
| 3 | Saving and offline catch-up |
| 4 | Moods and animation |
| 5 | Life stages and evolution |
| 6 | Git integration |
| 7 | Mini-games and items |
| 8 | Achievements and stats |
| 9 | Polish and UX |
| 10 | Packaging and v1.0.0 |

## License

MIT (to be added).
