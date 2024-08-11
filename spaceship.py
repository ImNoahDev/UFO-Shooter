# spaceship.py

import pygame
import math

class Spaceship:
    def __init__(self, x, y):
        self.image = pygame.image.load('assets/images/spaceship.png')  # Load your spaceship image
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = 0
        self.speed = 5
        self.rotation_speed = 5
        self.bullets = []

    def rotate(self, direction):
        self.angle += self.rotation_speed * direction
        self.image = pygame.transform.rotate(pygame.image.load('assets/images/spaceship.png'), self.angle)

    def move(self):
        dx = self.speed * math.cos(math.radians(self.angle))
        dy = self.speed * math.sin(math.radians(self.angle))
        self.rect.x += dx
        self.rect.y -= dy

    def shoot(self):
        # Create a new Bullet instance
        bullet = Bullet(self.rect.centerx, self.rect.centery, self.angle)
        self.bullets.append(bullet)

    def update(self):
        self.move()
        for bullet in self.bullets:
            bullet.update()

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, new_rect.topleft)
        for bullet in self.bullets:
            bullet.draw(screen)
