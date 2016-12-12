import pygame
import os

from app.settings import *
from app.sprites.collisionMask import CollisionMask


class Item(pygame.sprite.Sprite):
    def __init__(self,name,method, type=None,image=os.path.join('img', 'mine1.png')):
        super().__init__()

        self.name = name
        self.method = method
        self.specialAttributeNum = 0

        # self.image = pygame.transform.scale(pygame.image.load(image), (TILEDIMX, TILEDIMY))
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

        self.type = type

    def useItem(self):
        # self.soundSelect.play(0)
        self.method()