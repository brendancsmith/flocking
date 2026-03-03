# Flocking

A flocking birds simulation using classic [boids](https://en.wikipedia.org/wiki/Boids) rules.

## Setup

```bash
uv sync
```

## Usage

```bash
flocking
```

Press **Escape** or close the window to quit.

## How It Works

Each bird follows three simple rules:

1. **Separation** — steer away from nearby neighbors to avoid crowding
2. **Alignment** — match the heading of nearby neighbors
3. **Cohesion** — steer toward the average position of nearby neighbors

These local rules produce emergent flocking behavior with no central coordination.
