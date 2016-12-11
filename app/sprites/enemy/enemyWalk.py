import pygame
import os
import math

from app.sprites.enemy.enemy import Enemy
from app.sprites.enemy.enemyAttack import EnemyAttack
from app.tools.animation import Animation
from app.AI.steeringAI import SteeringAI

from app.settings import *

class EnemyWalk(Enemy):
    def __init__(self, x, y, mapData=None):  # ?
        super().__init__(x, y)

        self.name = "enemyWalk"

        self.imageEnemy = pygame.image.load(os.path.join('img', 'walking_enemy.png'))

        self.frames = [self.imageEnemy]
        self.animation = Animation(self,self.frames,100)

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

        self.attackDMG = 1

        self.mode = WALKING
        self.timerAttack = 0
        self.timeToAttack = 60
        self.timeInAttack = 5
        self.distanceToAttack = 25
        self.attackSprite = None

    def applyAI(self):

        if self.mode == IN_ATTACK:
            if self.timerAttack == 0:
                self.timerAttack += 1

                # create an invisible sprite that damage player
                self.attackSprite = EnemyAttack(self.rect.x, self.rect.y, (self.image.get_width(), self.image.get_height()), self.attackDMG)
                self.attackSprite.setMapData(self.mapData)

                # do an animation? TODO

                # self.soundAttack.play()

            elif self.timerAttack < self.timeInAttack:
                    self.timerAttack +=1
            else:
                self.timerAttack = 0
                self.mode = WALKING
                self.AI = SteeringAI(self.mapData, self.rect, self.speedx, self.speedy)
                self.attackSprite.kill()

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
                self.mode = PREPARE_ATTACK
                self.timerAttack = 0
                self.speedx = 0
                self.speedy = 0
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

    def onCollision(self, collidedWith, sideOfCollision,limit=0):
        if collidedWith == SOLID:
            if sideOfCollision == RIGHT:
                # On colle la sprite sur le mur à droite
                self.speedx = 0
                self.collisionMask.rect.right += self.mapData.tmxData.tilewidth - (
                self.collisionMask.rect.right % self.mapData.tmxData.tilewidth) - 1
            elif sideOfCollision == LEFT:
                self.speedx = 0
                self.collisionMask.rect.left -= (
                self.collisionMask.rect.left % self.mapData.tmxData.tilewidth)  # On colle la sprite sur le mur à gauche
            elif sideOfCollision == DOWN:
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
