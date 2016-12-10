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
        self.x = x
        self.y = y
        self.friction = 0.01

        self.initialSpeed = 20
        self.speedx = speedx
        self.speedy = speedy

        self.isPhysicsApplied = False
        self.isCollisionApplied = False
        self.isFrictionApplied = True
        self.collisionMask = CollisionMask(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        self.mapData = mapData

    def update(self):
        self.applyFriction()

        self.x += self.speedx
        self.y += self.speedy

        self.rect.x = self.x
        self.rect.y = self.y

    def applyFriction(self):
        if self.speedx > 0 and self.speedx - self.friction > 0:
            self.speedx -= self.friction
        elif self.speedx > 0:
            self.speedx = 0

        if self.speedx < 0 and self.speedx + self.friction < 0:
            self.speedx += self.friction
        elif self.speedx < 0:
            self.speedx = 0

        if self.speedy > 0 and self.speedy - self.friction > 0:
            self.speedy -= self.friction
        elif self.speedy > 0:
            self.speedy = 0

        if self.speedy < 0 and self.speedy + self.friction < 0:
            self.speedy += self.friction
        elif self.speedy < 0:
            self.speedy = 0