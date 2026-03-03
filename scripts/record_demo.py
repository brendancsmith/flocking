"""Record a short demo gif of the flocking simulation."""

from __future__ import annotations

import os
import random
import tempfile

os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame  # noqa: E402

from flocking.birds import Boid, FlockSettings  # noqa: E402
from flocking.main import BG_COLOR, HEIGHT, WIDTH, draw_boid, make_flock  # noqa: E402

FRAMES = 300  # 5 seconds at 60fps
RECORD_EVERY = 2  # save every Nth frame (30fps output)


def main() -> None:
    pygame.init()
    screen = pygame.Surface((WIDTH, HEIGHT))

    random.seed(42)
    settings = FlockSettings()
    flock = make_flock(100, WIDTH, HEIGHT)

    with tempfile.TemporaryDirectory() as tmpdir:
        saved = 0
        for frame in range(FRAMES):
            for boid in flock:
                boid.update(flock, WIDTH, HEIGHT, settings)

            screen.fill(BG_COLOR)
            for boid in flock:
                draw_boid(screen, boid)

            if frame % RECORD_EVERY == 0:
                path = os.path.join(tmpdir, f"frame_{saved:04d}.bmp")
                pygame.image.save(screen, path)
                saved += 1

        pygame.quit()

        gif_path = os.path.join(os.path.dirname(__file__), "..", "demo.gif")
        gif_path = os.path.normpath(gif_path)
        os.system(
            f"ffmpeg -y -framerate 30 -i {tmpdir}/frame_%04d.bmp "
            f"-vf 'scale=512:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse' "
            f"{gif_path}"
        )
        print(f"Saved demo to {gif_path}")


if __name__ == "__main__":
    main()
