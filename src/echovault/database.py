import os
import sqlite3
from pathlib import Path


class EchoVaultDB:
    def __init__(self):
        self.db_path = Path.home() / ".config" / "EchoVault" / "sonicbox.db"

    def exists(self) -> bool:
        return self.db_path.exists()

    def get_connection(self):
        return sqlite3.connect(str(self.db_path))

    def fetch_tracks(self) -> list[dict]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, artist, title, album, duration, file_path, cover
                FROM tracks
                ORDER BY artist, album, title
                """
            )
            rows = cursor.fetchall()
        finally:
            conn.close()

        tracks = []
        for track_id, artist, title, album, duration, file_path, cover in rows:
            tracks.append(
                {
                    "id": track_id,
                    "title": title,
                    "artist": artist,
                    "album": album,
                    "duration": duration,
                    "file_path": file_path,
                    "cover": cover,
                }
            )
        return tracks

    def fetch_stats(self) -> dict:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM tracks")
            total_tracks = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(DISTINCT artist_id) FROM tracks WHERE artist_id IS NOT NULL"
            )
            unique_artists = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM tracks WHERE isLiked = 1")
            liked_songs = cursor.fetchone()[0]

            cursor.execute("SELECT SUM(duration) FROM tracks WHERE duration IS NOT NULL")
            total_seconds = cursor.fetchone()[0] or 0
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            total_duration = f"{hours}h {minutes}m"

            cursor.execute("SELECT file_path FROM tracks")
            file_paths = cursor.fetchall()
            total_size = 0
            for (path,) in file_paths:
                if path and os.path.exists(path):
                    total_size += os.path.getsize(path)
            storage_mb = total_size / (1024 * 1024)
            storage_used = f"{storage_mb:.1f} MB"

            cursor.execute("SELECT COUNT(*) FROM folders")
            folders = cursor.fetchone()[0]

            cursor.execute(
                "SELECT SUM(duration * noOfPlays) FROM tracks WHERE duration IS NOT NULL"
            )
            listening_seconds = cursor.fetchone()[0] or 0
            listening_hours = int(listening_seconds // 3600)
            listening_minutes = int((listening_seconds % 3600) // 60)
            listening_time = f"{listening_hours}h {listening_minutes}m"
        finally:
            conn.close()

        return {
            "total_tracks": total_tracks,
            "artists": unique_artists,
            "liked_songs": liked_songs,
            "storage_used": storage_used,
            "folders": folders,
            "total_duration": total_duration,
            "listening_time": listening_time,
        }

    def increment_play_count(self, track_id: int) -> None:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tracks SET noOfPlays = noOfPlays + 1 WHERE id = ?",
                (track_id,),
            )
            conn.commit()
        finally:
            conn.close()
