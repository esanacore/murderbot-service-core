"""Tests for the mock hardware/audio/rgb/telemetry backends.

These mocks are what let the rest of the test suite (and, later, real
service code) run with no Raspberry Pi attached (AGENTS.md rule 8). The
tests here are less about business logic and more about pinning the
contract: fail-open defaults and the brightness cap must hold even in
the mock, since the mock is what real code is unit-tested against.
"""

from murderbot_core.audio import MockAudioPlayer
from murderbot_core.hardware import MockAtxInterface
from murderbot_core.rgb import MockRgbController
from murderbot_core.telemetry import MockTelemetrySource, TelemetrySample


def test_atx_interface_defaults_to_main_rail_off() -> None:
    atx = MockAtxInterface()
    assert atx.is_main_rail_on() is False


def test_atx_interface_records_pulses() -> None:
    atx = MockAtxInterface()
    atx.pulse_power(duration_ms=250)
    atx.pulse_reset()
    assert atx.power_pulses == [250]
    assert atx.reset_pulses == [200]


def test_atx_interface_close_is_recorded() -> None:
    atx = MockAtxInterface()
    atx.close()
    assert atx.closed is True


def test_audio_player_tracks_play_calls_and_playing_state() -> None:
    player = MockAudioPlayer()
    assert player.is_playing() is False

    player.play("startup.wav")

    assert player.play_calls == ["startup.wav"]
    assert player.is_playing() is True

    player.stop()
    assert player.is_playing() is False


def test_rgb_controller_clamps_brightness_to_configured_cap() -> None:
    rgb = MockRgbController(brightness_cap=0.5)

    rgb.set_brightness(1.0)

    assert rgb.brightness == 0.5


def test_rgb_controller_off_resets_state() -> None:
    rgb = MockRgbController()
    rgb.set_animation("boot")
    rgb.set_brightness(0.8)

    rgb.off()

    assert rgb.is_on is False
    assert rgb.current_animation is None
    assert rgb.brightness == 0.0


def test_telemetry_source_unavailable_returns_none_even_with_sample_set() -> None:
    telemetry = MockTelemetrySource(available=False)
    telemetry.set_sample(TelemetrySample(source="test", cpu_temp_c=55.0))

    assert telemetry.is_available() is False
    assert telemetry.read() is None


def test_telemetry_source_available_returns_set_sample() -> None:
    telemetry = MockTelemetrySource(available=True)
    sample = TelemetrySample(source="test", cpu_temp_c=55.0)
    telemetry.set_sample(sample)

    assert telemetry.read() == sample
