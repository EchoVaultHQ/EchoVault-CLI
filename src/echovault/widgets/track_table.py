from textual.widgets import DataTable


class TrackTable(DataTable):
    def on_mount(self) -> None:
        self.cursor_type = "row"
        self.show_cursor = True
        self.add_column("Title", width=35)
        self.add_column("Artist", width=25)
        self.add_column("Album", width=25)
        self.add_column("Duration", width=12)

    def populate(self, tracks: list[dict]) -> None:
        self.clear()
        for track in tracks:
            duration = track["duration"]
            if duration:
                minutes = int(duration // 60)
                seconds = int(duration % 60)
                formatted_duration = f"{minutes:02}:{seconds:02}"
            else:
                formatted_duration = "--:--"

            self.add_row(
                track["title"] or "Unknown Title",
                track["artist"] or "Unknown Artist",
                track["album"] or "Unknown Album",
                formatted_duration,
                key=f"track-{track['id']}",
            )
