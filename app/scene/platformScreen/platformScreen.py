
from app.scene.platformScreen.eventHandlerPlatformScreen import EventHandlerPlatformScreen
from app.scene.platformScreen.logicHandlerPlatformScreen import LogicHandlerPlatformScreen
from app.scene.drawer import Drawer
from app.settings import *
from app.sprites.GUI.showItem import ShowItem
from app.sprites.playerPlatform import PlayerPlatform
from app.scene.musicFactory import MusicFactory
from app.sprites.GUI.showBarricadeCharges import ShowBarricadeCharges
from app.sprites.GUI.HUDPlatformScreen import HUDPlatformScreen

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

        MusicFactory(PLATFORM_SCREEN, self.mapData.nameMap)

    def mainLoop(self):

        self.sceneRunning = True
        while self.sceneRunning:
            self.eventHandler.eventHandle()
            self.logicHandler.handle(self.player, self.gameData)
            self.checkNewMap(self.logicHandler.newMapData)
            self.drawer.draw(self.screen, self.mapData.camera, self.mapData.spritesHUD, self.player)

        # Update gold before you leave
        self.gameData.gold = self.mapData.gold

    def checkNewMap(self, newMapData):
        if newMapData is not None:
            # we got to change
            self.sceneRunning = False
            self.nextScene = SHOP_SCREEN
            self.gameData.typeScene = SHOP_SCREEN
            self.gameData.mapData = None


    def addHUD(self):
        self.HUD = HUDPlatformScreen(self.gameData,self.player)
        self.mapData.spritesHUD.add(self.HUD)

    def close(self):
        self.sceneRunning = False

    def backToMain(self):
        self.nextScene = TITLE_SCREEN
        self.gameData.typeScene = TITLE_SCREEN
        self.gameData.gold = self.mapData.gold

        self.close()

