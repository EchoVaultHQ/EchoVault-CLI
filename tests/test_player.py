import time
from unittest.mock import patch

import pygame

from echovault.player import AudioPlayer


def _loaded_player() -> AudioPlayer:
    """An AudioPlayer with playback state faked, so tests exercise our own
    elapsed-time bookkeeping without depending on a real audio device."""
    player = AudioPlayer()
    player.loaded = True
    return player


def test_volume_initialized_and_adjustable():
    player = AudioPlayer()
    assert player.volume == 0.7  # was never initialized before this fix
    player.volume_up()
    assert round(player.volume, 2) == 0.75
    player.volume_down()
    player.volume_down()
    assert round(player.volume, 2) == 0.65


@patch.object(pygame.mixer.music, "unpause")
@patch.object(pygame.mixer.music, "pause")
@patch.object(pygame.mixer.music, "play")
def test_elapsed_time_freezes_on_pause_and_resumes_without_reset(*_mocks):
    player = _loaded_player()

    player.play()
    time.sleep(0.2)
    elapsed_while_playing = player.get_elapsed_seconds()
    assert elapsed_while_playing >= 0.2

    player.pause()
    frozen = player.get_elapsed_seconds()
    time.sleep(0.2)
    assert player.get_elapsed_seconds() == frozen  # must not advance while paused

    player.play()  # resume
    time.sleep(0.2)
    resumed = player.get_elapsed_seconds()
    assert resumed > frozen  # continues from the frozen point, not from 0


@patch.object(pygame.mixer.music, "play")
def test_load_track_resets_elapsed_state(_mock_play):
    player = _loaded_player()
    player.play()
    time.sleep(0.1)
    assert player.get_elapsed_seconds() > 0

    player.current_track = None
    player.loaded = False
    player._play_started_at = None
    player._paused_elapsed = 5.0  # simulate stale state from a previous track
    assert player.get_elapsed_seconds() == 5.0  # frozen (not playing)


if __name__ == "__main__":
    test_volume_initialized_and_adjustable()
    test_elapsed_time_freezes_on_pause_and_resumes_without_reset()
    test_load_track_resets_elapsed_state()
    print("All player self-checks passed.")
