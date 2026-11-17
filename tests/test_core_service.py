"""Tests for services/src/murderbot_core/core_service.py.

Verifies the safety invariant directly: building and driving the core
must never produce a power/reset pulse, audio playback, or LED output,
because this module holds no hardware references at all.
"""

from __future__ import annotations

import logging
import subprocess
import sys
import textwrap
import types
from pathlib import Path

import pytest

from murderbot_core.config import ConfigError
from murderbot_core.core_service import build_core, main
from murderbot_core.events import Event, EventType
from murderbot_core.logging_setup import _MurderbotHandler
from murderbot_core.state_machine import HostState

# Hardware-facing subpackages the core process must never touch. A real
# backend lives in one of these; the core only subscribes to the bus.
_FORBIDDEN_PREFIXES = (
    "murderbot_core.hardware",
    "murderbot_core.audio",
    "murderbot_core.rgb",
    "murderbot_core.telemetry",
)


def _write_config_tree(tmp_path: Path) -> Path:
    (tmp_path / "hardware.yaml").write_text("atx_enabled: false\n")
    (tmp_path / "profiles.yaml").write_text("profiles:\n  unknown_host:\n    audio_clip: null\n")
    (tmp_path / "logging.yaml").write_text("level: INFO\ndestinations:\n  - stdout\n")
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


def test_core_does_not_drive_any_hardware(tmp_path: Path) -> None:
    """Safety invariant: the core process loads no hardware-facing code.

    Runs the real entrypoint in a fresh interpreter: ``main()`` against a
    config tree, then one event of every type the machine consumes
    published through the bus. Afterwards none of the hardware-facing
    subpackages may be present in ``sys.modules``. Code that was never
    imported cannot have been called, so a start, restart, or crash of
    this process cannot assert an ATX pulse, play a clip, or drive LEDs.

    A subprocess is used because ``sys.modules`` in the test process is
    shared with every other test module (which do import the mocks), so
    an in-process check would be order dependent.
    """
    config_dir = _write_config_tree(tmp_path)
    script = textwrap.dedent(
        """
        import sys
        from pathlib import Path

        from murderbot_core import core_service
        from murderbot_core.events import Event

        config_dir = Path(sys.argv[1])
        assert core_service.main([str(config_dir)]) == 0
        machine, bus = core_service.build_core(
            config_dir / "hardware.yaml",
            config_dir / "profiles.yaml",
            config_dir / "logging.yaml",
        )
        for event_type in sorted(machine.consumed_event_types, key=lambda t: t.value):
            bus.publish(Event(type=event_type))

        forbidden = tuple(sys.argv[2:])
        loaded = sorted(
            name
            for name in sys.modules
            if any(name == p or name.startswith(p + ".") for p in forbidden)
        )
        print("LOADED=" + ",".join(loaded))
        """
    )

    result = subprocess.run(
        [sys.executable, "-c", script, str(config_dir), *_FORBIDDEN_PREFIXES],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "LOADED=\n" in result.stdout, (
        f"core_service loaded hardware-facing modules: {result.stdout!r}; hardware "
        "must live in a separate wiring layer, not in the core process"
    )


def test_core_module_binds_no_hardware_names() -> None:
    """Fast in-process companion to the subprocess check above.

    Catches both ``from murderbot_core.hardware import X`` (the bound
    object's ``__module__``) and ``from murderbot_core import hardware``
    (a bound module object, identified by ``__name__``).
    """
    import murderbot_core.core_service as core_service

    offenders = set()
    for value in core_service.__dict__.values():
        if isinstance(value, types.ModuleType):
            origin: object = value.__name__
        else:
            origin = getattr(value, "__module__", None)
        if isinstance(origin, str) and origin.startswith(_FORBIDDEN_PREFIXES):
            offenders.add(origin)

    assert not offenders, (
        f"core_service binds {sorted(offenders)}; hardware must live in a "
        "separate wiring layer, not in the core process"
    )


def test_main_returns_zero_and_runs(tmp_path: Path, caplog) -> None:
    config_dir = _write_config_tree(tmp_path)

    with caplog.at_level(logging.INFO):
        rc = main([str(config_dir)])

    assert rc == 0
    assert any("murderbot-core starting" in rec.message for rec in caplog.records)
    assert any("murderbot-core running" in rec.message for rec in caplog.records)


def test_main_uses_default_config_dir_when_no_args(tmp_path: Path, monkeypatch, caplog) -> None:
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


@pytest.mark.parametrize(
    "bad_logging_yaml",
    ["level: NOT_A_LEVEL\n", "level: [unclosed\n", "destinations:\n  - syslog\n"],
    ids=["unknown-level", "malformed-yaml", "unsupported-destination"],
)
def test_build_core_degrades_logging_gracefully_on_bad_config(
    tmp_path: Path, caplog: pytest.LogCaptureFixture, bad_logging_yaml: str
) -> None:
    # A bad logging.yaml must not block startup; the service still loads
    # hardware/profiles, warns, and runs on the safe defaults (INFO, stdout).
    config_dir = _write_config_tree(tmp_path)
    (config_dir / "logging.yaml").write_text(bad_logging_yaml)
    root = logging.getLogger()

    try:
        with caplog.at_level(logging.WARNING):
            machine, _bus = build_core(
                config_dir / "hardware.yaml",
                config_dir / "profiles.yaml",
                config_dir / "logging.yaml",
            )

        assert machine.state is HostState.STANDBY
        assert any("falling back to default logging" in rec.message for rec in caplog.records)
        ours = [h for h in root.handlers if isinstance(h, _MurderbotHandler)]
        assert len(ours) == 1
        assert ours[0].stream is sys.stdout
    finally:
        for handler in list(root.handlers):
            if isinstance(handler, _MurderbotHandler):
                root.removeHandler(handler)


def test_build_core_degrades_when_logging_config_is_missing(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    config_dir = _write_config_tree(tmp_path)
    (config_dir / "logging.yaml").unlink()

    with caplog.at_level(logging.WARNING):
        machine, _bus = build_core(
            config_dir / "hardware.yaml",
            config_dir / "profiles.yaml",
            config_dir / "logging.yaml",
        )

    assert machine.state is HostState.STANDBY
    assert any("falling back to default logging" in rec.message for rec in caplog.records)


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
