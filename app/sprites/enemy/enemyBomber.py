import pygame
import os
import math

from app.sprites.enemy.enemyCollision import EnemyCollision
from app.sprites.explosion import Explosion
from app.tools.animation import Animation
from app.AI.steeringAI import SteeringAI
from app.tools.imageBox import *
from app.sprites.collisionMask import CollisionMask
from app.sprites.GUI.lifeBar import LifeBar

from app.settings import *

class EnemyBomber(EnemyCollision):
    def __init__(self, x, y, mapData=None):
        super().__init__(x, y)

        self.name = "enemyBomber"

        self.imageEnemy = rectSurface((ENEMY_DIMX, ENEMY_DIMY), ORANGE, 2)
        self.attackingEnemy = rectSurface((ENEMY_DIMX, ENEMY_DIMY), RED, 2)

        self.enemyFrames = [self.imageEnemy]
        self.attackingFrames = [self.attackingEnemy, self.imageEnemy]
        self.animation = Animation(self, self.enemyFrames, 100)

        self.rect = self.imageEnemy.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y

        self.speedx = 0
        self.speedy = 0
        self.maxSpeedx = 2.4
        self.maxSpeedy = 2.4

        self.setMapData(mapData)

        self.isPhysicsApplied = True
        self.isCollisionApplied = True

        self.AI = SteeringAI(self.mapData, self.rect, self.maxSpeedx, self.maxSpeedy)
        self.collisionMask = CollisionMask(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        self.attackDMG = 1

        self.mode = WALKING
        self.timerAttack = 0
        self.timeToAttack = 30
        self.distanceToAttack = 45
        self.attackSprite = None

        self.maxHealth = 3
        super().generateLifeBar(self.maxHealth)

        self.bounty = 12


    def applyAI(self):

        if self.mode == IN_ATTACK:
            self.detonate()

        elif self.mode == PREPARE_ATTACK:
            if self.timerAttack < self.timeToAttack:
                self.timerAttack += 1
            else:
                self.timerAttack = 0
                self.mode = IN_ATTACK

        else:
            # if player is close :  init timer to attack
            distX = self.mapData.player.rect.x-self.rect.x
            distY = self.mapData.player.rect.y-self.rect.y
            if math.sqrt(distX**2 + distY**2) < self.distanceToAttack:
                self.prepareAttack()
                self.animation = Animation(self, self.attackingFrames, 5)

        # Move even if he want to blow
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
        self.detonate()
        super().dead()

    def detonate(self):
        explosion = Explosion(self.rect.midbottom[0], self.rect.midbottom[1])
        self.mapData.camera.add(explosion)
        self.mapData.allSprites.add(explosion)
        self.mapData.friendlyExplosion.add(explosion)

    def prepareAttack(self):
        self.mode = PREPARE_ATTACK
        self.timerAttack = 0
