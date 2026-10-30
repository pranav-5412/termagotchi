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
