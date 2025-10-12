import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(r"assets//player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5
        self.health = 100

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    def update(self):
        self.handle_input()

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
        print(f"Player: Took damage of {amount}. Current health: {self.health}")
    
    def is_dead(self):
        return self.health <= 0
    
    def heal(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100
        print(f"Player: Healed by {amount}. Current health: {self.health}")
    
    def get_health(self):
        return self.health
    
    def set_health(self, new_health):
        self.health = max(0, min(100, new_health))
        print(f"Player: Health set to {self.health}")
    
    def get_position(self):
        return self.rect.topleft