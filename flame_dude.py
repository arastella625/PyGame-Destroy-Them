import pygame
from player import Player


class FlameDude(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(r"assets/flame_dude.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 3
        self.health = 50
        self.player_pos = (0, 0)  # Initialize player position

    def handle_input(self):
        # Move smoothly towards player_pos
        if self.player_pos:
            player_x, player_y = self.player_pos
            if self.rect.x < player_x:
                self.rect.x += self.speed
            elif self.rect.x > player_x:
                self.rect.x -= self.speed
            if self.rect.y < player_y:
                self.rect.y += self.speed
            elif self.rect.y > player_y:
                self.rect.y -= self.speed
        

    def update(self):
        self.handle_input()