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
        self.upgrade["barricade"] = ['Level',0,25,1,1.1]
        self.upgrade["grenade"] = ['Level',0,400,1,1.1]
        self.upgrade["mine"] = ['Level',0,400,1,1.1]
        self.upgrade["gunCooldown"] = ['Cooldown', 40, 40, 0.9, 1.1]
        self.upgrade["barricadeCooldown"] = ['Cooldown', 175, 25, 0.9, 1.2]
        self.upgrade["grenadeCooldown"] = ['Cooldown', 100, 150, 0.9, 1.3]
        self.upgrade["mineCooldown"] = ['Cooldown', 100, 50, 0.9, 1.4]

        self.gold = 50

        if TAG_MARIE == 1:
            self.gold = 10000
        if TAG_BP == 1:
            self.gold = 100000000

        self.maxItemOfAType = 99

        self.scene = scene

        self.mapData = None
        self.shopScreenData = None

        self.currentLevel = 1

        #self.initLevel(5)

    def initLevel(self, level):

        if level == 1:
            self.gold = 50
        elif level == 2:
            self.gold = 160
        elif level == 3:
            self.gold = 370
        elif level == 4:
            self.gold = 880
        elif level == 5:
            self.gold = 1790
        elif level == 6:
            self.gold = 9999999

        self.currentLevel = level