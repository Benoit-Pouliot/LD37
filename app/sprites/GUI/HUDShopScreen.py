import pygame
import os
from app.settings import *


class HUDShopScreeen(pygame.sprite.Sprite):
    def __init__(self,gameData=None):
        super().__init__()

        self.gameData=gameData

        self.fontSize = HUD_FONT_SIZE
        self.HUDfont = pygame.font.SysFont(FONT_NAME, self.fontSize)

        self.image = pygame.Surface((SCREEN_WIDTH, HUD_HEIGHT))
        self.rect = self.image.get_rect()

        self.rect.x = 0
        self.rect.y = 0

        self.borderHUD = 5

        self.interior = pygame.Rect(0, 0, self.rect.width,
                                    self.rect.height -  self.borderHUD)
        self.color1 = HUD_COLOR_1
        self.color2 = HUD_COLOR_2

        self.fontSize = HUD_FONT_SIZE
        self.HUDfont = pygame.font.SysFont(FONT_NAME, self.fontSize)
        self.goldText = 'Gold : ' + str(self.gameData.gold)
        self.printedGold = self.HUDfont.render(self.goldText, True, (0, 0, 0))
        self.textGoldPos = (SCREEN_WIDTH * 0.8, 10)
        self.image.blit(self.printedGold, self.textGoldPos)

    def update(self):
        self.image.fill(self.color2)
        self.image.fill(self.color1, self.interior)

        self.updateGold()

    def updateGold(self):
        self.goldText = 'Gold : ' + str(self.gameData.gold)
        self.printedGold = self.HUDfont.render(self.goldText, True, (0, 0, 0))
        self.image.blit(self.printedGold, self.textGoldPos)