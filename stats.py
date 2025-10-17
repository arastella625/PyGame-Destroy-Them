import json
import os
import pathlib
import time
from typing import Dict, Any

class StatsManager:
    def __init__(self, appname: str = "Destroy-Them", filename: str | None = None):
        # pick a sensible per-user folder (Windows: %APPDATA%)
        if filename:
            self.filepath = pathlib.Path(filename).resolve()
        else:
            if os.name == "nt":
                appdata = os.getenv("APPDATA")
                # If APPDATA points into the MS Store package cache, prefer the real user roaming folder
                if appdata and ("Packages" not in appdata and "LocalCache" not in appdata):
                    base = pathlib.Path(appdata)
                else:
                    # prefer explicit user profile fallback (real roaming folder)
                    base = pathlib.Path(os.getenv("USERPROFILE", pathlib.Path.home())) / "AppData" / "Roaming"
            else:
                base = pathlib.Path.home() / ".local" / "share"
            folder = (base / appname)
            folder.mkdir(parents=True, exist_ok=True)
            self.filepath = (folder / "stats.json").resolve()

        # default counters
        self.data: Dict[str, Any] = {
            "total_playtime_seconds": 0.0,
            "games_played": 0,
            "total_kills": 0,
            "total_score": 0,
            "last_session": None
        }
        self._session_start = time.time()
        self.load()

    def load(self):
        if self.filepath.exists():
            try:
                with self.filepath.open("r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    if isinstance(loaded, dict):
                        self.data.update(loaded)
                print(f"StatsManager: Loaded stats from {self.filepath}")
            except Exception as e:
                # ignore corrupt file; keep defaults
                print(f"StatsManager: Failed to load stats ({e}), using defaults")
                pass

    def save(self):
        # ensure parent folder exists (defensive)
        try:
            self.filepath.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"StatsManager: Failed to ensure parent dir {self.filepath.parent}: {e}")

        # atomic write
        tmp = self.filepath.with_suffix(".tmp")
        try:
            with tmp.open("w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
            os.replace(tmp, self.filepath)
            print(f"StatsManager: Saved stats to {self.filepath}")
        except Exception as e:
            print(f"StatsManager: Failed to save stats ({e})")
        finally:
            try:
                if tmp.exists():
                    tmp.unlink()
            except Exception:
                pass

    def add_score(self, amount: int):
        self.data["total_score"] += int(amount)

    def record_kill(self, count: int = 1):
        self.data["total_kills"] += int(count)

    def start_game(self):
        self._session_start = time.time()
        self.data["games_played"] += 1

    def end_game(self):
        elapsed = time.time() - self._session_start
        self.data["total_playtime_seconds"] += elapsed
        self.data["last_session"] = time.time()
        self.save()

    def get(self) -> Dict[str, Any]:
        return dict(self.data)