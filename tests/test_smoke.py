"""Smoke tests: the environment resolves, the simulator runs, and the server answers.

They say nothing about limits or safety.
"""

import mcp
import pytest

import liquid_handler_mcp.deck
import liquid_handler_mcp.server


def test_simulator_builds_the_deck() -> None:
    deck = liquid_handler_mcp.deck.build_deck()

    summary = liquid_handler_mcp.deck.describe(deck)

    assert summary["simulated"] is True
    assert summary["pipette"]["name"] == liquid_handler_mcp.deck.PIPETTE_NAME
    assert summary["pipette"]["max_volume_ul"] == 300
    assert [item["role"] for item in summary["labware"]] == ["tip_rack", "plate", "reservoir"]


def test_simulator_runs_a_plain_transfer() -> None:
    deck = liquid_handler_mcp.deck.build_deck()
    source = deck.labware["reservoir"]["A1"]
    destination = deck.labware["plate"]["A1"]

    deck.pipette.pick_up_tip()
    deck.pipette.aspirate(100, source)
    deck.pipette.dispense(100, destination)
    deck.pipette.drop_tip()

    assert not deck.pipette.has_tip


@pytest.mark.anyio
async def test_server_describes_the_deck() -> None:
    async with mcp.Client(liquid_handler_mcp.server.mcp, raise_exceptions=True) as client:
        result = await client.call_tool("describe_deck", {})

    assert not result.is_error
    assert result.structured_content["pipette"]["name"] == liquid_handler_mcp.deck.PIPETTE_NAME
