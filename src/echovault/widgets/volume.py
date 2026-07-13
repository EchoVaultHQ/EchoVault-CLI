from textual.widgets import Static

_SEGMENTS = 14


class VolumeIndicator(Static):
    def update_volume(self, level: float) -> None:
        filled = round(level * _SEGMENTS)
        bar = "█" * filled + "░" * (_SEGMENTS - filled)
        pct = round(level * 100)
        self.update(f"Vol {bar} {pct:>3}%")
