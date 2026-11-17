"""Tests for services/src/murderbot_core/logging_setup.py.

Covers load_logging_config (parse + validate) and configure_logging
(idempotent reconfiguration, destination resolution, level mapping).
"""

from __future__ import annotations

import logging
from pathlib import Path

import pytest

from murderbot_core.logging_setup import (
    LoggingConfig,
    LoggingConfigError,
    _MurderbotHandler,
    configure_logging,
    load_logging_config,
)

# The committed example the parser is documented against; the deployed
# logging.yaml is a copy of it.
_EXAMPLE_CONFIG = (
    Path(__file__).resolve().parent.parent / "configs" / "examples" / "logging.example.yaml"
)


def _murderbot_handlers(root: logging.Logger) -> list[_MurderbotHandler]:
    return [h for h in root.handlers if isinstance(h, _MurderbotHandler)]


def test_load_logging_config_parses_committed_example_file() -> None:
    # Guards the "keep this file in sync with that parser" promise in the
    # example's header: if the schema and the example drift, this fails.
    config = load_logging_config(_EXAMPLE_CONFIG)

    assert config.level == "INFO"
    assert config.destinations == ["stdout"]


def test_load_logging_config_parses_full_example(tmp_path: Path) -> None:
    path = tmp_path / "logging.yaml"
    path.write_text("level: DEBUG\ndestinations:\n  - stdout\n  - stderr\n")

    config = load_logging_config(path)

    assert config.level == "DEBUG"
    assert config.destinations == ["stdout", "stderr"]


def test_load_logging_config_defaults_when_file_minimal(tmp_path: Path) -> None:
    path = tmp_path / "logging.yaml"
    path.write_text("")

    config = load_logging_config(path)

    assert config.level == "INFO"
    assert config.destinations == ["stdout"]


def test_load_logging_config_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(LoggingConfigError):
        load_logging_config(tmp_path / "does-not-exist.yaml")


def test_load_logging_config_rejects_non_mapping_yaml(tmp_path: Path) -> None:
    path = tmp_path / "logging.yaml"
    path.write_text("- just\n- a\n- list\n")

    with pytest.raises(LoggingConfigError):
        load_logging_config(path)


def test_load_logging_config_rejects_unknown_level(tmp_path: Path) -> None:
    path = tmp_path / "logging.yaml"
    path.write_text("level: CHATTE\n")

    with pytest.raises(LoggingConfigError):
        load_logging_config(path)


def test_load_logging_config_level_is_case_insensitive(tmp_path: Path) -> None:
    path = tmp_path / "logging.yaml"
    path.write_text("level: warning\n")

    config = load_logging_config(path)

    assert config.level == "WARNING"


def test_load_logging_config_rejects_empty_destinations(tmp_path: Path) -> None:
    path = tmp_path / "logging.yaml"
    path.write_text("destinations: []\n")

    with pytest.raises(LoggingConfigError):
        load_logging_config(path)


def test_load_logging_config_rejects_non_string_destination(tmp_path: Path) -> None:
    path = tmp_path / "logging.yaml"
    path.write_text("destinations:\n  - 42\n")

    with pytest.raises(LoggingConfigError):
        load_logging_config(path)


def test_load_logging_config_accepts_single_destination_string(tmp_path: Path) -> None:
    # A single destination written as a scalar YAML string is normalized to
    # a one-element list, matching the common "destinations: stderr" shape.
    path = tmp_path / "logging.yaml"
    path.write_text("destinations: stderr\n")

    config = load_logging_config(path)

    assert config.destinations == ["stderr"]


def test_configure_logging_default_applies_info_stdout() -> None:
    root = logging.getLogger()

    try:
        configure_logging()

        assert root.level == logging.INFO
        ours = _murderbot_handlers(root)
        assert len(ours) == 1
        assert ours[0].stream is __import__("sys").stdout
    finally:
        for handler in _murderbot_handlers(root):
            root.removeHandler(handler)


def test_configure_logging_explicit_level_keeps_stdout() -> None:
    root = logging.getLogger()

    try:
        configure_logging(level=logging.DEBUG)

        assert root.level == logging.DEBUG
        ours = _murderbot_handlers(root)
        assert len(ours) == 1
        assert ours[0].stream is __import__("sys").stdout
    finally:
        for handler in _murderbot_handlers(root):
            root.removeHandler(handler)


def test_configure_logging_explicit_string_level() -> None:
    root = logging.getLogger()

    try:
        configure_logging(level="ERROR")

        assert root.level == logging.ERROR
    finally:
        for handler in _murderbot_handlers(root):
            root.removeHandler(handler)


