from textual.app import ComposeResult
from textual.widgets import Static

_TILES = [
    ("stat-total-tracks", "Total Tracks", "total_tracks", None),
    ("stat-artists", "Artists", "artists", None),
    ("stat-liked-songs", "Liked Songs", "liked_songs", None),
    ("stat-storage-used", "Storage Used", "storage_used", None),
    ("stat-folders", "Folders", "folders", None),
    ("stat-total-duration", "Total Duration", "total_duration", None),
    ("stat-listening-time", "Listening Time", "listening_time", "stats-tile-final"),
]


class StatsPanel(Static):
    def compose(self) -> ComposeResult:
        for tile_id, label, _key, extra_class in _TILES:
            yield Static(f"[b]{label}[/b]\n--", id=tile_id, classes=extra_class or "")

    def apply_stats(self, stats: dict) -> None:
        for tile_id, label, key, _extra_class in _TILES:
            self.query_one(f"#{tile_id}", Static).update(f"[b]{label}[/b]\n{stats[key]}")
