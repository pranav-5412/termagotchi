"""Tests for the sprite engine."""

from termagotchi.sprites import Part, PetSpec, Pose, Renderer, blink, sine, validate


def _spec(rows=("##", "##"), palette=None, pose=None) -> PetSpec:
    return PetSpec(
        key="t",
        palette=palette or {"#": "#ff0000"},
        parts=(Part("body", 1, 1, rows),),
        pose=pose or (lambda state, t: {"body": Pose()}),
        canvas=(8, 8),
    )


def test_valid_spec_has_no_errors() -> None:
    assert validate(_spec()) == []


def test_validate_flags_ragged_rows_and_bad_colors() -> None:
    assert validate(_spec(rows=("##", "#")))
    assert validate(_spec(rows=("#x",)))


def test_validate_flags_part_outside_canvas() -> None:
    assert validate(_spec(rows=("#" * 9,)))


def test_validate_flags_unknown_pose_part() -> None:
    assert validate(_spec(pose=lambda state, t: {"tail": Pose()}))


def test_snapshot_paints_part_at_scale() -> None:
    image = Renderer(_spec(), scale=2).snapshot("idle", 0.0)
    assert image.pixelColor(2, 2).red() == 255
    assert image.pixelColor(0, 0).alpha() == 0


def test_facing_left_mirrors_the_image() -> None:
    renderer = Renderer(_spec(), scale=2)
    right = renderer.snapshot("idle", 0.0, facing=1)
    left = renderer.snapshot("idle", 0.0, facing=-1)
    assert right.pixelColor(2, 2).alpha() == 255
    assert left.pixelColor(2, 2).alpha() == 0
    assert left.pixelColor(13, 2).alpha() == 255


def test_helpers() -> None:
    assert abs(sine(0.25, 1.0)) - 1.0 < 1e-9
    assert blink(0.0) and not blink(1.0)


def test_grid_pads_rows_to_equal_width() -> None:
    from termagotchi.sprites import grid

    assert grid("\n##\n#\n") == ("##", "#.")


def test_fx_poses_show_only_in_matching_state() -> None:
    from termagotchi.sprites import fx_poses

    assert fx_poses("sleep", 0.0)["zzz"].visible and not fx_poses("idle", 0.0)["zzz"].visible
    assert fx_poses("eat", 0.0)["bowl"].visible


def test_blob_has_outline_ring_and_filled_core() -> None:
    from termagotchi.sprites import blob

    rows = blob(9, 9, "a", "o")
    assert rows[4][4] == "a"
    assert rows[0][0] == "." and rows[4][0] == "o" and rows[0][4] == "o"
    assert all(len(row) == 9 for row in rows)


def test_blob_shades_light_and_dark() -> None:
    from termagotchi.sprites import blob

    flat = "".join(blob(14, 14, "a", "o", light="l", dark="d"))
    assert "l" in flat and "d" in flat


def test_overlay_and_mirror() -> None:
    from termagotchi.sprites import mirror, overlay

    base = ("aaa", "aaa")
    assert overlay(base, ("b.",), 1, 0) == ("aba", "aaa")
    assert overlay(base, ("bb",), 2, 1) == ("aaa", "aab")
    assert mirror(("ab.",)) == (".ba",)


def test_rect_has_rounded_outline_and_shading() -> None:
    from termagotchi.sprites import rect

    rows = rect(6, 5, "a", "o", light="l", dark="d")
    assert rows[0][0] == "." and rows[0][1] == "o" and rows[2][0] == "o"
    assert rows[1][1] == "l" and rows[3][4] == "d" and rows[2][2] == "a"
    assert all(len(row) == 6 for row in rows) and len(rows) == 5
