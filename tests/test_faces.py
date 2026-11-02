"""Tests for mood faces."""

import pytest

from termagotchi.faces import FACES, face
from termagotchi.mood import MOODS


def test_every_mood_has_a_face():
    assert set(FACES) == set(MOODS)


def test_faces_are_distinct():
    assert len(set(FACES.values())) == len(MOODS)


def test_face_lookup():
    assert face("happy") == FACES["happy"]


def test_unknown_mood_raises():
    with pytest.raises(KeyError):
        face("angry")
