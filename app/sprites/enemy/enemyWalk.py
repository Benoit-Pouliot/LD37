import pygame
import os
import math

from app.sprites.enemy.enemy import Enemy
from app.sprites.enemy.enemyAttack import EnemyAttack
from app.tools.animation import Animation
from app.AI.steeringAI import SteeringAI
from app.sprites.collisionMask import CollisionMask
from app.sprites.GUI.lifeBar import LifeBar

from app.settings import *

class EnemyWalk(Enemy):
    def __init__(self, x, y, mapData=None):  # ?
        super().__init__(x, y)

        self.name = "enemyWalk"

        self.imageEnemy = pygame.image.load(os.path.join('img', 'walking_enemy.png'))
        self.attackingEnemy = pygame.image.load(os.path.join('img', 'shooting_enemy.png'))

        self.enemyFrames = [self.imageEnemy]
        self.attackingFrames = [self.attackingEnemy]
        self.animation = Animation(self, self.enemyFrames, 100)

        self.rect = self.imageEnemy.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y

        self.speedx = 0
        self.speedy = 0
        self.maxSpeedx = 1
        self.maxSpeedy = 1

        self.setMapData(mapData)  # ?

        self.isPhysicsApplied = True
        self.isCollisionApplied = True

        self.soundDead = pygame.mixer.Sound(os.path.join('music_pcm', 'Punch2.wav'))
        self.soundDead.set_volume(1)

        self.AI = SteeringAI(self.mapData, self.rect, self.speedx, self.speedy)
        self.collisionMask = CollisionMask(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        self.attackDMG = 1

        self.mode = WALKING
        self.timerAttack = 0
        self.timeToAttack = 60
        self.timeInAttack = 5
        self.distanceToAttack = 25
        self.attackSprite = None
        self.factorAttack = 1.5

        self.maxHealth = 5
        self.lifeBar = LifeBar(5, self.rect.width)
        self.mapData.allSprites.add(self.lifeBar)
        self.mapData.camera.add(self.lifeBar, layer=CAMERA_HUD_LAYER)
        self.lifeBar.rect.x = self.rect.x
        self.lifeBar.rect.bottom = self.rect.top - 3


    def applyAI(self):

        if self.mode == IN_ATTACK:
            if self.timerAttack == 0:
                self.timerAttack += 1

                # create an invisible sprite that damage player
                valueX = float(self.image.get_width())*self.factorAttack
                valueY = float(self.image.get_height())*self.factorAttack
                positionX = float(self.rect.x)-(valueX-self.image.get_width())/2
                positionY = float(self.rect.y)-(valueY-self.image.get_height())/2
                self.attackSprite = EnemyAttack(positionX, positionY, (valueX, valueY), self.attackDMG)
                self.attackSprite.setMapData(self.mapData)

                # do an animation
                self.animation = Animation(self, self.attackingFrames, 100)

            elif self.timerAttack < self.timeInAttack:
                self.timerAttack += 1
            else:
                self.timerAttack = 0
                self.mode = WALKING
                self.AI = SteeringAI(self.mapData, self.rect, self.speedx, self.speedy)
                self.attackSprite.kill()
                self.animation = Animation(self, self.enemyFrames, 100)

        elif self.mode == PREPARE_ATTACK:
            if self.timerAttack < self.timeToAttack:
                self.timerAttack += 1
            else:
                self.timerAttack = 0
                self.mode = IN_ATTACK

        else:
            # if player is close : stop and init timer to attack
            distX = self.mapData.player.rect.x-self.rect.x
            distY = self.mapData.player.rect.y-self.rect.y
            if math.sqrt(distX**2 + distY**2) < self.distanceToAttack:
                self.prepareAttack()
            else:
                steeringX, steeringY = self.AI.getAction()

                self.speedx += steeringX
                self.speedy += steeringY

    def update(self):
        self.capSpeed()

        self.x += self.speedx
        self.y += self.speedy
        self.rect.x = self.x
        self.rect.y = self.y

        self.lifeBar.rect.x = self.rect.x
        self.lifeBar.rect.bottom = self.rect.top - 3

        self.checkIfIsAlive()

        super().update()

    def capSpeed(self):
        if self.speedx > self.maxSpeedx:
            self.speedx = self.maxSpeedx
        if self.speedx < -self.maxSpeedx:
            self.speedx = -self.maxSpeedx
        if self.speedy > self.maxSpeedy:
            self.speedy = self.maxSpeedy
        if self.speedy < -self.maxSpeedy:
            self.speedy = -self.maxSpeedy

    def isHit(self, dmg):
        self.lifeBar.healthCurrent -= dmg

    def checkIfIsAlive(self):
        if self.lifeBar.healthCurrent <= 0:
            self.dead()

    def dead(self):
        self.soundDead.play()
        self.lifeBar.kill()
        super().dead()

    def prepareAttack(self):
        self.mode = PREPARE_ATTACK
        self.timerAttack = 0
        self.speedx = 0
        self.speedy = 0

    def onCollision(self, collidedWith, sideOfCollision,limit=0):
        if collidedWith == SOLID:
            if sideOfCollision == RIGHT:
                # On colle la sprite sur le mur à droite
                self.speedx = 0
                self.collisionMask.rect.right += self.mapData.tmxData.tilewidth - (
                self.collisionMask.rect.right % self.mapData.tmxData.tilewidth) - 1
            elif sideOfCollision == LEFT:
                self.speedx = 0
                self.collisionMask.rect.left -= (self.collisionMask.rect.left % self.mapData.tmxData.tilewidth)  # On colle la sprite sur le mur à gauche
            elif sideOfCollision == DOWN:
                while self.mapData.tmxData.get_tile_gid(
                                (self.collisionMask.rect.left + 1) / self.mapData.tmxData.tilewidth,
                                (self.collisionMask.rect.bottom) / self.mapData.tmxData.tileheight,
                                COLLISION_LAYER) != SOLID and self.mapData.tmxData.get_tile_gid(
                            self.collisionMask.rect.right / self.mapData.tmxData.tilewidth,
                            (self.collisionMask.rect.bottom) / self.mapData.tmxData.tileheight, COLLISION_LAYER) != SOLID:
                    self.collisionMask.rect.top += 1
                self.collisionMask.rect.top -= 1  # Redescendre de 1 pour sortir du plafond
                self.speedy = 0

            elif sideOfCollision == UP:
                # Coller le player sur le plafond
                while self.mapData.tmxData.get_tile_gid(
                                (self.collisionMask.rect.left + 1) / self.mapData.tmxData.tilewidth,
                                (self.collisionMask.rect.top) / self.mapData.tmxData.tileheight,
                                COLLISION_LAYER) != SOLID and self.mapData.tmxData.get_tile_gid(
                            self.collisionMask.rect.right / self.mapData.tmxData.tilewidth,
                            (self.collisionMask.rect.top) / self.mapData.tmxData.tileheight, COLLISION_LAYER) != SOLID:
                    self.collisionMask.rect.bottom -= 1
                self.collisionMask.rect.bottom += 1  # Redescendre de 1 pour sortir du plafond
                self.speedy = 0


        if collidedWith == SPIKE:
            self.dead()

        if collidedWith == OBSTACLE:
            if sideOfCollision == RIGHT:
                if TAG_MARIE == 1:
                    print(limit)
                #On colle le player à gauche de l'obstacle
                self.speedx = 0
                self.rect.right += -2

            if sideOfCollision == LEFT:
                self.speedx = 0
                self.rect.left += 2
            if sideOfCollision == DOWN:
                self.speedy = 0
                self.rect.bottom += -2

            if sideOfCollision == UP:
                self.speedy = 0
                self.rect.top += 2
