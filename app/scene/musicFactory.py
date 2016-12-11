import pygame
import os
from app.settings import *


class MusicFactory:
    def __init__(self, typeScene=None, secondOption=None):

        self.nameMusic = None
        if typeScene == TITLE_SCREEN:
            self.nameMusic = 'MainTheme'
        elif typeScene == PLATFORM_SCREEN:
            if secondOption >= 1:
                self.nameMusic = 'TheLoomingBattle'
        elif typeScene == SHOP_SCREEN:
            self.nameMusic = 'MainTheme'

        if self.nameMusic is not None:
            if self.nameMusic == 'TheLoomingBattle':
                pygame.mixer.music.load(os.path.join('music_pcm', self.nameMusic + '.ogg'))
            else:
                pygame.mixer.music.load(os.path.join('music_pcm', self.nameMusic + '.wav'))
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()

