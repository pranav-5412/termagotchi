"""Dog: tan pup with floppy ears that does a play bow and barks."""

from termagotchi.sprites import FX_PALETTE, Part, PetSpec, Pose, blink, fx_poses, grid, sine, sleep_and_eat_parts

PALETTE = {
    **FX_PALETTE,
    "o": "#33200f", "a": "#d9a35f", "l": "#ecc487", "d": "#b07a38", "D": "#9a6a2e",
    "c": "#f7ead2", "b": "#6b4423", "n": "#141414", "e": "#1e1e1e", "w": "#ffffff",
    "t": "#e86a7a",
}

TAIL = grid("""
oo....
oao...
oao...
.oao..
.oao..
..oao.
..oao.
...oao
""")
BODY = grid("""
..ooooooooooooo..
.ollllllllllllo..
oaaaaaabbbbaaaaao
oaaaaabbbbbbaaaao
oaaaaaabbbbaaaaao
oaaaaaaaaaaaaaaao
oaaaaaaaaaaaaaaao
.occccccccccccco.
..ooooooooooooo..
""")
HEAD = grid("""
...ooooooo...
..oaaaaaaao..
.oaaaaaaaaao.
oaaaaaaaaaaao
oaaaaaaaaaaao
oaaaaaaaaaaao
oaaacccccaaao
oaaccnnnccaao
oaacccccccaao
.oaacctccaao.
..ooooooooo..
""")
EAR_L = grid("""
.ooo
obbo
obbo
obbo
obbo
.obo
..oo
""")
EAR_R = grid("""
ooo.
obbo
obbo
obbo
obbo
obo.
oo..
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
ew.....we
ee.....ee
""")
EYES_CLOSED = grid("""
oo.....oo
.........
""")
BANG = grid("""
o.o
o.o
o.o
...
o.o
""")

ZZZ, BOWL = sleep_and_eat_parts(27, 2, 26, 27)

PARTS = (
    Part("tail", 0, 11, TAIL, pivot=(5, 7), z=0),
    Part("far_back", 8, 21, FAR_LEG, pivot=(2, 0), z=1),
    Part("far_front", 19, 21, FAR_LEG, pivot=(2, 0), z=1),
    Part("body", 6, 14, BODY, z=2),
    Part("near_back", 11, 21, LEG, pivot=(2, 0), z=3),
    Part("near_front", 22, 21, LEG, pivot=(2, 0), z=3),
    Part("ear_l", 15, 8, EAR_L, pivot=(2, 0), z=3),
    Part("ear_r", 28, 8, EAR_R, pivot=(2, 0), z=3),
    Part("head", 17, 7, HEAD, pivot=(6.5, 9), z=4),
    Part("eyes", 19, 10, EYES, pivot=(4.5, 0), z=5),
    Part("eyes_closed", 19, 10, EYES_CLOSED, pivot=(4.5, 0), z=5),
    Part("bang", 26, 0, BANG, z=6),
    ZZZ,
    BOWL,
)


def _face(t: float, asleep: bool = False, dy: float = 0.0, angle: float = 0.0, flap: float = 0.0):
    """Head, eyes, and ears move together."""
    shut = asleep or blink(t, 3.8)
    return {
        "head": Pose(dy=dy, angle=angle),
        "eyes": Pose(dy=dy, angle=angle, visible=not shut),
        "eyes_closed": Pose(dy=dy, angle=angle, visible=shut),
        "ear_l": Pose(dy=dy, angle=angle + flap),
        "ear_r": Pose(dy=dy, angle=angle - flap),
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
    poses["bang"] = Pose(visible=False)
    if state == "idle":
        poses.update(_face(t, dy=sine(t, 2.6, 0.5), angle=sine(t, 5, 3), flap=sine(t, 2.6, 3)))
        poses["body"] = Pose(sy=1 + sine(t, 2.6, 0.02))
        poses["tail"] = Pose(angle=sine(t, 1.0, 20))
    elif state == "walk":
        poses.update(_legs(sine(t, 0.55, 26)))
        bob = abs(sine(t, 0.55, 0.7)) - 0.4
        poses.update(_face(t, dy=bob, flap=sine(t, 0.55, 12, 0.2)))
        poses["body"] = Pose(dy=bob)
        poses["tail"] = Pose(angle=sine(t, 0.35, 22))
    elif state == "eat":
        poses.update(_face(t, dy=3.5 + sine(t, 0.45, 1.3), angle=sine(t, 0.45, 5), flap=sine(t, 0.45, 8)))
        poses["tail"] = Pose(angle=sine(t, 0.5, 25))
    elif state == "sleep":
        poses.update(_face(t, asleep=True, dy=4, angle=6, flap=-8))
        poses["body"] = Pose(sy=0.95 + sine(t, 3.4, 0.015), dy=1)
        poses["tail"] = Pose(angle=10)
    else:  # special: play bow, then bark twice
        cycle = t % 2.4
        bark = cycle > 0.8 and (cycle % 0.6) < 0.25
        poses["body"] = Pose(angle=7, dy=1)
        poses.update(_face(t, dy=4 - (3 if bark else 0), angle=7 - (14 if bark else 0), flap=sine(t, 0.3, 14)))
        poses.update(_legs(0))
        poses["near_front"] = Pose(angle=22)
        poses["far_front"] = Pose(angle=22)
        poses["tail"] = Pose(angle=sine(t, 0.25, 26), dy=-3)
        poses["bang"] = Pose(visible=bark, dy=-sine(t, 0.3, 1))
    return poses


SPEC = PetSpec(
    key="dog",
    palette=PALETTE,
    parts=PARTS,
    pose=pose,
    move="walk",
    speed=46,
    special_name="play bow",
)
