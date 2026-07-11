from murderbot_core.events import Event, EventType
from murderbot_core.state_machine import HostState, HostStateMachine


def test_initial_state_is_standby_with_no_history() -> None:
    """Construction/restart must never itself imply a transition
    (docs/architecture.md invariant, AGENTS.md rule 5)."""
    sm = HostStateMachine()
    assert sm.state is HostState.STANDBY
    assert sm.history == []


def test_main_rail_on_moves_standby_to_host_starting() -> None:
    sm = HostStateMachine()
    sm.handle(Event(type=EventType.MAIN_RAIL_ON))
    assert sm.state is HostState.HOST_STARTING


def test_heartbeat_moves_host_starting_to_host_running() -> None:
    sm = HostStateMachine()
    sm.handle(Event(type=EventType.MAIN_RAIL_ON))
    sm.handle(Event(type=EventType.HOST_HEARTBEAT))
    assert sm.state is HostState.HOST_RUNNING


def test_stable_timeout_also_moves_host_starting_to_host_running() -> None:
    sm = HostStateMachine()
    sm.handle(Event(type=EventType.MAIN_RAIL_ON))
    sm.handle(Event(type=EventType.STABLE_TIMEOUT))
    assert sm.state is HostState.HOST_RUNNING


def test_main_rail_off_during_host_starting_returns_to_standby() -> None:
    sm = HostStateMachine()
    sm.handle(Event(type=EventType.MAIN_RAIL_ON))
    sm.handle(Event(type=EventType.MAIN_RAIL_OFF))
    assert sm.state is HostState.STANDBY


def test_main_rail_off_during_host_running_moves_to_shutting_down() -> None:
    sm = HostStateMachine()
    sm.handle(Event(type=EventType.MAIN_RAIL_ON))
    sm.handle(Event(type=EventType.HOST_HEARTBEAT))
    sm.handle(Event(type=EventType.MAIN_RAIL_OFF))
    assert sm.state is HostState.HOST_SHUTTING_DOWN


def test_full_boot_to_shutdown_cycle() -> None:
    sm = HostStateMachine()
    sm.handle(Event(type=EventType.MAIN_RAIL_ON))
    sm.handle(Event(type=EventType.HOST_HEARTBEAT))
    sm.handle(Event(type=EventType.MAIN_RAIL_OFF))
    assert sm.state is HostState.HOST_SHUTTING_DOWN
    sm.handle(Event(type=EventType.MAIN_RAIL_OFF))
    assert sm.state is HostState.STANDBY


def test_fault_detected_from_any_non_fault_state() -> None:
    for setup_events in (
        [],
        [Event(type=EventType.MAIN_RAIL_ON)],
        [Event(type=EventType.MAIN_RAIL_ON), Event(type=EventType.HOST_HEARTBEAT)],
        [
            Event(type=EventType.MAIN_RAIL_ON),
            Event(type=EventType.HOST_HEARTBEAT),
            Event(type=EventType.MAIN_RAIL_OFF),
        ],
    ):
        sm = HostStateMachine()
        for event in setup_events:
            sm.handle(event)
        sm.handle(Event(type=EventType.FAULT_DETECTED))
        assert sm.state is HostState.FAULT


def test_fault_cleared_returns_to_standby_only_if_main_rail_confirmed_off() -> None:
    sm = HostStateMachine()
    sm.handle(Event(type=EventType.MAIN_RAIL_ON))
    sm.handle(Event(type=EventType.FAULT_DETECTED))
    assert sm.state is HostState.FAULT

    # Main rail is still (sensed) on - fault must not silently clear.
    sm.handle(Event(type=EventType.FAULT_CLEARED))
    assert sm.state is HostState.FAULT

    sm.handle(Event(type=EventType.MAIN_RAIL_OFF))
    sm.handle(Event(type=EventType.FAULT_CLEARED))
    assert sm.state is HostState.STANDBY


def test_unhandled_event_does_not_change_state() -> None:
    sm = HostStateMachine()
    sm.handle(Event(type=EventType.HOST_WINDOWS))
    assert sm.state is HostState.STANDBY
    assert sm.history == []


def test_history_records_each_transition_in_order() -> None:
    sm = HostStateMachine()
    sm.handle(Event(type=EventType.MAIN_RAIL_ON))
    sm.handle(Event(type=EventType.HOST_HEARTBEAT))

    assert [t.to_state for t in sm.history] == [
        HostState.HOST_STARTING,
        HostState.HOST_RUNNING,
    ]
    assert sm.history[0].from_state is HostState.STANDBY
    assert sm.history[1].from_state is HostState.HOST_STARTING


def test_handle_returns_resulting_state() -> None:
    sm = HostStateMachine()
    result = sm.handle(Event(type=EventType.MAIN_RAIL_ON))
    assert result is sm.state is HostState.HOST_STARTING
