# asteroid.py

import pygame
import random
import math

# constants.py

WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
START_ASTEROIDS = 5
LEVEL_INCREASE = 2

class Asteroid:
    def __init__(self, x, y):
        self.image = pygame.image.load('assets/images/asteroid.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 2
        self.angle = random.uniform(0, 360)
        self.dx = self.speed * math.cos(math.radians(self.angle))
        self.dy = self.speed * math.sin(math.radians(self.angle))

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.x < 0 or self.rect.x > WIDTH:
            self.dx = -self.dx
        if self.rect.y < 0 or self.rect.y > HEIGHT:
            self.dy = -self.dy

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
