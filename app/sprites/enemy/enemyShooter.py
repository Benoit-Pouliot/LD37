import pygame
import os
import math

from app.sprites.enemy.enemyCollision import EnemyCollision
from app.sprites.bullet import Shuriken
from app.tools.animation import Animation
from app.tools.imageBox import rectSurface
from app.AI.steeringAI import SteeringAI
from app.sprites.collisionMask import CollisionMask

from app.settings import *
import random


class EnemyShooter(EnemyCollision):
    def __init__(self, x, y, mapData=None):
        super().__init__(x, y)

        self.name = "enemyShooter"

        self.imageEnemy = rectSurface((ENEMY_DIMX, ENEMY_DIMY), RED, 2)

        self.frames = [self.imageEnemy]
        self.animation = Animation(self, self.frames, 100)

        self.rect = self.imageEnemy.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y

        self.speedx = 0
        self.speedy = 0
        self.maxSpeedx = 2
        self.maxSpeedy = 2

        self.setMapData(mapData)

        self.isGravityApplied = True
        self.isCollisionApplied = True

        self.AI = SteeringAI(self.mapData, self.rect, self.maxSpeedx, self.maxSpeedy)
        self.collisionMask = CollisionMask(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        self.imageWaitNextShoot = 60
        self.distanceToAttack = 200
        self.speedShuriken = 3

        # self.imageIterShoot = random.randint(10, (self.imageWaitNextShoot - 10))  # To shoot bullets at random pace
        self.imageIterShoot = self.imageWaitNextShoot + 1

        self.maxHealth = 5
        super().generateLifeBar(self.maxHealth)

        self.bounty = 25


    def applyAI(self):
        self.imageIterShoot += 1

        diffX = self.mapData.player.rect.centerx - self.rect.centerx
        diffY = self.mapData.player.rect.centery - self.rect.centery
        if math.sqrt(diffX**2 + diffY**2) <= self.distanceToAttack:
            self.speedx = 0
            self.speedy = 0
            if self.imageIterShoot > self.imageWaitNextShoot:
                norm = math.sqrt(diffX**2+diffY**2+EPS)
                speedx_bullet = diffX/norm*self.speedShuriken
                speedy_bullet = diffY/norm*self.speedShuriken
                bullet = Shuriken(self.rect.centerx, self.rect.centery, speedx_bullet, speedy_bullet, False)

                self.mapData.camera.add(bullet)
                self.mapData.allSprites.add(bullet)
                self.mapData.enemyBullet.add(bullet)
                self.imageIterShoot = 0
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
