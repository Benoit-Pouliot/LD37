__author__ = 'Bobsleigh'
import pygame
from app.settings import *

class PlayerLifeBar(pygame.sprite.Sprite):
    def __init__(self, healthMax,width=150,height=16):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10

        self.healthMax = healthMax
        self.healthCurrent = healthMax
        self.isDisplayed = True

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
        if dmg > 0:
            dmgBar = pygame.Rect(0, 0, self.width*(dmg)/self.healthMax, self.heights)
            pygame.draw.rect(self.image, RED, dmgBar)