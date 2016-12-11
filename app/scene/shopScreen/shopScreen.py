# Imports
import os
import sys

import pygame

from app.mapData import MapData
from app.sprites.GUI.button import Button
from app.sprites.GUI.HUDShopScreen import HUDShopScreeen
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

        self.addUpgrade('gun',(50,80))
        self.addUpgrade('barricade',(250,80))

        self.startGameButton = Button((600,500),(100,80),'Fight!',self.nextLevel)
        self.shopScreenData.allSprites.add(self.startGameButton)
        self.shopScreenData.notifySet.add(self.startGameButton)

        self.addHUD()

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
            self.drawer.draw(self.screen, None, self.shopScreenData.spritesHUD, None,self.shopScreenData.allSprites)  # Drawer in THIS file, below


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

    def pay(self,amount):
        if self.gameData.gold >=amount:
            self.sold = True
            self.gameData.gold -= amount

    def buy(self,item):
        if self.sold == True:
            self.gameData.upgrade[item][1] += self.gameData.upgrade[item][3] #Increase lvl
            self.gameData.upgrade[item][2] = int(round(self.gameData.upgrade[item][4]*self.gameData.upgrade[item][2])) #Increase cost
            self.sold = False
            self.recreateButton(self.upgradeList[item])
        else:
            print('Not enough money')

    def buyGun(self):
        self.pay(self.gameData.upgrade['gun'][2])
        self.buy('gun')

    def buyBarricadeUp(self):
        self.pay(self.gameData.upgrade['barricade'][2])
        self.buy('barricade')

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

    def addHUD(self):
        self.HUD = HUDShopScreeen(self.gameData)
        self.shopScreenData.spritesHUD.add(self.HUD)