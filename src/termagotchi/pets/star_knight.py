"""Star Knight: gold-armored knight with a star shield who slashes with a glowing arc."""

from termagotchi.pets.biped import (
    ARM_PIVOT, ARM_SLOTS, HEAD_SLOT, LEG_PIVOT, LEG_SLOTS, RIGHT_SHOULDER, TORSO_SLOT, base_pose,
    hold, neck_pivot,
)
from termagotchi.sprites import (
    FX_PALETTE, Part, PetSpec, Pose, blob, grid, lift, overlay, rect, sine, sleep_and_eat_parts,
)

PALETTE = {
    **FX_PALETTE,
    "o": "#3a2a05", "G": "#e8b923", "l": "#ffe27a", "d": "#a87b0e", "S": "#9aa5b5",
    "s": "#d6dde8", "k": "#4a5568", "P": "#3f6fd8", "p": "#7aa2ff", "V": "#1a1a22",
    "E": "#fff1a0", "W": "#fff7d6", "Y": "#ffd23a",
}

HAND_REST = (23.5, 24.0)  # where the sword hand sits with the arm hanging down
SWORD_X, SWORD_Y, SWORD_H = 21, 9, 17


def _head() -> tuple[str, ...]:
    helmet = blob(16, 14, "G", "o", "l", "d")
    helmet = overlay(helmet, grid("VVVVVVVVVV\nVVVVVVVVVV"), 3, 6)
    return overlay(helmet, grid("G\nG\nG"), 7, 5)


def _torso() -> tuple[str, ...]:
    torso = rect(12, 9, "G", "o", "l", "d")
    torso = overlay(torso, grid(".W.\nWWW\n.W."), 4, 2)
    return overlay(torso, grid("kkkkkkkkkk"), 1, 6)


def _arm() -> tuple[str, ...]:
    return overlay(rect(4, 9, "G", "o", "l", "d"), grid("SSSS\nSSSS"), 0, 7)


def _leg() -> tuple[str, ...]:
    return overlay(rect(5, 8, "G", "o", "l", "d"), grid("SSSSS\nSSSSS\nkkkkk"), 0, 5)


def _shield() -> tuple[str, ...]:
    return overlay(blob(9, 12, "S", "o", "s", "k"), grid(".Y.\nYYY\n.Y."), 3, 4)


def _sword() -> tuple[str, ...]:
    rows = ["..s.."] + [".sSk."] * 10 + ["GGGGG", "..d..", "..d..", ".YYY.", "..o.."]
    return grid("\n".join(rows))


def _slash() -> tuple[str, ...]:
    """A crescent: the part of one circle not covered by a shifted second circle."""
    w = 18
    rows = []
    for y in range(w):
        row = ""
        for x in range(w):
            outer = ((x - 8.5) / 8.5) ** 2 + ((y - 8.5) / 8.5) ** 2 <= 1
            inner = ((x - 5.5) / 8.5) ** 2 + ((y - 8.5) / 8.5) ** 2 <= 1
            row += ("W" if x > 11 else "Y") if outer and not inner else "."
        rows.append(row)
    return tuple(rows)


EYES = grid("""
EE....EE
EE....EE
""")
EYES_CLOSED = grid("""
........
........
""")

hx, hy = HEAD_SLOT
ZZZ, BOWL = sleep_and_eat_parts(27, 1, 25, 27)

PARTS = (
    Part("plume", 11, 0, blob(10, 6, "P", "o", "p", "P"), pivot=neck_pivot(11, 0), z=3),
    Part("leg_l", *LEG_SLOTS[0], _leg(), pivot=LEG_PIVOT, z=1),
    Part("leg_r", *LEG_SLOTS[1], _leg(), pivot=LEG_PIVOT, z=1),
    Part("torso", *TORSO_SLOT, _torso(), z=2),
    Part("sword", SWORD_X, SWORD_Y, _sword(), pivot=(HAND_REST[0] - SWORD_X, HAND_REST[1] - SWORD_Y), z=2),
    Part("arm_l", *ARM_SLOTS[0], _arm(), pivot=ARM_PIVOT, z=3),
    Part("shield", 0, 15, _shield(), pivot=(8, 3), z=4),
    Part("arm_r", *ARM_SLOTS[1], _arm(), pivot=ARM_PIVOT, z=3),
    Part("head", hx, hy, _head(), pivot=neck_pivot(hx, hy), z=4),
    Part("eyes", 12, 9, EYES, pivot=neck_pivot(12, 9), z=5),
    Part("eyes_closed", 12, 9, EYES_CLOSED, pivot=neck_pivot(12, 9), z=5),
    Part("slash", 10, 6, _slash(), pivot=(9, 9), z=6),
    ZZZ,
    BOWL,
)
HEAD_EXTRA = ("plume",)
RISER = ("head", "plume", "eyes", "eyes_closed", "torso", "arm_l", "arm_r", "shield", "sword")


def _grip(arm_angle: float, arm_dy: float = 0.0, blade: float = 0.0) -> Pose:
    """Keep the sword in the right hand. blade is 0 with the blade up, 1 along the arm."""
    return hold(RIGHT_SHOULDER, HAND_REST, arm_angle, arm_dy, 180 * blade)


def pose(state: str, t: float) -> dict[str, Pose]:
    poses = base_pose(state, t, HEAD_EXTRA)
    poses["slash"] = Pose(visible=False)
    arm_l, arm_r = poses["arm_l"], poses["arm_r"]
    poses["shield"] = arm_l
    poses["sword"] = _grip(arm_r.angle, arm_r.dy)
    poses["plume"] = Pose(angle=poses["plume"].angle + sine(t, 1.3, 5), dy=poses["plume"].dy)
    if state == "special":  # raise the sword, slash down with a glowing arc, sheathe
        p = (t % 3.0) / 3.0
        if p < 0.3:  # wind up
            k = p / 0.3
            raise_arm = -150 * k
            poses["arm_r"] = Pose(angle=raise_arm)
            poses["sword"] = _grip(raise_arm, blade=k)
        elif p < 0.5:  # slash
            k = (p - 0.3) / 0.2
            swing = -150 + 120 * k
            poses["arm_r"] = Pose(angle=swing)
            poses["sword"] = _grip(swing, blade=1)
            poses["slash"] = Pose(visible=True, angle=-70 + 140 * k, alpha=0.9)
            lift(poses, ("head", "plume", "eyes", "eyes_closed", "torso"), dy=0.6)
        elif p < 0.75:  # hold, glint
            poses["arm_r"] = Pose(angle=-30)
            poses["sword"] = _grip(-30, blade=1)
            poses["slash"] = Pose(visible=p < 0.6, angle=70, alpha=max(0.0, 1 - (p - 0.5) / 0.1))
        else:  # return to guard
            k = (p - 0.75) / 0.25
            back = -30 * (1 - k)
            poses["arm_r"] = Pose(angle=back)
            poses["sword"] = _grip(back, blade=1 - k)
    return poses


SPEC = PetSpec(
    key="star_knight",
    palette=PALETTE,
    parts=PARTS,
    pose=pose,
    move="walk",
    speed=32,
    special_name="star slash",
)
