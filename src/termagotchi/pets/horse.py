"""Horse: chestnut mare with a flowing mane that rears up and whinnies."""

from termagotchi.pets.quad import Look, arc, build, layout, make_pose
from termagotchi.sprites import FX_PALETTE, Part, PetSpec, Pose, lift, rect, sine

PALETTE = {
    **FX_PALETTE,
    "o": "#2e1a0e", "a": "#a8622c", "l": "#c98448", "d": "#7e4620", "c": "#c98448",
    "p": "#e8b9a0", "e": "#141414", "m": "#2b1d14", "M": "#4a3223", "h": "#3b3b3b",
}

LOOK = Look(body=(20, 9), head=(11, 13), leg_w=3, ears="point", ear_size=(3, 4), tail="tuft",
            tail_size=(4, 10), hoof="h", swing=24.0)
LAY = layout(LOOK)
MANE = Part("mane", LAY.hx - 2, LAY.hy + 1, rect(4, 11, "m", "o", "M", "m"), z=3)
PARTS, HEAD, BODY = build(LOOK, head_parts=(MANE,))


def special(poses: dict[str, Pose], t: float, rig) -> None:
    """Crouch, rear up on the hind legs, paw the air, then come down."""
    p = (t % 3.4) / 3.4
    if p < 0.2:
        poses["body"] = Pose(sy=0.92, dy=1)
    elif p < 0.7:
        k = arc((p - 0.2) / 0.5)
        poses["body"] = Pose(angle=-24 * k, dy=-2 * k)
        lift(poses, HEAD, dy=-6 * k, dx=-1 * k)
        poses["near_front"] = Pose(angle=-70 * k + sine(t, 0.3, 8) * k, dy=-4 * k)
        poses["far_front"] = Pose(angle=-60 * k - sine(t, 0.3, 8) * k, dy=-4 * k)
        poses["tail"] = Pose(angle=30 * k + sine(t, 0.4, 10))


SPEC = PetSpec(
    key="horse",
    palette=PALETTE,
    parts=PARTS,
    pose=make_pose(HEAD, BODY, LOOK, special),
    move="walk",
    speed=52,
    special_name="rear up",
)
