import pygame
import os
from app.sprites.upgrade.upgrade import Upgrade

from app.settings import *
from app.sprites.collisionMask import CollisionMask


class MineCooldown(Upgrade):
    def __init__(self):
        super().__init__()

        self.name = 'mineCooldown'

        self.icon = pygame.image.load(os.path.join('img', 'biere1.png'))

        # self.image = pygame.transform.scale(pygame.image.load(image), (TILEDIMX, TILEDIMY))

        self.type = type

    def useItem(self):
        # self.soundSelect.play(0)
        self.method()