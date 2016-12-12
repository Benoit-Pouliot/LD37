import pygame
import os

from app.settings import *
from app.sprites.collisionMask import CollisionMask


class Upgrade(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.name = 'name'
        self.method = self.doNothing
        self.attribute = 0
        self.cost = 0

        self.fontSize = 20
        self.upgFont = pygame.font.SysFont(FONT_NAME, self.fontSize)

        self.width = 150
        self.height = 200

        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()

        self.borderButton = 5

        self.interior = pygame.Rect(self.borderButton,self.borderButton,self.width-2*self.borderButton,self.height-2*self.borderButton)


        self.icon = pygame.image.load(os.path.join('img', 'mine1.png'))
        self.iconPos = [0, 0]

        self.attributeName = 'Peanut'
        self.textAttribute = self.attributeName + ' : ' + str(self.attribute)
        self.textAttributePos = [0,0]

        self.textCost = 'Cost : ' + str(self.cost)
        self.textCostPos = [0, 0]

        self.isSelected = False

        # Color
        self.color1 = COLOR_MENU_1
        self.color2 = COLOR_MENU_2

    def doNothing(self):
        pass
        # print('You did nothing')

    def update(self):

        if self.isSelected:
            self.color1 = COLOR_MENU_SELECT_1
            self.color2 = COLOR_MENU_SELECT_2
            self.printedAttribute = self.upgFont.render(self.textAttribute, True, COLOR_MENU_FONTS_SELECT)
            self.printedCost = self.upgFont.render(self.textCost, True, COLOR_MENU_FONTS_SELECT)

        else:
            self.color1 = COLOR_MENU_1
            self.color2 = COLOR_MENU_2
            self.printedAttribute = self.upgFont.render(self.textAttribute, True, COLOR_MENU_FONTS)
            self.printedCost = self.upgFont.render(self.textCost, True, COLOR_MENU_FONTS)

        self.setUpgradeSpec()

        self.image.fill(self.color2)
        self.image.fill(self.color1,self.interior)
        self.image.blit(self.icon, self.iconPos)
        self.image.blit(self.printedAttribute,self.textAttributePos)
        self.image.blit(self.printedCost,self.textCostPos)


    def setUpgradeSpec(self):
        self.textAttribute = self.attributeName + ' : ' + str(self.attribute)
        self.textCost = 'Cost : ' + str(self.cost)

        # Button real space
        self.textAttributePos = [(self.image.get_width()-self.printedAttribute.get_width())/2,self.interior.bottom-3*self.fontSize]
        self.textCostPos = [(self.image.get_width()-self.printedCost.get_width())/2,self.interior.bottom-1.5*self.fontSize]

        self.iconPos = [(self.image.get_width()-self.icon.get_width())/2, (self.image.get_height()*0.6 - self.icon.get_height()) * 0.5]

    def notify(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.method()

    def resizeIcon(self):
        resizeSizeX = 64
        imageSizeY = self.icon.get_height() * resizeSizeX / self.icon.get_width()

        self.icon = pygame.transform.scale(self.icon, (int(resizeSizeX), int(imageSizeY)))