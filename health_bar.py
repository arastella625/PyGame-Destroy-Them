import pygame

class HealthBar():
    def __init__(self, x, y, width, height, max_health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_health
        self.current_health = max_health
        self.background_image = pygame.transform.scale(pygame.image.load(r"assets/health_bar_bg.png").convert_alpha(), (width, height))
        self.health_bar_image = pygame.transform.scale(pygame.image.load(r"assets/health_bar.png").convert(), (width, height))
        self.health_bar_border_image = pygame.transform.scale(pygame.image.load(r"assets/health_bar_border.png").convert_alpha(), (width, height))

    def update(self, new_health):
        self.current_health = max(0, min(self.max_health, new_health))

    def draw(self, surface):
        # Draw background and border
        surface.blit(self.background_image, (self.x, self.y))
        surface.blit(self.health_bar_border_image, (self.x, self.y))

        if self.current_health < self.max_health:
            self.health_bar_image = pygame.transform.scale(self.health_bar_image, (int(self.width * (self.current_health / self.max_health)), self.height))
            surface.blit(self.health_bar_image, (self.x, self.y))
            
        else:
            surface.blit(self.health_bar_image, (self.x, self.y))

    def take_damage(self, amount):
        print(f"HealthBar: Taking damage of {amount}. Current health: {self.current_health}")
        self.update(self.current_health - amount)

    def heal(self, amount):
        self.update(self.current_health + amount)

    def is_dead(self):
        return self.current_health <= 0
  