# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Flocking is a boids flocking simulation — a pygame GUI that renders a flock of birds following separation, alignment, and cohesion rules.

## Commands

```bash
uv sync                          # install dependencies
uv run flocking                  # run the simulation
uv run ruff check src/           # lint
uv run ruff format --check src/  # format check
uv run mypy src/                 # type check
```

## Architecture

- `src/flocking/main.py` — Pygame event loop, window setup, renders the flock each frame
- `src/flocking/birds.py` — `Boid` dataclass implementing the three classic boid rules (separation, alignment, cohesion) plus edge avoidance. Each boid draws itself as a directional triangle.

Tuning constants (weights, radii, speeds) are module-level in `birds.py`.

## Style

- Ruff: line-length 100, target py311, rules: E, F, I, N, W, UP
- mypy: strict mode (pygame stubs missing, so `ignore_missing_imports = true` for pygame)
