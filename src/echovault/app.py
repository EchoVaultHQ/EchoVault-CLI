from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Static , Footer , DataTable
from textual.theme import Theme
from rich.text import Text
import sqlite3
import os
from pathlib import Path
import pygame
from typing import Optional
import random

dracula_theme = Theme(
    name="dracula",
    primary="#BD93F9",
    secondary="#6272A4",
    accent="#FF79C6",
    foreground="#F8F8F2",
    background="#282A36",
    panel="#1E1F29",
    surface="#3A3C4E",
    success="#50FA7B",
    warning="#F1FA8C",
    error="#FF5555",
    dark=True,
    variables={
        "block-cursor-text-style": "none",
        "footer-key-foreground": "#88C0D0",
        "input-selection-background": "#81a1c1 35%",
    },
)

arctic_theme = Theme(
    name="arctic",
    primary="#88C0D0",
    secondary="#81A1C1",
    accent="#B48EAD",
    foreground="#D8DEE9",
    background="#2E3440",
    success="#A3BE8C",
    warning="#EBCB8B",
    error="#BF616A",
    surface="#3B4252",
    panel="#434C5E",
    dark=True,
    variables={
        "block-cursor-text-style": "none",
        "footer-key-foreground": "#88C0D0",
        "input-selection-background": "#81a1c1 35%",
    },
)

class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.current_track: Optional[str] = None
        self.loaded = False
        self.is_playing = False
        self.is_paused = False
        self.playlist: list = []
        self.current_index: int = 0
        self.shuffle_mode = False
        self.repeat_mode = False  # False = no repeat, True = repeat all
        self.shuffle_indices: list = []
        
    def load_track(self, file_path: str) -> bool:
        try:
            pygame.mixer.music.load(file_path)
            self.current_track = file_path
            self.loaded = True
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
        else:
            pygame.mixer.music.play()
        self.is_playing = True
    
    def pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.is_playing = False
    
    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
    
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

