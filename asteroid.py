# asteroid.py

import pygame
import random

class Asteroid:
    def __init__(self, x, y):
        self.image = pygame.image.load('assets/images/asteroid.png')  # Load your asteroid image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = random.uniform(1, 3)
        self.angle = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-2, 2)

    def update(self):
        dx = self.speed * math.cos(math.radians(self.angle))
        dy = self.speed * math.sin(math.radians(self.angle))
        self.rect.x += dx
        self.rect.y -= dy
        self.angle += self.rotation_speed

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, new_rect.topleft)
