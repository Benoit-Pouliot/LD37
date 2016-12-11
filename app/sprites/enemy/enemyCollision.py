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

class EnemyCollision(Enemy):
    def __init__(self, x, y):  # ?
        super().__init__(x, y)


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
