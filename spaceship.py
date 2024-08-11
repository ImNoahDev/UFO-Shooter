# spaceship.py

import pygame
import math
from bullet import Bullet
from constants import WIDTH, HEIGHT, BLACK

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
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = 0
        self.speed = 0
        self.max_speed = 5
        self.acceleration = 0.2
        self.deceleration = 0.05
        self.rotation_speed = 5
        self.bullets = []
        self.lives = 3

    def rotate(self, direction):
        self.angle += self.rotation_speed * direction
        self.angle %= 360

    def thrust(self):
        if self.speed < self.max_speed:
            self.speed += self.acceleration

    def stop_thrust(self):
        if self.speed > 0:
            self.speed -= self.deceleration
        if self.speed < 0:
            self.speed = 0

    def move(self):
        dx = self.speed * math.cos(math.radians(self.angle))
        dy = self.speed * math.sin(math.radians(self.angle))
        self.rect.x += dx
        self.rect.y -= dy
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
        for asteroid in asteroids:
            if self.rect.colliderect(asteroid.rect):
                print("Collision detected between spaceship and asteroid")
                self.lives -= 1
                if self.lives <= 0:
                    print("Game Over")
                return True
        return False
