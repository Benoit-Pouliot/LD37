import pygame
import os
from app.sprites.upgrade.upgrade import Upgrade

from app.settings import *
from app.sprites.collisionMask import CollisionMask


class Gun(Upgrade):
    def __init__(self):
        super().__init__()

        self.name = 'gun'

        self.icon = pygame.image.load(os.path.join('img', 'bullet.png'))

        self.resizeIcon()

        self.type = type

    def useItem(self):
        # self.soundSelect.play(0)
        self.method()
