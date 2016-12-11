import pygame
from app.sprites.enemy.enemy import Enemy
from app.sprites.collisionMask import CollisionMask
from app.settings import *


class EnemyAttack(Enemy):
    def __init__(self, x, y, size=(1,1), attackDMG=0):
        super().__init__(x,y)

        self.name = "enemyAttack"

        self.image = pygame.Surface(size)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


        self.isPhysicsApplied = False
        self.isCollisionApplied = False
        self.collisionMask = CollisionMask(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        self.soundDead = None

        self.dictProperties = {}

        self.attackDMG = attackDMG
        self.friendly = False

        if TAG_BP == 1:
            self.image.fill(BLACK)


    def setMapData(self, mapData):
        self.mapData = mapData
        self.mapData.camera.add(self)
        self.mapData.allSprites.add(self)
        self.mapData.attackGroup.add(self)

    def update(self):
        # self.animation.update(self)
        self.updateCollisionMask()

    def updateCollisionMask(self):
        self.collisionMask.rect.x = self.rect.x
        self.collisionMask.rect.y = self.rect.y

    def isHit(self):
        pass

    def dead(self):
        self.kill()

    def notify(self, event):
        pass

