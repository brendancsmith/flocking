"""Flocking simulation entry point."""

from __future__ import annotations

import random

import pygame

from flocking.birds import Boid, FlockSettings

WIDTH = 1024
HEIGHT = 768
NUM_BOIDS = 100
FPS = 60
BG_COLOR = (15, 15, 25)
HUD_COLOR = (180, 180, 180)
SPAWN_BURST = 10


def make_flock(n: int) -> list[Boid]:
    return [Boid(x=random.uniform(0, WIDTH), y=random.uniform(0, HEIGHT)) for _ in range(n)]


def spawn_at(flock: list[Boid], x: float, y: float, count: int = SPAWN_BURST) -> None:
    for _ in range(count):
        flock.append(Boid(x=x + random.uniform(-20, 20), y=y + random.uniform(-20, 20)))


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


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flocking")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 14)

    settings = FlockSettings()
    flock = make_flock(NUM_BOIDS)
    paused = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_r:
                    flock = make_flock(NUM_BOIDS)
                elif event.key == pygame.K_SPACE:
                    mx, my = pygame.mouse.get_pos()
                    spawn_at(flock, mx, my)
                elif event.key == pygame.K_UP:
                    settings.max_speed = min(settings.max_speed + 0.5, 12.0)
                elif event.key == pygame.K_DOWN:
                    settings.max_speed = max(settings.max_speed - 0.5, 1.0)
                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                    settings.perception_radius = min(settings.perception_radius + 10, 200)
                elif event.key == pygame.K_MINUS:
                    settings.perception_radius = max(settings.perception_radius - 10, 20)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                spawn_at(flock, event.pos[0], event.pos[1])

        if not paused:
            mouse_pos = pygame.mouse.get_pos()
            mouse_buttons = pygame.mouse.get_pressed()
            for boid in flock:
                boid.update(flock, WIDTH, HEIGHT, settings, mouse_pos, mouse_buttons)

        screen.fill(BG_COLOR)
        for boid in flock:
            boid.draw(screen)
        draw_hud(screen, font, clock, flock, settings, paused)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
