import random
import time
from typing import Optional

import pygame


class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.current_track: Optional[str] = None
        self.current_track_meta: Optional[dict] = None
        self.loaded = False
        self.is_playing = False
        self.is_paused = False
        self.playlist: list = []
        self.current_index: int = 0
        self.shuffle_mode = False
        self.repeat_mode = False  # False = no repeat, True = repeat all
        self.shuffle_indices: list = []
        self.volume = 0.7
        pygame.mixer.music.set_volume(self.volume)
        self._play_started_at: Optional[float] = None
        self._paused_elapsed: float = 0.0

    def load_track(self, file_path: str) -> bool:
        try:
            pygame.mixer.music.load(file_path)
            self.current_track = file_path
            self.loaded = True
            self._play_started_at = None
            self._paused_elapsed = 0.0
            return True
        except Exception as e:
            print(f"Error loading track: {e}")
            self.loaded = False
            return False

    def play(self):
        if not self.loaded:
            print("Cannot play: no track loaded.")
            return

        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self._play_started_at = time.monotonic()
        else:
            pygame.mixer.music.play()
            self._paused_elapsed = 0.0
            self._play_started_at = time.monotonic()
        self.is_playing = True

    def pause(self):
        if self.is_playing:
            self._paused_elapsed = self.get_elapsed_seconds()
            pygame.mixer.music.pause()
            self.is_paused = True
            self.is_playing = False
            self._play_started_at = None

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self._play_started_at = None
        self._paused_elapsed = 0.0

    def get_elapsed_seconds(self) -> float:
        if self.is_playing and self._play_started_at is not None:
            return self._paused_elapsed + (time.monotonic() - self._play_started_at)
        return self._paused_elapsed

    def is_track_finished(self) -> bool:
        return self.loaded and self.is_playing and not pygame.mixer.music.get_busy()

    def toggle_shuffle(self):
        self.shuffle_mode = not self.shuffle_mode
        if self.shuffle_mode:
            self.shuffle_indices = list(range(len(self.playlist)))
            random.shuffle(self.shuffle_indices)
        return self.shuffle_mode

    def toggle_repeat(self):
        self.repeat_mode = not self.repeat_mode
        return self.repeat_mode

    def set_playlist(self, tracks: list):
        self.playlist = tracks
        self.shuffle_indices = list(range(len(tracks)))

    def next_track(self) -> Optional[dict]:
        if not self.playlist:
            return None

        if self.shuffle_mode:
            current_shuffle_pos = self.shuffle_indices.index(self.current_index)
            next_shuffle_pos = (current_shuffle_pos + 1) % len(self.shuffle_indices)
            self.current_index = self.shuffle_indices[next_shuffle_pos]
        else:
            self.current_index = (self.current_index + 1) % len(self.playlist)

        if self.current_index == 0 and not self.repeat_mode:
            return None

        return self.playlist[self.current_index]

    def previous_track(self) -> Optional[dict]:
        if not self.playlist:
            return None

        if self.shuffle_mode:
            current_shuffle_pos = self.shuffle_indices.index(self.current_index)
            prev_shuffle_pos = (current_shuffle_pos - 1) % len(self.shuffle_indices)
            self.current_index = self.shuffle_indices[prev_shuffle_pos]
        else:
            self.current_index = (self.current_index - 1) % len(self.playlist)

        return self.playlist[self.current_index]

    def volume_up(self):
        self.volume = min(1.0, self.volume + 0.05)
        pygame.mixer.music.set_volume(self.volume)
        return self.volume

    def volume_down(self):
        self.volume = max(0.0, self.volume - 0.05)
        pygame.mixer.music.set_volume(self.volume)
        return self.volume
