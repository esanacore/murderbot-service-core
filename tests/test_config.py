from pathlib import Path

import pytest

from murderbot_core.config import ConfigError, load_hardware_config, load_profiles


def test_load_hardware_config_defaults_are_safe_when_file_minimal(tmp_path: Path) -> None:
    path = tmp_path / "hardware.yaml"
    path.write_text("atx_enabled: true\n")

    config = load_hardware_config(path)

    assert config.atx_enabled is True
    assert config.rgb_enabled is False
    assert config.audio_enabled is False
    assert config.telemetry_enabled is False
    assert config.rgb_brightness_cap == 0.0


def test_load_hardware_config_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(ConfigError):
        load_hardware_config(tmp_path / "does-not-exist.yaml")


def test_load_hardware_config_rejects_out_of_range_brightness_cap(tmp_path: Path) -> None:
    path = tmp_path / "hardware.yaml"
    path.write_text("rgb_brightness_cap: 1.5\n")

    with pytest.raises(ConfigError):
        load_hardware_config(path)


def test_load_hardware_config_rejects_non_mapping_yaml(tmp_path: Path) -> None:
    path = tmp_path / "hardware.yaml"
    path.write_text("- just\n- a\n- list\n")

    with pytest.raises(ConfigError):
        load_hardware_config(path)


def test_load_hardware_config_preserves_unknown_keys_as_extra(tmp_path: Path) -> None:
    path = tmp_path / "hardware.yaml"
    path.write_text("atx_enabled: true\nfuture_field: 42\n")

    config = load_hardware_config(path)

    assert config.extra == {"future_field": 42}


def test_load_profiles_parses_named_profiles(tmp_path: Path) -> None:
    path = tmp_path / "profiles.yaml"
    path.write_text(
        "profiles:\n"
        "  windows:\n"
        "    audio_clip: startup_windows.wav\n"
        "    rgb_animation: boot_blue\n"
        "  linux:\n"
        "    audio_clip: startup_linux.wav\n"
    )

    profiles = load_profiles(path)

    assert set(profiles) == {"windows", "linux"}
    assert profiles["windows"].audio_clip == "startup_windows.wav"
    assert profiles["windows"].rgb_animation == "boot_blue"
    assert profiles["linux"].rgb_animation is None


def test_load_profiles_empty_file_returns_empty_dict(tmp_path: Path) -> None:
    path = tmp_path / "profiles.yaml"
    path.write_text("")

    assert load_profiles(path) == {}


def test_load_profiles_rejects_non_mapping_profile_entry(tmp_path: Path) -> None:
    path = tmp_path / "profiles.yaml"
    path.write_text("profiles:\n  windows: not-a-mapping\n")

    with pytest.raises(ConfigError):
        load_profiles(path)
