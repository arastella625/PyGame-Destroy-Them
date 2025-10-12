import pygame
from player import Player
from flame_dude import FlameDude
from health_bar import HealthBar
import random

class WaveManager:
    def __init__(self, screen_width, screen_height, player):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player = player
        self.enemies = pygame.sprite.Group()
        self.wave_number = 0
        self.spawn_wave()

    def spawn_wave(self):
        self.wave_number += 1
        num_enemies = self.wave_number * 2  # Increase number of enemies each wave
        for _ in range(num_enemies):
            x = random.randint(0, self.screen_width - 50)
            y = random.randint(0, self.screen_height - 50)
            enemy = FlameDude(x, y)
            self.enemies.add(enemy)

    def update(self):
        self.enemies.update()
        # Check for collisions between player and enemies
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                print("Player hit by enemy!")
                # Handle player damage here

    def draw(self, surface):
        self.enemies.draw(surface)

    def is_wave_cleared(self):
        print("Checking if wave is cleared. Enemies remaining:", len(self.enemies))
        return len(self.enemies) == 0
    
    def give_player_position(self):
        for enemy in self.enemies:
            enemy.player_pos = self.player.get_position()