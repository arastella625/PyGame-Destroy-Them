import pygame
from player import Player
from health_bar import HealthBar

MAIN_PLAYER_START_X = 375
MAIN_PLAYER_START_Y = 275
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800


def handle_player_damage(health_bar, amount):
    health_bar.take_damage(amount)
    if health_bar.is_dead():
        print("Player has died!")
        # Handle player death (e.g., end game, respawn, etc.)

def handle_key_input(health_bar, event, damage_amount, heal_amount):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_d:  # Press 'D' to take damage
            handle_player_damage(health_bar, damage_amount)
        elif event.key == pygame.K_h:  # Press 'H' to heal
            health_bar.heal(heal_amount)

def main():

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pygame Window")
    clock = pygame.time.Clock()
    player = Player(MAIN_PLAYER_START_X, MAIN_PLAYER_START_Y)
    background_image = pygame.transform.scale(pygame.image.load(r"assets/background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
    health_bar = HealthBar(20, 20, 200, 25, player.health)



    running = True
    damage_amount = 10
    heal_amount = 5

    while running:
        # Process player input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                raise SystemExit ("Exiting the game.")
            elif event.type == pygame.KEYDOWN:
                handle_key_input(health_bar, event, damage_amount, heal_amount)
        # Do logical updates here 
        # ....
        player.update()
        handle_player_damage(health_bar, 0)  # Just to check if dead

        screen.fill((0, 0, 0))  # Fill the screen with black

        # Render graphics here
        # ....
        screen.blit(background_image, (0, 0))
        screen.blit(player.image, player.rect)

        health_bar.draw(screen)

        pygame.display.flip()   # Update the display
        clock.tick(60)  # Cap the frame rate at 60 FPS  

    pygame.quit()

if __name__ == "__main__":
    main()

