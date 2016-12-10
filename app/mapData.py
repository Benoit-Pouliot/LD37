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
    def __init__(self, mapName="WorldMap", nameInZone="StartPointWorld", screenSize=(SCREEN_WIDTH, SCREEN_HEIGHT)):

        self.nameMap = mapName

        self.tmxData = pytmx.util_pygame.load_pygame(self.reqImageName(self.nameMap))
        self.tiledMapData = pyscroll.data.TiledMapData(self.tmxData)
        self.cameraPlayer = pyscroll.BufferedRenderer(self.tiledMapData, screenSize, clamp_camera=True)
        # self.soundController = soundPlayerController()

        self.allSprites = pygame.sprite.Group()
        self.enemyGroup = pygame.sprite.Group()
        self.obstacleGroup = pygame.sprite.Group()
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
                    if obj.name == "enemyGenerator":
                        self.enemyGeneratorSupervisor.addEnemyGenerator(enemy)

        # All the data to spawn enemies
        self.enemyGenListData = EnemyGenListData(self)

        # FOR DEBUG
        self.enemyGenListData.addData(120,[1],3,120)
        if TAG_BP == 1:
            self.enemyGenListData.addData(60,[1],3,60)
            self.enemyGenListData.addData(10,[1],20,1)
            self.enemyGenListData.addData(5,[1],2,1)

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

    def reqImageName(self, nameMap):
        return os.path.join('tiles_map', nameMap + ".tmx")
