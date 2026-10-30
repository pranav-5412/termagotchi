"""Registry of desktop pets. Each module in PET_MODULES exports one `SPEC`."""

from importlib import import_module

from termagotchi.sprites import PetSpec

# One entry per species, added in the commit that draws it.
PET_MODULES: tuple[str, ...] = ("cat", "dog", "rabbit", "fox", "owl", "penguin", "sugar_glider", "dragon", "robot")


def load_all() -> dict[str, PetSpec]:
    """Import every pet module and return specs keyed by species."""
    specs: dict[str, PetSpec] = {}
    for name in PET_MODULES:
        spec: PetSpec = import_module(f"termagotchi.pets.{name}").SPEC
        specs[spec.key] = spec
    return specs
