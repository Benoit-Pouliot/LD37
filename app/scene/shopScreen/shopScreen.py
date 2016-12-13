# Imports
import os
import sys

import pygame

from app.mapData import MapData
from app.sprites.GUI.button import Button
from app.sprites.GUI.HUDShopScreen import HUDShopScreeen
from app.scene.shopScreen.eventHandlerShopScreen import EventHandlerShopScreen
from app.sprites.upgrade.barricadeUp import BarricadeUp
from app.sprites.upgrade.grenadeUpgrade import GrenadeUpgrade
from app.sprites.upgrade.mineUpgrade import MineUpgrade
from app.sprites.upgrade.gun import Gun
from app.sprites.upgrade.barricadeCooldown import BarricadeCooldown
from app.sprites.upgrade.grenadeCooldown import GrenadeCooldown
from app.sprites.upgrade.mineCooldown import MineCooldown
from app.sprites.upgrade.gunCooldown import GunCooldown
from app.scene.shopScreen.logicHandlerShopScreen import LogicHandlerShopScreen
from app.settings import *
from app.scene.drawer import Drawer
from app.scene.musicFactory import MusicFactory


class ShopScreen:
    def __init__(self, screen, gameData=None):
        self.screen = screen

        self.gameData = gameData
        self.shopScreenData = self.gameData.mapData

        self.screen.fill((0, 0, 0))
        titleImage = pygame.image.load(os.path.join('img', 'ShopScreen.png'))
        self.screen.blit(titleImage, (0, 0))

        self.upgradeList = {}

        # We should adjust position.

        self.addUpgrade('gun',(1*SCREEN_WIDTH/10,80))
        self.addUpgrade('barricade',(3*SCREEN_WIDTH/10,80))
        self.addUpgrade('grenade', (5*SCREEN_WIDTH/10, 80))
        self.addUpgrade('mine', (7*SCREEN_WIDTH/10, 80))

        self.addUpgrade('gunCooldown', (1 * SCREEN_WIDTH / 10, SCREEN_HEIGHT/2))

        if self.gameData.upgrade['barricade'][1] > 0:
            self.addUpgrade('barricadeCooldown', (3 * SCREEN_WIDTH / 10, SCREEN_HEIGHT/2))
        if self.gameData.upgrade['grenade'][1] > 0:
            self.addUpgrade('grenadeCooldown', (5 * SCREEN_WIDTH / 10, SCREEN_HEIGHT/2))
        if self.gameData.upgrade['mine'][1] > 0:
            self.addUpgrade('mineCooldown', (7 * SCREEN_WIDTH / 10, SCREEN_HEIGHT/2))


        self.startGameButton = Button((560,510),(150,60),'Fight!',self.nextLevel)
        self.shopScreenData.allSprites.add(self.startGameButton)
        self.shopScreenData.notifySet.add(self.startGameButton)

        self.addHUD()

        self.eventHandler = EventHandlerShopScreen(self.gameData)
        self.logicHandler = LogicHandlerShopScreen(self.screen, self.gameData)
        self.drawer = Drawer()

        # self.type = SHOP_SCREEN
        self.nextScene = None

        self.iconWidth = 100
        self.iconHeight = 100

        self.sold = False

        self.soundPaid = pygame.mixer.Sound(os.path.join('music_pcm', 'paidMoney.wav'))
        self.soundPaid.set_volume(.25)
        self.soundNotEM = pygame.mixer.Sound(os.path.join('music_pcm', 'notEnoughMoney.wav'))
        self.soundNotEM.set_volume(.25)
        self.menuSelect = pygame.mixer.Sound(os.path.join('music_pcm', 'menu_select.wav'))
        self.menuSelect.set_volume(.25)

        MusicFactory(SHOP_SCREEN)


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
        elif name == 'grenade':
             self.upgradeList[name] = GrenadeUpgrade()
             self.upgradeList[name].method = self.buyGrenadeUpgrade
        elif name == 'mine':
             self.upgradeList[name] = MineUpgrade()
             self.upgradeList[name].method = self.buyMineUpgrade
        elif name == 'gunCooldown':
            self.upgradeList[name] = GunCooldown()
            self.upgradeList[name].method = self.buyGunCooldown
        elif name == 'barricadeCooldown':
             self.upgradeList[name] = BarricadeCooldown()
             self.upgradeList[name].method = self.buyBarricadeCooldown
        elif name == 'grenadeCooldown':
             self.upgradeList[name] = GrenadeCooldown()
             self.upgradeList[name].method = self.buyGrenadeCooldown
        elif name == 'mineCooldown':
             self.upgradeList[name] = MineCooldown()
             self.upgradeList[name].method = self.buyMineCooldown

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
            self.gameData.upgrade[item][2] *= 2 #Increase cost
            self.sold = False
            self.recreateButton(self.upgradeList[item])
            self.soundPaid.play()
        else:
            if TAG_MARIE == 1:
                print('Not enough money')
            self.soundNotEM.play()

    def buyGun(self):
        self.pay(self.gameData.upgrade['gun'][2])
        self.buy('gun')

    def buyBarricadeUp(self):
        self.pay(self.gameData.upgrade['barricade'][2])
        self.buy('barricade')

    def buyGrenadeUpgrade(self):
        self.pay(self.gameData.upgrade['grenade'][2])
        self.buy('grenade')

    def buyMineUpgrade(self):
        self.pay(self.gameData.upgrade['mine'][2])
        self.buy('mine')

    def buyGunCooldown(self):
        self.pay(self.gameData.upgrade['gunCooldown'][2])
        if self.sold == True:
            self.gameData.upgrade['gunCooldown'][1] = int(self.gameData.upgrade['gunCooldown'][1] * self.gameData.upgrade['gunCooldown'][3]) #Increase lvl
            self.gameData.upgrade['gunCooldown'][2] *= 2 #Increase cost
            self.sold = False
            self.recreateButton(self.upgradeList['gunCooldown'])
        else:
            self.soundNotEM.play()

    def buyBarricadeCooldown(self):
        self.pay(self.gameData.upgrade['barricadeCooldown'][2])
        if self.sold == True:
            self.gameData.upgrade['barricadeCooldown'][1] = int(self.gameData.upgrade['barricadeCooldown'][1] * self.gameData.upgrade['gunCooldown'][3]) #Increase lvl
            self.gameData.upgrade['barricadeCooldown'][2] *= 2 #Increase cost
            self.sold = False
            self.recreateButton(self.upgradeList['barricadeCooldown'])
        else:
            self.soundNotEM.play()

    def buyGrenadeCooldown(self):
        self.pay(self.gameData.upgrade['grenadeCooldown'][2])
        if self.sold == True:
            self.gameData.upgrade['grenadeCooldown'][1] = int(self.gameData.upgrade['grenadeCooldown'][1] * self.gameData.upgrade['grenadeCooldown'][3]) #Increase lvl
            self.gameData.upgrade['grenadeCooldown'][2] *= 2 #Increase cost
            self.sold = False
            self.recreateButton(self.upgradeList['grenadeCooldown'])
        else:
            self.soundNotEM.play()

    def buyMineCooldown(self):
        self.pay(self.gameData.upgrade['mineCooldown'][2])
        if self.sold == True:
            self.gameData.upgrade['mineCooldown'][1] = int(self.gameData.upgrade['mineCooldown'][1] * self.gameData.upgrade['mineCooldown'][3]) #Increase lvl
            self.gameData.upgrade['mineCooldown'][2] *= 2 #Increase cost
            self.sold = False
            self.recreateButton(self.upgradeList['mineCooldown'])
        else:
            self.soundNotEM.play()

    def recreateButton(self,item):
        item.attribute = self.gameData.upgrade[item.name][1]
        item.cost = self.gameData.upgrade[item.name][2]

    def doNothing(self):
        pass
        # print('You did nothing')

    def nextLevel(self):
        self.menuSelect.play()
        self.sceneRunning = False
        self.nextScene = PLATFORM_SCREEN
        self.gameData.typeScene = PLATFORM_SCREEN
        self.gameData.mapData = MapData("LevelRoom", "StartPointWorld", self.gameData.currentLevel)

    def addHUD(self):
        self.HUD = HUDShopScreeen(self.gameData)
        self.shopScreenData.spritesHUD.add(self.HUD)