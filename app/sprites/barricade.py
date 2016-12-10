import os
import pygame

from app.sprites.enemy.enemy import Enemy
from app.scene.platformScreen.collisionPlayerPlatform import *
# from app.tool.animation import Animation
from app.tools.animation import Animation
from app.sprites.collisionMask import CollisionMask
from app.sprites.GUI.lifeBar import LifeBar



class Barricade(pygame.sprite.Sprite):
    def __init__(self, centerx, centery,maxHealth = 20):
        super().__init__()

        self.name = "barricade"

        self.imageBarricade = pygame.image.load(os.path.join('img', 'Barricade.png'))
        self.image = self.imageBarricade

        self.frames = [self.imageBarricade]
        self.animation = None

        self.rect = self.image.get_rect()
        self.rect.x = centerx-self.rect.width/2
        self.rect.y = centery-self.rect.width/2

        self.speedx = 0
        self.speedy = 0

        self.isPhysicsApplied = False
        self.isCollisionApplied = True
        self.collisionMask = CollisionMask(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        self.maxHealth = maxHealth

        self.lifeBar = LifeBar(maxHealth)

        self.lifeBar.rect.x = self.rect.x
        self.lifeBar.rect.top = self.rect.bottom +3


    def update(self):
        if self.animation is not None :
           next(self.animation)

    def onCollision(self, collidedWith, sideOfCollision):
        if collidedWith == SOLID:
            self.destroy()

    def destroy(self):
        self.kill()