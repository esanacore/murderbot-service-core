"""Shared logging configuration for all murderbot-* services.

Each systemd unit (services/systemd/) calls configure_logging() once at
startup so log format/level is consistent across services and journald
captures structured, greppable output rather than each service inventing
its own format.
"""

from __future__ import annotations

import logging
import sys

_LOG_FORMAT = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"


def configure_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format=_LOG_FORMAT,
        stream=sys.stdout,
    )
