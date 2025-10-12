import pygame
from fiery_bullet import FieryBullet

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(r"assets//player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5
        self.health = 10000
        self.bullets = pygame.sprite.Group()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT or keys[pygame.K_d]]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_SPACE]:
            print("Player: Shoot!")
            self.shoot()


    def update(self):
        self.handle_input()
        self.bullets.update()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.bullets.draw(surface)

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
        print(f"Player: Took damage of {amount}. Current health: {self.health}")
    
    def shoot(self):
        print("Player: Shooting a fiery bullet!")
        mouse_x, mouse_y = self.get_mouse_position()
        direction = (mouse_x - self.rect.centerx, mouse_y - self.rect.centery)
        length = (direction[0]**2 + direction[1]**2) ** 0.5
        if length != 0:
            direction = (direction[0]/length, direction[1]/length)
        bullet = FieryBullet(self.rect.centerx, self.rect.top, direction)
        self.bullets.add(bullet)

    def get_mouse_position(self):
        return pygame.mouse.get_pos()
    
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