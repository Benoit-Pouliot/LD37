# Imports
import os
import sys

import pygame

from app.sprites.GUI.button import Button
from app.sprites.GUI.menu.menu import Menu
from app.scene.shopScreen.eventHandlerShopScreen import EventHandlerShopScreen
from app.scene.titleScreen.eventHandlerTitleScreen import EventHandlerTitleScreen
from app.scene.shopScreen.logicHandlerShopScreen import LogicHandlerShopScreen
from app.settings import *
from app.scene.drawer import Drawer


class ShopScreen:
    def __init__(self, screen, gameData=None):
        self.screen = screen

        self.gameData = gameData

        self.screen.fill((0, 0, 0))
        titleImage = pygame.image.load(os.path.join('img', 'menu.png'))
        self.screen.blit(titleImage, (0, 0))

        # Define MainMenu
        self.menu = Menu(pygame.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 12 / 16, SCREEN_WIDTH / 3, SCREEN_HEIGHT * 0.25))

        self.menu.addOption('Shop', self.goToTheShop)
        self.menu.addOption('Exit', sys.exit)

        self.eventHandler = EventHandlerTitleScreen(self.menu)
        self.drawer = Drawer()

        self.type = TITLE_SCREEN
        self.nextScene = None

    def mainLoop(self):
        self.sceneRunning = True
        while self.sceneRunning:
            self.eventHandler.eventHandle(self.menu.optionList, self.menu.selector)
            self.menu.update()  # This would be in the logic
            self.drawer.draw(self.screen, None, self.menu, None)  # Drawer in THIS file, below


    def goToTheShop(self):
        self.nextScene = SHOP_SCREEN
        self.sceneRunning = False
        self.gameData.typeScene = SHOP_SCREEN
        self.gameData.mapData = None