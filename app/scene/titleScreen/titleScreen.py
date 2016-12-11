# Imports
import os
import sys

import pygame

from app.sprites.GUI.button import Button
from app.scene.titleScreen.eventHandlerTitleScreen import EventHandlerTitleScreen
from app.mapData import MapData
from app.settings import *
from app.scene.musicFactory import MusicFactory
from app.scene.drawer import Drawer

from app.shopScreenData import ShopScreenData
import weakref


class TitleScreen:
    def __init__(self, screen, gameData=None):
        self.screen = screen

        self.gameData = gameData

        self.screen.fill((0,0,0))
        titleImage = pygame.image.load(os.path.join('img', 'TitleScreen.png'))
        self.screen.blit(titleImage, (0, 0))

        self.spritesHUD = pygame.sprite.Group()
        self.notifySet = weakref.WeakSet()

        self.startGameButton = Button((540, 2*SCREEN_HEIGHT/5), (150, 50), 'Start game', self.goToTheShop)
        self.spritesHUD.add(self.startGameButton)
        self.notifySet.add(self.startGameButton)

        self.exitButton = Button((540, 11*SCREEN_HEIGHT/20), (150, 50), 'Exit', sys.exit)
        self.spritesHUD.add(self.exitButton)
        self.notifySet.add(self.exitButton)

        self.eventHandler = EventHandlerTitleScreen()
        self.drawer = Drawer()

        self.type = TITLE_SCREEN
        self.nextScene = None

        MusicFactory(TITLE_SCREEN)


    def mainLoop(self):
        self.sceneRunning = True
        while self.sceneRunning:
            self.eventHandler.eventHandle(self.notifySet)
            self.handle()  # This would be in the logic
            self.drawer.draw(self.screen, None, self.spritesHUD, None)  # Drawer in THIS file, below

    def handle(self):
        self.checkHighlight()
        self.spritesHUD.update()

    def checkHighlight(self):
        mousePos = pygame.mouse.get_pos()
        for obj in self.notifySet:
            if obj.rect.collidepoint(mousePos):
                obj.isSelected = True
            else:
                obj.isSelected = False


    def startGame(self):
        self.nextScene = PLATFORM_SCREEN
        self.sceneRunning = False
        self.gameData.typeScene = PLATFORM_SCREEN
        self.gameData.mapData = MapData("LevelRoom", "StartPointWorld")

    def goToTheShop(self):
        self.nextScene = SHOP_SCREEN
        self.sceneRunning = False
        self.gameData.typeScene = SHOP_SCREEN
        self.gameData.mapData = None
        self.gameData.shopScreenData = ShopScreenData()