import pygame


class FieryBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.image.load(r"assets/fiery_bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        self.direction = direction  # Direction should be a tuple (dx, dy)

    def update(self):
        # Update bullet position based on mouse position
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        
        # Remove the bullet if it goes off-screen
        if (self.rect.right < 0 or self.rect.left > pygame.display.get_surface().get_width() or
                self.rect.bottom < 0 or self.rect.top > pygame.display.get_surface().get_height()):
            self.kill()
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)