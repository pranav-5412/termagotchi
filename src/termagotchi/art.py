"""ASCII sprites for every species. All art here is original."""

# key -> (display name, sprite)
SPECIES: dict[str, tuple[str, str]] = {
    "cat": (
        "Cat",
        r"""
   /\_/\
  ( o.o )
   > ^ <
""",
    ),
    "dog": (
        "Dog",
        r"""
  /^ ^\
 / 0 0 \
 V\ Y /V
  / - \
""",
    ),
    "rabbit": (
        "Rabbit",
        r"""
  (\ /)
  ( . .)
  c(")(")
""",
    ),
    "fox": (
        "Fox",
        r"""
  /\   /\
 /  \_/  \
 \  o o  /
  \_ v _/
""",
    ),
    "owl": (
        "Owl",
        r"""
  {o,o}
  /)_)
   " "
""",
    ),
    "penguin": (
        "Penguin",
        r"""
   (o>
  //\
  V_/_
""",
    ),
    "dragon": (
        "Dragon",
        r"""
   ,  ,
  /(  )\
 ( @  @ )
  \ -- /~
   `||`
""",
    ),
    "robot": (
        "Robot",
        r"""
   [o_o]
  /|___|\
   |___|
   d   b
""",
    ),
    "ghost": (
        "Ghost",
        r"""
   .-.
  (o o)
  | O \
   \   \
    `~~~'
""",
    ),
    "alien": (
        "Alien",
        r"""
   .-""-.
  / o  o \
  \  \/  /
   '-..-'
""",
    ),
    "comet_captain": (
        "Captain Comet (hero)",
        r"""
   \|/
  .-*-.
 ( o o )
  \_v_/
  /|_|\
""",
    ),
    "star_knight": (
        "Star Knight (hero)",
        r"""
    _/\_
   (o  o)
  /|[**]|\
   _/  \_
""",
    ),
    "storm_mage": (
        "Storm Mage (hero)",
        r"""
    /\
   /__\
  ( oo )
  /|~~|\
    ||
""",
    ),
    "shadow_ninja": (
        "Shadow Ninja (hero)",
        r"""
   .----.
  |=o==o=|
   \ -- /
  --|##|--
    /  \
""",
    ),
}

DEFAULT_SPECIES = "cat"


def species_keys() -> list[str]:
    """Return species keys in menu order."""
    return list(SPECIES)


def display_name(species: str) -> str:
    """Return the menu name for a species key."""
    return SPECIES[species][0]


def sprite(species: str = DEFAULT_SPECIES) -> str:
    """Return the ASCII sprite for a species (more moods come on Day 4)."""
    return SPECIES[species][1].strip("\n")
