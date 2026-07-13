from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static
from textual_image.widget import Image


class AlbumArt(Container):
    def compose(self) -> ComposeResult:
        yield Image(id="cover-image")
        yield Static("\n♪\n\nNo cover art", id="cover-placeholder")

    def on_mount(self) -> None:
        self._show_placeholder()

    def update_cover(self, cover_path: str | None) -> None:
        if cover_path and Path(cover_path).exists():
            self.query_one("#cover-image", Image).image = cover_path
            self._show_image()
        else:
            self._show_placeholder()

    def _show_image(self) -> None:
        self.query_one("#cover-image", Image).styles.display = "block"
        self.query_one("#cover-placeholder", Static).styles.display = "none"

    def _show_placeholder(self) -> None:
        self.query_one("#cover-image", Image).styles.display = "none"
        self.query_one("#cover-placeholder", Static).styles.display = "block"
