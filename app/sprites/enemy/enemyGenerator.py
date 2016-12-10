import pygame
from app.sprites.collisionMask import CollisionMask

class EnemyGenerator(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.name = "enemyGenerator"

        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.mapData = None

        self.isPhysicsApplied = False
        self.isFrictionApplied = False
        self.isCollisionApplied = False
        self.collisionMask = CollisionMask(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        self.soundDead = None

        self.dictProperties = {}

    def setMapData(self, mapData):
        self.mapData = mapData

    def update(self):
        pass

    def isHit(self):
        pass

    def dead(self):
        self.kill()

