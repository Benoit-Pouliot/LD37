# Imports
import os
import sys

import pygame

from app.mapData import MapData
from app.sprites.GUI.button import Button
from app.sprites.GUI.menu.menu import Menu
from app.scene.shopScreen.eventHandlerShopScreen import EventHandlerShopScreen
from app.sprites.upgrade.barricadeUp import BarricadeUp
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

        self.upgradeList = {}

        # We should adjust position.

        self.addUpgrade('gun',(50,50))
        self.addUpgrade('barricade',(250,50))

        self.startGameButton = Button((600,500),(100,80),'Fight!',self.nextLevel)
        self.shopScreenData.allSprites.add(self.startGameButton)
        self.shopScreenData.notifySet.add(self.startGameButton)

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


    def addUpgrade(self,name,pos):
        if name == 'gun':
            self.upgradeList[name] = Gun()
            self.upgradeList[name].method = self.buyGun
        elif name == 'barricade':
             self.upgradeList[name] = BarricadeUp()
             self.upgradeList[name].method = self.buyBarricadeUp

        item = self.upgradeList[name]
        item.attributeName = self.gameData.upgrade[item.name][0]
        item.attribute = self.gameData.upgrade[item.name][1]
        item.cost = self.gameData.upgrade[item.name][2]

        self.shopScreenData.allSprites.add(item)
        self.shopScreenData.notifySet.add(item)

        item.rect.x = pos[0]
        item.rect.y = pos[1]

    def buyGun(self):
        self.gameData.upgrade['gun'][1] += self.gameData.upgrade['gun'][3]
        self.gameData.upgrade['gun'][2] = int(round(self.gameData.upgrade['gun'][4]*self.gameData.upgrade['gun'][2]))
        self.recreateButton(self.upgradeList['gun'])

    def buyBarricadeUp(self):
        print('You bought a barricade')
        self.gameData.upgrade['barricade'][1] += self.gameData.upgrade['barricade'][3]
        self.gameData.upgrade['barricade'][2] = int(round(self.gameData.upgrade['barricade'][4]*self.gameData.upgrade['barricade'][2]))
        self.recreateButton(self.upgradeList['barricade'])

    def recreateButton(self,item):
        item.attribute = self.gameData.upgrade[item.name][1]
        item.cost = self.gameData.upgrade[item.name][2]

    def doNothing(self):
        print('You did nothing')

    def nextLevel(self):
        self.sceneRunning = False
        self.nextScene = PLATFORM_SCREEN
        self.gameData.typeScene = PLATFORM_SCREEN
        self.gameData.mapData = MapData("LevelRoom", "StartPointWorld")