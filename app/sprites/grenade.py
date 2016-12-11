import pygame, os, math
from app.sprites.collisionMask import CollisionMask
from app.sprites.explosion import Explosion
from app.settings import *
from app.tools.cooldown import Cooldown
from app.tools.animation import Animation

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speedy, mapData):
        super().__init__()

        self.name = "Grenade"

        self.grenadeFrames = [pygame.image.load(os.path.join('img', 'grenade.png'))]
        self.image = self.grenadeFrames[0]
        for k in range(1, 8):
            self.grenadeFrames.append(pygame.transform.rotate(self.grenadeFrames[k-1], k*30))
        self.animation = Animation(self, self.grenadeFrames, 6)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.friction = 0.3

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

        if self.speedx**2+self.speedy**2 >= .1:
            self.animation.update(self)

        self.detonationTimer.update()

        if self.detonationTimer.isZero:
            self.detonate()

    def applyFriction(self):
        initialNorm = math.sqrt(self.speedx**2 + self.speedy**2)
        finalNorm = initialNorm - self.friction

        self.speedx = self.speedx * (finalNorm/(initialNorm+EPS))
        self.speedy = self.speedy * (finalNorm/(initialNorm+EPS))

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
