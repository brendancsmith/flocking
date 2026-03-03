# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Flocking is a multi-agent CLI that orchestrates Claude subagents ("birds") to answer sports betting questions. It uses the Claude Agent SDK to spawn a lead agent that delegates to specialist birds:
- **Lark** (Data Scout): Fetches/checks sports data via the `sports` CLI
- **Kite** (Betting Analyst): Runs predictions, value bets, portfolio optimization via the `sports` CLI

The lead agent coordinates: Lark gathers data first, then Kite analyzes it, and the lead synthesizes a betting brief.

## Commands

```bash
# Install dependencies
uv sync

# Run the CLI
uv run flocking ask "What are the best NFL bets this week?"
uv run flocking ask "NBA standings" --sport nba
uv run flocking ask "Predict KC@BUF" --max-turns 50

# Lint
uv run ruff check src/
uv run ruff format --check src/

# Type check
uv run mypy src/
```

## Architecture

- `src/flocking/main.py` — Typer CLI app. Defines the `ask` command and the lead agent's system prompt. Streams responses from `claude_agent_sdk.query()`.
- `src/flocking/birds.py` — `AgentDefinition` configs for each bird. The `FLOCK` dict maps bird names to their definitions. Each bird gets specific tools and a prompt describing available `sports` CLI commands.

The agents run against a sibling repo at `/Users/brendan/repos/brendancsmith/sports` which provides the `sports` CLI and SQLite/Parquet data in `~/.sports/`.

## Key Dependencies

- `claude-agent-sdk` — spawns and manages subagents (mypy stubs are not available; `ignore_missing_imports = true`)
- `typer` + `rich` — CLI framework and output formatting
- `anyio` — async runtime for the agent SDK's async streaming API

## Style

- Ruff: line-length 100, target py311, rules: E, F, I, N, W, UP
- mypy: strict mode
