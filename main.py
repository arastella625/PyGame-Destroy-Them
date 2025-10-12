import pygame
from player import Player
from health_bar import HealthBar
from wave_manager import WaveManager

MAIN_PLAYER_START_X = 375
MAIN_PLAYER_START_Y = 275
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800



def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pygame Window")
    clock = pygame.time.Clock()
    player = Player(MAIN_PLAYER_START_X, MAIN_PLAYER_START_Y)
    background_image = pygame.transform.scale(pygame.image.load(r"assets/background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)).convert() 
    health_bar = HealthBar(20, 20, 200, 25, player.health)
    wave_manager = WaveManager(SCREEN_WIDTH, SCREEN_HEIGHT, player, health_bar)

    running = True
    while running:
        # Process player input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                raise SystemExit ("Exiting the game.")                
                
        # Do logical updates here 
        # ....
        if wave_manager.is_wave_cleared():
            wave_manager.spawn_wave()
        player.update()
        wave_manager.update()

        # Render graphics here
        # ....
        screen.fill((0, 0, 0))  # Fill the screen with black
        screen.blit(background_image, (0, 0))
        screen.blit(player.image, player.rect)

        health_bar.draw(screen)
        wave_manager.draw(screen)
        player.draw(screen) 

        pygame.display.flip()   # Update the display
        clock.tick(60)  # Cap the frame rate at 60 FPS  
    pygame.quit()

if __name__ == "__main__":
    main()


