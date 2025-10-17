import unittest
import tempfile
import json
from pathlib import Path

from stats import StatsManager

class TestStatsManager(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.filepath = Path(self.tmpdir.name) / "stats.json"

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_save_and_load(self):
        stats = StatsManager(appname="TestApp", filename=str(self.filepath))
        before_games = stats.data.get("games_played", 0)
        stats.start_game()
        self.assertEqual(stats.data["games_played"], before_games + 1)
        stats.record_kill(3)
        stats.add_score(150)
        stats.end_game()  # triggers save

        self.assertTrue(self.filepath.exists())
        loaded = json.loads(self.filepath.read_text(encoding="utf-8"))
        self.assertIn("total_kills", loaded)
        self.assertIn("total_score", loaded)
        self.assertGreaterEqual(loaded["total_kills"], 3)
        self.assertGreaterEqual(loaded["total_score"], 150)

if __name__ == "__main__":
    unittest.main()