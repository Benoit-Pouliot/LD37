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
        self.shopScreenData.allSprites.update()
