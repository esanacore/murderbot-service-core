"""Configuration loading for murderbot-core.

Real configuration lives outside version control on the deployed Pi (see
SECURITY.md and docs/security.md); this module only knows how to parse
and validate it. See configs/examples/ for sanitized example files this
loader is designed against.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


class ConfigError(Exception):
    """Raised when configuration is missing, malformed, or fails validation."""


@dataclass(frozen=True)
class HardwareConfig:
    """Parsed contents of hardware.yaml.

    Fields default to conservative/disabled values (AGENTS.md rule 5:
    safe defaults) so a missing or partial config never silently enables
    hardware the operator didn't explicitly configure.
    """

    atx_enabled: bool = False
    rgb_enabled: bool = False
    audio_enabled: bool = False
    telemetry_enabled: bool = False
    rgb_brightness_cap: float = 0.0
    extra: dict[str, Any] = field(default_factory=dict)


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ConfigError(f"config file not found: {path}")
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        raise ConfigError(f"config file {path} must contain a YAML mapping at the top level")
    return data


def load_hardware_config(path: Path) -> HardwareConfig:
    data = _read_yaml(path)

    brightness_cap = float(data.get("rgb_brightness_cap", 0.0))
    if not 0.0 <= brightness_cap <= 1.0:
        raise ConfigError(f"rgb_brightness_cap must be between 0.0 and 1.0, got {brightness_cap!r}")

    known_keys = {
        "atx_enabled",
        "rgb_enabled",
        "audio_enabled",
        "telemetry_enabled",
        "rgb_brightness_cap",
    }
    extra = {k: v for k, v in data.items() if k not in known_keys}

    return HardwareConfig(
        atx_enabled=bool(data.get("atx_enabled", False)),
        rgb_enabled=bool(data.get("rgb_enabled", False)),
        audio_enabled=bool(data.get("audio_enabled", False)),
        telemetry_enabled=bool(data.get("telemetry_enabled", False)),
        rgb_brightness_cap=brightness_cap,
        extra=extra,
    )


@dataclass(frozen=True)
class Profile:
    """One entry from profiles.yaml (FR-08: per host-state/OS profiles)."""

    name: str
    audio_clip: str | None = None
    rgb_animation: str | None = None


def load_profiles(path: Path) -> dict[str, Profile]:
    data = _read_yaml(path)
    profiles_data = data.get("profiles", {})
    if not isinstance(profiles_data, dict):
        raise ConfigError(f"'profiles' in {path} must be a mapping of name -> settings")

    profiles: dict[str, Profile] = {}
    for name, settings in profiles_data.items():
        if not isinstance(settings, dict):
            raise ConfigError(f"profile {name!r} in {path} must be a mapping")
        profiles[name] = Profile(
            name=name,
            audio_clip=settings.get("audio_clip"),
            rgb_animation=settings.get("rgb_animation"),
        )
    return profiles
