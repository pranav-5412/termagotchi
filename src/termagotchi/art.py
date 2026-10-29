"""ASCII sprites for every species. All art here is original."""

import textwrap

# key -> (display name, rich color, sprite)
SPECIES: dict[str, tuple[str, str, str]] = {
    "cat": (
        "Cat",
        "orange1",
        r"""
        /\_____/\
       /  o   o  \
   ---(  == ^ ==  )---
       )  \___/  (
      (  /     \  )
     ( (  )   (  ) )
    (__(__)___(__)__)
          \_____/~~~
""",
    ),
    "dog": (
        "Dog",
        "tan",
        r"""
    .--.         .--.
   /    \_______/    \
  |  ()  .-----.  ()  |
   \    /  o o  \    /
    '--|    _    |--'
       |   (_)   |
        \  \_/  /
         \_____/
        /|  |  |\
       (_|__|__|_)
""",
    ),
    "rabbit": (
        "Rabbit",
        "pink1",
        r"""
      ()       ()
      ||       ||
      ||       ||
     /  \_____/  \
    (    o   o    )
    (      Y      )
     \    '-'    /
     /   `---'   \
    /    |   |    \
   (    (|   |)    )
    \____(_)_(_)___/
""",
    ),
    "fox": (
        "Fox",
        "dark_orange",
        r"""
    /\              /\
   /  \____________/  \
  / /\              /\ \
 / /  \            /  \ \
|  |   \ o      o /   |  |
|  |    \        /    |  |
 \  \   `.      .`   /  /
  \  `.   \    /   .`  /
   `-._`-.__vv__.-`_.-`
       `--.____.--`
""",
    ),
    "owl": (
        "Owl",
        "khaki1",
        r"""
      ___       ___
     /   \_____/   \
    |   (O)   (O)   |
    |       V       |
    |     /|||\     |
    |    / ||| \    |
     \  /_/|||\_\  /
      \___________/
         |_| |_|
        _|_|_|_|_
""",
    ),
    "penguin": (
        "Penguin",
        "cyan",
        r"""
         .-----.
        /       \
       |  o   o  |
       |    V    |
        \   ^   /
      .--`-----'--.
     / |    ,    | \
    /  |   (_)   |  \
   (   |         |   )
    \  |   ___   |  /
     `-|__/   \__|-'
       /_)     (_\
""",
    ),
    "sugar_glider": (
        "Sugar Glider",
        "plum1",
        r"""
        _       _
       / \_____/ \
      |  (O) (O)  |
       \    w    /
  ~~~~~--\_____/--~~~~~
 /  ~~~~~/  |  \~~~~~  \
 \_~~~~~(   |   )~~~~~_/
    ~~~~ \__|__/ ~~~~
          _/ \_
         (_)~(_)~~~~
""",
    ),
    "dragon": (
        "Dragon",
        "green",
        r"""
        ,           ,
       /(           )\
   .--'  \  _____  /  '--.
  /  \    \/ @ @ \/    /  \
 /    \    \  ^  /    /    \
/  /\  \    \_v_/    /  /\  \
\_/  \_/ `---------' \_/  \_/
         /  |||||  \
        /___ ||||| ___\~~~
""",
    ),
    "robot": (
        "Robot",
        "bright_cyan",
        r"""
           o
           |
      .---------.
      |  _   _  |
      | (_) (_) |
      |    _    |
      |  \___/  |
      '---------'
     __|_______|__
    |  |  [_]  |  |
    |__|  ===  |__|
       |__| |__|
       /_/   \_\
""",
    ),
    "ghost": (
        "Ghost",
        "white",
        r"""
         .-------.
       .'  _   _  '.
      /   (o) (o)   \
     |       O       |
     |               |
     |  ~         ~  |
     |               |
     |/\  /\  /\  /\ |
     '  \/  \/  \/  \'
""",
    ),
    "alien": (
        "Alien",
        "bright_green",
        r"""
         .-------.
       .'    _    '.
      /  /\     /\  \
     |  /  \ _ /  \  |
     |  \ @ / \ @ /  |
      \  \_/   \_/  /
       '.   ===   .'
         '-.___.-'
           /| |\
          / | | \
""",
    ),
    "comet_captain": (
        "Captain Comet (hero)",
        "bright_blue",
        r"""
           .-----.
          / ===== \
         |  O   O  |
         |    ^    |
          \  ___  /
      /\   `-----'   /\
     /  \__ /|*|\ __/  \
    / /\   | |*~| |   /\ \
   / /  \__|_|~*|_|__/  \ \
   \/      /  | |  \      \/
          /   | |   \
         /____| |____\
              /_\
""",
    ),
    "star_knight": (
        "Star Knight (hero)",
        "gold1",
        r"""
            _/|\_
           / .|. \
          | /===\ |
          ||(o o)||
          | \ - / |
         _|__\_/__|_
        /|  [***]  |\
       / | /|***|\ | \
      (_)|/ |***| \|(_)
          \_|___|_/
           /|   |\
          /_|   |_\
""",
    ),
    "storm_mage": (
        "Storm Mage (hero)",
        "medium_purple1",
        r"""
           /\
          /  \
         / ~~ \
        /      \
       /        \
  ~~~/____________\~~~
      |  o    o  |
       \  ____  /
    /|\__________/|\
   / |  \______/  | \
  /  |  |      |  |  \
""",
    ),
    "shadow_ninja": (
        "Shadow Ninja (hero)",
        "grey50",
        r"""
         .-------.
        /  _____  \
       |  (_o_o_)  |
        \  `---'  /
      ___`-------'___
     /   \  ___  /   \
    /  /\ \|###|/ /\  \
   /__/  \_|###|_/  \__\
        _/ |###| \_
       /___|   |___\
""",
    ),
    "tomahawk_scout": (
        "Tomahawk Scout (hero)",
        "dark_olive_green3",
        r"""
          .-----.           ,-.
         / ,---. \         /  |
        | | o o | |       (   |
        |  \_-_/  |        \  |
         \  `-'  /          `-|
       .--`-----'--.         |
      /  |  ___  |  \        |
     /   | | _ | |   \=======+
    (____| |___| |____)      |
         |_|   |_|
         /_|   |_\
""",
    ),
}

DEFAULT_SPECIES = "cat"


def species_keys() -> list[str]:
    """Return species keys in menu order."""
    return list(SPECIES)


def display_name(species: str) -> str:
    """Return the menu name for a species key, such as 'Star Knight (hero)'."""
    return SPECIES[species][0]


def species_label(species: str) -> str:
    """Return the plain species name without the '(hero)' tag."""
    return display_name(species).split(" (")[0]


def color(species: str) -> str:
    """Return the rich color name for a species."""
    return SPECIES[species][1]


def sprite(species: str = DEFAULT_SPECIES) -> str:
    """Return the ASCII sprite for a species (more moods come on Day 4)."""
    return textwrap.dedent(SPECIES[species][2]).strip("\n")