class EchoVault(App):
    CSS_PATH = "app.tcss"
    
    BINDINGS = [
        ("space", "toggle_play", "Play/Pause"),
        ("n", "next_track", "Next"),
        ("p", "previous_track", "Previous"),
        ("s", "toggle_shuffle", "Shuffle"),
        ("r", "toggle_repeat", "Repeat"),
        ("+", "volume_up", "Vol +"),
        ("-", "volume_down", "Vol -"),
        ("q", "quit", "Quit"),
    ]
    
    def __init__(self, db_path: str = "sonic.db"):
        super().__init__()
        home = Path.home()
        self.db_path = home / ".config" / "EchoVault" / "sonicbox.db"
        if not self.db_path.exists():
            print(f"Database not found at: {self.db_path}")
        self.audio_player = AudioPlayer()
        self.tracks_data = []
    
    def compose(self) -> ComposeResult:
        with Container(id="app-grid"):
            # for displaying tracks
            with VerticalScroll(id="left-pane"):
                yield DataTable(id="track-table",show_cursor=True)
            # app name        
            with Horizontal(id="top-right"):
                ECHO_ASCII = Text(
                    r"""
                ______     _            __     __          _ _    
                | ____|___| |__   ___   \ \   / /_ _ _   _| | |_  
                |  _| / __| '_ \ / _ \   \ \ / / _` | | | | | __| 
                | |__| (__| | | | (_) |   \ V / (_| | |_| | | |_  
                |_____\___|_| |_|\___/     \_/ \__,_|\__,_|_|\__|              
                """
                )
                ECHO_ASCII.stylize("bold")
                yield Static(ECHO_ASCII, id="logo")
            # for displaying user library information
            with Container(id="bottom-right"):
                yield Static("Total Tracks")
                yield Static("Artists")
                yield Static("Liked Songs")
                yield Static("Storage Used")
                yield Static("Folders")
                yield Static("Total Duration")
                yield Static("Listening Time", id="bottom-right-final")
        yield Footer()
    
    def get_db_connection(self):
        return sqlite3.connect(str(self.db_path))
    
    # will be replaced by db call
    def load_track_data(self) -> None:
        if not self.db_path.exists():
            self.notify("Database not found!", severity="error")
            return
        
        table = self.query_one("#track-table", DataTable)
        table.cursor_type = "row"
        table.show_cursor = True
        table.clear(columns=True)
        
        # Add columns with widths
        table.add_column("Title", width=35)
        table.add_column("Artist", width=25)
        table.add_column("Album", width=25)
        table.add_column("Duration", width=12)
        
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, artist, title, album, duration, file_path
                FROM tracks
                ORDER BY artist, album, title
            """)
            
            rows = cursor.fetchall()
            self.tracks_data = []
            
            for track_id, artist, title, album, duration, file_path in rows:
                # Format duration
                if duration:
                    minutes = int(duration // 60)
                    seconds = int(duration % 60)
                    formatted_duration = f"{minutes:02}:{seconds:02}"
                else:
                    formatted_duration = "--:--"
                
                table.add_row(
                    title or "Unknown Title",
                    artist or "Unknown Artist",
                    album or "Unknown Album",
                    formatted_duration,
                    key=f"track-{track_id}"
                )
                
                self.tracks_data.append({
                    "id": track_id, 
                    "title": title,
                    "artist": artist,
                    "album": album,
                    "duration": duration,
                    "file_path": file_path
                })
            
            conn.close()
            
            self.audio_player.set_playlist(self.tracks_data)
            
            if len(self.tracks_data) > 0:
                self.notify(f"Loaded {len(self.tracks_data)} tracks")
            else:
                self.notify("No tracks found in database", severity="warning")
        except Exception as e:
            self.notify(f"Error loading tracks: {e}", severity="error")
            
    def load_stats(self) -> None:
        if not self.db_path.exists():
            return
            
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Total tracks
            cursor.execute("SELECT COUNT(*) FROM tracks")
            total_tracks = cursor.fetchone()[0]
            
            # Unique artists
            cursor.execute("SELECT COUNT(DISTINCT artist_id) FROM tracks WHERE artist_id IS NOT NULL")
            unique_artists = cursor.fetchone()[0]
            
            # Liked songs
            cursor.execute("SELECT COUNT(*) FROM tracks WHERE isLiked = 1")
            liked_songs = cursor.fetchone()[0]
            
            # Total duration
            cursor.execute("SELECT SUM(duration) FROM tracks WHERE duration IS NOT NULL")
            total_seconds = cursor.fetchone()[0] or 0
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            total_duration = f"{hours}h {minutes}m"
            
            # Storage used (sum of file sizes)
            cursor.execute("SELECT file_path FROM tracks")
            file_paths = cursor.fetchall()
            total_size = 0
            for (path,) in file_paths:
                if path and os.path.exists(path):
                    total_size += os.path.getsize(path)
            storage_mb = total_size / (1024 * 1024)
            storage_used = f"{storage_mb:.1f} MB"
            
            # Folders
            cursor.execute("SELECT COUNT(*) FROM folders")
            folders = cursor.fetchone()[0]
            
            # Listening time (sum of plays * duration)
            cursor.execute("SELECT SUM(duration * noOfPlays) FROM tracks WHERE duration IS NOT NULL")
            listening_seconds = cursor.fetchone()[0] or 0
            listening_hours = int(listening_seconds // 3600)
            listening_minutes = int((listening_seconds % 3600) // 60)
            listening_time = f"{listening_hours}h {listening_minutes}m"
            
            conn.close()
            
            stats = {
                "Total Tracks": total_tracks,
                "Artists": unique_artists,
                "Liked Songs": liked_songs,
                "Storage Used": storage_used,
                "Folders": folders,
                "Total Duration": total_duration,
                "Listening Time": listening_time,
            }
            
            # Update Static widgets
            bottom_widgets = self.query("#bottom-right > Static")
            
            for static in bottom_widgets:
                label_text = static.render().plain.strip()
                
                for key in stats:
                    if key in label_text:
                        value = stats[key]
                        static.update(f"[b]{key}[/b]\n{value}")
                        break
                        
        except Exception as e:
            self.notify(f"Error loading stats: {e}", severity="error")


        
    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        table = self.query_one("#track-table", DataTable)
        row_key = event.row_key
        
        # Extract track ID from row key
        track_id = int(row_key.value.split("-")[1])
        
        # Find track in tracks_data
        for idx, track in enumerate(self.tracks_data):
            if track["id"] == track_id:
                self.audio_player.current_index = idx
                file_path = track["file_path"]
                
                if os.path.exists(file_path):
                    if self.audio_player.load_track(file_path):
                        self.audio_player.play()
                        
                        # Update play count
                        try:
                            conn = self.get_db_connection()
                            cursor = conn.cursor()
                            cursor.execute(
                                "UPDATE tracks SET noOfPlays = noOfPlays + 1 WHERE id = ?",
                                (track_id,)
                            )
                            conn.commit()
                            conn.close()
                        except Exception as e:
                            print(f"Error updating play count: {e}")
                        
                        self.notify(f"{track['title']} - {track['artist']}")
                    else:
                        self.notify(f"Error loading track", severity="error")
                else:
                    self.notify(f"File not found: {file_path}", severity="error")
                break
    
    def action_toggle_play(self) -> None:
        if self.audio_player.is_playing:
            self.audio_player.pause()
        else:
            self.audio_player.play()
    
    def action_next_track(self) -> None:
        next_track = self.audio_player.next_track()
        if next_track and os.path.exists(next_track["file_path"]):
            if self.audio_player.load_track(next_track["file_path"]):
                self.audio_player.play()
                self.notify(f"{next_track['title']} - {next_track['artist']}")
    
    def action_previous_track(self) -> None:
        prev_track = self.audio_player.previous_track()
        if prev_track and os.path.exists(prev_track["file_path"]):
            if self.audio_player.load_track(prev_track["file_path"]):
                self.audio_player.play()
                self.notify(f"{prev_track['title']} - {prev_track['artist']}")
    
    def action_toggle_shuffle(self) -> None:
        shuffle_on = self.audio_player.toggle_shuffle()
        self.notify(f"Shuffle: {'ON' if shuffle_on else 'OFF'}")
    
    def action_toggle_repeat(self) -> None:
        repeat_on = self.audio_player.toggle_repeat()
        self.notify(f"Repeat: {'ON' if repeat_on else 'OFF'}")
    
    def on_mount(self) -> None:
        self.register_theme(arctic_theme) 
        self.register_theme(dracula_theme)
        self.theme = "dracula"
        
        # Load tracks and stats from database
        self.load_track_data()
        self.load_stats()
        
def main():
    # entry point function for Hatch
    app = EchoVault()
    app.run()
    
if __name__ == "__main__":
    main()