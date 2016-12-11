__author__ = 'Bobsleigh'


import pygame, os
from app.sprites.collisionMask import CollisionMask
from app.sprites.explosion import Explosion
from app.settings import *
from app.tools.cooldown import Cooldown

class Mine(pygame.sprite.Sprite):
    def __init__(self, x, y, mapData):
        super().__init__()

        self.name = "Mine"

        self.image = pygame.image.load(os.path.join('img', 'Bullet.png'))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.isPhysicsApplied = False
        self.isCollisionApplied = False
        self.collisionMask = CollisionMask(self.rect.x, self.rect.y, self.rect.width*1.2, self.rect.height*1.2)

        self.mapData = mapData
        self.armCooldown = Cooldown(100)
        self.armCooldown.start()

    def update(self):
        self.armCooldown.update()

    def detonate(self):
        if self.armCooldown.isZero:
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
