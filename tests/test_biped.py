"""Tests for the shared biped base poses."""

from termagotchi.pets.biped import base_pose, neck_pivot
from termagotchi.sprites import STATES


def test_neck_pivot_is_relative_to_part_position() -> None:
    assert neck_pivot(8, 3) == (8.0, 13.0)


def test_every_state_poses_core_parts() -> None:
    for state in STATES:
        poses = base_pose(state, 0.3)
        assert {"head", "eyes", "eyes_closed", "torso", "arm_l", "arm_r"} <= set(poses)


def test_head_props_follow_the_head() -> None:
    poses = base_pose("sleep", 0.0, head_extra=("hat",), body_extra=("scarf",))
    assert poses["hat"].dy == poses["head"].dy == 2
    assert poses["scarf"].dy == 1


def test_walk_swings_legs_in_opposite_directions() -> None:
    poses = base_pose("walk", 0.15)
    assert poses["leg_l"].angle == -poses["leg_r"].angle != 0
