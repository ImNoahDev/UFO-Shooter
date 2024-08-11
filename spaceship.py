# spaceship.py

import pygame
import math
from bullet import Bullet
from constants import WIDTH, HEIGHT, BLACK
import time

WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FPS = 60
START_ASTEROIDS = 5
LEVEL_INCREASE = 2

class Spaceship:
    def __init__(self, x, y):
        self.image = pygame.image.load('assets/images/spaceship.png')
        self.image = pygame.transform.scale(self.image, (70, 50))
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = 0
        self.speed = 0.3
        self.max_speed = 2
        self.acceleration = 0.2
        self.deceleration = 0.05
        self.rotation_speed = 5
        self.velocity_x = 0
        self.velocity_y = 0
        self.bullets = []
        self.lives = 3
        self.last_collision_time = 0  # Track time of the last collision
        self.collision_cooldown = 1.3  # 1.3 seconds cooldown
        self.game_start_time = time.time()  # Record when the game starts
        self.invincibility_period = 3  # 3 seconds invincibility period
        self.flash_duration = 0.8  # Duration for the red flash
        self.flash_start_time = 0
        self.flash_active = False
        self.knockback_force = 6  # Force to push back when dying

    def rotate(self, angle):
        self.angle += angle * self.rotation_speed
        self.angle %= 360
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def thrust(self):
        radian_angle = math.radians(self.angle)
        self.velocity_x += self.speed * math.cos(radian_angle)
        self.velocity_y += self.speed * math.sin(radian_angle)

    def stop_thrust(self):
        self.velocity_x *= 0.99
        self.velocity_y *= 0.99

    def move(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Screen wrapping logic
        self.rect.x %= WIDTH
        self.rect.y %= HEIGHT

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery, self.angle)
        self.bullets.append(bullet)

    def update(self):
        self.move()
        for bullet in self.bullets:
            if not bullet.update():
                self.bullets.remove(bullet)

    def draw(self, screen):
        # Draw the spaceship with the current angle
        rotated_image = pygame.transform.rotate(self.original_image, -self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)

        # Flash effect
        if self.flash_active:
            current_time = time.time()
            if current_time - self.flash_start_time > self.flash_duration:
                self.flash_active = False
                # Reset to the original image after flash duration
                screen.blit(rotated_image, new_rect.topleft)
            else:
                flash_surface = pygame.Surface(rotated_image.get_size())
                flash_surface.set_alpha(128)  # Semi-transparent
                flash_surface.fill(RED)  # Use the RED color defined above
                screen.blit(rotated_image, new_rect.topleft)
                screen.blit(flash_surface, new_rect.topleft, special_flags=pygame.BLEND_RGBA_ADD)
        else:
            # No flash, just draw the rotated image normally
            screen.blit(rotated_image, new_rect.topleft)

        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(screen)

    def check_collision(self, asteroids):
        current_time = time.time()
        if current_time - self.game_start_time < self.invincibility_period:
            return False

        if current_time - self.last_collision_time < self.collision_cooldown:
            return False

        for asteroid in asteroids:
            if self.rect.colliderect(asteroid.rect):
                if self.lives > 0:
                    self.lives -= 1
                    asteroids.remove(asteroid)
                    print(f"Lives remaining: {self.lives}")
                    self.last_collision_time = current_time
                    self.flash_active = True
                    self.flash_start_time = current_time
                    # Apply knockback
                    radian_angle = math.radians(self.angle)
                    self.velocity_x -= self.knockback_force * math.cos(radian_angle)
                    self.velocity_y += self.knockback_force * math.sin(radian_angle)
                    return True
        return False