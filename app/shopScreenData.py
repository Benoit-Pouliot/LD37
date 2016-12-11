
import pygame
from app.settings import *
import os

import weakref
# from app.sound.soundPlayerController import *
# from app.sprites.player import *

class ShopScreenData:
    def __init__(self, mapName="WorldMap", nameInZone="StartPointWorld", screenSize=(SCREEN_WIDTH, SCREEN_HEIGHT)):

        self.allSprites = pygame.sprite.Group()
        self.spritesHUD = pygame.sprite.Group()
        # Set of all object that needs to be notified of events.
        # Weak references are used to prevent this set from keeping objects alive

        self.notifySet = weakref.WeakSet()