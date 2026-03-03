"""Boid (bird) agent for the flocking simulation."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field

import pygame


@dataclass
class FlockSettings:
    """Mutable runtime-tunable simulation parameters."""

    separation_weight: float = 1.5
    alignment_weight: float = 1.0
    cohesion_weight: float = 1.0
    perception_radius: float = 80.0
    separation_radius: float = 30.0
    max_speed: float = 4.0
    max_force: float = 0.15
    margin: int = 50
    turn_factor: float = 0.3
    mouse_force: float = 0.4


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
        mouse_pos: tuple[int, int] | None = None,
        mouse_buttons: tuple[bool, bool, bool] = (False, False, False),
    ) -> None:
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
            ax += (ali_x / ali_count - self.vx) * settings.alignment_weight * 0.05
            ay += (ali_y / ali_count - self.vy) * settings.alignment_weight * 0.05
        if coh_count > 0:
            ax += (coh_x / coh_count - self.x) * settings.cohesion_weight * 0.001
            ay += (coh_y / coh_count - self.y) * settings.cohesion_weight * 0.001

        # Mouse attraction (left-click) / repulsion (right-click)
        if mouse_pos is not None and (mouse_buttons[0] or mouse_buttons[2]):
            mdx = mouse_pos[0] - self.x
            mdy = mouse_pos[1] - self.y
            mdist = (mdx * mdx + mdy * mdy) ** 0.5
            if mdist > 0:
                direction = 1.0 if mouse_buttons[0] else -1.0
                strength = settings.mouse_force / max(mdist * 0.02, 0.5)
                ax += direction * mdx / mdist * strength
                ay += direction * mdy / mdist * strength

        # Steer away from edges
        if self.x < settings.margin:
            ax += settings.turn_factor
        elif self.x > width - settings.margin:
            ax -= settings.turn_factor
        if self.y < settings.margin:
            ay += settings.turn_factor
        elif self.y > height - settings.margin:
            ay -= settings.turn_factor

        # Clamp acceleration
        force = (ax * ax + ay * ay) ** 0.5
        if force > settings.max_force:
            ax = ax / force * settings.max_force
            ay = ay / force * settings.max_force

        self.vx += ax
        self.vy += ay

        # Clamp speed
        speed = (self.vx * self.vx + self.vy * self.vy) ** 0.5
        if speed > settings.max_speed:
            self.vx = self.vx / speed * settings.max_speed
            self.vy = self.vy / speed * settings.max_speed

        self.x += self.vx
        self.y += self.vy

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the boid as a small triangle pointing in its direction of travel."""
        angle = math.atan2(self.vy, self.vx)
        size = 6
        points = [
            (self.x + math.cos(angle) * size * 2, self.y + math.sin(angle) * size * 2),
            (
                self.x + math.cos(angle + 2.5) * size,
                self.y + math.sin(angle + 2.5) * size,
            ),
            (
                self.x + math.cos(angle - 2.5) * size,
                self.y + math.sin(angle - 2.5) * size,
            ),
        ]
        pygame.draw.polygon(surface, (220, 220, 220), points)
