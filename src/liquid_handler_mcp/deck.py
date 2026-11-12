"""The simulated deck: one OT-2 with a fixed pipette and labware.

The deck comes from Opentrons' own simulator, ``opentrons.simulate``, so the calls made
here are the calls a real OT-2 protocol makes.
"""

from __future__ import annotations

import dataclasses
import typing

import opentrons.protocol_api
import opentrons.simulate

ROBOT_TYPE = "OT-2"
# The OT-2 supports API levels up to 2.28 on robot software 10.0.0.
API_LEVEL = "2.20"

PIPETTE_NAME = "p300_single_gen2"
PIPETTE_MOUNT = "right"

# role -> (labware load name, deck slot)
LAYOUT: dict[str, tuple[str, str]] = {
    "tip_rack": ("opentrons_96_tiprack_300ul", "1"),
    "plate": ("corning_96_wellplate_360ul_flat", "2"),
    "reservoir": ("nest_12_reservoir_15ml", "3"),
}


@dataclasses.dataclass
class Deck:
    """A simulated robot with its pipette and its labware, keyed by role."""

    protocol: opentrons.protocol_api.ProtocolContext
    pipette: opentrons.protocol_api.InstrumentContext
    labware: dict[str, opentrons.protocol_api.Labware]


def build_deck() -> Deck:
    """Create a simulated OT-2 and load the layout onto it.

    Each call starts a simulator that keeps a background thread until the process exits,
    and Opentrons offers no way to close one, so build a deck once and reuse it.
    """
    protocol = opentrons.simulate.get_protocol_api(API_LEVEL, robot_type=ROBOT_TYPE)
    labware = {
        role: protocol.load_labware(load_name, slot) for role, (load_name, slot) in LAYOUT.items()
    }
    pipette = protocol.load_instrument(PIPETTE_NAME, PIPETTE_MOUNT, tip_racks=[labware["tip_rack"]])
    return Deck(protocol=protocol, pipette=pipette, labware=labware)


def describe(deck: Deck) -> dict[str, typing.Any]:
    """Return what an agent needs to know before it plans: the pipette and each labware."""
    return {
        "robot": ROBOT_TYPE,
        "api_level": API_LEVEL,
        "simulated": deck.protocol.is_simulating(),
        "pipette": {
            "name": deck.pipette.name,
            "mount": deck.pipette.mount,
            "min_volume_ul": deck.pipette.min_volume,
            "max_volume_ul": deck.pipette.max_volume,
            "has_tip": deck.pipette.has_tip,
        },
        "labware": [
            _describe_labware(role, LAYOUT[role][1], item) for role, item in deck.labware.items()
        ],
    }


def _describe_labware(
    role: str, slot: str, item: opentrons.protocol_api.Labware
) -> dict[str, typing.Any]:
    wells = item.wells()
    summary: dict[str, typing.Any] = {
        "role": role,
        "slot": slot,
        "load_name": item.load_name,
        "well_count": len(wells),
        "first_well": wells[0].well_name,
        "last_well": wells[-1].well_name,
    }
    if not item.is_tiprack:
        summary["well_max_volume_ul"] = wells[0].max_volume
    return summary
