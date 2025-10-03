import pygame
from player import Player

MAIN_PLAYER_START_X = 375
MAIN_PLAYER_START_Y = 275


def main():

    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption("Pygame Window")
    clock = pygame.time.Clock()
    player = Player(MAIN_PLAYER_START_X, MAIN_PLAYER_START_Y)

    running = True
    while running:
        # Process player input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                raise SystemExit ("Exiting the game.")
        # Do logical updates here 
        # ....

        screen.fill((0, 0, 0))  # Fill the screen with black

        # Render graphics here
        # ....
        player.update()
        screen.blit(player.image, player.rect)

        pygame.display.flip()   # Update the display
        clock.tick(60)  # Cap the frame rate at 60 FPS  

    pygame.quit()

if __name__ == "__main__":
    main()