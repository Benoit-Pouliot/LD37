from app.mapData import MapData
from app.sprites.bullet import *
from app.settings import *
from app.scene.platformScreen.collisionPlayerPlatform import CollisionPlayerPlatform
from app.tools.functionTools import *
import pygame

class LogicHandlerPlatformScreen:
    def __init__(self, screen, player, mapData):

        self.sceneRunning = True
        self.endState = None
        self.collisionChecker = CollisionPlayerPlatform(player, mapData)
        self.newMapData = None
        self.mapData = mapData

        self.endingLevelCondition = None
        self.alreadyWon = False

        self.screen = screen

    def handle(self, player, gameData):
        self.applyFriction(self.mapData.allSprites)
        self.handleZoneCollision(player)
        self.collisionChecker.collisionAllSprites(player, self.mapData, gameData)
        self.mapData.internalMapTime += 1
        self.mapData.enemyGeneratorSupervisor.updateSupervisor()
        self.handleBullets(self.mapData, player)
        self.handleExplosions(self.mapData, player)
        self.handleAttacks(self.mapData, player)
        self.gameOverCondition(player)
        self.mapData.allSprites.update()
        self.mapData.spritesHUD.update()
        self.endLevelCondition(gameData)

    def handleZoneCollision(self, player):
        for obj in self.mapData.tmxData.objects:
            if self.isPlayerIsInZone(player, obj) == True:
                if obj.name == "OutZone":
                    nameNewZone = obj.LevelZone
                    nameInZone = obj.InZone

                    # Initializing new map
                    self.newMapData = MapData(nameNewZone, nameInZone)

    def isPlayerIsInZone(self, player, zone):

        if player.rect.centerx  >= zone.x and \
           player.rect.centerx <= zone.x + zone.width and \
           player.rect.centery >= zone.y and \
           player.rect.centery <= zone.y + zone.height:
           return True
        else:
           return False

    def applyGravity(self, allSprites):
        for sprite in allSprites:
            if sprite.isPhysicsApplied == True or sprite.isGravityApplied == True:
                sprite.speedy += GRAVITY

    def applyFriction(self, allSprites):
        for sprite in allSprites:
            if sprite.isPhysicsApplied == True:
                pass
                if sprite.speedx > 0 and sprite.speedx - FRICTION > 0:
                    sprite.speedx -= FRICTION
                elif sprite.speedx > 0:
                    sprite.speedx = 0

                if sprite.speedx < 0 and sprite.speedx + FRICTION < 0:
                    sprite.speedx += FRICTION
                elif sprite.speedx < 0:
                    sprite.speedx = 0

                if sprite.speedy > 0 and sprite.speedy - FRICTION > 0:
                    sprite.speedy -= FRICTION
                elif sprite.speedy > 0:
                    sprite.speedy = 0

                if sprite.speedy < 0 and sprite.speedy + FRICTION < 0:
                    sprite.speedy += FRICTION
                elif sprite.speedy < 0:
                    sprite.speedy = 0

    def handleBullets(self, mapData, player):
        for bullet in mapData.friendlyBullet:
            if type(bullet) == PlayerBullet:
                collisionBulletEnemy(bullet, mapData)

        collisionBulletPlayer(mapData, player)

    def handleExplosions(self, mapData, player):
        for explosion in mapData.friendlyExplosion:
            collisionExplosionEnemy(explosion, mapData)

    def handleAttacks(self, mapData, player):
        collisionAttackPlayer(mapData, player)
        for barricade in mapData.obstacleGroup:
            collisionBarricadePlayer(mapData, barricade)

    def gameOverCondition(self,player):
        if player.isAlive == False:
            self.endingLevelCondition = PLAYER_DEAD
            self.newMapData = True
            self.sceneRunning = False

    def endLevelCondition(self, gameData):
        if self.mapData.internalMapTime > self.mapData.levelEndTime:
            if len(self.mapData.enemyGroup.sprites()) == 0:
                if gameData.currentLevel == 6:
                    if self.alreadyWon == False:
                        self.endingLevelCondition = LAST_LEVEL_WON
                        self.alreadyWon = True
                        self.lastInfiniteLevel()
                else:
                    gameData.currentLevel += 1
                    self.newMapData = True
                    self.sceneRunning = False
                    self.endingLevelCondition = LEVEL_WON


    def lastInfiniteLevel(self):
            self.mapData.enemyGenListData.addData(6000, [1], 4, 200)
            self.mapData.enemyGenListData.addData(6300, [1], 4, 200)
            self.mapData.enemyGenListData.addData(6500, [2], 4, 200)
            self.mapData.enemyGenListData.addData(6700, [3], 4, 200)
            self.mapData.enemyGenListData.addData(6900, [4], 4, 200)
            self.mapData.enemyGenListData.addData(7000, [2], 4, 200)
            self.mapData.enemyGenListData.addData(7200, [3], 4, 200)
            self.mapData.enemyGenListData.addData(7400, [4], 4, 200)
            self.mapData.enemyGenListData.addData(7500, [1], 4, 200)
            self.mapData.enemyGenListData.addData(7650, [2], 4, 200)
            self.mapData.enemyGenListData.addData(7750, [3], 4, 200)
            self.mapData.enemyGenListData.addData(7850, [4], 4, 200)

        # if TAG_PHIL ==1:
        #     print(self.mapData.internalMapTime)