def test_configure_logging_from_path(tmp_path: Path) -> None:
    path = tmp_path / "logging.yaml"
    path.write_text("level: WARNING\ndestinations:\n  - stderr\n")

    root = logging.getLogger()

    try:
        configure_logging(path=path)

        assert root.level == logging.WARNING
        ours = _murderbot_handlers(root)
        assert len(ours) == 1
        assert ours[0].stream is __import__("sys").stderr
    finally:
        for handler in _murderbot_handlers(root):
            root.removeHandler(handler)


def test_configure_logging_from_config_object(tmp_path: Path) -> None:
    path = tmp_path / "logging.yaml"
    path.write_text("level: CRITICAL\ndestinations:\n  - stdout\n  - stderr\n")
    config = load_logging_config(path)

    root = logging.getLogger()

    try:
        configure_logging(config=config)

        assert root.level == logging.CRITICAL
        assert len(_murderbot_handlers(root)) == 2
    finally:
        for handler in _murderbot_handlers(root):
            root.removeHandler(handler)


def test_configure_logging_is_idempotent_on_reconfigure(tmp_path: Path) -> None:
    # Calling configure_logging twice must replace, not stack, handlers.
    path = tmp_path / "logging.yaml"
    path.write_text("level: INFO\ndestinations:\n  - stdout\n")

    root = logging.getLogger()

    try:
        configure_logging(path=path)
        first_count = len(_murderbot_handlers(root))
        configure_logging(path=path)

        assert len(_murderbot_handlers(root)) == first_count == 1
    finally:
        for handler in _murderbot_handlers(root):
            root.removeHandler(handler)


def test_configure_logging_rejects_unsupported_destination(tmp_path: Path) -> None:
    path = tmp_path / "logging.yaml"
    path.write_text("destinations:\n  - /tmp/somewhere.log\n")

    with pytest.raises(LoggingConfigError):
        configure_logging(path=path)


def test_load_logging_config_preserves_unknown_keys_by_ignoring(tmp_path: Path) -> None:
    # Unknown keys are tolerated (forward-compat) rather than rejected,
    # matching config.py's "extra" posture.
    path = tmp_path / "logging.yaml"
    path.write_text("level: INFO\nfuture_option: true\n")

    config = load_logging_config(path)

    assert config.level == "INFO"


def test_load_logging_config_rejects_malformed_yaml(tmp_path: Path) -> None:
    # A YAML syntax error must surface as LoggingConfigError, not a raw
    # yaml.YAMLError, so callers have a single exception to handle.
    path = tmp_path / "logging.yaml"
    path.write_text("level: [unclosed\n")

    with pytest.raises(LoggingConfigError):
        load_logging_config(path)


def test_load_logging_config_rejects_unreadable_path(tmp_path: Path) -> None:
    # A directory where the file should be exists() but cannot be opened.
    path = tmp_path / "logging.yaml"
    path.mkdir()

    with pytest.raises(LoggingConfigError):
        load_logging_config(path)


def test_configure_logging_explicit_string_level_is_case_insensitive() -> None:
    root = logging.getLogger()

    try:
        configure_logging(level="debug")

        assert root.level == logging.DEBUG
    finally:
        for handler in _murderbot_handlers(root):
            root.removeHandler(handler)


@pytest.mark.parametrize("bad_level", ["CHATTY", "basic_format", ""])
def test_configure_logging_rejects_unknown_string_level(bad_level: str) -> None:
    # "basic_format" upper-cases to a real attribute of the logging module
    # that is not a level; it must be rejected, not passed to setLevel().
    root = logging.getLogger()
    level_before = root.level

    with pytest.raises(LoggingConfigError):
        configure_logging(level=bad_level)

    assert root.level == level_before
    assert _murderbot_handlers(root) == []


def test_configure_logging_rejects_unknown_numeric_level() -> None:
    with pytest.raises(LoggingConfigError):
        configure_logging(level=17)


def test_configure_logging_rejects_invalid_config_object() -> None:
    # LoggingConfig can be built directly, bypassing load_logging_config.
    with pytest.raises(LoggingConfigError):
        configure_logging(LoggingConfig(level="LOUD"))


def test_configure_logging_failure_keeps_existing_handlers(tmp_path: Path) -> None:
    # A rejected reconfiguration must not tear down working logging.
    bad = tmp_path / "logging.yaml"
    bad.write_text("destinations:\n  - syslog\n")
    root = logging.getLogger()

    try:
        configure_logging(level="WARNING")
        installed = _murderbot_handlers(root)

        with pytest.raises(LoggingConfigError):
            configure_logging(path=bad)

        assert _murderbot_handlers(root) == installed
        assert root.level == logging.WARNING
    finally:
        for handler in _murderbot_handlers(root):
            root.removeHandler(handler)
