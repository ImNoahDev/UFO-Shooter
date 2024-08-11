# bullet.py

import pygame
import math

class Bullet:
    def __init__(self, x, y, angle):
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle
        self.speed = 10

    def update(self):
        dx = self.speed * math.cos(math.radians(self.angle))
        dy = self.speed * math.sin(math.radians(self.angle))
        self.rect.x += dx
        self.rect.y -= dy

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, new_rect.topleft)
