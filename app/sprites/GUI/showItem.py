from app.settings import *
import pygame
import os

class ShowItem(pygame.sprite.Sprite):
    def __init__(self,fontSize=18):
        super().__init__()

        self.image= pygame.Surface([150, 48])
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        self.hudFont = pygame.font.SysFont(MENU_FONT, fontSize)
        self.weapon = 'None'
        self.text = 'Weapon : ' +self.weapon
        self.number = 12
        self.printedText = self.hudFont.render(self.text, True, HUD_FONT_COLOR)
        self.textPos = [10, 10]
        self.image.blit(self.printedText, self.textPos)

    def update(self):
        self.text = 'Weapon : ' + self.weapon
        self.image = pygame.Surface([150, 48])
        self.printedText = self.hudFont.render(self.text, True, HUD_FONT_COLOR)
        self.image.blit(self.printedText, self.textPos)
