import pygame
from app.sprites.collisionMask import CollisionMask
from app.tools.animation import Animation


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.name = "enemy"

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

    def setMapData(self, mapData):
        self.mapData = mapData

    def update(self):
        self.animation.update(self)
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

    def prepareAttack(self):
        pass

