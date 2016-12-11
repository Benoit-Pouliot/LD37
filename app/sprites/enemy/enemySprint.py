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

        self.imageEnemy = pygame.Surface((ENEMY_DIMX, ENEMY_DIMY))
        self.imageEnemy.fill(YELLOW)

        self.attackingEnemy = pygame.Surface((ENEMY_DIMX, ENEMY_DIMY))
        self.attackingEnemy.fill(RED)

        self.enemyFrames = [self.imageEnemy]
        self.prepareAttackingFrames = [self.attackingEnemy, self.imageEnemy]
        self.attackingFrames = [self.attackingEnemy]
        self.animation = Animation(self, self.enemyFrames, 100)

        self.rect = self.imageEnemy.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y

        self.maxSpeedWalkx = 2
        self.maxSpeedWalky = 2

        self.speedx = 0
        self.speedy = 0
        self.maxSpeedx = self.maxSpeedWalkx
        self.maxSpeedy = self.maxSpeedWalky

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
        self.distanceToSprint = 150
        self.speedSprint = 25
        self.maxSpeedSprintx = self.speedSprint
        self.maxSpeedSprinty = self.speedSprint
        self.speedAttackX = 0
        self.speedAttackY = 0

        self.maxHealth = 5
        super().generateLifeBar(self.maxHealth)

        self.bounty = 20

    def applyAI(self):

        if self.mode == IN_ATTACK:
            self.speedx = self.speedAttackX
            self.speedy = self.speedAttackY

            if self.timerSprint <= self.timeInSprint:
                self.timerSprint += 1
            else:
                self.timerSprint = 0
                self.mode = WALKING
                self.maxSpeedx = self.maxSpeedWalkx
                self.maxSpeedy = self.maxSpeedWalky
                self.speedx = 0
                self.speedy = 0

        elif self.mode == PREPARE_ATTACK:
            if self.timerSprint == 0:
                self.timerSprint += 1
                diffX = self.mapData.player.rect.centerx - self.rect.centerx
                diffY = self.mapData.player.rect.centery - self.rect.centery
                norm = math.sqrt(diffX**2+diffY**2+EPS)
                self.speedAttackX = diffX/norm*self.speedSprint
                self.speedAttackY = diffY/norm*self.speedSprint
            elif self.timerSprint < self.timeToSprint:
                self.timerSprint += 1
            else:
                self.timerSprint = 0
                self.mode = IN_ATTACK
                self.animation = Animation(self, self.enemyFrames, 100)
                self.maxSpeedx = self.maxSpeedSprintx
                self.maxSpeedy = self.maxSpeedSprinty

        else:
            # if player is close : stop and init timer to sprint
            distX = self.mapData.player.rect.centerx-self.rect.centerx
            distY = self.mapData.player.rect.centery-self.rect.centery
            if math.sqrt(distX**2 + distY**2) < self.distanceToSprint:
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
        self.animation = Animation(self, self.prepareAttackingFrames, 5)
        self.timerSprint = 0
        self.speedx = 0
        self.speedy = 0
