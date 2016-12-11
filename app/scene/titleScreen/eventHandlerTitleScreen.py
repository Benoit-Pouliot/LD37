import pygame
from app.tools.functionTools import *


class EventHandlerTitleScreen():
    def __init__(self):
        self.menuPause = None

    def eventHandle(self,notifySet):
        self.notifySet = notifySet
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    pass
                    #self.menuPause.mainLoop()
                # elif event.key == pygame.K_ESCAPE:
                #     self.menuPause.mainLoop()

            for obj in self.notifySet:
                obj.notify(event)



