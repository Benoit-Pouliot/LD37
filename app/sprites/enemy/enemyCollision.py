import pygame
import os
import math
from app.sprites.enemy.enemy import Enemy
from app.sprites.GUI.lifeBar import LifeBar

from app.settings import *

class EnemyCollision(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.soundDead = pygame.mixer.Sound(os.path.join('music_pcm', 'Punch2.wav'))
        self.soundDead.set_volume(1)

    def update(self):
        self.updateLifeBar()
        self.checkIfIsAlive()
        super().update()

    def generateLifeBar(self, health=1):
        self.maxHealth = health
        self.lifeBar = LifeBar(health, self.rect.width)
        self.mapData.allSprites.add(self.lifeBar)
        self.mapData.camera.add(self.lifeBar, layer=CAMERA_HUD_LAYER)
        self.lifeBar.rect.x = self.rect.x
        self.lifeBar.rect.bottom = self.rect.top - 3

    def updateLifeBar(self):
        self.lifeBar.rect.x = self.rect.x
        self.lifeBar.rect.bottom = self.rect.top - 3

    def isHit(self, dmg):
        self.lifeBar.healthCurrent -= dmg

    def checkIfIsAlive(self):
        if self.lifeBar.healthCurrent <= 0:
            self.dead()

    def dead(self):
        self.soundDead.play()
        self.lifeBar.kill()
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
                self.collisionMask.rect.left -= (self.collisionMask.rect.left % self.mapData.tmxData.tilewidth)  # On colle la sprite sur le mur à gauche PAS UTILISÉ?? PCQ COLLISION MASK ET NON RECT DE LENNEMI
            elif sideOfCollision == DOWN:
                self.speedy = 0
                # while self.mapData.tmxData.get_tile_gid(
                #                 (self.collisionMask.rect.left + 1) / self.mapData.tmxData.tilewidth,
                #                 (self.collisionMask.rect.bottom) / self.mapData.tmxData.tileheight,
                #                 COLLISION_LAYER) != SOLID and self.mapData.tmxData.get_tile_gid(
                #             self.collisionMask.rect.right / self.mapData.tmxData.tilewidth,
                #             (self.collisionMask.rect.bottom) / self.mapData.tmxData.tileheight, COLLISION_LAYER) != SOLID:
                #     self.collisionMask.rect.top += 1
                # self.collisionMask.rect.top -= 1  # Redescendre de 1 pour sortir du plafond

            elif sideOfCollision == UP:
                # Coller le player sur le plafond
                # while self.mapData.tmxData.get_tile_gid(
                #                 (self.collisionMask.rect.left + 1) / self.mapData.tmxData.tilewidth,
                #                 (self.collisionMask.rect.top) / self.mapData.tmxData.tileheight,
                #                 COLLISION_LAYER) != SOLID and self.mapData.tmxData.get_tile_gid(
                #             self.collisionMask.rect.right / self.mapData.tmxData.tilewidth,
                #             (self.collisionMask.rect.top) / self.mapData.tmxData.tileheight, COLLISION_LAYER) != SOLID:
                #     self.collisionMask.rect.bottom -= 1
                # self.collisionMask.rect.bottom += 1  # Redescendre de 1 pour sortir du plafond
                self.speedy = 0


        if collidedWith == OBSTACLE:
            if sideOfCollision == RIGHT:
                #On colle le sprite à gauche de l'obstacle
                self.speedx = 0
                self.rect.right = limit
            if sideOfCollision == LEFT:
                self.speedx = 0
                self.rect.left = limit
            if sideOfCollision == DOWN:
                self.speedy = 0
                self.rect.bottom = limit

            if sideOfCollision == UP:
                self.speedy = 0
                self.rect.top = limit
