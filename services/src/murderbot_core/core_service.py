"""Entrypoint for the ``murderbot-core`` systemd unit.

This module is the process that owns the host state machine, the event
bus, and profile selection. It is deliberately minimal at this phase:
it loads configuration, builds the state machine and bus, and wires
*logging* of transitions. The hardware-driving wiring (ATX pulses,
audio playback, RGB animation) is a separate concern that subscribes to
the same bus in later phases — see ``docs/software.md``.

Safety invariant (``docs/architecture.md``, ``AGENTS.md`` rule 5): this
process must never itself assert a power/reset pulse, play audio, or
illuminate LEDs. It holds trivially here because this module performs no
hardware I/O at all — it only observes state and logs it. The moment a
real backend is wired in, that wiring belongs in a separate module that
reacts to bus events, never in this one.
"""

from __future__ import annotations

import logging
import sys
import typing
from pathlib import Path

from murderbot_core.config import load_hardware_config, load_profiles
from murderbot_core.events import Event, EventBus
from murderbot_core.logging_setup import LoggingConfigError, configure_logging
from murderbot_core.state_machine import HostStateMachine

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_DIR = Path("/etc/murderbot")


def _observe_and_drive(machine: HostStateMachine) -> typing.Callable[[Event], None]:
    """Return the single bus handler for state-affecting events.

    Combines transition logging with feeding the event into the state
    machine, so each such event is handled exactly once. The machine is
    pure (no I/O), so running it inline is safe — this is the
    *observation* path, not the *action* path. Hardware reactions are
    separate subscribers wired in later phases, never here.
    """

    def _handler(event: Event) -> None:
        logger.info("bus event: %s", event.type.value)
        machine.handle(event)

    return _handler


def build_core(
    hardware_path: Path,
    profiles_path: Path,
    logging_path: Path,
) -> tuple[HostStateMachine, EventBus]:
    """Construct the core wiring for one service process.

    Pure setup: config parsing, bus, state machine, and the observation
    handler. No hardware I/O. Returns the machine and bus so a caller
    (or tests) can drive events through them.

    Hardware/profile parsing raises ``ConfigError`` on bad input, which
    ``main`` lets surface as a non-zero exit. Logging setup degrades
    gracefully (falls back to defaults) rather than blocking startup,
    because a broken logging config must never prevent the service from
    coming up in a safe, observable state.
    """
    try:
        configure_logging(path=logging_path)
    except LoggingConfigError as exc:
        # Fall back to defaults and warn; the service still starts.
        logging.basicConfig(level=logging.WARNING)
        logging.getLogger(__name__).warning("falling back to default logging: %s", exc)

    hardware = load_hardware_config(hardware_path)
    profiles = load_profiles(profiles_path)

    bus = EventBus()
    machine = HostStateMachine()

    # Observation path: one handler per state-affecting event type, which
    # logs the transition and feeds it into the machine. Hardware *actions*
    # are separate subscribers wired in later phases — never here. The
    # event set is derived from the machine itself so it stays in sync
    # with state_machine.py's transition table if EventType grows.
    for event_type in machine.consumed_event_types:
        bus.subscribe(event_type, _observe_and_drive(machine))

    logger.info(
        "murderbot-core starting: hardware=%s profiles=%d",
        hardware,
        len(profiles),
    )
    return machine, bus


def main(argv: list[str] | None = None) -> int:
    """Process entrypoint.

    Configuration paths default to ``/etc/murderbot`` (the deployed
    location) but the config directory is overridable as the single
    positional CLI argument, which is what makes this runnable from
    unit tests and from a developer bench without a deployed config
    tree. Additional positional args are currently ignored.
    """
    args = list(sys.argv[1:] if argv is None else argv)
    config_dir = Path(args[0]) if args else DEFAULT_CONFIG_DIR

    hardware_path = config_dir / "hardware.yaml"
    profiles_path = config_dir / "profiles.yaml"
    logging_path = config_dir / "logging.yaml"

    machine, bus = build_core(hardware_path, profiles_path, logging_path)

    logger.info("murderbot-core running; host state=%s", machine.state.value)
    # The real service blocks here on the event loop of its transport
    # (PiKVM GPIO daemon, host-agent socket, ...). That wiring is not
    # implemented yet — see docs/software.md "What's implemented today".
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
