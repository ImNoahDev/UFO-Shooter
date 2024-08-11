# bullet.py

import pygame
import math
from constants import WIDTH, HEIGHT

class Bullet:
    def __init__(self, x, y, angle):
        self.image = pygame.image.load('assets/images/bullet.png')
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle
        self.speed = 10
        # Invert the angle calculation if necessary
        self.dx = self.speed * math.cos(math.radians(-self.angle))
        self.dy = self.speed * math.sin(math.radians(-self.angle))

    def update(self):
        self.rect.x += self.dx
        self.rect.y -= self.dy

        # Check if the bullet is off-screen
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            return False
        return True

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.original_image, -self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, new_rect.topleft)