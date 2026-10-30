"""Pet behavior: picks what a desktop pet does next. No Qt, so it is testable."""

from __future__ import annotations

import random

# state -> (selection weight, min seconds, max seconds). Walking ends on arrival.
CHOICES: dict[str, tuple[float, float, float]] = {
    "idle": (30, 1.5, 4.0),
    "walk": (35, 3.0, 12.0),
    "eat": (10, 2.5, 4.0),
    "sleep": (10, 5.0, 10.0),
    "special": (15, 2.0, 4.0),
}


class Brain:
    """Moves one pet along a horizontal strip and switches its state over time."""

    def __init__(self, left: float, right: float, speed: float, rng: random.Random | None = None):
        self.left = left
        self.right = right
        self.speed = speed
        self.rng = rng or random.Random()
        self.x = self.rng.uniform(left, right)
        self.facing = 1
        self.state = "idle"
        self.state_time = 0.0
        self.duration = 2.0
        self.target = self.x
        self.held = False

    def set_state(self, state: str, duration: float | None = None) -> None:
        """Switch state now. Walking picks a new target on the strip."""
        _, low, high = CHOICES[state]
        self.state = state
        self.state_time = 0.0
        self.duration = duration if duration is not None else self.rng.uniform(low, high)
        if state == "walk":
            self.target = self.rng.uniform(self.left, self.right)
            self.facing = 1 if self.target >= self.x else -1

    def _next(self) -> None:
        states = list(CHOICES)
        weights = [CHOICES[s][0] for s in states]
        self.set_state(self.rng.choices(states, weights)[0])

    def update(self, dt: float) -> None:
        """Advance by dt seconds."""
        if self.held:
            return
        self.state_time += dt
        if self.state == "walk":
            step = self.speed * dt
            if abs(self.target - self.x) <= step or self.state_time > self.duration:
                self.x = min(max(self.target, self.left), self.right)
                self._next()
                return
            self.x += step * self.facing
        elif self.state_time >= self.duration:
            self._next()
