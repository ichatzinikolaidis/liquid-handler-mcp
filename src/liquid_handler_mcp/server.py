"""The MCP server: the tools an agent uses to operate the simulated deck.

Run it with ``uv run liquid-handler-mcp``. It serves over stdio.
"""

from __future__ import annotations

import logging
import threading
import typing

import mcp.server as mcp_server

import liquid_handler_mcp.deck

logger = logging.getLogger(__name__)

mcp = mcp_server.MCPServer("liquid-handler")
# A tool that raises gives the model an is_error result. Only a ToolError, from
# mcp.server.mcpserver.exceptions, keeps its message. Any other exception reaches the model
# as "Error executing tool <name>". Arguments that fail validation never reach the tool.

# The SDK runs each synchronous tool in a worker thread, and an agent may call tools in
# parallel, so every use of the deck holds this lock.
_lock = threading.Lock()
_deck: liquid_handler_mcp.deck.Deck | None = None


def _get_deck() -> liquid_handler_mcp.deck.Deck:
    """Return the process's one deck, building it on first use. Call with ``_lock`` held."""
    global _deck
    if _deck is None:
        logger.info("Starting the simulator")
        _deck = liquid_handler_mcp.deck.build_deck()
    return _deck


@mcp.tool()
def describe_deck() -> dict[str, typing.Any]:
    """Describe the simulated robot: its pipette, and each labware with its slot and wells.

    Read-only: nothing moves. Call this before planning any liquid handling.
    """
    with _lock:
        return liquid_handler_mcp.deck.describe(_get_deck())


def main() -> None:
    """Serve over stdio until the client disconnects."""
    # logging writes to stderr, which leaves stdout to the MCP messages.
    logging.basicConfig(level=logging.INFO)
    mcp.run()


if __name__ == "__main__":
    main()
