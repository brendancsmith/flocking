"""Boid (bird) agent for the flocking simulation."""

from __future__ import annotations

import random
from dataclasses import dataclass, field


@dataclass
class FlockSettings:
    """Mutable runtime-tunable simulation parameters."""

    separation_weight: float = 1.5
    alignment_weight: float = 1.0
    cohesion_weight: float = 1.0
    alignment_damping: float = 0.05
    cohesion_damping: float = 0.001
    perception_radius: float = 80.0
    separation_radius: float = 30.0
    max_speed: float = 4.0
    max_force: float = 0.15
    margin: int = 50
    turn_factor: float = 0.3
    mouse_force: float = 0.4
    mouse_falloff: float = 0.02
    mouse_min_factor: float = 0.5


@dataclass
class MouseState:
    """Current mouse input state."""

    pos: tuple[int, int]
    attract: bool
    repel: bool


@dataclass
class Boid:
    """A single bird in the flock."""

    x: float
    y: float
    vx: float = field(default_factory=lambda: random.uniform(-2, 2))
    vy: float = field(default_factory=lambda: random.uniform(-2, 2))

    def update(
        self,
        flock: list[Boid],
        width: int,
        height: int,
        settings: FlockSettings,
        mouse: MouseState | None = None,
    ) -> None:
        ax, ay = self._flock_forces(flock, settings)
        mx, my = self._mouse_steering(settings, mouse)
        ax += mx
        ay += my
        ex, ey = self._edge_avoidance(width, height, settings)
        ax += ex
        ay += ey

        ax, ay = _clamp(ax, ay, settings.max_force)
        self.vx += ax
        self.vy += ay
        self.vx, self.vy = _clamp(self.vx, self.vy, settings.max_speed)

        self.x += self.vx
        self.y += self.vy

    def _flock_forces(self, flock: list[Boid], settings: FlockSettings) -> tuple[float, float]:
        """Compute combined separation, alignment, and cohesion in a single neighbor pass."""
        ax, ay = 0.0, 0.0
        sep_x, sep_y, sep_count = 0.0, 0.0, 0
        ali_x, ali_y, ali_count = 0.0, 0.0, 0
        coh_x, coh_y, coh_count = 0.0, 0.0, 0

        for other in flock:
            if other is self:
                continue
            dx = other.x - self.x
            dy = other.y - self.y
            dist = (dx * dx + dy * dy) ** 0.5
            if dist < settings.perception_radius:
                ali_x += other.vx
                ali_y += other.vy
                ali_count += 1
                coh_x += other.x
                coh_y += other.y
                coh_count += 1
                if dist < settings.separation_radius and dist > 0:
                    sep_x -= dx / dist
                    sep_y -= dy / dist
                    sep_count += 1

        if sep_count > 0:
            ax += sep_x / sep_count * settings.separation_weight
            ay += sep_y / sep_count * settings.separation_weight
        if ali_count > 0:
            steer_x = (ali_x / ali_count - self.vx) * settings.alignment_damping
            steer_y = (ali_y / ali_count - self.vy) * settings.alignment_damping
            ax += steer_x * settings.alignment_weight
            ay += steer_y * settings.alignment_weight
        if coh_count > 0:
            steer_x = (coh_x / coh_count - self.x) * settings.cohesion_damping
            steer_y = (coh_y / coh_count - self.y) * settings.cohesion_damping
            ax += steer_x * settings.cohesion_weight
            ay += steer_y * settings.cohesion_weight

        return ax, ay

    def _mouse_steering(
        self, settings: FlockSettings, mouse: MouseState | None
    ) -> tuple[float, float]:
        if mouse is None or not (mouse.attract or mouse.repel):
            return 0.0, 0.0
        mdx = mouse.pos[0] - self.x
        mdy = mouse.pos[1] - self.y
        mdist = (mdx * mdx + mdy * mdy) ** 0.5
        if mdist == 0:
            return 0.0, 0.0
        direction = 1.0 if mouse.attract else -1.0
        strength = settings.mouse_force / max(
            mdist * settings.mouse_falloff, settings.mouse_min_factor
        )
        return direction * mdx / mdist * strength, direction * mdy / mdist * strength

    def _edge_avoidance(
        self, width: int, height: int, settings: FlockSettings
    ) -> tuple[float, float]:
        ax, ay = 0.0, 0.0
        if self.x < settings.margin:
            ax += settings.turn_factor
        elif self.x > width - settings.margin:
            ax -= settings.turn_factor
        if self.y < settings.margin:
            ay += settings.turn_factor
        elif self.y > height - settings.margin:
            ay -= settings.turn_factor
        return ax, ay


def _clamp(x: float, y: float, limit: float) -> tuple[float, float]:
    """Clamp a 2D vector to a maximum magnitude."""
    mag = (x * x + y * y) ** 0.5
    if mag > limit:
        return x / mag * limit, y / mag * limit
    return x, y
