import os

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import DataTable, Footer, Header

from .database import EchoVaultDB
from .player import AudioPlayer
from .theme import arctic_theme, dracula_theme, echovault_purple
from .widgets.album_art import AlbumArt
from .widgets.now_playing import NowPlayingBar
from .widgets.progress import PlaybackProgress
from .widgets.stats import StatsPanel
from .widgets.track_table import TrackTable
from .widgets.volume import VolumeIndicator


class EchoVault(App):
    CSS_PATH = "app.tcss"

    BINDINGS = [
        ("space", "toggle_play", "Play/Pause"),
        ("n", "next_track", "Next"),
        ("p", "previous_track", "Previous"),
        ("s", "toggle_shuffle", "Shuffle"),
        ("r", "toggle_repeat", "Repeat"),
        ("+", "volume_up", "Vol +"),
        ("equals_sign", "volume_up", "Vol +"),
        ("shift+equals_sign", "volume_up", "Vol +"),
        ("-", "volume_down", "Vol -"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()
        self.db = EchoVaultDB()
        self.audio_player = AudioPlayer()
        self.tracks_data: list[dict] = []

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="app-grid"):
            with Vertical(id="left-pane"):
                yield TrackTable(id="track-table")
            with Vertical(id="right-pane"):
                yield AlbumArt(id="album-art")
                yield StatsPanel(id="stats-panel")
        yield NowPlayingBar(id="now-playing")
        yield Footer()

    def on_mount(self) -> None:
        self.register_theme(echovault_purple)
        self.register_theme(dracula_theme)
        self.register_theme(arctic_theme)
        self.theme = "echovault_purple"

        if not self.db.exists():
            self.notify(f"Database not found at: {self.db.db_path}", severity="error")

        self.load_track_data()
        self.load_stats()
        self.query_one(VolumeIndicator).update_volume(self.audio_player.volume)
        self.set_interval(0.5, self._tick_playback)

    def load_track_data(self) -> None:
        if not self.db.exists():
            return
        try:
            self.tracks_data = self.db.fetch_tracks()
            self.query_one(TrackTable).populate(self.tracks_data)
            self.audio_player.set_playlist(self.tracks_data)
            if self.tracks_data:
                self.notify(f"Loaded {len(self.tracks_data)} tracks")
            else:
                self.notify("No tracks found in database", severity="warning")
        except Exception as e:
            self.notify(f"Error loading tracks: {e}", severity="error")

    def load_stats(self) -> None:
        if not self.db.exists():
            return
        try:
            self.query_one(StatsPanel).apply_stats(self.db.fetch_stats())
        except Exception as e:
            self.notify(f"Error loading stats: {e}", severity="error")

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        track_id = int(event.row_key.value.split("-")[1])
        for idx, track in enumerate(self.tracks_data):
            if track["id"] == track_id:
                self.audio_player.current_index = idx
                self._start_track(track)
                break

    def _start_track(self, track: dict) -> None:
        file_path = track["file_path"]
        if not os.path.exists(file_path):
            self.notify(f"File not found: {file_path}", severity="error")
            return
        if not self.audio_player.load_track(file_path):
            self.notify("Error loading track", severity="error")
            return
        self.audio_player.current_track_meta = track
        self.audio_player.play()
        self.db.increment_play_count(track["id"])
        self.load_stats()
        self.notify(f"{track['title']} - {track['artist']}")
        self._update_now_playing(track)

    def _update_now_playing(self, track: dict) -> None:
        now_playing = self.query_one(NowPlayingBar)
        now_playing.update_track(track["title"] or "Unknown Title", track["artist"] or "Unknown Artist")
        now_playing.is_playing = True
        now_playing.query_one(PlaybackProgress).set_duration(track["duration"])
        self.query_one(AlbumArt).update_cover(track.get("cover"))

    def action_toggle_play(self) -> None:
        now_playing = self.query_one(NowPlayingBar)
        if self.audio_player.is_playing:
            self.audio_player.pause()
            now_playing.is_playing = False
        else:
            self.audio_player.play()
            now_playing.is_playing = self.audio_player.is_playing

    def action_next_track(self) -> None:
        self._advance(self.audio_player.next_track())

    def action_previous_track(self) -> None:
        self._advance(self.audio_player.previous_track())

    def _advance(self, track: dict | None) -> None:
        if track and os.path.exists(track["file_path"]):
            if self.audio_player.load_track(track["file_path"]):
                self.audio_player.current_track_meta = track
                self.audio_player.play()
                self.notify(f"{track['title']} - {track['artist']}")
                self._update_now_playing(track)

    def action_toggle_shuffle(self) -> None:
        shuffle_on = self.audio_player.toggle_shuffle()
        self.notify(f"Shuffle: {'ON' if shuffle_on else 'OFF'}")

    def action_toggle_repeat(self) -> None:
        repeat_on = self.audio_player.toggle_repeat()
        self.notify(f"Repeat: {'ON' if repeat_on else 'OFF'}")

    def action_volume_up(self) -> None:
        level = self.audio_player.volume_up()
        self.query_one(VolumeIndicator).update_volume(level)

    def action_volume_down(self) -> None:
        level = self.audio_player.volume_down()
        self.query_one(VolumeIndicator).update_volume(level)

    def _tick_playback(self) -> None:
        if self.audio_player.is_track_finished():
            self.action_next_track()
            return
        if self.audio_player.is_playing:
            elapsed = self.audio_player.get_elapsed_seconds()
            self.query_one(PlaybackProgress).set_elapsed(elapsed)


def main():
    # entry point function for Hatch
    app = EchoVault()
    app.run()


if __name__ == "__main__":
    main()
