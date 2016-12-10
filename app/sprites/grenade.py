__author__ = 'Bobsleigh'

import pygame, os
from app.sprites.collisionMask import CollisionMask

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speedy, mapData):
        super().__init__()

        self.name = "Grenade"

        self.image = pygame.image.load(os.path.join('img', 'Bullet.png'))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.initialSpeed = 20
        self.speedx = speedx
        self.speedy = speedy

        self.isPhysicsApplied = False
        self.isCollisionApplied = False
        self.collisionMask = CollisionMask(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        self.mapData = mapData

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy