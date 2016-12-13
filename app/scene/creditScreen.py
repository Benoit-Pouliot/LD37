import os
import pygame

from app.settings import *
from app.tools.functionTools import *
from app.tools.messageBox.messageBox import MessageBox
from app.scene.drawer import Drawer

from app.sprites.GUI.button import Button
import weakref


class CreditScreen:
    def __init__(self, screen, gameData=None):
        self.screen = screen

        self.gameData = gameData
        self.allSprites = pygame.sprite.Group()
        self.spritesHUD = pygame.sprite.Group()
        self.notifySet = weakref.WeakSet()

        self.drawer = Drawer()

        self.screen.fill((0,0,0))
        titleImage = pygame.image.load(os.path.join('img', 'TitleScreen.png'))
        self.screen.blit(titleImage, (0, 0))

        self.createControlBox(60, SCREEN_HEIGHT / 10, 0.55*SCREEN_WIDTH, 4 * SCREEN_HEIGHT / 5)

        self.backToTitleScreenButton = Button((520, 17 * SCREEN_HEIGHT / 20), (250, 50), 'Back to main menu', self.goToTitleScreen)
        self.spritesHUD.add(self.backToTitleScreenButton)
        self.notifySet.add(self.backToTitleScreenButton)



        self.type = CREDIT_SCREEN
        self.nextScene = None

    def mainLoop(self):
        self.sceneRunning = True
        while self.sceneRunning:
            self.eventHandle(self.notifySet)
            self.handle()  # This would be in the logic
            self.drawer.draw(self.screen, None, self.spritesHUD, None,self.allSprites)

    def handle(self):
        self.checkHighlight()
        self.allSprites.update()
        self.spritesHUD.update()

    def checkHighlight(self):
        mousePos = pygame.mouse.get_pos()
        for obj in self.notifySet:
            if obj.rect.collidepoint(mousePos):
                obj.isSelected = True
            else:
                obj.isSelected = False

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


    def createControlBox(self,x,y,width,height):
        self.textGoal = MessageBox(x,y,width,height)
        self.textGoal.textList.append('For Ludum Dare 37')
        self.textGoal.textList.append('')
        self.textGoal.textList.append('')
        self.textGoal.textList.append('Credit :')
        self.textGoal.textList.append('')
        self.textGoal.textList.append('Game and design : Bobsleigh\'s team')
        self.textGoal.textList.append('')
        self.textGoal.textList.append('Music : ')
        self.textGoal.textList.append('')
        self.textGoal.textList.append('Night by Paulius Jurgelevièius')
        self.textGoal.textList.append('Inspiration by Paulius Jurgelevièius')

        self.allSprites.add(self.textGoal)  # Add sprite

    def goToTitleScreen(self):
        self.nextScene = TITLE_SCREEN
        self.sceneRunning = False
        self.gameData.typeScene = TITLE_SCREEN
        self.gameData.mapData = None