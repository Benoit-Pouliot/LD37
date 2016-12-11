import pygame
from app.settings import *

class Drawer:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.FPS = FPS

    def draw(self, screen, camera, spritesHUD, player,otherSprite=None):

        if camera != None:
            camera.center((player.rect.centerx, player.rect.centery - (HUD_HEIGHT / 2)))
            camera.draw(screen)

        if otherSprite != None:
            otherSprite.draw(screen)

        spritesHUD.draw(screen)
        pygame.display.flip()
        self.clock.tick(self.FPS)
