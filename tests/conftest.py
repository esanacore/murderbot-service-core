"""Shared pytest fixtures for the murderbot_core test suite."""

from __future__ import annotations

import logging
from collections.abc import Iterator

import pytest


@pytest.fixture(autouse=True)
def _restore_root_logger() -> Iterator[None]:
    """Snapshot the root logger's handlers and level, and restore them.

    ``configure_logging()`` (and so ``core_service.build_core``/``main``)
    mutates the process-wide root logger. Without this, a handler bound to
    one test's captured ``sys.stdout`` would outlive that test and leak
    into the next one.
    """
    root = logging.getLogger()
    handlers = list(root.handlers)
    level = root.level
    try:
        yield
    finally:
        root.handlers[:] = handlers
        root.setLevel(level)
