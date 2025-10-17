import unittest
import tempfile
import json
import pygame
from pathlib import Path
from unittest import mock

_orig_pygame_image_load = None

from stats import StatsManager
from player import Player
from wave_manager import WaveManager

class DummyHealthBar:
    def __init__(self, x=20, y=20, h=25):
        self.x = x
        self.y = y
        self.height = h
    def take_damage(self, amount):
        pass

class DummyBullet(pygame.sprite.Sprite):
    def __init__(self, rect, damage=9999):
        super().__init__()
        self.image = pygame.Surface((1,1))
        self.rect = pygame.Rect(rect)
        self._damage = damage
    def get_damage(self):
        return self._damage
    
class TestWaveManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # pygame must be initialized and image.load patched
        pygame.init()
        pygame.display.set_mode((1,1))
        global _orig_pygame_image_load
        _orig_pygame_image_load = pygame.image.load
        pygame.image.load = lambda path: pygame.Surface((32,32), pygame.SRCALPHA)

    @classmethod
    def tearDownClass(cls):
        global _orig_pygame_image_load
        if _orig_pygame_image_load is not None:
            pygame.image.load = _orig_pygame_image_load
        pygame.quit()

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.stats_file = Path(self.tmpdir.name) / "wm_stats.json"
        self.stats = StatsManager(appname="WMTest", filename=str(self.stats_file))

        self.player = Player(100, 100)
        self.health_bar = DummyHealthBar()
        self.wm = WaveManager(200, 200, self.player, self.health_bar, stats=self.stats)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_enemy_kill_increments_score_and_stats(self):
        # ensure some enemies spawned
        self.assertGreater(len(self.wm.enemies), 0)

        enemy = next(iter(self.wm.enemies))
        # create bullet overlapping enemy
        bullet = DummyBullet(enemy.rect)
        self.player.bullets.add(bullet)

        # run update to process collision
        self.wm.update()

        # debug: print location of the stats file so you can inspect it before cleanup
        print(f"DEBUG: stats file path = {self.stats_file}", flush=True)

        # score should increase by at least the placeholder 100
        self.assertGreaterEqual(self.wm.score, 100)
        # stats file should exist and contain totals
        self.assertTrue(self.stats_file.exists())
        data = json.loads(self.stats_file.read_text(encoding="utf-8"))
        self.assertGreaterEqual(data.get("total_kills", 0), 1)
        self.assertGreaterEqual(data.get("total_score", 0), 100)

if __name__ == "__main__":
    unittest.main()