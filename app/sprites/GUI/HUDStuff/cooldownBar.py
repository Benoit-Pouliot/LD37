import pygame
from app.settings import *


class CooldownBar (pygame.sprite.Sprite):
    def __init__(self, statMax, width=32, height=5):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 300

        self.statMax = statMax
        self.statCurrent = statMax
        self.isDisplayed = True

    def update(self):

        self.widthReload = self.width*self.statCurrent/self.statMax
        if self.statCurrent < self.statMax:
            self.image.fill(YELLOW)

            reloadBar = pygame.Rect(0, 0, self.widthReload, self.height)
            pygame.draw.rect(self.image, BLUE, reloadBar)