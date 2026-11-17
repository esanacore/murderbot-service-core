"""Shared logging configuration for all murderbot-* services.

Each systemd unit (services/systemd/) calls configure_logging() once at
startup so log format/level is consistent across services and journald
captures structured, greppable output rather than each service inventing
its own format.

Configuration is data-driven: the schema is documented in
``configs/examples/logging.example.yaml`` and loaded by
``load_logging_config()``. The level and destination list come from that
file on the deployed Pi; nothing here hardcodes a level except the safe
default applied when no config path is supplied.
"""

from __future__ import annotations

import logging
import sys
import typing
from dataclasses import dataclass, field
from pathlib import Path

import yaml

_LOG_FORMAT = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"

# Canonical level names (case-insensitive on input). The example config
# documents this set; anything else is a ConfigError rather than silently
# passing through to logging, which would silently accept garbage.
_LEVEL_NAMES = frozenset({"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"})


class LoggingConfigError(Exception):
    """Raised when a logging config file is missing, malformed, or invalid."""


@dataclass(frozen=True)
class LoggingConfig:
    """Parsed contents of logging.yaml.

    Defaults are the safe/quiet choices (INFO, stdout) so a missing or
    partial config never unexpectedly raises verbosity or writes to a
    file the operator didn't provision.
    """

    level: str = "INFO"
    destinations: list[str] = field(default_factory=lambda: ["stdout"])


def _read_yaml(path: Path) -> dict[str, object]:
    if not path.exists():
        raise LoggingConfigError(f"logging config file not found: {path}")
    # Unreadable files and YAML syntax errors are reported as
    # LoggingConfigError too, so callers that degrade gracefully on a bad
    # logging config (core_service.build_core) have one exception to catch.
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
    except (OSError, yaml.YAMLError) as exc:
        raise LoggingConfigError(f"logging config {path} could not be read: {exc}") from exc
    if not isinstance(data, dict):
        raise LoggingConfigError(
            f"logging config {path} must contain a YAML mapping at the top level"
        )
    return data


def load_logging_config(path: Path) -> LoggingConfig:
    """Parse and validate a logging.yaml file.

    Raises :class:`LoggingConfigError` on a missing file, a non-mapping
    root, an unknown level, or an invalid destinations list.
    """
    data = _read_yaml(path)

    level = _validated_level_name(str(data.get("level", "INFO")))

    destinations = data.get("destinations", ["stdout"])
    if isinstance(destinations, str):
        destinations = [destinations]
    if not isinstance(destinations, list) or not destinations:
        raise LoggingConfigError(
            f"'destinations' must be a non-empty list of strings, got {destinations!r}"
        )
    for dest in destinations:
        if not isinstance(dest, str) or not dest:
            raise LoggingConfigError(f"each destination must be a non-empty string, got {dest!r}")

    return LoggingConfig(level=level, destinations=list(destinations))


def _destination_stream(destination: str) -> typing.IO[str]:
    """Resolve a destination name to a writable stream.

    Only 'stdout' and 'stderr' are supported; anything else is rejected
    rather than silently opened, so a typo in the config fails loudly at
    startup instead of at first log line.
    """
    if destination == "stdout":
        return sys.stdout
    if destination == "stderr":
        return sys.stderr
    raise LoggingConfigError(
        f"unsupported log destination {destination!r}; supported: 'stdout', 'stderr'"
    )


class _MurderbotHandler(logging.StreamHandler[typing.IO[str]]):
    """A handler installed by configure_logging().

    Tagged with this class so configure_logging can later remove only its
    own handlers (idempotent reconfiguration) without stripping handlers
    installed by test frameworks, application code, or other libraries —
    which would silently break log capture and observability.
    """

    pass


def configure_logging(
    config: LoggingConfig | None = None,
    *,
    level: int | str | None = None,
    path: Path | None = None,
) -> None:
    """Apply structured logging for the calling service.

    Three mutually-composable modes:

    * ``configure_logging()`` — safe defaults (INFO, stdout).
    * ``configure_logging(level=...)`` — explicit level, stdout. Kept for
      callers that don't have a config file (e.g. unit tests).
    * ``configure_logging(path=Path(...))`` — load and apply a logging.yaml
      file, including its destination list.

    A ``config`` object may be passed directly to avoid re-parsing a file
    that was already validated elsewhere. Precedence when several are
    given: ``config``, then ``path``, then ``level``.

    Raises :class:`LoggingConfigError` for an unknown level or destination
    (from any of the three sources) before touching the root logger, so a
    rejected call leaves the existing logging setup intact.
    """
    if config is None:
        if path is not None:
            config = load_logging_config(path)
        elif level is not None:
            config = LoggingConfig(
                level=level if isinstance(level, str) else _level_name(level),
            )
        else:
            config = LoggingConfig()

    # Re-validated here because LoggingConfig can be constructed directly
    # and ``level=`` never passes through load_logging_config().
    level_name = _validated_level_name(config.level)
    streams = [_destination_stream(dest) for dest in config.destinations]
    # logging.basicConfig accepts a single stream/handler; route through
    # a multi-stream handler so 'stdout' + 'stderr' both land in journald
    # capture without one shadowing the other.
    new_handlers = [_MurderbotHandler(stream) for stream in streams]
    for handler in new_handlers:
        handler.setFormatter(logging.Formatter(_LOG_FORMAT))

    root = logging.getLogger()
    # Replace only handlers we previously installed (idempotent
    # reconfiguration), leaving test/framework handlers alone.
    for existing in list(root.handlers):
        if isinstance(existing, _MurderbotHandler):
            root.removeHandler(existing)
    for handler in new_handlers:
        root.addHandler(handler)

    root.setLevel(getattr(logging, level_name))


def _validated_level_name(level: str) -> str:
    """Normalize a level name to upper case, rejecting anything unknown."""
    name = level.upper()
    if name not in _LEVEL_NAMES:
        raise LoggingConfigError(
            f"logging level must be one of {sorted(_LEVEL_NAMES)}, got {name!r}"
        )
    return name


def _level_name(level: int) -> str:
    """Map a numeric logging level back to its canonical name."""
    for name in _LEVEL_NAMES:
        if getattr(logging, name) == level:
            return name
    raise LoggingConfigError(f"unsupported numeric log level: {level!r}")
