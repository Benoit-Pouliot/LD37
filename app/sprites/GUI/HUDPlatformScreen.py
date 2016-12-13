import pygame
import os
from app.settings import *
from app.sprites.GUI.HUDStuff.statDisplay import StatDisplay
from app.sprites.GUI.lifeBar import LifeBar
from app.sprites.GUI.HUDStuff.cooldownBar import CooldownBar


class HUDPlatformScreen(pygame.sprite.Sprite):
    def __init__(self,gameData=None,player=None):
        super().__init__()

        self.gameData = gameData

        self.player = player

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
        self.HUDFont = pygame.font.SysFont(FONT_NAME, self.fontSize)

        # self.showItem = StatDisplay(self.image, (5, 5), self.HUDFont, 'Item')
        self.barricadeCharges = StatDisplay(self.image, (5, 5), self.HUDFont, 'Barricades')

        self.cooldownBarricades = CooldownBar(self.player.barricadeCooldown.max, width=SCREEN_WIDTH / 10,
                                              height=HUD_HEIGHT / 2)
        self.cooldownBarricades.rect.x = 30 * (SCREEN_WIDTH - self.cooldownBarricades.width) / 100
        self.cooldownBarricades.rect.y = 5

        self.lifeBar = LifeBar(self.player.maxHealth,width=SCREEN_WIDTH/5,height=HUD_HEIGHT/2)
        self.lifeBar.rect.x = (SCREEN_WIDTH-self.lifeBar.width)/2
        self.lifeBar.rect.y = 5

        self.goldAmount = StatDisplay(self.image, (SCREEN_WIDTH * 0.85, 5), self.HUDFont, 'Gold')


    def update(self):
        self.image.fill(self.color2)
        self.image.fill(self.color1, self.interior)

        self.updateGoldAmount()
        # self.updateShowItem()

        if self.gameData.upgrade['barricade'][1]>0:
            self.updateBarricadeCharges()
            self.updateCooldownBarricades()
        self.updateLifeBar()

    def updateGoldAmount(self):
        self.goldAmount.stat = str(self.gameData.mapData.gold)
        self.goldAmount.printText()

    def updateShowItem(self):
        self.showItem.stat = str(self.player.inventory.itemList[self.player.currentItem].name)
        self.showItem.printText()

    def updateBarricadeCharges(self):
        self.barricadeCharges.stat2 = self.player.barricadeChargesMax
        self.barricadeCharges.stat = str(self.player.barricadeCharges) + ' out of ' + str(self.barricadeCharges.stat2)
        self.barricadeCharges.printText()

    def updateLifeBar(self):
        self.lifeBar.healthCurrent = self.player.lifeBar.healthCurrent
        self.lifeBar.update()
        self.image.blit(self.lifeBar.image, (self.lifeBar.rect.x, self.lifeBar.rect.y))

    def updateCooldownBarricades(self):
        self.cooldownBarricades.statCurrent = self.player.barricadeCooldown.max-self.player.barricadeCooldown.value
        self.cooldownBarricades.update()
        self.image.blit(self.cooldownBarricades.image, (self.cooldownBarricades.rect.x, self.cooldownBarricades.rect.y))