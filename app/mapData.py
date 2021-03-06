import pygame
import pyscroll
import pytmx
import re
import pygame
from app.settings import *
from app.tools.functionTools import *
import os

from app.sprites.enemyFactory import EnemyFactory
from app.enemyGenListData import EnemyGenListData
from app.sprites.enemySupervisor import EnemySupervisor
import weakref
# from app.sound.soundPlayerController import *
# from app.sprites.player import *

class MapData:
    def __init__(self, mapName="LevelRoom", nameInZone="StartPointWorld",currentLevel=1, screenSize=(SCREEN_WIDTH, SCREEN_HEIGHT)):

        self.nameMap = mapName

        self.currentLevel = currentLevel
        self.levelEndTime = 2000

        self.tmxData = pytmx.util_pygame.load_pygame(self.reqImageName(self.nameMap))
        self.tiledMapData = pyscroll.data.TiledMapData(self.tmxData)
        self.cameraPlayer = pyscroll.BufferedRenderer(self.tiledMapData, screenSize, clamp_camera=True)
        # self.soundController = soundPlayerController()

        self.allSprites = pygame.sprite.Group()
        self.enemyGroup = pygame.sprite.Group()
        self.attackGroup = pygame.sprite.Group()
        self.obstacleGroup = pygame.sprite.Group()
        self.mineGroup = pygame.sprite.Group()
        self.itemGroup = pygame.sprite.Group()
        self.friendlyBullet = pygame.sprite.Group()
        self.friendlyExplosion = pygame.sprite.Group()
        self.enemyBullet = pygame.sprite.Group()
        self.spritesHUD = pygame.sprite.Group()
        # Set of all object that needs to be notified of events.
        # Weak references are used to prevent this set from keeping objects alive
        self.notifySet = weakref.WeakSet()

        # The player will be set in playerPlatform for instance
        self.player = None

        self.internalMapTime = 0
        # EnemySupervisor
        self.enemyGeneratorSupervisor = EnemySupervisor(self)

        eFactory = EnemyFactory()

        for obj in self.tmxData.objects:
            if obj.type == "enemy":
                enemy = eFactory.create(obj, self)
                if enemy is not None:
                    self.allSprites.add(enemy)
                    self.enemyGroup.add(enemy)

            if obj.type == "enemyGenerator":
                enemy = eFactory.create(obj, self)
                if enemy is not None:
                    self.allSprites.add(enemy)
                    self.enemyGeneratorSupervisor.addEnemyGenerator(enemy)

        # All the data to spawn enemies
        self.enemyGenListData = EnemyGenListData(self)

        # FOR DEBUG
        # self.enemyGenListData.addData(120,[1],3,120)
        if TAG_MARIE == 1:
            pass
            #self.enemyGenListData.addData(120, [1,2,3,4], 1, 120)
        if TAG_BP == 1:
            # self.enemyGenListData.addData(120, [1], 1, 1200)
            self.enemyGenData(self.currentLevel)
        if TAG_ANIKA == 1:
            self.enemyGenListData.addData(120, [2], 1, 120)
            self.enemyGenListData.addData(120, [3], 1, 120)

        self.enemyGenData(self.currentLevel)

        # Put camera in mapData
        self.camera = pyscroll.PyscrollGroup(map_layer=self.cameraPlayer, default_layer=SPRITE_LAYER)
        self.camera.add(self.allSprites)

        # Spawn point of the player
        valBool = False
        for obj in self.tmxData.objects:
            if obj.name == "InZone":
                if obj.StartPoint == nameInZone:
                    self.spawmPointPlayerx = obj.x
                    self.spawmPointPlayery = obj.y
                    valBool = True

        # The game is not complete?
        if valBool == False:
            quitGame()

        #Money!!

        self.gold = 0

    def reqImageName(self, nameMap):
        return os.path.join('tiles_map', nameMap + ".tmx")

    def enemyGenData(self, currentLevel):
        if currentLevel == 1: # 110 gold
            self.enemyGenListData.addData(400, [1], 1, 0)
            self.enemyGenListData.addData(800, [1], 2, 0)
            self.enemyGenListData.addData(1800, [1], 4, 0)
            self.enemyGenListData.addData(2800, [1], 4, 0)
            self.levelEndTime = 2800

        if currentLevel == 2: #210 gold
            self.enemyGenListData.addData(400, [1], 4, 0)
            self.enemyGenListData.addData(800, [1], 4, 0)
            self.enemyGenListData.addData(1000, [1], 5, 0)
            self.enemyGenListData.addData(2500, [1], 8, 0)
            self.levelEndTime = 3001

        if currentLevel == 3: #510
            self.enemyGenListData.addData(400, [1], 4, 0)
            self.enemyGenListData.addData(500, [1], 3, 0)
            self.enemyGenListData.addData(500, [2], 2, 0)
            self.enemyGenListData.addData(600, [1], 3, 0)
            self.enemyGenListData.addData(600, [2], 1, 0)
            self.enemyGenListData.addData(700, [1], 4, 0)
            self.enemyGenListData.addData(2500, [1], 4, 0)
            self.enemyGenListData.addData(2600, [1], 4, 0)
            self.enemyGenListData.addData(2600, [2], 4, 0)
            self.enemyGenListData.addData(2800, [1], 4, 0)
            self.enemyGenListData.addData(3400, [1], 5, 0)
            self.enemyGenListData.addData(3800, [1], 5, 0)
            self.enemyGenListData.addData(3800, [2], 3, 0)
            self.enemyGenListData.addData(4300, [1], 5, 0)
            self.levelEndTime = 4301

        if currentLevel == 4: #910
            self.enemyGenListData.addData(400, [1], 4, 0)
            self.enemyGenListData.addData(500, [1], 3, 0)
            self.enemyGenListData.addData(500, [2], 2, 0)
            self.enemyGenListData.addData(500, [3], 3, 0)
            self.enemyGenListData.addData(600, [1], 3, 0)
            self.enemyGenListData.addData(600, [2], 1, 0)
            self.enemyGenListData.addData(700, [1], 4, 0)
            self.enemyGenListData.addData(2500, [1], 4, 0)
            self.enemyGenListData.addData(2600, [1], 4, 0)
            self.enemyGenListData.addData(2600, [3], 3, 0)
            self.enemyGenListData.addData(2600, [2], 4, 0)
            self.enemyGenListData.addData(2800, [1], 4, 0)
            self.enemyGenListData.addData(3400, [3], 3, 0)
            self.enemyGenListData.addData(3400, [1], 5, 0)
            self.enemyGenListData.addData(3800, [1], 5, 0)
            self.enemyGenListData.addData(3800, [2], 3, 0)
            self.enemyGenListData.addData(4300, [1], 5, 0)
            self.enemyGenListData.addData(5000, [1], 6, 0)
            self.enemyGenListData.addData(5300, [3], 3, 0)
            self.enemyGenListData.addData(5800, [1], 6, 0)
            self.enemyGenListData.addData(6200, [1], 6, 0)
            self.enemyGenListData.addData(6600, [2], 4, 0)
            self.enemyGenListData.addData(7000, [1], 6, 0)
            self.levelEndTime = 7001

        if currentLevel == 5: #1120
            self.enemyGenListData.addData(400, [1], 4, 0)
            self.enemyGenListData.addData(500, [1], 3, 0)
            self.enemyGenListData.addData(500, [4], 3, 0)
            self.enemyGenListData.addData(600, [1], 3, 0)
            self.enemyGenListData.addData(700, [1], 4, 0)
            self.enemyGenListData.addData(800, [4], 2, 0)
            self.enemyGenListData.addData(1000, [1], 4, 0)
            self.enemyGenListData.addData(1200, [4], 2, 0)
            self.enemyGenListData.addData(1200, [1], 4, 0)
            self.enemyGenListData.addData(1600, [2], 1, 0)
            self.enemyGenListData.addData(1600, [1], 4, 0)
            self.enemyGenListData.addData(1600, [4], 2, 0)
            self.enemyGenListData.addData(1800, [1], 4, 0)
            self.enemyGenListData.addData(2000, [4], 1, 0)
            self.enemyGenListData.addData(2100, [4], 1, 0)
            self.enemyGenListData.addData(2100, [1], 4, 0)
            self.enemyGenListData.addData(2200, [4], 1, 0)
            self.enemyGenListData.addData(2300, [1], 4, 0)
            self.enemyGenListData.addData(2300, [4], 1, 0)
            self.enemyGenListData.addData(2500, [1], 4, 0)
            self.enemyGenListData.addData(2500, [2], 1, 0)
            self.enemyGenListData.addData(2600, [1], 4, 0)
            self.enemyGenListData.addData(2600, [4], 2, 0)
            self.enemyGenListData.addData(2800, [1], 4, 0)
            self.enemyGenListData.addData(3000, [1], 4, 0)
            self.enemyGenListData.addData(3200, [1], 4, 0)
            self.enemyGenListData.addData(3400, [4], 2, 0)
            self.enemyGenListData.addData(3400, [1], 4, 0)
            self.enemyGenListData.addData(3600, [1], 4, 0)
            self.enemyGenListData.addData(3800, [1], 5, 0)
            self.enemyGenListData.addData(4300, [1], 5, 0)
            self.enemyGenListData.addData(4500, [2], 1, 0)
            self.enemyGenListData.addData(4800, [1], 4, 0)
            self.enemyGenListData.addData(4800, [4], 4, 0)
            self.enemyGenListData.addData(5200, [1], 4, 0)
            self.enemyGenListData.addData(5300, [1], 4, 0)
            self.enemyGenListData.addData(5400, [1], 6, 0)
            self.enemyGenListData.addData(5500, [1], 6, 0)
            self.levelEndTime = 5001

        if currentLevel == 6:
            self.enemyGenListData.addData(400, [1], 4, 0)
            self.enemyGenListData.addData(500, [2], 4, 0)
            self.enemyGenListData.addData(450, [3], 4, 0)
            self.enemyGenListData.addData(500, [4], 3, 0)
            self.enemyGenListData.addData(600, [1], 3, 0)
            self.enemyGenListData.addData(650, [3], 3, 0)
            self.enemyGenListData.addData(700, [2], 4, 0)
            self.enemyGenListData.addData(750, [4], 2, 0)
            self.enemyGenListData.addData(800, [4], 2, 0)
            self.enemyGenListData.addData(900, [3], 4, 0)
            self.enemyGenListData.addData(1000, [1], 4, 0)
            self.enemyGenListData.addData(1050, [4], 2, 0)
            self.enemyGenListData.addData(1100, [3], 4, 0)
            self.enemyGenListData.addData(1200, [4], 2, 0)
            self.enemyGenListData.addData(1200, [1], 4, 0)
            self.enemyGenListData.addData(1400, [2], 2, 0)
            self.enemyGenListData.addData(1600, [2], 1, 0)
            self.enemyGenListData.addData(1600, [1], 4, 0)
            self.enemyGenListData.addData(1600, [4], 2, 0)
            self.enemyGenListData.addData(1700, [1], 4, 0)
            self.enemyGenListData.addData(1700, [2], 2, 0)
            self.enemyGenListData.addData(1800, [1], 4, 0)
            self.enemyGenListData.addData(1900, [3], 4, 0)
            self.enemyGenListData.addData(2000, [4], 1, 0)
            self.enemyGenListData.addData(2100, [4], 1, 0)
            self.enemyGenListData.addData(2100, [1], 4, 0)
            self.enemyGenListData.addData(2200, [4], 1, 0)
            self.enemyGenListData.addData(2300, [1], 4, 0)
            self.enemyGenListData.addData(2300, [4], 1, 0)
            self.enemyGenListData.addData(2400, [3], 4, 0)
            self.enemyGenListData.addData(2500, [1], 4, 0)
            self.enemyGenListData.addData(2500, [2], 1, 0)
            self.enemyGenListData.addData(2600, [1], 4, 0)
            self.enemyGenListData.addData(2600, [4], 2, 0)
            self.enemyGenListData.addData(2700, [2], 2, 0)
            self.enemyGenListData.addData(2800, [1], 4, 0)
            self.enemyGenListData.addData(2900, [3], 4, 0)
            self.enemyGenListData.addData(3000, [1], 4, 0)
            self.enemyGenListData.addData(3200, [1], 4, 0)
            self.enemyGenListData.addData(3300, [3], 4, 0)
            self.enemyGenListData.addData(3400, [4], 2, 0)
            self.enemyGenListData.addData(3400, [1], 4, 0)
            self.enemyGenListData.addData(3600, [1], 4, 0)
            self.enemyGenListData.addData(3500, [4], 4, 0)
            self.enemyGenListData.addData(3600, [3], 4, 0)
            self.enemyGenListData.addData(3700, [1], 4, 0)
            self.enemyGenListData.addData(3800, [1], 5, 0)
            self.enemyGenListData.addData(3900, [2], 4, 0)
            self.enemyGenListData.addData(4000, [1], 4, 0)
            self.enemyGenListData.addData(4200, [4], 4, 0)
            self.enemyGenListData.addData(4300, [1], 5, 0)
            self.enemyGenListData.addData(4500, [2], 1, 0)
            self.enemyGenListData.addData(4600, [1], 4, 0)
            self.enemyGenListData.addData(4700, [3], 4, 0)
            self.enemyGenListData.addData(4800, [1], 4, 0)
            self.enemyGenListData.addData(4800, [4], 4, 0)
            self.enemyGenListData.addData(5000, [2], 4, 0)
            self.enemyGenListData.addData(5200, [1], 4, 0)
            self.enemyGenListData.addData(5300, [1], 4, 0)
            self.enemyGenListData.addData(5400, [1], 6, 0)
            self.enemyGenListData.addData(5500, [4], 10, 0)

            self.levelEndTime = 5001

            #FROM HERE, ITS MADNESS INFINITY!!! (End of game chaos)


        #
        # if currentLevel == 7:
        #     self.enemyGenListData.addData(10, [1], 1, 0)
        #     self.levelEndTime = 12