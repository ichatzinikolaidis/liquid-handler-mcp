# liquid-handler-mcp

An MCP server that lets Claude operate a simulated Opentrons OT-2 liquid handler.
The point of the project is the boundary: the server enforces what the agent may do, and an eval measures where the agent goes wrong.

If a `CLAUDE.local.md` sits beside this file, read it too.
It holds the maintainer's private notes and is never committed.

## Who decides what

What the server refuses, and what the eval measures and how it is graded, are the maintainer's decisions.
For those, lay out the options and their trade-offs, and implement what is chosen.
Do not pick silently, and do not add a limit or an eval task that was not asked for.

All code here is written fresh for this project.
Do not bring in code or documents from any other project.

## Still to build

1. **Find out what the simulator already refuses.**
   Try the obvious mistakes and record each as a test: aspirating with no tip, a volume outside the pipette's range, picking up a tip when the rack is empty, a well that does not exist, dispensing more than a well holds, aspirating from an empty well.
   Whatever the simulator lets through is what the server has to track and refuse itself.
2. **Action tools.**
   Picking up and dropping a tip, aspirating and dispensing, each returning the state the agent needs for its next step.
3. **Limits, enforced in the server.**
   Never in the tool descriptions alone.
   Each limit has a test that shows the refusal and the message the agent receives.
4. **The eval.**
   A set of tasks, some of them physically invalid, scored on whether the agent completes the valid ones and refuses or flags the others.
5. **The README.**
   How to run it, what the eval found, and where the agent failed.

## Conventions

- Python with type hints, checked by ruff: `uv run ruff check` and `uv run ruff format`.
- `uv run pytest` passes before every commit.
- Quantities carry their unit in the name, such as `volume_ul`.
- Log with `logging`, and never `print`.
- Record a decision once, as a comment where it applies, and not again in Markdown.
- In Markdown, start each sentence on a new line.
