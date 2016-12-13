import pygame

from app.scene.platformScreen.eventHandlerPlatformScreen import EventHandlerPlatformScreen
from app.scene.platformScreen.logicHandlerPlatformScreen import LogicHandlerPlatformScreen
from app.scene.drawer import Drawer
from app.settings import *
from app.sprites.GUI.showItem import ShowItem
from app.sprites.playerPlatform import PlayerPlatform
from app.scene.musicFactory import MusicFactory
from app.sprites.GUI.showBarricadeCharges import ShowBarricadeCharges
from app.sprites.GUI.HUDPlatformScreen import HUDPlatformScreen
from app.shopScreenData import ShopScreenData
from app.tools.counter import Counter
from app.tools.messageBox.messageBox import MessageBox

from app.mapData import MapData


class PlatformScreen:
    def __init__(self, screen, gameData):
        self.screen = screen
        self.gameData = gameData
        self.nextScene = None

        self.mapData = self.gameData.mapData
        self.mapData.gold = self.gameData.gold

        self.player = PlayerPlatform(self.mapData.spawmPointPlayerx, self.mapData.spawmPointPlayery, self.gameData)

        self.mapData.allSprites.add(self.player)
        self.mapData.camera.add(self.player)
        self.mapData.notifySet.add(self.player)
        self.camera = self.mapData.camera

        self.eventHandler = EventHandlerPlatformScreen(self.gameData)
        self.logicHandler = LogicHandlerPlatformScreen(self.screen, self.player, self.mapData)
        self.drawer = Drawer()

        self.addHUD()

        message = 'Level '+str(self.gameData.currentLevel)
        self.createLevelBox(SCREEN_WIDTH/2-150, SCREEN_HEIGHT/2-250, 300, 50, message)
        self.counter = Counter()
        self.duration = 120  #In frames

        MusicFactory(PLATFORM_SCREEN, self.mapData.currentLevel)

    def mainLoop(self):

        # To say something
        fontScreen = pygame.font.SysFont(FONT_NAME, 40)

        self.sceneRunning = True
        while self.sceneRunning:
            self.eventHandler.eventHandle()
            self.logicHandler.handle(self.player, self.gameData)
            self.checkNewMap(self.logicHandler.newMapData)

            self.counter.count()
            if self.counter.value == self.duration:
                self.textLevel.kill()

            #Check if last level won...
            if self.logicHandler.endingLevelCondition == LAST_LEVEL_WON:
                message = fontScreen.render('YOU WON! Endless wave incoming!', True, WHITE)
                messagePos = [(SCREEN_WIDTH - message.get_width()) / 2,
                              (SCREEN_HEIGHT) / 2-20]
                self.screen.blit(message, messagePos)

                message2 = fontScreen.render('Try to get as much gold as you can!', True,
                                            WHITE)
                messagePos2 = [(SCREEN_WIDTH - message.get_width()) / 2,
                              (SCREEN_HEIGHT) / 2+20]
                self.screen.blit(message2, messagePos2)

                pygame.display.flip()
                pygame.time.wait(4000)
                self.logicHandler.endingLevelCondition = None

            self.drawer.draw(self.screen, self.mapData.camera, self.mapData.spritesHUD, self.player)

        # Update gold before you leave
        self.gameData.gold = self.mapData.gold


        if self.logicHandler.endingLevelCondition == PLAYER_DEAD:
            message = fontScreen.render('You died! Get your revenge on those creeps!', True, WHITE)
            messagePos = [(SCREEN_WIDTH - message.get_width()) / 2,
                          (SCREEN_HEIGHT )/ 2]
        elif self.logicHandler.endingLevelCondition == LEVEL_WON:
            message = fontScreen.render('You won! Get ready for the next level!', True, WHITE)
            messagePos = [(SCREEN_WIDTH - message.get_width()) / 2,
                          (SCREEN_HEIGHT )/ 2]

        self.screen.blit(message, messagePos)

        pygame.display.flip()
        pygame.time.wait(2000)


    def checkNewMap(self, newMapData):
        if newMapData is not None:
            # we got to change
            self.sceneRunning = False
            self.nextScene = SHOP_SCREEN
            self.gameData.typeScene = SHOP_SCREEN
            self.gameData.mapData = ShopScreenData()


    def addHUD(self):
        self.HUD = HUDPlatformScreen(self.gameData,self.player)
        self.mapData.spritesHUD.add(self.HUD)

    def createLevelBox(self,x,y,width,height, message):
        self.textLevel = MessageBox(x,y,width,height)
        self.textLevel.textList.append(message)
        self.textLevel.isPhysicsApplied = False
        self.textLevel.isCollisionApplied = False

        self.mapData.spritesHUD.add(self.textLevel)  # Add sprite
