import random

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import Static

from .progress import PlaybackProgress
from .volume import VolumeIndicator

_EQ_BARS = "▁▂▃▅▇"


class NowPlayingBar(Horizontal):
    track_title: reactive[str] = reactive("Nothing playing", init=False)
    track_artist: reactive[str] = reactive("", init=False)
    is_playing: reactive[bool] = reactive(False)

    def compose(self) -> ComposeResult:
        with Vertical(id="now-playing-track"):
            yield Static(self.track_title, id="now-playing-title")
            yield Static(self.track_artist, id="now-playing-artist")
        yield PlaybackProgress(id="now-playing-progress")
        with Horizontal(id="now-playing-side"):
            yield VolumeIndicator(id="now-playing-volume")
            yield Static("♪ ♪ ♪", id="now-playing-eq")

    def on_mount(self) -> None:
        self.set_interval(0.3, self._tick_eq)

    def update_track(self, title: str, artist: str) -> None:
        self.track_title = title
        self.track_artist = artist

    def watch_track_title(self, title: str) -> None:
        self.query_one("#now-playing-title", Static).update(title)

    def watch_track_artist(self, artist: str) -> None:
        self.query_one("#now-playing-artist", Static).update(artist)

    def _tick_eq(self) -> None:
        eq = self.query_one("#now-playing-eq", Static)
        if self.is_playing:
            eq.update(" ".join(random.choice(_EQ_BARS) for _ in range(5)))
        else:
            eq.update(_EQ_BARS[0] * 5)
