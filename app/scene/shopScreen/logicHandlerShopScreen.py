import pygame
from app.settings import *

class LogicHandlerShopScreen:
    def __init__(self,screen,gameData):

        self.sceneRunning = True
        self.screen = screen
        self.gameData = gameData
        self.shopScreenData = gameData.shopScreenData

        self.winningCondition = None

    def handle(self):
        self.checkHighlight()
        self.shopScreenData.allSprites.update()
        self.shopScreenData.spritesHUD.update()

    def checkHighlight(self):
        mousePos = pygame.mouse.get_pos()
        for obj in self.gameData.shopScreenData.notifySet:
            if obj.rect.collidepoint(mousePos):
                obj.isSelected = True
            else:
                obj.isSelected = False
