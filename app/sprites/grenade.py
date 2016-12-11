__author__ = 'Bobsleigh'

import pygame, os
from app.sprites.collisionMask import CollisionMask
from app.sprites.explosion import Explosion
from app.settings import *
from app.tools.cooldown import Cooldown

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
        self.friction = 0.4

        self.initialSpeed = 20
        self.speedx = speedx
        self.speedy = speedy

        self.isPhysicsApplied = False
        self.isCollisionApplied = True
        self.collisionMask = CollisionMask(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        self.mapData = mapData

        self.detonationTimer = Cooldown(60)
        self.detonationTimer.start()

    def update(self):
        self.applyFriction()

        self.x += self.speedx
        self.y += self.speedy

        self.rect.x = self.x
        self.rect.y = self.y

        self.detonationTimer.update()

        if self.detonationTimer.isZero:
            self.detonate()

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

    def detonate(self):
        explosion = Explosion(self.rect.midbottom[0], self.rect.midbottom[1])

        self.mapData.camera.add(explosion)
        self.mapData.allSprites.add(explosion)
        self.mapData.friendlyExplosion.add(explosion)

        self.kill()

    def onCollision(self, collidedWith, sideOfCollision,objectSize=0):
        if collidedWith == SOLID:
            if sideOfCollision == RIGHT:
                # On colle la sprite sur le mur à droite
                self.speedx = 0
                self.collisionMask.rect.right += self.mapData.tmxData.tilewidth - (
                self.collisionMask.rect.right % self.mapData.tmxData.tilewidth) - 1
            elif sideOfCollision == LEFT:
                self.speedx = 0
                self.collisionMask.rect.left -= (
                self.collisionMask.rect.left % self.mapData.tmxData.tilewidth)  # On colle la sprite sur le mur à gauche
            elif sideOfCollision == DOWN:
                self.speedy = 0

            elif sideOfCollision == UP:
                # Coller le player sur le plafond
                while self.mapData.tmxData.get_tile_gid(
                                (self.collisionMask.rect.left + 1) / self.mapData.tmxData.tilewidth,
                                (self.collisionMask.rect.top) / self.mapData.tmxData.tileheight,
                                COLLISION_LAYER) != SOLID and self.mapData.tmxData.get_tile_gid(
                            self.collisionMask.rect.right / self.mapData.tmxData.tilewidth,
                            (self.collisionMask.rect.top) / self.mapData.tmxData.tileheight, COLLISION_LAYER) != SOLID:
                    self.collisionMask.rect.bottom -= 1
                self.collisionMask.rect.bottom += 1  # Redescendre de 1 pour sortir du plafond
                self.speedy = 0
