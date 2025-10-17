# PyGame-Destroy-Them
This repo will house my final project for CS521. I am using PyGame to create a very simple version of games like "Vampire Survivors".

A small top-down shooter built with Pygame. Control a player, shoot enemies, survive waves, and track basic stats (score, kills, playtime) saved to disk.

---

## Quick start

Requirements
- Python 3.10+ (3.11 recommended)
- pip

Install dependencies (Windows / terminal / project root):
````
python -m pip install --upgrade pip
pip install pygame
````

# How to Run Game

```
python main.py
```

# How to Run UnitTests

```
python -m unittest discover -s tests -v
```

# Controls

Move: Arrow keys or WASD
Aim: Mouse cursor
Shoot: Space (there is a cooldown so you cannot hold fire continuously — default ~1 second)
Quit: Close window (or Ctrl+C in terminal)

## Gameplay mechanics (overview)

# Player

Has a health value shown near the health bar.
Fires "fiery" bullets toward the mouse cursor.
Fire is rate-limited by a cooldown (adjustable in Player.shot_cooldown in milliseconds).
Player bullets are managed by a sprite Group.

# Enemies (FlameDude)

Move toward the player and have their own health and damage values.
Show a brief red "damage flash" overlay when hit and an optional small health bar above them.
When killed they increment the score (default placeholder: +100 per kill).
Waves

Waves spawn progressively more enemies (WaveManager.spawn_wave()).
WaveManager tracks score, draws enemies, health text, and score text.

# Stats persistence

A small StatsManager records totals (games played, total playtime seconds, total kills, total score, last session timestamp) and writes them to a JSON file.

## Where stats are saved

By default StatsManager writes a JSON file in a per-user app data folder:

Windows (normal CPython): %APPDATA%\Destroy-Them\stats.json (usually C:\Users\<you>\AppData\Roaming\Destroy-Them\stats.json)
If you're using the Microsoft Store packaged Python, APPDATA can be redirected into the Python package cache. The code attempts to fallback to the real roaming folder when that happens.

You can also force a specific file path by constructing StatsManager with a filename:
```
from stats import StatsManager
stats = StatsManager(appname="Destroy-Them", filename=r"C:\path\to\stats.json")
```
Example stats.json contents:
```
{
  "total_playtime_seconds": 300.89,
  "games_played": 7,
  "total_kills": 228,
  "total_score": 22800,
  "last_session": 1760713384.2163131
}
```

## Assets
Place graphical assets in the assets/ folder at the project root:

  assets/player.png
  assets/flame_dude.png
  assets/background.png
  (These filenames are referenced by the code; use same names or change the paths in source.)

## Running & debugging tips

Run from an integrated terminal (VS Code) or an external terminal so stdout/stderr and debug prints (file paths, save confirmations) are visible.

Tests use tempfile and remove temporary files after each run. If you want to inspect test-created files, add a print() in the test or disable cleanup temporarily.


https://github.com/arastella625/PyGame-Destroy-Them.git