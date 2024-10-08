import pygame
import sys
import random
from spaceship import Spaceship
from asteroid import Asteroid
from bullet import Bullet
from constants import WIDTH, HEIGHT, WHITE, BLACK, FPS, START_ASTEROIDS, LEVEL_INCREASE

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

def create_asteroids(num_asteroids, spaceship_rect):
    asteroids = []
    min_distance = 100  # Minimum distance from the spaceship
    for _ in range(num_asteroids):
        while True:
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            asteroid_rect = pygame.Rect(x, y, 50, 50)  # Assuming 50x50 size for the asteroid

            # Check if the asteroid is far enough from the spaceship
            if asteroid_rect.colliderect(spaceship_rect.inflate(min_distance, min_distance)):
                continue  # Retry if too close

            asteroid = Asteroid(x, y)
            asteroids.append(asteroid)
            break
    return asteroids

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def game_over_screen(screen, font, score):
    screen.fill((0, 0, 0))
    game_over_text = font.render('Game Over', True, (255, 0, 0))
    score_text = font.render(f'Your Score: {score}', True, (255, 255, 255))
    restart_text = font.render('Press R to Restart or Q to Quit', True, (255, 255, 255))

    game_over_rect = game_over_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    score_rect = score_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    restart_rect = restart_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    screen.blit(restart_text, restart_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def menu_screen(screen, font):
    screen.fill(BLACK)
    title_text = font.render('Asteroids Shooter', True, WHITE)
    start_text = font.render('Press ENTER to Start', True, WHITE)
    quit_text = font.render('Press Q to Quit', True, WHITE)

    title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    start_rect = start_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    quit_rect = quit_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))

    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)
    screen.blit(quit_text, quit_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def game_loop():
    level = 1
    score = 0
    spaceship = Spaceship(WIDTH // 2, HEIGHT // 2)
    asteroids = create_asteroids(START_ASTEROIDS, spaceship.rect)

    paused = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused

        if not paused:
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

            spaceship.update()

            # Update and draw asteroids
            for asteroid in asteroids:
                asteroid.update()

            # Handle bullet collisions with asteroids
            for bullet in spaceship.bullets[:]:
                for asteroid in asteroids[:]:
                    if bullet.rect.colliderect(asteroid.rect):
                        spaceship.bullets.remove(bullet)
                        asteroids.remove(asteroid)
                        score += 10
                        break  # Break out of the asteroid loop after collision

            # Check if the spaceship collides with any asteroids
            if spaceship.check_collision(asteroids):
                if spaceship.lives <= 0:
                    game_over_screen(screen, font, score)
                    return  # Return to main menu after game over

            # Check if all asteroids are cleared
            if not asteroids:
                level += 1
                score += 100
                asteroids = create_asteroids(START_ASTEROIDS + (level - 1) * LEVEL_INCREASE, spaceship.rect)

            screen.fill(WHITE)
            spaceship.draw(screen)
            
            for asteroid in asteroids:
                asteroid.draw(screen)

            # Draw bullets and remove off-screen bullets
            spaceship.bullets = [bullet for bullet in spaceship.bullets if bullet.update()]
            for bullet in spaceship.bullets:
                bullet.draw(screen)

            draw_text(f"Score: {score}", font, BLACK, screen, 100, 20)
            draw_text(f"Lives: {spaceship.lives}", font, BLACK, screen, WIDTH - 100, 20)
            draw_text(f"Level: {level}", font, BLACK, screen, WIDTH // 2, 20)

            pygame.display.flip()
            clock.tick(FPS)

        else:
            # Display pause screen
            screen.fill(BLACK)
            pause_text = font.render('Paused', True, WHITE)
            resume_text = font.render('Press ESC to Resume', True, WHITE)
            quit_text = font.render('Press Q to Quit', True, WHITE)

            pause_rect = pause_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
            resume_rect = resume_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            quit_rect = quit_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))

            screen.blit(pause_text, pause_rect)
            screen.blit(resume_text, resume_rect)
            screen.blit(quit_text, quit_rect)

            pygame.display.flip()

            while paused:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            paused = False
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()

def main():
    while True:
        menu_screen(screen, font)
        game_loop()

if __name__ == "__main__":
    main()
