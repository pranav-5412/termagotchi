"""Shared layout and base poses for the upright heroes (not a species itself).

Slots on the 32x32 canvas: head 16x14 at (8,3), torso 12x9 at (10,16), arms 4x9 at (6,17)
and (22,17), legs 5x8 at (11,24) and (16,24). Heroes draw into these slots and add props.
"""

from collections.abc import Iterable

from termagotchi.sprites import Pose, blink, fx_poses, lift, sine

NECK = (16.0, 16.0)  # absolute point the head tilts around
HEAD_SLOT = (8, 3)
TORSO_SLOT = (10, 16)
ARM_SLOTS = ((6, 17), (22, 17))
LEG_SLOTS = ((11, 24), (16, 24))
ARM_PIVOT = (2.0, 1.0)
LEG_PIVOT = (2.5, 0.0)


def neck_pivot(x: int, y: int) -> tuple[float, float]:
    """Pivot for a head part at (x, y) so the head group tilts about the neck."""
    return NECK[0] - x, NECK[1] - y


def head_group(
    t: float, extra: Iterable[str], dy: float = 0.0, angle: float = 0.0,
    asleep: bool = False, blink_every: float = 3.6,
) -> dict[str, Pose]:
    """Pose head, eyes, and any head props together."""
    shut = asleep or blink(t, blink_every, 0.18)
    poses = {name: Pose(dy=dy, angle=angle) for name in ("head", *extra)}
    poses["eyes"] = Pose(dy=dy, angle=angle, visible=not shut)
    poses["eyes_closed"] = Pose(dy=dy, angle=angle, visible=shut)
    return poses


def base_pose(
    state: str, t: float, head_extra: Iterable[str] = (), body_extra: Iterable[str] = (),
    blink_every: float = 3.6,
) -> dict[str, Pose]:
    """Idle, walk, eat, and sleep poses. Any other state is posed like idle."""
    head_extra, body_extra = tuple(head_extra), tuple(body_extra)
    poses = fx_poses(state, t)
    if state == "walk":
        step = sine(t, 0.6, 1.0)
        bob = -abs(step) * 0.8
        poses.update(head_group(t, head_extra, dy=bob, blink_every=blink_every))
        poses["torso"] = Pose(dy=bob)
        lift(poses, body_extra, dy=bob)
        poses["arm_l"] = Pose(angle=-26 * step, dy=bob)
        poses["arm_r"] = Pose(angle=26 * step, dy=bob)
        poses["leg_l"] = Pose(angle=24 * step)
        poses["leg_r"] = Pose(angle=-24 * step)
    elif state == "eat":
        poses.update(head_group(t, head_extra, dy=2.5 + sine(t, 0.45, 1.0), angle=4,
                                blink_every=blink_every))
        poses["arm_l"] = Pose(angle=30)
        poses["arm_r"] = Pose(angle=-30)
    elif state == "sleep":
        poses.update(head_group(t, head_extra, dy=2, angle=8, asleep=True))
        poses["torso"] = Pose(dy=1)
        lift(poses, body_extra, dy=1)
        poses["arm_l"] = Pose(angle=5, dy=1)
        poses["arm_r"] = Pose(angle=-5, dy=1)
    else:
        poses.update(head_group(t, head_extra, dy=sine(t, 3, 0.4), angle=sine(t, 6, 3),
                                blink_every=blink_every))
        poses["torso"] = Pose(sy=1 + sine(t, 3, 0.015))
        poses["arm_l"] = Pose(angle=sine(t, 3, 4))
        poses["arm_r"] = Pose(angle=-sine(t, 3, 4))
    return poses
