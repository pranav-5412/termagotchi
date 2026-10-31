"""Tests for the first-run flow."""

from rich.console import Console

from termagotchi import cli, storage
from termagotchi.pet import Pet


def _args(*argv: str):
    return cli.build_parser().parse_args(list(argv))


def test_first_run_uses_flags_and_creates_a_save(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv(storage.SAVE_ENV, str(tmp_path / "save.json"))
    pet = cli.start_pet(Console(), _args("--pet", "dog", "--name", "Rex"))
    assert (pet.name, pet.species) == ("Rex", "dog")
    assert storage.load() is not None


def test_existing_save_skips_the_menu(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv(storage.SAVE_ENV, str(tmp_path / "save.json"))
    storage.save(Pet(name="Zed", species="fox"))
    monkeypatch.setattr(cli, "choose_species", lambda console: (_ for _ in ()).throw(AssertionError))
    assert cli.start_pet(Console(), _args()).name == "Zed"


def test_new_flag_ignores_the_save(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv(storage.SAVE_ENV, str(tmp_path / "save.json"))
    storage.save(Pet(name="Zed", species="fox"))
    pet = cli.start_pet(Console(), _args("--new", "--pet", "cat", "--name", "Tom"))
    assert pet.name == "Tom"
