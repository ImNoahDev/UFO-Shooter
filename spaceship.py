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
        self.collision_cooldown = 1.3  # 2 seconds cooldown

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
            bullet.update()

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.original_image, -self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, new_rect.topleft)
        for bullet in self.bullets:
            bullet.draw(screen)

    def check_collision(self, asteroids):
        current_time = time.time()
        if current_time - self.last_collision_time < self.collision_cooldown:
            return False  # Not enough time has passed since last collision

        for asteroid in asteroids:
            if self.rect.colliderect(asteroid.rect):
                # Handle collision: Reduce lives and remove the asteroid
                self.lives -= 1
                asteroids.remove(asteroid)
                print(f"Lives remaining: {self.lives}")  # Debugging output
                self.last_collision_time = current_time  # Update the last collision time
                return True  # Collision occurred

        return False  # No collision