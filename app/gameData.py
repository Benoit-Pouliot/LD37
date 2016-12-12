from app.settings import *

#To initialize my pet
import os
import pygame


# All the global data for the game and player
class GameData:
    def __init__(self, scene=None):

        #Was map unlocked?
        self.upgrade = {} #Give [attributeName,attributeNumber,cost,attributeUpper,costUpper]
        self.upgrade["gun"] = ['Level',1,100,1,1.1]
        self.upgrade["barricade"] = ['Level',0,50,1,1.1]
        self.upgrade["grenade"] = ['Level',0,400,1,1.1]
        self.upgrade["mine"] = ['Level',0,900,1,1.1]
        self.upgrade["gunCooldown"] = ['Cooldown', 40, 1, 0.9, 1.1]
        self.upgrade["barricadeCooldown"] = ['Cooldown', 300, 2, 0.9, 1.2]
        self.upgrade["grenadeCooldown"] = ['Cooldown', 100, 200, 0.9, 1.3]
        self.upgrade["mineCooldown"] = ['Cooldown', 40, 200, 0.9, 1.4]

        self.gold = 50

        if TAG_MARIE == 1:
            self.gold = 10000

        self.maxItemOfAType = 99

        self.scene = scene

        self.mapData = None
        self.shopScreenData = None

        self.currentLevel = 1

        #self.initLevel(6)

    def initLevel(self, level):

        if level == 1:
            self.gold = 50
        elif level == 2:
            self.gold = 160
        elif level == 3:
            self.gold = 370
        elif level == 4:
            self.gold = 20000
        elif level == 6:
            self.gold = 9999999

        self.currentLevel = level