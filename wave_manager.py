import pygame
from player import Player
from flame_dude import FlameDude
from health_bar import HealthBar
import random

class WaveManager:
    def __init__(self, screen_width, screen_height, player, health_bar):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player = player
        self.health_bar = health_bar
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.wave_number = 0
        self.spawn_wave()

    def spawn_wave(self):
        self.wave_number += 1
        num_enemies = self.wave_number * 2
        for _ in range(num_enemies):
            while True:
                x = random.randint(0, self.screen_width - 50)
                y = random.randint(0, self.screen_height - 50)
                new_enemy = FlameDude(x, y)
                if not any(new_enemy.rect.colliderect(e.rect) for e in self.enemies):
                    self.enemies.add(new_enemy)
                    break

    def update(self):
        for enemy in self.enemies:
            enemy.set_player_position(self.player.get_position())
            enemy.update()
            enemy.avoid_overlap(self.enemies)
            if self.player.rect.inflate(-10, -10).colliderect(enemy.rect.inflate(-10, -10)):
                self.player.take_damage(enemy.give_damage())
                print("Player hit by enemy!")
                self.health_bar.take_damage(enemy.give_damage())
        collisions = pygame.sprite.groupcollide(self.enemies, self.player.bullets, False, True)
        for enemy, bullets in collisions.items():
            for bullet in bullets:
                # bullet has .damage set in FieryBullet
                enemy.take_damage(bullet.get_damage())
                enemy.kill() if enemy.is_dead() else None
                print("Enemy hit by bullet!")
        if self.player.is_dead():
            print("Player is dead!")
            pygame.quit()
            raise SystemExit("Game Over")

    def draw(self, surface):
        self.enemies.draw(surface)

    def is_wave_cleared(self):
        print("Checking if wave is cleared. Enemies remaining:", len(self.enemies))
        return len(self.enemies) == 0
    
    def give_player_position(self):
        for enemy in self.enemies:
            enemy.player_pos = self.player.get_position()