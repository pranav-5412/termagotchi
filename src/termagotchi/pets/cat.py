"""Cat: orange tabby that pounces."""

import math

from termagotchi.sprites import FX_PALETTE, Part, PetSpec, Pose, blink, fx_poses, grid, sine, sleep_and_eat_parts

PALETTE = {
    **FX_PALETTE,
    "o": "#3a2112", "a": "#e8923c", "l": "#f7b864", "d": "#b8641f", "D": "#a35a1e",
    "c": "#fbe6c0", "p": "#f08a9a", "n": "#e0707f", "g": "#8fd14f", "e": "#1e1e1e",
}

TAIL = grid("""
.oo....
oaao...
odao...
oaao...
oaao...
.oao...
.oao...
..oao..
..oao..
...oao.
...oaao
....oao
.....oo
""")
BODY = grid("""
..ooooooooooooo..
.ollllllllllllo..
oaaaaadaaadaaaaao
oaaaaaadaaadaaaao
oaaaaaaaaaaaaaaao
oaaaaaaaaaaaaaaao
oaaaaaaaaaaaaaaao
.occccccccccccco.
..ooooooooooooo..
""")
HEAD = grid("""
oo.........oo
oaoo.....ooao
oapaoooooapao
oaaadaaadaaao
oaaaaaaaaaaao
oaaaaaaaaaaao
oaaaaaaaaaaao
oaacccnccaaao
oaacccccccaao
.oaaaaaaaaao.
..ooooooooo..
""")
LEG = grid("""
oaao
oaao
oaao
oaao
oaao
oaco
occo
oooo
""")
FAR_LEG = grid("""
oDDo
oDDo
oDDo
oDDo
oDDo
oDDo
oDDo
oooo
""")
EYES = grid("""
gg.....gg
ge.....eg
ge.....eg
""")
EYES_CLOSED = grid("""
.........
oo.....oo
.........
""")

ZZZ, BOWL = sleep_and_eat_parts(27, 2, 26, 27)

PARTS = (
    Part("tail", 0, 9, TAIL, pivot=(5.5, 12), z=0),
    Part("far_back", 8, 21, FAR_LEG, pivot=(2, 0), z=1),
    Part("far_front", 19, 21, FAR_LEG, pivot=(2, 0), z=1),
    Part("body", 6, 14, BODY, z=2),
    Part("near_back", 11, 21, LEG, pivot=(2, 0), z=3),
    Part("near_front", 22, 21, LEG, pivot=(2, 0), z=3),
    Part("head", 18, 7, HEAD, pivot=(6.5, 9), z=4),
    Part("eyes", 20, 11, EYES, pivot=(4.5, 0), z=5),
    Part("eyes_closed", 20, 11, EYES_CLOSED, pivot=(4.5, 0), z=5),
    ZZZ,
    BOWL,
)


def _face(t: float, asleep: bool = False, dy: float = 0.0, angle: float = 0.0) -> dict[str, Pose]:
    """Head and eyes move together; eyes close on blink or sleep."""
    shut = asleep or blink(t)
    return {
        "head": Pose(dy=dy, angle=angle),
        "eyes": Pose(dy=dy, angle=angle, visible=not shut),
        "eyes_closed": Pose(dy=dy, angle=angle, visible=shut),
    }


def _legs(swing: float) -> dict[str, Pose]:
    return {
        "near_front": Pose(angle=swing),
        "far_front": Pose(angle=-swing),
        "near_back": Pose(angle=-swing),
        "far_back": Pose(angle=swing),
    }


def pose(state: str, t: float) -> dict[str, Pose]:
    poses = fx_poses(state, t)
    if state == "idle":
        poses.update(_face(t, dy=sine(t, 3, 0.4)))
        poses["body"] = Pose(sy=1 + sine(t, 3, 0.02))
        poses["tail"] = Pose(angle=sine(t, 2.4, 12))
    elif state == "walk":
        swing = sine(t, 0.6, 26)
        poses.update(_legs(swing))
        poses.update(_face(t, dy=abs(sine(t, 0.6, 0.7)) - 0.4))
        poses["body"] = Pose(dy=abs(sine(t, 0.6, 0.6)) - 0.3)
        poses["tail"] = Pose(angle=-8 + sine(t, 0.6, 6))
    elif state == "eat":
        poses.update(_face(t, dy=3 + sine(t, 0.5, 1.2), angle=sine(t, 0.5, 5)))
        poses["tail"] = Pose(angle=sine(t, 1.6, 10))
    elif state == "sleep":
        poses.update(_face(t, asleep=True, dy=3, angle=8))
        poses["body"] = Pose(sy=0.95 + sine(t, 3.5, 0.015), dy=1)
        poses["tail"] = Pose(angle=14)
    else:  # special: stalk, pounce, land
        p = (t % 3.0) / 3.0
        if p < 0.4:  # crouch and wiggle
            poses["body"] = Pose(sy=0.85, dy=2)
            poses.update(_face(t, dy=3.5))
            poses["tail"] = Pose(angle=sine(t, 0.25, 16))
            poses.update(_legs(sine(t, 0.3, 4)))
        elif p < 0.72:  # leap in an arc
            k = (p - 0.4) / 0.32
            lift = -11 * math.sin(math.pi * k)
            tilt = -14 + 28 * k
            poses["body"] = Pose(dy=lift, angle=tilt * 0.5, sy=1.05)
            poses.update(_face(t, dy=lift - 1, angle=tilt * 0.4))
            poses["tail"] = Pose(dy=lift, angle=30)
            poses.update(_legs(-35 + 70 * k))
            for name in ("near_front", "far_front", "near_back", "far_back"):
                poses[name] = Pose(dy=lift, angle=poses[name].angle)
        else:  # settle
            k = (p - 0.72) / 0.28
            poses["body"] = Pose(sy=0.9 + 0.1 * k, dy=1 - k)
            poses.update(_face(t, dy=1 - k))
            poses["tail"] = Pose(angle=20 - 20 * k)
    return poses


SPEC = PetSpec(
    key="cat",
    palette=PALETTE,
    parts=PARTS,
    pose=pose,
    move="walk",
    speed=38,
    special_name="pounce",
)
