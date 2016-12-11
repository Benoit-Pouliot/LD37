import pygame
from app.sprites.collisionMask import CollisionMask
from app.tools.animation import Animation

from app.settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.name = "enemy"
        self.type = "enemy"

        self.imageEnemy = pygame.Surface((1, 1))
        self.imageEnemy.set_alpha(0)
        self.image = self.imageEnemy

        self.frames = [self.imageEnemy]
        self.animation = Animation(self, self.frames, 100)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


        self.isPhysicsApplied = False
        self.isCollisionApplied = False
        self.collisionMask = CollisionMask(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        self.soundDead = None

        self.dictProperties = {}

        self.attackDMG = 0
        self.friendly = False

        self.mapData = None

        self.bounty = 0

    def setMapData(self, mapData):
        self.mapData = mapData

    def update(self):
        self.animation.update(self)
        self.updateCollisionMask()

    def applyAI(self):
        pass

    def updateCollisionMask(self):
        self.collisionMask.rect.x = self.rect.x
        self.collisionMask.rect.y = self.rect.y

    def isHit(self,dmg=0):
        pass

    def dead(self):
        if self.mapData != None:
            self.mapData.gold += self.bounty
            if TAG_MARIE == 1:
                print('Gold : ' + str(self.mapData.gold))

        self.kill()

    def notify(self, event):
        pass

    def attackOnCollision(self):
        pass

