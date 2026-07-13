from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import ProgressBar, Static


def _format_mmss(seconds: float) -> str:
    seconds = max(0, int(seconds))
    return f"{seconds // 60:02}:{seconds % 60:02}"


class PlaybackProgress(Horizontal):
    def compose(self) -> ComposeResult:
        yield Static("00:00", id="elapsed-label")
        yield ProgressBar(total=100, show_eta=False, show_percentage=False, id="progress-bar")
        yield Static("00:00", id="total-label")

    def set_duration(self, duration: float | None) -> None:
        bar = self.query_one(ProgressBar)
        bar.update(total=duration or 0)
        self.query_one("#total-label", Static).update(_format_mmss(duration or 0))
        self.set_elapsed(0)

    def set_elapsed(self, elapsed: float) -> None:
        self.query_one(ProgressBar).update(progress=elapsed)
        self.query_one("#elapsed-label", Static).update(_format_mmss(elapsed))
