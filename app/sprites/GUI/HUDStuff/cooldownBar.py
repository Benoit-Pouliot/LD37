import pygame
from app.settings import *
from app.tools.imageBox import rectSurface


class CooldownBar (pygame.sprite.Sprite):
    def __init__(self, statMax, width=32, height=5):
        super().__init__()
        self.width = width
        self.height = height
        self.sizeBorder = 1
        self.image = rectSurface((self.width, self.height), BLUE, self.sizeBorder)

        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 300

        self.statMax = statMax
        self.statCurrent = statMax
        self.isDisplayed = True

    def update(self):

        self.widthReload = (self.width-2*self.sizeBorder)*self.statCurrent/self.statMax
        if self.statCurrent < self.statMax:
            self.image = rectSurface((self.width, self.height), YELLOW, self.sizeBorder)

            reloadBar = pygame.Rect(self.sizeBorder, self.sizeBorder, self.widthReload, self.height-2*self.sizeBorder)
            pygame.draw.rect(self.image, BLUE, reloadBar)
        else:
            self.image = rectSurface((self.width, self.height), BLUE, self.sizeBorder)