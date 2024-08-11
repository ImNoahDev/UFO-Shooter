# main.py

import pygame
import sys
import random
from spaceship import Spaceship
from asteroid import Asteroid
from bullet import Bullet
from constants import WIDTH, HEIGHT, WHITE, BLACK, FPS, START_ASTEROIDS, LEVEL_INCREASE
import math

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids Shooter")

# Set up the clock
clock = pygame.time.Clock()

# Load sounds
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound('assets/sounds/shoot.wav')
explosion_sound = pygame.mixer.Sound('assets/sounds/explosion.wav')

# Load font
font = pygame.font.SysFont('Arial', 24)

# main.py
def create_asteroids(num_asteroids):
    asteroids = [Asteroid(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(num_asteroids)]
    print(f"Created {len(asteroids)} asteroids")
    return asteroids

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)
def main():
    level = 1
    score = 0
    spaceship = Spaceship(WIDTH // 2, HEIGHT // 2)
    asteroids = create_asteroids(START_ASTEROIDS)

    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Key Presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            spaceship.rotate(-1)
        if keys[pygame.K_RIGHT]:
            spaceship.rotate(1)
        if keys[pygame.K_UP]:
            spaceship.thrust()
        else:
            spaceship.stop_thrust()
        if keys[pygame.K_SPACE]:
            if not spaceship.bullets or spaceship.bullets[-1].rect.bottom < 0:
                spaceship.shoot()
                shoot_sound.play()

        # Update game objects
        spaceship.update()
        for asteroid in asteroids:
            asteroid.update()

        # Check collisions
        if spaceship.check_collision(asteroids):
            if spaceship.lives <= 0:
                game_over_screen(screen, font, score)
                running = False
                continue

        # Check if all asteroids are cleared
        if not asteroids:
            level += 1
            score += 100
            asteroids = create_asteroids(START_ASTEROIDS + (level - 1) * LEVEL_INCREASE)

        # Drawing
        screen.fill(WHITE)
        spaceship.draw(screen)
        for asteroid in asteroids:
            asteroid.draw(screen)

        # Draw UI elements
        draw_text(f"Score: {score}", font, BLACK, screen, 100, 20)
        draw_text(f"Lives: {spaceship.lives}", font, BLACK, screen, WIDTH - 100, 20)
        draw_text(f"Level: {level}", font, BLACK, screen, WIDTH // 2, 20)
        
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

if __name__ == "__main__":
    main()
