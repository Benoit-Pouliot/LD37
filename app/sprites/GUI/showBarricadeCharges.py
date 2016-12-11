from app.settings import *
import pygame
import os

class ShowBarricadeCharges(pygame.sprite.Sprite):
    def __init__(self,mapData, fontSize=18):
        super().__init__()

        self.image= pygame.Surface((48, 48))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH - self.rect.width
        self.rect.y = 0
        self.mapData = mapData

        self.hudFont = pygame.font.SysFont(MENU_FONT, fontSize)
        self.chargesCurrent = mapData.player.barricadeCharges
        self.chargesRenderedValue = self.chargesCurrent
        self.chargesMax = mapData.player.barricadeChargesMax
        self.text = str(self.chargesCurrent) + " / " + str(self.chargesMax)
        self.printedText = self.hudFont.render(self.text, True, HUD_FONT_COLOR)
        self.textPos = [10, 10]
        self.image.blit(self.printedText, self.textPos)

    def update(self):
        if self.chargesCurrent != self.mapData.player.barricadeCharges:
            self.text = str(self.mapData.player.barricadeCharges) + " / " + str(self.chargesMax)
            self.printedText = self.hudFont.render(self.text, True, HUD_FONT_COLOR)
            self.image.fill(BLACK)
            self.image.blit(self.printedText, self.textPos)
            self.chargesCurrent = self.mapData.player.barricadeCharges

