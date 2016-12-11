import pygame
import os
import math

from app.sprites.enemy.enemyCollision import EnemyCollision
from app.sprites.bullet import Shuriken
from app.tools.animation import Animation
from app.AI.steeringAI import SteeringAI

from app.settings import *
import random


class EnemyShooter(EnemyCollision):
    def __init__(self, x, y, mapData=None):
        super().__init__(x, y)

        self.name = "enemyShooter"

        self.imageEnemy = pygame.image.load(os.path.join('img', 'shooting_enemy.png'))

        self.frames = [self.imageEnemy]
        self.animation = Animation(self,self.frames,20)

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

        self.AI = SteeringAI(self.mapData, self.rect, self.speedx, self.speedy)

        self.imageWaitNextShoot = 30
        self.distanceToAttack = 200
        self.speedShuriken = 8

        # self.imageIterShoot = random.randint(10, (self.imageWaitNextShoot - 10))  # To shoot bullets at random pace
        self.imageIterShoot = self.imageWaitNextShoot + 1

        self.maxHealth = 5
        super().generateLifeBar(self.maxHealth)

        self.bounty = 14



    def applyAI(self):
        steeringX, steeringY = self.AI.getAction()
        self.imageIterShoot += 1

        diffX = self.mapData.player.rect.centerx - self.rect.centerx
        diffY = self.mapData.player.rect.centery - self.rect.centery

        if self.imageIterShoot > self.imageWaitNextShoot and math.sqrt(diffX**2 + diffY**2) < self.distanceToAttack:
            norm = math.sqrt(diffX**2+diffY**2+EPS)
            speedx_bullet = diffX/norm*self.speedShuriken
            speedy_bullet = diffY/norm*self.speedShuriken
            bullet = Shuriken(self.rect.centerx, self.rect.centery, speedx_bullet, speedy_bullet, False)

            self.mapData.camera.add(bullet)
            self.mapData.allSprites.add(bullet)
            self.mapData.enemyBullet.add(bullet)
            self.imageIterShoot = 0

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
