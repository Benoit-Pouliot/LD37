import pygame
from app.settings import *

class StatDisplay:
    def __init__(self,screen,pos,font,statName=None, textColor=HUD_FONT_COLOR):
        self.screen = screen
        self.stat = None
        self.statName = statName
        self.printedLine = None
        self.position = pos
        self.font = font
        self.textColor = textColor
        self.stat2 = None

    def printText(self):
        if self.statName is None:
            self.printedLine = self.font.render(str(self.stat), True, self.textColor)
        else:
            self.printedLine = self.font.render(self.statName + ' : ' + self.stat, True, self.textColor)

        self.screen.blit(self.printedLine, self.position)