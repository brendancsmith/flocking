"""Flocking CLI: a flock of little birds."""

from __future__ import annotations

import anyio
import typer
from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query
from rich.console import Console

from flocking.birds import FLOCK, SPORTS_CLI_DIR

app = typer.Typer(
    name="flocking",
    help="A flock of little birds.",
    no_args_is_help=True,
)
console = Console()

SYSTEM_PROMPT = """\
You are the lead of a small flock of analyst birds.

You have two specialist subagents:
- **lark** (Data Scout): Fetches fresh data, checks standings, schedules, and recent results.
- **kite** (Betting Analyst): Runs predictions, finds value bets, builds portfolios, \
and analyzes model performance.

Workflow:
1. For any question, first deploy **lark** to ensure data is fresh and gather context \
(standings, schedules, recent results).
2. Then deploy **kite** for analysis (predictions, value bets, portfolio optimization).
3. Synthesize their findings into a clear, actionable betting brief.

When deploying a bird, use the Task tool to spawn it as a subagent. Be specific about \
what you need from each bird.

Output format:
- Lead with the key takeaway or recommendation
- Include specific numbers: probabilities, edges, bet sizes, records
- Note any caveats: stale data, model limitations, small sample sizes
- Keep it concise — this is a betting brief, not a research paper
"""


async def _run(prompt: str, max_turns: int, sport: str | None) -> None:
    full_prompt = prompt
    if sport:
        full_prompt = f"[Sport filter: {sport}] {prompt}"

    async for message in query(
        prompt=full_prompt,
        options=ClaudeAgentOptions(
            cwd=SPORTS_CLI_DIR,
            system_prompt=SYSTEM_PROMPT,
            allowed_tools=["Bash", "Read", "Glob", "Grep", "Task"],
            permission_mode="bypassPermissions",
            allow_dangerously_skip_permissions=True,
            max_turns=max_turns,
            agents=FLOCK,
        ),
    ):
        if isinstance(message, ResultMessage):
            console.print(message.result)


@app.command()
def ask(
    prompt: str = typer.Argument(help="Question for the flock"),
    max_turns: int = typer.Option(30, "--max-turns", "-t", help="Maximum agent turns"),
    sport: str | None = typer.Option(None, "--sport", "-s", help="Filter to a specific sport"),
) -> None:
    """Ask the flock a question."""
    anyio.run(lambda: _run(prompt, max_turns, sport))


if __name__ == "__main__":
    app()
