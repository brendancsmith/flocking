"""Flocking simulation entry point."""

from __future__ import annotations

import math
import random

import pygame

from flocking.birds import Boid, Bounds, FlockSettings, MouseState

__all__ = ["BG_COLOR", "BOUNDS", "HEIGHT", "WIDTH", "draw_boid", "make_flock", "step_and_render"]

WIDTH = 1024
HEIGHT = 768
BOUNDS: Bounds = (WIDTH, HEIGHT)
NUM_BOIDS = 100
FPS = 60
BG_COLOR = (15, 15, 25)
HUD_COLOR = (180, 180, 180)
SPAWN_BURST = 10
SPAWN_SCATTER = 20.0

# Keyboard adjustment constants
SPEED_STEP = 0.5
SPEED_MIN = 1.0
SPEED_MAX = 12.0
PERCEPTION_STEP = 10.0
PERCEPTION_MIN = 20.0
PERCEPTION_MAX = 200.0

# Boid rendering
BOID_SIZE = 6
BOID_COLOR = (220, 220, 220)
WING_ANGLE = 2.5  # radians (~143 degrees)
NOSE_LENGTH_RATIO = 2


def make_flock(n: int, bounds: Bounds) -> list[Boid]:
    width, height = bounds
    return [Boid(x=random.uniform(0, width), y=random.uniform(0, height)) for _ in range(n)]


def spawn_at(flock: list[Boid], x: float, y: float, count: int = SPAWN_BURST) -> None:
    for _ in range(count):
        flock.append(
            Boid(
                x=x + random.uniform(-SPAWN_SCATTER, SPAWN_SCATTER),
                y=y + random.uniform(-SPAWN_SCATTER, SPAWN_SCATTER),
            )
        )


def draw_boid(surface: pygame.Surface, boid: Boid) -> None:
    angle = math.atan2(boid.vy, boid.vx)
    points = [
        (
            boid.x + math.cos(angle) * BOID_SIZE * NOSE_LENGTH_RATIO,
            boid.y + math.sin(angle) * BOID_SIZE * NOSE_LENGTH_RATIO,
        ),
        (
            boid.x + math.cos(angle + WING_ANGLE) * BOID_SIZE,
            boid.y + math.sin(angle + WING_ANGLE) * BOID_SIZE,
        ),
        (
            boid.x + math.cos(angle - WING_ANGLE) * BOID_SIZE,
            boid.y + math.sin(angle - WING_ANGLE) * BOID_SIZE,
        ),
    ]
    pygame.draw.polygon(surface, BOID_COLOR, points)


def step_and_render(
    surface: pygame.Surface,
    flock: list[Boid],
    bounds: Bounds,
    settings: FlockSettings,
    mouse: MouseState | None = None,
) -> None:
    """Update all boids and redraw the scene."""
    for boid in flock:
        boid.update(flock, bounds, settings, mouse)
    surface.fill(BG_COLOR)
    for boid in flock:
        draw_boid(surface, boid)


def draw_hud(
    surface: pygame.Surface,
    font: pygame.font.Font,
    clock: pygame.time.Clock,
    flock: list[Boid],
    settings: FlockSettings,
    paused: bool,
) -> None:
    lines = [
        f"Boids: {len(flock)}   FPS: {clock.get_fps():.0f}",
        f"Speed: {settings.max_speed:.1f}   Perception: {settings.perception_radius:.0f}",
        f"Sep: {settings.separation_weight:.1f}  Ali: {settings.alignment_weight:.1f}"
        f"  Coh: {settings.cohesion_weight:.1f}",
    ]
    if paused:
        lines.insert(0, "PAUSED")
    y = 10
    for line in lines:
        img = font.render(line, True, HUD_COLOR)
        surface.blit(img, (10, y))
        y += img.get_height() + 2


def handle_keydown(key: int, flock: list[Boid], settings: FlockSettings) -> tuple[list[Boid], bool]:
    """Handle a keydown event. Returns (flock, should_toggle_pause)."""
    if key == pygame.K_p:
        return flock, True
    if key == pygame.K_r:
        return make_flock(NUM_BOIDS, BOUNDS), False
    if key == pygame.K_SPACE:
        mx, my = pygame.mouse.get_pos()
        spawn_at(flock, mx, my)
        return flock, False
    if key == pygame.K_UP:
        settings.max_speed = min(settings.max_speed + SPEED_STEP, SPEED_MAX)
        return flock, False
    if key == pygame.K_DOWN:
        settings.max_speed = max(settings.max_speed - SPEED_STEP, SPEED_MIN)
        return flock, False
    if key in (pygame.K_PLUS, pygame.K_EQUALS):
        settings.perception_radius = min(
            settings.perception_radius + PERCEPTION_STEP, PERCEPTION_MAX
        )
        return flock, False
    if key == pygame.K_MINUS:
        settings.perception_radius = max(
            settings.perception_radius - PERCEPTION_STEP, PERCEPTION_MIN
        )
        return flock, False
    return flock, False


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flocking")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 14)

    settings = FlockSettings()
    flock = make_flock(NUM_BOIDS, BOUNDS)
    paused = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    flock, toggle = handle_keydown(event.key, flock, settings)
                    if toggle:
                        paused = not paused
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                spawn_at(flock, event.pos[0], event.pos[1])

        if not paused:
            buttons = pygame.mouse.get_pressed()
            mouse = MouseState(
                pos=pygame.mouse.get_pos(),
                attract=buttons[0],
                repel=buttons[2],
            )
            step_and_render(screen, flock, BOUNDS, settings, mouse)
        else:
            screen.fill(BG_COLOR)
            for boid in flock:
                draw_boid(screen, boid)

        draw_hud(screen, font, clock, flock, settings, paused)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
