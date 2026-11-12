# liquid-handler-mcp

An MCP server that lets Claude operate a simulated Opentrons OT-2 liquid handler.
The aim is for the server, not the tool descriptions, to enforce what the agent may do, and for an eval to measure where the agent goes wrong.
Everything runs in Opentrons' own simulator, so no robot is needed.

## Status

Work in progress.
The server has one read-only tool, `describe_deck`, which reports the pipette and the labware.

Next:

1. Action tools: pick up and drop a tip, aspirate and dispense.
2. Limits enforced in the server, each with a test that shows the refusal and the message the agent receives.
3. An eval: tasks, some of them physically invalid, scored on whether the agent completes the valid ones and refuses or flags the others.

## What you need

- [uv](https://docs.astral.sh/uv/), which installs Python 3.12 and the dependencies.
- Git.

## Set up

```sh
uv sync
uv run pytest
```

## Use it from Claude Code

`.mcp.json` registers the server for this folder, and Claude Code asks to enable it when it opens the project.
It runs `uv run liquid-handler-mcp`, which serves over stdio.
Then ask Claude to describe the deck.
If Claude Code connects and then fails, run `uv run liquid-handler-mcp` alone: it should print nothing and wait, since anything it prints to stdout corrupts the MCP messages.

## Layout

| Path | What |
| --- | --- |
| `src/liquid_handler_mcp/deck.py` | The simulated OT-2: its pipette, its labware, and a description of both |
| `src/liquid_handler_mcp/server.py` | The MCP server and its tools |
| `tests/test_smoke.py` | Checks that the environment resolves, the simulator runs and the server answers |
| `.mcp.json` | Registers the server with Claude Code |
| `CLAUDE.md` | Notes for coding agents and contributors: who decides what, what is still to build, and the conventions |
