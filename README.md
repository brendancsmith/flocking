# Flocking

A flock of little birds. Multi-agent CLI for sports betting analysis powered by the Claude Agent SDK.

## Setup

```bash
uv sync
```

Requires the [sports](https://github.com/brendancsmith/sports) CLI to be set up at `~/repos/brendancsmith/sports` with data in `~/.sports/`.

## Usage

```bash
# Ask the flock anything
flocking ask "What are the best value bets this week?"

# Filter to a specific sport
flocking ask "Who's going to win tonight?" --sport nba

# Allow more agent turns for complex questions
flocking ask "Build me a Kelly portfolio across all sports" --max-turns 50
```

## How It Works

Flocking spawns a lead agent that coordinates two specialist birds:

- **Lark** (Data Scout) fetches fresh data, standings, schedules, and results
- **Kite** (Betting Analyst) runs predictions, finds value bets, and builds portfolios

The lead deploys Lark first to gather context, then Kite for analysis, and synthesizes their findings into a concise betting brief.
