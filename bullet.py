# bullet.py

import pygame
import math
from constants import WIDTH, HEIGHT

class Bullet:
    def __init__(self, x, y, angle):
        self.image = pygame.image.load('assets/images/bullet.png')
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle
        self.speed = 10
        self.dx = self.speed * math.cos(math.radians(self.angle))
        self.dy = -self.speed * math.sin(math.radians(self.angle))

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if (self.rect.x < 0 or self.rect.x > WIDTH or
            self.rect.y < 0 or self.rect.y > HEIGHT):
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def check_collision(self, asteroids):
        for asteroid in asteroids:
            if self.rect.colliderect(asteroid.rect):
                return asteroid
        return None

    def kill(self):
        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, new_rect.topleft)
        pass
