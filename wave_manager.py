import pygame
from player import Player
from flame_dude import FlameDude
from health_bar import HealthBar
import random

class WaveManager:
    def __init__(self, screen_width, screen_height, player, health_bar, stats=None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player = player
        self.health_bar = health_bar
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.wave_number = 0
        self.score = 0
        # initialize font
        pygame.font.init()
        self.font = pygame.font.Font(None, 28)  # None = default font, size 28
        self.spawn_wave()
        self.stats = stats  # Store stats manager if provided

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
                if enemy.is_dead():
                    enemy.kill()
                    self.score += 100  # placeholder score per kill
                    print("Enemy killed! Score:", self.score)
                    if self.stats:
                        self.stats.record_kill(1)
                        self.stats.add_score(100)
                        self.stats.save()  # optional: save after each kill
                else:
                    print("Enemy hit by bullet!")
        if self.player.is_dead():
            print("Player is dead!")
            pygame.quit()
            raise SystemExit("Game Over")

    def draw(self, surface):
        # draw each enemy using its custom draw (so overlays/health bars appear)
        for enemy in self.enemies:
            if hasattr(enemy, "draw"):
                enemy.draw(surface)
            else:
                surface.blit(enemy.image, enemy.rect)

        # determine health bar position/size (robust fallback)
        padding = 6
        if hasattr(self.health_bar, "rect"):
            bar_x, bar_y, bar_h = self.health_bar.rect.x, self.health_bar.rect.y, self.health_bar.rect.height
        else:
            bar_x = getattr(self.health_bar, "x", 20)
            bar_y = getattr(self.health_bar, "y", 20)
            bar_h = getattr(self.health_bar, "height", getattr(self.health_bar, "h", 25))

        # render texts
        health_text = self.font.render(f"Health: {self.player.get_health()}", True, (255, 255, 255))
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 0))

        # draw health text below the health bar
        health_pos = (bar_x, bar_y + bar_h + padding)
        surface.blit(health_text, health_pos)

        # place score at top-right with 10px padding
        score_pos_x = self.screen_width - score_text.get_width() - 10
        surface.blit(score_text, (score_pos_x, 10))

    def is_wave_cleared(self):
        print("Checking if wave is cleared. Enemies remaining:", len(self.enemies))
        return len(self.enemies) == 0
    
    def give_player_position(self):
        for enemy in self.enemies:
            enemy.player_pos = self.player.get_position()