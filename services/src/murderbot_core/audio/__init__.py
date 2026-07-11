"""Audio-service interface.

Defines the Protocol every real I2S/ALSA audio backend must implement,
plus a MockAudioPlayer for tests. No real backend exists yet — see
AGENTS.md rule 8. Must remain muted/off if unavailable
(docs/architecture.md "Audio service" failure rule).
"""

from __future__ import annotations

from typing import Protocol


class AudioPlayer(Protocol):
    """Plays a single local audio clip, with no network/remote fetch.

    Real clips are never committed to this repository (assets/README.md);
    implementations resolve clip names to local, operator-installed
    files.
    """

    def play(self, clip_name: str) -> None:
        """Play the named clip once. Must not block indefinitely."""
        ...

    def stop(self) -> None:
        """Stop any in-progress playback immediately."""
        ...

    def is_playing(self) -> bool: ...


class MockAudioPlayer:
    """In-memory AudioPlayer for tests. Never touches real audio hardware."""

    def __init__(self) -> None:
        self.play_calls: list[str] = []
        self._playing = False

    def play(self, clip_name: str) -> None:
        self.play_calls.append(clip_name)
        self._playing = True

    def stop(self) -> None:
        self._playing = False

    def is_playing(self) -> bool:
        return self._playing
