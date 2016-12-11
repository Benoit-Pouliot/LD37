# Imports
import os
import sys

import pygame


from app.sprites.GUI.button import Button
from app.sprites.GUI.menu.menu import Menu
from app.scene.shopScreen.eventHandlerShopScreen import EventHandlerShopScreen
from app.sprites.upgrade.gun import Gun
from app.scene.shopScreen.logicHandlerShopScreen import LogicHandlerShopScreen
from app.settings import *
from app.scene.drawer import Drawer


class ShopScreen:
    def __init__(self, screen, gameData=None):
        self.screen = screen

        self.gameData = gameData
        self.shopScreenData = self.gameData.shopScreenData

        self.screen.fill((0, 0, 0))
        titleImage = pygame.image.load(os.path.join('img', 'menu.png'))
        self.screen.blit(titleImage, (0, 0))

        self.addUpgrade((50,200))

        self.eventHandler = EventHandlerShopScreen(self.gameData)
        self.logicHandler = LogicHandlerShopScreen(self.screen, self.gameData)
        self.drawer = Drawer()

        self.type = TITLE_SCREEN
        self.nextScene = None

        self.iconWidth = 100
        self.iconHeight = 100

    def mainLoop(self):
        self.sceneRunning = True
        while self.sceneRunning:
            self.eventHandler.eventHandle()
            self.logicHandler.handle()
            self.drawer.draw(self.screen, None, self.shopScreenData.allSprites, None)  # Drawer in THIS file, below


    def addUpgrade(self,pos):
        item = Gun()
        item.method = self.buyGun
        self.shopScreenData.allSprites.add(item)
        self.shopScreenData.notifySet.add(item)

        item.rect.x = pos[0]
        item.rect.y = pos[0]


    def buyGun(self):
        print('You bought a gun')

    def doNothing(self):
        print('You did nothing')