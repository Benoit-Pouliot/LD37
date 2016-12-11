import pygame
import os

from app.sprites.enemy.enemyCollision import EnemyCollision
from app.sprites.bullet import Shuriken
from app.tools.animation import Animation
from app.AI.steeringAI import SteeringAI

from app.settings import *
import random


class EnemyShooter(EnemyCollision):
    def __init__(self, x, y, theMap=None, direction="Right"):
        super().__init__(x, y)

        self.name = "enemyShooter"

        self.imageEnemy = pygame.image.load(os.path.join('img', 'shooting_enemy.png'))

        self.frames = [self.imageEnemy]
        self.animation = Animation(self,self.frames,20)

        self.rect = self.imageEnemy.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speedx = 0
        self.speedy = 0
        self.maxSpeedx = 2
        self.maxSpeedy = 2

        self.mapData = theMap

        self.setDirection(direction)

        self.isGravityApplied = True
        self.isCollisionApplied = True

        self.imageWaitNextShoot = 30

        # self.imageIterShoot = random.randint(10, (self.imageWaitNextShoot - 10))  # To shoot bullets at random pace
        self.imageIterShoot = 0

        self.dictProperties = {'direction': self.setDirection}

        self.AI = SteeringAI(self.mapData, self.rect, self.speedx, self.speedy)

    def setDirection(self, direction):
        if direction is "Right":
            self.direction = "Right"
        else:
            self.direction = "Left"

    def setTheMap(self, theMap):
        self.mapData = theMap

    def applyAI(self):
        steeringX, steeringY = self.AI.getAction()

        distx = self.mapData.player.rect.x - self.rect.x
        disty = self.mapData.player.rect.y - self.rect.y

        distance = distx + disty

        self.imageIterShoot += 1

        if distance < 100:
            if self.imageIterShoot > self.imageWaitNextShoot:
                speedx_bullet = self.speedx * 2 + steeringX
                speedy_bullet = self.speedy * 2 + steeringY
                bullet = Shuriken(self.rect.centerx, self.rect.centery, speedx_bullet, speedy_bullet, False)

                self.mapData.camera.add(bullet)
                self.mapData.allSprites.add(bullet)
                self.mapData.enemyBullet.add(bullet)

                self.imageIterShoot = 0

        self.speedx += steeringX
        self.speedy += steeringY
        
    def update(self):
        super().update()

        self.capSpeed()

        self.rect.x += self.speedx
        self.rect.y += self.speedy

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
        super().dead(self)