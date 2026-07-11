"""Event types and the in-process event bus that connects murderbot-core
to the audio, RGB, and telemetry services.

See docs/architecture.md "State model" for the full event list and
docs/software.md for why this is the only sanctioned communication path
between services (no direct imports between service packages).
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Any


@unique
class EventType(Enum):
    POWER_BUTTON = "power_button"
    RESET_BUTTON = "reset_button"
    MAIN_RAIL_ON = "main_rail_on"
    MAIN_RAIL_OFF = "main_rail_off"
    HOST_WINDOWS = "host_windows"
    HOST_LINUX = "host_linux"
    HOST_HEARTBEAT = "host_heartbeat"
    TEMPERATURE_WARNING = "temperature_warning"
    PIKVM_DEGRADED = "pikvm_degraded"
    AUDIO_COMPLETE = "audio_complete"
    ANIMATION_COMPLETE = "animation_complete"

    # Internal-only signals not in the original engineering report's event
    # list, needed to implement the FAULT transitions and the "stable
    # timeout" alternative to a heartbeat shown in docs/architecture.md's
    # state diagram. These are software-architecture decisions (see ADR
    # process in docs/decisions/), not hardware facts.
    STABLE_TIMEOUT = "stable_timeout"
    FAULT_DETECTED = "fault_detected"
    FAULT_CLEARED = "fault_cleared"


@dataclass(frozen=True)
class Event:
    """An immutable, timestamped occurrence on the bus.

    ``payload`` carries event-specific data (e.g. a measured temperature
    for TEMPERATURE_WARNING). It defaults to an empty dict rather than
    None so consumers never need a None-check before a dict lookup.
    """

    type: EventType
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.monotonic)


EventHandler = Callable[[Event], None]


class EventBus:
    """A minimal synchronous publish/subscribe bus.

    Deliberately not a singleton/module-level global (see AGENTS.md rule
    on avoiding global mutable state) — each service process constructs
    its own EventBus (or, in tests, a shared one is passed in explicitly).
    """

    def __init__(self) -> None:
        self._subscribers: dict[EventType, list[EventHandler]] = {}

    def subscribe(self, event_type: EventType, handler: EventHandler) -> None:
        self._subscribers.setdefault(event_type, []).append(handler)

    def unsubscribe(self, event_type: EventType, handler: EventHandler) -> None:
        handlers = self._subscribers.get(event_type)
        if handlers and handler in handlers:
            handlers.remove(handler)

    def publish(self, event: Event) -> None:
        for handler in list(self._subscribers.get(event.type, [])):
            handler(event)
