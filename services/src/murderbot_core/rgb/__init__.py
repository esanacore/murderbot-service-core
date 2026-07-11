"""RGB-service interface.

Defines the Protocol every real NeoPixel/level-shifter backend must
implement, plus a MockRgbController for tests. No real backend exists
yet — see AGENTS.md rule 8. Must default off on configuration or
hardware error (docs/architecture.md "RGB service" failure rule), and
every implementation must enforce a brightness cap (FR-06, FR-07,
docs/power-design.md).
"""

from __future__ import annotations

from typing import Protocol


class RgbController(Protocol):
    """Drives an addressable LED strip with an enforced brightness cap."""

    def set_animation(self, name: str) -> None:
        """Switch to the named animation profile (e.g. 'boot', 'idle')."""
        ...

    def set_brightness(self, level: float) -> None:
        """Set brightness in [0.0, 1.0]. Implementations MUST clamp to
        the configured cap (docs/power-design.md), never trust the
        caller's value directly."""
        ...

    def off(self) -> None:
        """Immediately turn all LEDs off. Must be safe to call at any time,
        including before any animation has been set."""
        ...


class MockRgbController:
    """In-memory RgbController for tests. Never touches real LED hardware."""

    def __init__(self, *, brightness_cap: float = 1.0) -> None:
        if not 0.0 <= brightness_cap <= 1.0:
            raise ValueError("brightness_cap must be between 0.0 and 1.0")
        self._brightness_cap = brightness_cap
        self.current_animation: str | None = None
        self.brightness = 0.0
        self.is_on = False

    def set_animation(self, name: str) -> None:
        self.current_animation = name
        self.is_on = True

    def set_brightness(self, level: float) -> None:
        self.brightness = max(0.0, min(level, self._brightness_cap))

    def off(self) -> None:
        self.is_on = False
        self.current_animation = None
        self.brightness = 0.0
