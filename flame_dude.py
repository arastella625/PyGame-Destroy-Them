import pygame
from player import Player


class FlameDude(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(r"assets/flame_dude.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 2
        self.health = 50
        self.damage = 10
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
    
    def avoid_overlap(self, others):
        for other in others:
            if other is not self and self.rect.colliderect(other.rect):
                dx = self.rect.x - other.rect.x
                dy = self.rect.y - other.rect.y
                if abs(dx) > abs(dy):
                    self.rect.x += self.speed if dx >= 0 else -self.speed
                else:
                    self.rect.y += self.speed if dy >= 0 else -self.speed

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
        print(f"FlameDude: Took damage of {amount}. Current health: {self.health}")
    
    def give_damage(self):
        return self.damage  # Fixed damage amount for simplicity
    
    def is_dead(self):
        return self.health <= 0
    
    def heal(self, amount):
        self.health += amount
        if self.health > 50:
            self.health = 50
        print(f"FlameDude: Healed by {amount}. Current health: {self.health}")
    
    def get_health(self):
        return self.health
    
    def set_health(self, new_health):
        self.health = max(0, min(50, new_health))
        print(f"FlameDude: Health set to {self.health}")

    def get_position(self):
        return self.rect.topleft
    
    def set_position(self, new_pos):
        self.rect.topleft = new_pos
        print(f"FlameDude: Position set to {self.rect.topleft}")
    
    def get_player_position(self):
        return self.player_pos
    
    def set_player_position(self, new_pos):
        self.player_pos = new_pos
        print(f"FlameDude: Player position set to {self.player_pos}")
    
    def get_distance_to_player(self):
        if self.player_pos:
            player_x, player_y = self.player_pos
            return ((self.rect.x - player_x) ** 2 + (self.rect.y - player_y) ** 2) ** 0.5
        return None
    
    def set_speed(self, new_speed):
        self.speed = new_speed
        print(f"FlameDude: Speed set to {self.speed}")
    
    def get_speed(self):
        return self.speed
    
    def reset(self):
        self.health = 50
        self.player_pos = (0, 0)
        print("FlameDude: Reset to initial state")
    
    def is_near_player(self, threshold):
        distance = self.get_distance_to_player()
        if distance is not None:
            return distance < threshold
        return False
    
    def flee_from_player(self):
        if self.player_pos:
            player_x, player_y = self.player_pos
            if self.rect.x < player_x:
                self.rect.x -= self.speed
            elif self.rect.x > player_x:
                self.rect.x += self.speed
            if self.rect.y < player_y:
                self.rect.y -= self.speed
            elif self.rect.y > player_y:
                self.rect.y += self.speed
            print("FlameDude: Fleeing from player")
    
    def attack_player(self):
        if self.is_near_player(30):  # Arbitrary attack range
            print("FlameDude: Attacking player!")
            # Implement attack logic here

    def stop(self):
        print("FlameDude: Stopping movement")
        # Implement stop logic here
        pass

    def patrol(self, points):
        print("FlameDude: Patrolling between points", points)
        # Implement patrol logic here
        pass

