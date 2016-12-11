import pygame
import os
import math

from app.sprites.enemy.enemyCollision import EnemyCollision
from app.tools.animation import Animation
from app.AI.steeringAI import SteeringAI
from app.sprites.collisionMask import CollisionMask

from app.settings import *

class EnemySprint(EnemyCollision):
    def __init__(self, x, y, mapData=None):  # ?
        super().__init__(x, y)

        self.name = "enemySprint"

        self.imageEnemy = pygame.image.load(os.path.join('img', 'sprinting_enemy.png'))

        self.enemyFrames = [self.imageEnemy]
        self.animation = Animation(self, self.enemyFrames, 100)

        self.rect = self.imageEnemy.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y

        self.speedx = 0
        self.speedy = 0
        self.maxSpeedx = 2
        self.maxSpeedy = 2

        self.setMapData(mapData)  # ?

        self.isPhysicsApplied = True
        self.isCollisionApplied = True

        self.soundDead = pygame.mixer.Sound(os.path.join('music_pcm', 'Punch2.wav'))
        self.soundDead.set_volume(1)

        self.AI = SteeringAI(self.mapData, self.rect, self.speedx, self.speedy)
        self.collisionMask = CollisionMask(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        self.sprintDMG = 1

        self.mode = WALKING
        self.timerSprint = 0
        self.timeToSprint = 60
        self.timeInSprint = 5
        self.distanceToSprint = 25
        self.SprintSprite = None

    def applyAI(self):

        if self.mode == SPRINT:
            if self.timerSprint == 0:
                self.timerSprint += 1

            elif self.timerSprint < self.timeInSprint:
                self.timerSprint += 1
            else:
                self.timerSprint = 0
                self.mode = WALKING
                self.AI = SteeringAI(self.mapData, self.rect, self.speedx, self.speedy)
                self.animation = Animation(self, self.enemyFrames, 100)

        elif self.mode == PREPARE_SPRINT:
            if self.timerSprint < self.timeToSprint:
                self.timerSprint += 1
            else:
                self.timerSprint = 0
                self.mode = IN_SPRINT

        else:
            # if player is close : stop and init timer to sprint
            distX = self.mapData.player.rect.x-self.rect.x
            distY = self.mapData.player.rect.y-self.rect.y
            if math.sqrt(distX**2 + distY**2) < self.distanceToSprint:
                self.prepareSprint()
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

    def dead(self):
        self.soundDead.play()
        super().dead()

    def prepareSprint(self):
        self.mode = PREPARE_SPRINT
        self.timerSprint = 0
        self.speedx = 0
        self.speedy = 0