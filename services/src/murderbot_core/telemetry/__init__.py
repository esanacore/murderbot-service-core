"""Telemetry-service interface.

Defines the Protocol every real telemetry transport (from host-agents/ or
onboard sensors) must implement, plus a MockTelemetrySource for tests. No
real backend exists yet — see AGENTS.md rule 8. Telemetry is always
optional: the system remains fully useful without it
(docs/architecture.md "Host agent" row).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class TelemetrySample:
    source: str
    cpu_temp_c: float | None = None
    gpu_temp_c: float | None = None
    cpu_utilization_pct: float | None = None


class TelemetrySource(Protocol):
    """A single, authenticated telemetry feed (docs/security.md)."""

    def is_available(self) -> bool:
        """Whether this source is currently reachable/authenticated."""
        ...

    def read(self) -> TelemetrySample | None:
        """Return the latest sample, or None if unavailable."""
        ...


class MockTelemetrySource:
    """In-memory TelemetrySource for tests. Never performs real I/O."""

    def __init__(self, *, available: bool = True) -> None:
        self._available = available
        self._sample: TelemetrySample | None = None

    def set_sample(self, sample: TelemetrySample | None) -> None:
        self._sample = sample

    def is_available(self) -> bool:
        return self._available

    def read(self) -> TelemetrySample | None:
        if not self._available:
            return None
        return self._sample
