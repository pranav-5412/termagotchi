"""Robot: cyan bot with blinking lights that breaks into a dance."""

import math

from termagotchi.sprites import (
    FX_PALETTE, Part, PetSpec, Pose, blink, fx_poses, grid, lift, overlay, rect, sine,
    sleep_and_eat_parts,
)

PALETTE = {
    **FX_PALETTE,
    "o": "#0e2a33", "a": "#37c8d8", "l": "#8ff0f7", "d": "#1f8fa0", "m": "#6c7a86",
    "S": "#0c1c24", "E": "#7dffb0", "R": "#ff4d4d", "Y": "#ffd23a",
}


def _head() -> tuple[str, ...]:
    base = tuple("." * 20 for _ in range(11))
    base = overlay(base, rect(16, 11, "a", "o", "l", "d"), 2, 0)
    base = overlay(base, rect(2, 4, "m", "o"), 0, 4)
    base = overlay(base, rect(2, 4, "m", "o"), 18, 4)
    return overlay(base, rect(12, 6, "S", "o"), 4, 2)


def _arm() -> tuple[str, ...]:
    return overlay(rect(4, 11, "a", "o", "l", "d"), grid("mmmm\nmmmm"), 0, 9)


def _torso() -> tuple[str, ...]:
    return overlay(rect(16, 10, "a", "o", "l", "d"), rect(8, 5, "S", "o"), 4, 2)


EYES = grid("""
EEE....EEE
EEE....EEE
""")
EYES_CLOSED = grid("""
..........
EEE....EEE
""")
LIGHTS = grid("E.R.Y")
ANTENNA = grid("""
RR
RR
mm
""")

ZZZ, BOWL = sleep_and_eat_parts(27, 1, 25, 27)

PARTS = (
    Part("antenna", 15, 0, ANTENNA, pivot=(1, 3), z=1),
    Part("head", 6, 3, _head(), pivot=(10, 11), z=3),
    Part("eyes", 11, 6, EYES, pivot=(5, 6), z=4),
    Part("eyes_closed", 11, 6, EYES_CLOSED, pivot=(5, 6), z=4),
    Part("neck", 14, 13, rect(4, 2, "m", "o"), z=1),
    Part("torso", 8, 15, _torso(), z=2),
    Part("lights", 13, 19, LIGHTS, z=3),
    Part("arm_l", 4, 16, _arm(), pivot=(2, 1), z=3),
    Part("arm_r", 24, 16, _arm(), pivot=(2, 1), z=3),
    Part("leg_l", 10, 24, rect(5, 5, "a", "o", "l", "d"), pivot=(2.5, 0), z=1),
    Part("leg_r", 17, 24, rect(5, 5, "a", "o", "l", "d"), pivot=(2.5, 0), z=1),
    Part("foot_l", 9, 28, rect(7, 4, "m", "o"), z=2),
    Part("foot_r", 16, 28, rect(7, 4, "m", "o"), z=2),
    ZZZ,
    BOWL,
)
HEAD = ("head", "eyes", "eyes_closed")
UPPER = HEAD + ("neck", "torso", "lights", "arm_l", "arm_r", "antenna")


def _head_pose(t: float, asleep: bool = False, dy: float = 0.0, angle: float = 0.0):
    shut = asleep or blink(t, 3.6, 0.2)
    return {
        "head": Pose(dy=dy, angle=angle),
        "eyes": Pose(dy=dy, angle=angle, visible=not shut),
        "eyes_closed": Pose(dy=dy, angle=angle, visible=shut),
    }


def pose(state: str, t: float) -> dict[str, Pose]:
    poses = fx_poses(state, t)
    poses["lights"] = Pose(visible=(t % 1.0) < 0.6)
    if state == "idle":
        poses.update(_head_pose(t, dy=sine(t, 3, 0.4), angle=sine(t, 6, 3)))
        poses["antenna"] = Pose(angle=sine(t, 2.0, 10))
        poses["torso"] = Pose(sy=1 + sine(t, 3, 0.015))
        poses["arm_l"] = Pose(angle=sine(t, 3, 3))
        poses["arm_r"] = Pose(angle=-sine(t, 3, 3))
    elif state == "walk":
        step = sine(t, 0.6, 1.0)
        bob = -abs(step) * 0.8
        poses["leg_l"] = Pose(dy=-max(0.0, step) * 2)
        poses["leg_r"] = Pose(dy=-max(0.0, -step) * 2)
        poses["foot_l"] = Pose(dy=-max(0.0, step) * 2)
        poses["foot_r"] = Pose(dy=-max(0.0, -step) * 2)
        poses["arm_l"] = Pose(angle=-24 * step, dy=bob)
        poses["arm_r"] = Pose(angle=24 * step, dy=bob)
        poses.update(_head_pose(t, dy=bob))
        poses["antenna"] = Pose(angle=sine(t, 0.6, 14), dy=bob)
        lift(poses, ("torso", "neck"), dy=bob)
        poses["lights"] = Pose(visible=(t % 1.0) < 0.6, dy=bob)
    elif state == "eat":  # recharge: lights flash fast
        poses["lights"] = Pose(visible=(t % 0.3) < 0.15)
        poses.update(_head_pose(t, dy=2, angle=4))
        poses["arm_l"] = Pose(angle=35)
        poses["arm_r"] = Pose(angle=-35)
        poses["antenna"] = Pose(angle=sine(t, 0.3, 8))
    elif state == "sleep":  # power down
        poses.update(_head_pose(t, asleep=True, dy=2, angle=6))
        poses["lights"] = Pose(visible=False)
        poses["antenna"] = Pose(angle=40)
        poses["arm_l"] = Pose(angle=4)
        poses["arm_r"] = Pose(angle=-4)
        lift(poses, ("torso",), dy=1)
    else:  # special: dance with pumping arms and a spinning antenna
        beat = sine(t, 0.6, 1.0)
        bounce = -abs(math.sin(2 * math.pi * t / 0.6)) * 1.5
        poses.update(_head_pose(t, dy=bounce, angle=10 * beat))
        poses["arm_l"] = Pose(angle=110 + 40 * beat, dy=bounce)
        poses["arm_r"] = Pose(angle=-110 + 40 * beat, dy=bounce)
        poses["antenna"] = Pose(sx=math.cos(2 * math.pi * t / 0.8), dy=bounce)
        poses["leg_l"] = Pose(dy=-max(0.0, beat) * 2)
        poses["leg_r"] = Pose(dy=-max(0.0, -beat) * 2)
        lift(poses, ("torso", "neck"), dy=bounce, dx=beat * 1.2)
        poses["lights"] = Pose(visible=(t % 0.2) < 0.1, dy=bounce, dx=beat * 1.2)
    return poses


SPEC = PetSpec(
    key="robot",
    palette=PALETTE,
    parts=PARTS,
    pose=pose,
    move="walk",
    speed=34,
    special_name="dance",
)
