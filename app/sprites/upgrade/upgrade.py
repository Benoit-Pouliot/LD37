import pygame
import os

from app.settings import *
from app.sprites.collisionMask import CollisionMask


class Upgrade(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.name = 'name'
        self.method = self.doNothing
        self.level = 0

        self.upgFont = pygame.font.SysFont(FONT_NAME, 24)

        self.width = 150
        self.height = 200

        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()

        self.borderButton = 10

        self.interior = pygame.Rect(self.borderButton,self.borderButton,self.width-2*self.borderButton,self.height-2*self.borderButton)


        self.icon = pygame.image.load(os.path.join('img', 'biere1.png'))
        self.iconPos = [0, 0]

        self.textLevel = 'Level ' + str(self.level)
        self.textPos = [0,0]

        self.isSelected = False

    def doNothing(self):
        print('You did nothing')

    def update(self):
        if self.isSelected:
            self.color1 = COLOR_MENU_SELECT_1
            self.color2 = COLOR_MENU_SELECT_2
            self.printedName = self.upgFont.render(self.textLevel, True, COLOR_MENU_FONTS_SELECT)
        else:
            self.color1 = COLOR_MENU_1
            self.color2 = COLOR_MENU_2
            self.printedName = self.upgFont.render(self.textLevel, True, COLOR_MENU_FONTS)

        self.image.fill(self.color2)
        self.image.fill(self.color1,self.interior)
        self.image.blit(self.icon, self.iconPos)
        self.image.blit(self.printedName,self.textPos)
        self.setUpgradeSpec()


    def setUpgradeSpec(self):
        # Button real space
        self.textPos = [(self.image.get_width()-self.printedName.get_width())/2,self.image.get_height()*0.6]

        self.iconPos = [(self.image.get_width()-self.icon.get_width())/2, (self.image.get_height()*0.6 - self.icon.get_height()) * 0.5]

    def notify(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.method()