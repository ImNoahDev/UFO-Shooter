# main.py

import pygame
import sys

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
FPS = 60

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids Shooter")

# Set up the clock
clock = pygame.time.Clock()

def main():
    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        # Drawing
        screen.fill(WHITE)  # Clear screen with white
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

if __name__ == "__main__":
    main()
