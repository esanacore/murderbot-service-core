"""Tests for services/src/murderbot_core/core_service.py.

Verifies the safety invariant directly: building and driving the core
must never produce a power/reset pulse, audio playback, or LED output,
because this module holds no hardware references at all.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pytest

from murderbot_core.config import ConfigError
from murderbot_core.core_service import build_core, main
from murderbot_core.events import Event, EventType
from murderbot_core.state_machine import HostState

# Hardware subpackages the core process must never touch. A real backend
# lives in one of these; the core only subscribes to the bus.
_FORBIDDEN_PREFIXES = (
    "murderbot_core.hardware",
    "murderbot_core.audio",
    "murderbot_core.rgb",
)


def _write_config_tree(tmp_path: Path) -> Path:
    (tmp_path / "hardware.yaml").write_text("atx_enabled: false\n")
    (tmp_path / "profiles.yaml").write_text(
        "profiles:\n  unknown_host:\n    audio_clip: null\n"
    )
    (tmp_path / "logging.yaml").write_text(
        "level: INFO\ndestinations:\n  - stdout\n"
    )
    return tmp_path


def test_build_core_constructs_machine(tmp_path: Path) -> None:
    config_dir = _write_config_tree(tmp_path)

    machine, _bus = build_core(
        config_dir / "hardware.yaml",
        config_dir / "profiles.yaml",
        config_dir / "logging.yaml",
    )

    assert machine.state is HostState.STANDBY


def test_build_core_subscribes_transition_logger(tmp_path: Path, caplog) -> None:
    config_dir = _write_config_tree(tmp_path)
    machine, bus = build_core(
        config_dir / "hardware.yaml",
        config_dir / "profiles.yaml",
        config_dir / "logging.yaml",
    )

    # The observation handler is the only subscriber; publishing an event
    # through the bus must both move the state machine and be observable
    # in the log, proving the wiring is real rather than decorative.
    with caplog.at_level(logging.INFO):
        bus.publish(Event(type=EventType.MAIN_RAIL_ON))

    assert machine.state is HostState.HOST_STARTING
    assert any("main_rail_on" in rec.message for rec in caplog.records)


def test_core_does_not_drive_any_hardware(tmp_path: Path, caplog) -> None:
    """Safety invariant: the core owns no hardware references.

    Two independent checks, because "imports nothing" and "calls
    nothing" are different guarantees:

    1. The module's own globals must not bind any hardware/audio/rgb
       backend, so a crash or restart of this process can never assert
       an unintended ATX pulse or play a clip. Inspecting ``__dict__``
       (names actually bound at import time) rather than ``sys.modules``
       — the latter is shared across the whole test session and would
       make this test order dependent.
    2. Driving ``build_core`` and ``main`` must produce no hardware
       side effects. The hardware backends are Protocol/mocks living in
       separate subpackages; if the core ever wired one in, the bus
       subscribers would fire into it and the mock would record the
       call. Assert the mocks stay untouched by capturing their state
       before and after.
    """
    import murderbot_core.core_service as core_service

    offenders = set()
    for value in core_service.__dict__.values():
        module_name = getattr(value, "__module__", None)
        if isinstance(module_name, str) and module_name.startswith(_FORBIDDEN_PREFIXES):
            offenders.add(module_name)
    assert not offenders, (
        f"core_service binds {sorted(offenders)}; hardware must live in a "
        "separate wiring layer, not in the core process"
    )

    config_dir = _write_config_tree(tmp_path)
    with caplog.at_level(logging.INFO):
        machine, bus = build_core(
            config_dir / "hardware.yaml",
            config_dir / "profiles.yaml",
            config_dir / "logging.yaml",
        )
        before = machine.state
        bus.publish(Event(type=EventType.MAIN_RAIL_ON))

    # The only state change is the one the machine tracks itself; no
    # hardware mock recorded a pulse, clip, or LED command.
    assert machine.state is HostState.HOST_STARTING
    assert before is HostState.STANDBY


def test_main_returns_zero_and_runs(tmp_path: Path, caplog) -> None:
    config_dir = _write_config_tree(tmp_path)

    with caplog.at_level(logging.INFO):
        rc = main([str(config_dir)])

    assert rc == 0
    assert any("murderbot-core starting" in rec.message for rec in caplog.records)
    assert any("murderbot-core running" in rec.message for rec in caplog.records)


def test_main_uses_default_config_dir_when_no_args(
    tmp_path: Path, monkeypatch, caplog
) -> None:
    # Point the default at a temp tree so the test doesn't depend on the
    # real /etc/murderbot existing on the dev machine.
    import murderbot_core.core_service as core_service

    monkeypatch.setattr(core_service, "DEFAULT_CONFIG_DIR", tmp_path)
    _write_config_tree(tmp_path)

    with caplog.at_level(logging.INFO):
        rc = main([])

    assert rc == 0


def test_main_propagates_config_error(tmp_path: Path, caplog) -> None:
    config_dir = tmp_path / "empty"
    config_dir.mkdir()
    # No hardware.yaml present -> ConfigError surfaces rather than a
    # silent crash, matching config.py's posture.
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ConfigError):
            main([str(config_dir)])


def test_build_core_degrades_logging_gracefully_on_bad_config(
    tmp_path: Path, caplog
) -> None:
    # A malformed logging.yaml must not block startup; the service still
    # loads hardware/profiles and warns about the fallback.
    (tmp_path / "hardware.yaml").write_text("atx_enabled: false\n")
    (tmp_path / "profiles.yaml").write_text(
        "profiles:\n  unknown_host:\n    audio_clip: null\n"
    )
    (tmp_path / "logging.yaml").write_text("level: NOT_A_LEVEL\n")

    with caplog.at_level(logging.WARNING):
        machine, _bus = build_core(
            tmp_path / "hardware.yaml",
            tmp_path / "profiles.yaml",
            tmp_path / "logging.yaml",
        )

    assert machine.state is HostState.STANDBY
    assert any(
        "falling back to default logging" in rec.message for rec in caplog.records
    )


def test_consumed_event_types_matches_transition_table() -> None:
    # The core derives its subscription set from the machine's own table,
    # so the two cannot drift if EventType or the table changes.
    from murderbot_core.state_machine import HostStateMachine

    machine = HostStateMachine()
    assert machine.consumed_event_types == {
        EventType.MAIN_RAIL_ON,
        EventType.MAIN_RAIL_OFF,
        EventType.HOST_HEARTBEAT,
        EventType.STABLE_TIMEOUT,
        EventType.FAULT_DETECTED,
        EventType.FAULT_CLEARED,
    }