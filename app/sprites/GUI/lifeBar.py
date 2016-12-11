import pygame
from app.settings import *
from app.tools.imageBox import rectSurface


class LifeBar (pygame.sprite.Sprite):
    def __init__(self, healthMax, width=32, height=5):
        super().__init__()
        self.width = width
        self.height = height
        # self.image = pygame.Surface([self.width, self.height])
        # self.image.fill(GREEN)
        self.sizeBorder = 1
        self.image = rectSurface((self.width, self.height), GREEN, self.sizeBorder)

        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 300

        self.healthMax = healthMax
        self.healthCurrent = healthMax
        self.isDisplayed = True

        self.isPhysicsApplied = False
        self.isCollisionApplied = False

    def subtract(self, amount):
        self.healthCurrent -= amount
        if self.healthCurrent < 0:
            self.healthCurrent = 0
        self.update()

    def add(self, amount):
        self.healthCurrent += amount
        if self.healthCurrent > self.healthMax:
            self.healthCurrent = self.healthMax

    def update(self):
        dmg = self.healthMax-self.healthCurrent
        self.widthRed = int((self.width-2*self.sizeBorder)*(dmg)/self.healthMax)
        if dmg > 0:
            dmgBar = pygame.Rect((self.width-2*self.sizeBorder)-self.widthRed+self.sizeBorder,
                                 self.sizeBorder,
                                 self.widthRed,
                                 self.height-2*self.sizeBorder)
            pygame.draw.rect(self.image, RED, dmgBar)
