"""ATX/GPIO hardware interface.

Defines the Protocol every real GPIO/ATX backend must implement, plus a
MockAtxInterface used by tests and by any service running without a
Raspberry Pi attached. No real backend exists yet — see AGENTS.md rule 8
and docs/software.md "What's implemented today vs. planned".
"""

from __future__ import annotations

from typing import Protocol


class AtxInterface(Protocol):
    """Isolated ATX power/reset control.

    Implementations MUST default to open (no asserted output) on
    construction and on any internal error — see docs/architecture.md
    "ATX interface: Fail open; no asserted switch state after process
    crash" and FR-03/FR-07 in docs/requirements.md.
    """

    def pulse_power(self, duration_ms: int = 200) -> None:
        """Momentarily assert the power-switch output, then release it."""
        ...

    def pulse_reset(self, duration_ms: int = 200) -> None:
        """Momentarily assert the reset-switch output, then release it."""
        ...

    def is_main_rail_on(self) -> bool:
        """Return the sensed host main-rail state (FR-04)."""
        ...

    def close(self) -> None:
        """Release GPIO resources and guarantee outputs are open."""
        ...


class MockAtxInterface:
    """In-memory AtxInterface for tests. Never touches real hardware."""

    def __init__(self, *, initial_main_rail_on: bool = False) -> None:
        self._main_rail_on = initial_main_rail_on
        self.power_pulses: list[int] = []
        self.reset_pulses: list[int] = []
        self.closed = False

    def pulse_power(self, duration_ms: int = 200) -> None:
        self.power_pulses.append(duration_ms)

    def pulse_reset(self, duration_ms: int = 200) -> None:
        self.reset_pulses.append(duration_ms)

    def is_main_rail_on(self) -> bool:
        return self._main_rail_on

    def set_main_rail(self, on: bool) -> None:
        """Test helper: simulate the sensed rail state changing."""
        self._main_rail_on = on

    def close(self) -> None:
        self.closed = True
