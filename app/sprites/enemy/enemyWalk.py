import pygame
import os
import math

from app.sprites.enemy.enemyCollision import EnemyCollision
from app.sprites.enemy.enemyAttack import EnemyAttack
from app.tools.animation import Animation
from app.AI.steeringAI import SteeringAI
from app.sprites.collisionMask import CollisionMask
from app.tools.imageBox import *
from app.sprites.GUI.lifeBar import LifeBar

from app.settings import *

class EnemyWalk(EnemyCollision):
    def __init__(self, x, y, mapData=None):  # ?
        super().__init__(x, y)

        self.name = "enemyWalk"

        self.imageEnemy = rectSurface((ENEMY_DIMX, ENEMY_DIMY), PURPLE, 2)
        self.attackingEnemy = rectSurface((ENEMY_DIMX, ENEMY_DIMY), RED, 2)

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

        self.setMapData(mapData)

        # if self.mapData.currentLevel >= 5:
        #     self.maxSpeedx = 1.4
        #     self.maxSpeedy = 1.4
        # else:
        self.maxSpeedx = 1
        self.maxSpeedy = 1

        self.isPhysicsApplied = True
        self.isCollisionApplied = True

        # self.soundDead = pygame.mixer.Sound(os.path.join('music_pcm', 'Punch2.wav'))
        # self.soundDead.set_volume(1)

        self.AI = SteeringAI(self.mapData, self.rect, self.maxSpeedx, self.maxSpeedy)
        self.collisionMask = CollisionMask(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        self.attackDMG = 1

        self.mode = WALKING
        self.timerAttack = 0
        self.timeToAttack = 20
        self.timeInAttack = 5
        self.distanceToAttack = 25
        self.attackSprite = None
        self.factorAttack = 1.5

        self.maxHealth = 5
        super().generateLifeBar(self.maxHealth)

        self.bounty = 10


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
                self.AI = SteeringAI(self.mapData, self.rect, self.maxSpeedx, self.maxSpeedy)
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

    def prepareAttack(self):
        self.mode = PREPARE_ATTACK
        self.timerAttack = 0
        self.speedx = 0
        self.speedy = 0

    def attackOnCollision(self):
        self.prepareAttack()
