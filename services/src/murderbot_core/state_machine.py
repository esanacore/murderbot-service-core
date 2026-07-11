"""The murderbot-core host-state machine.

See docs/architecture.md "State model" for the diagram this implements.

Invariant (docs/architecture.md, AGENTS.md rule 5): constructing/restarting
a HostStateMachine must never itself cause a power/reset pulse, audio
playback, or LED animation. This module only tracks and reports state; it
does not drive hardware. Side effects belong to a separate wiring layer
that subscribes to an EventBus and reacts to this machine's transitions.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum, unique

from murderbot_core.events import Event, EventType

logger = logging.getLogger(__name__)


@unique
class HostState(Enum):
    STANDBY = "standby"
    HOST_STARTING = "host_starting"
    HOST_RUNNING = "host_running"
    HOST_SHUTTING_DOWN = "host_shutting_down"
    FAULT = "fault"


@dataclass(frozen=True)
class Transition:
    """A recorded state change, for logging/testing."""

    from_state: HostState
    to_state: HostState
    event: Event


# Explicit transition table: (current state, event type) -> next state.
# Any (state, event) pair not listed here is a no-op for this state
# machine: the event is real and may still matter to other subscribers
# (e.g. HOST_WINDOWS for profile selection, docs/software.md FR-08), it
# just doesn't move the *host* state.
_TRANSITIONS: dict[tuple[HostState, EventType], HostState] = {
    (HostState.STANDBY, EventType.MAIN_RAIL_ON): HostState.HOST_STARTING,
    (HostState.HOST_STARTING, EventType.HOST_HEARTBEAT): HostState.HOST_RUNNING,
    (HostState.HOST_STARTING, EventType.STABLE_TIMEOUT): HostState.HOST_RUNNING,
    (HostState.HOST_STARTING, EventType.MAIN_RAIL_OFF): HostState.STANDBY,
    (HostState.HOST_RUNNING, EventType.MAIN_RAIL_OFF): HostState.HOST_SHUTTING_DOWN,
    (HostState.HOST_SHUTTING_DOWN, EventType.MAIN_RAIL_OFF): HostState.STANDBY,
    # FAULT is reachable from any state on FAULT_DETECTED.
    (HostState.STANDBY, EventType.FAULT_DETECTED): HostState.FAULT,
    (HostState.HOST_STARTING, EventType.FAULT_DETECTED): HostState.FAULT,
    (HostState.HOST_RUNNING, EventType.FAULT_DETECTED): HostState.FAULT,
    (HostState.HOST_SHUTTING_DOWN, EventType.FAULT_DETECTED): HostState.FAULT,
}

# Events that never move host state but are still valid to publish (they
# matter to other subscribers). Listed explicitly so publish() can
# distinguish "known, intentionally non-transitioning" from "unexpected".
_NON_TRANSITIONING_EVENTS = frozenset(
    {
        EventType.POWER_BUTTON,
        EventType.RESET_BUTTON,
        EventType.HOST_WINDOWS,
        EventType.HOST_LINUX,
        EventType.TEMPERATURE_WARNING,
        EventType.PIKVM_DEGRADED,
        EventType.AUDIO_COMPLETE,
        EventType.ANIMATION_COMPLETE,
    }
)


class HostStateMachine:
    """Tracks host power state from events; emits no hardware side effects.

    Pure and deterministic: `handle()` is a function of (current state,
    event) -> next state, with no I/O and no dependency on an EventBus.
    A separate wiring layer (not yet implemented — see docs/software.md)
    is responsible for subscribing `handle` to a real EventBus and for
    driving hardware/audio/RGB reactions off the resulting transitions;
    keeping that out of this class is what makes it trivially unit
    testable without a bus or mocks.
    """

    def __init__(self) -> None:
        self._state = HostState.STANDBY
        self._main_rail_on = False
        self.history: list[Transition] = []

    @property
    def state(self) -> HostState:
        return self._state

    def handle(self, event: Event) -> HostState:
        """Process one event, applying at most one transition.

        Returns the resulting state (unchanged if the event didn't cause
        a transition).
        """
        if event.type in (EventType.MAIN_RAIL_ON, EventType.MAIN_RAIL_OFF):
            self._main_rail_on = event.type is EventType.MAIN_RAIL_ON

        if self._state is HostState.FAULT:
            next_state = self._handle_fault_recovery(event)
        else:
            next_state = _TRANSITIONS.get((self._state, event.type))

        if next_state is None:
            if event.type not in _NON_TRANSITIONING_EVENTS and self._state is not HostState.FAULT:
                logger.debug(
                    "Event %s ignored in state %s (no defined transition)",
                    event.type,
                    self._state,
                )
            return self._state

        transition = Transition(from_state=self._state, to_state=next_state, event=event)
        self._state = next_state
        self.history.append(transition)
        logger.info(
            "State transition: %s -> %s (event=%s)",
            transition.from_state,
            transition.to_state,
            event.type,
        )

        return self._state

    def _handle_fault_recovery(self, event: Event) -> HostState | None:
        if event.type is EventType.FAULT_CLEARED and not self._main_rail_on:
            return HostState.STANDBY
        return None
