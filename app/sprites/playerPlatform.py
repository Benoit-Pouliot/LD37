import pygame
import os, math

from app.settings import *
from app.sprites.barricade import Barricade
from app.sprites.bullet import Bullet
from app.sprites.collisionMask import CollisionMask
from app.sprites.inventory import Inventory
from app.sprites.target import Target


class PlayerPlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, mapData):
        super().__init__()

        self.name = "player"

        self.imageBase=pygame.transform.scale(pygame.image.load(os.path.join('img', 'joueur_droite.png')), (20,20))

        self.imageShapeLeft = None
        self.imageShapeRight = None

        self.setShapeImage()
        self.image = self.imageShapeRight

        self.imageTransparent = pygame.Surface((1,1))
        self.imageTransparent.set_colorkey(BLACK)

        self.rect = self.image.get_rect() #Position centrée du player
        self.rect.x = x
        self.rect.y = y

        self.speedx = 0
        self.speedy = 0
        self.maxSpeedx = 5
        self.maxSpeedyUp = 5
        self.maxSpeedyDown = 5
        self.accx = 2
        self.accy = 2

        self.isPhysicsApplied = True
        self.isCollisionApplied = True
        self.facingSide = RIGHT

        self.life = 1
        self.lifeMax = 1
        self.lifeMaxCap = 5
        self.isInvincible = False
        self.invincibleFrameCounter = [0,0] #Timer,flashes nb
        self.invincibleTimer = 20 #Must be even number
        self.invincibleNbFlashes = 5

        self.rightPressed = False
        self.leftPressed = False
        self.upPressed = False
        self.downPressed = False

        self.mapData = mapData
        self.mapData.player = self

        self.target = Target(0,0)
        self.mapData.camera.add(self.target)
        self.mapData.allSprites.add(self.target)

        self.isAlive = True

        self.currentItem = 0

        if TAG_MARIE == 1:
            self.currentItem = 1

        self.inventory = Inventory()
        self.inventory.addItem('gun',self.shootBullet)
        self.inventory.addItem('barricade',self.createBarricade)

        #Link your own sounds here
        #self.soundSpring = pygame.mixer.Sound(os.path.join('music_pcm', 'LvlUpFail.wav'))
        #self.soundBullet = pygame.mixer.Sound(os.path.join('music_pcm', 'Gun.wav'))
        #self.soundGetHit = pygame.mixer.Sound(os.path.join('music_pcm', 'brokenGlass.wav'))
        #self.soundSpring.set_volume(1)
        #self.soundBullet.set_volume(.3)
        #self.soundGetHit.set_volume(.3)

        self.collisionMask = CollisionMask(self.rect.x + 3, self.rect.y, self.rect.width-6, self.rect.height)

    def setShapeImage(self):
        self.imageShapeLeft = pygame.transform.flip(self.imageBase, True, False)
        self.imageShapeRight = self.imageBase


    def update(self):
        self.capSpeed()
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.speedx > 0:
            self.image = self.imageShapeRight
            self.facingSide = RIGHT
        if self.speedx < 0:
            self.image = self.imageShapeLeft
            self.facingSide = LEFT

        self.invincibleUpdate()
        self.updateCollisionMask()
        self.updatePressedKeys()
        self.updateTarget()

    def capSpeed(self):
        if self.speedx > 0 and self.speedx > self.maxSpeedx:
            self.speedx = self.maxSpeedx
        if self.speedx < 0 and self.speedx < -self.maxSpeedx:
            self.speedx = -self.maxSpeedx
        if self.speedy > 0 and self.speedy > self.maxSpeedyDown:
            self.speedy = self.maxSpeedyDown
        if self.speedy < 0 and self.speedy < -self.maxSpeedyUp:
            self.speedy = -self.maxSpeedyUp

    def updateSpeedRight(self):
        self.speedx += self.accx

    def updateSpeedLeft(self):
        self.speedx -= self.accx

    def updateSpeedUp(self):
        self.speedy -= self.accy

    def updateSpeedDown(self):
        self.speedy += self.accy

    def updateCollisionMask(self):
        self.collisionMask.rect.x = self.rect.x
        self.collisionMask.rect.y = self.rect.y

    def updateTarget(self):
        mousePos = pygame.mouse.get_pos()

        diffx = mousePos[0]+self.mapData.cameraPlayer.view_rect.x-self.rect.centerx
        diffy = mousePos[1]+self.mapData.cameraPlayer.view_rect.y-self.rect.centery

        self.target.rect.centerx = TARGET_DISTANCE*(diffx)/self.vectorNorm(diffx,diffy) + self.rect.centerx
        self.target.rect.centery = TARGET_DISTANCE*(diffy)/self.vectorNorm(diffx,diffy) + self.rect.centery

        self.target.powerx = (diffx)/self.vectorNorm(diffx,diffy)
        self.target.powery = (diffy)/self.vectorNorm(diffx,diffy)

        angleRad = math.atan2(diffy, diffx)
        self.target.image = pygame.transform.rotate(self.target.imageOrig, -angleRad/math.pi*180)
        self.image = pygame.transform.rotate(self.imageBase, -angleRad/math.pi*180)

    def vectorNorm(self,x,y):
        return math.sqrt(x**2+y**2)

    def gainLife(self):
        if self.life < self.lifeMax:
            self.life = self.lifeMax

    def gainLifeMax(self):
        if self.lifeMax < self.lifeMaxCap:
            self.lifeMax += 1
            self.life = self.lifeMax
        else:
            self.lifeMax = self.lifeMaxCap
            self.life = self.lifeMax

    def knockedBack(self):
        #Can break collision ATM
        if self.speedx == 0:
            self.speedx = self.maxSpeedx

        self.speedx = (-self.speedx/abs(self.speedx)) * self.maxSpeedx
        self.speedy = (-self.speedy/abs(self.speedx)) * self.maxSpeedx

    def invincibleOnHit(self):
        self.isInvincible = True
        self.invincibleFrameCounter[0] = 1

    def invincibleUpdate(self):
        if self.invincibleFrameCounter[0] > 0 and self.invincibleFrameCounter[1] < self.invincibleNbFlashes:
            self.invincibleFrameCounter[0] += 1
            if self.invincibleFrameCounter[0]== self.invincibleTimer:
                self.invincibleFrameCounter[0] = 1
                self.invincibleFrameCounter[1] +=1

        elif self.invincibleFrameCounter[1] == self.invincibleNbFlashes:
            self.isInvincible = False
            self.invincibleFrameCounter = [0,0]
        self.visualFlash()

    def dead(self):
        self.isAlive = False

    def pickedPowerUpMaxHealth(self):
        self.gainLifeMax()

    def pickedPowerUpHealth(self):
        self.gainLife()

    def visualFlash(self):
        if self.invincibleFrameCounter[0] == 5:
            self.imageShapeLeft = self.imageTransparent
            self.imageShapeRight = self.imageTransparent
            self.image = self.imageTransparent
        elif self.invincibleFrameCounter[0] == 15:
            self.setShapeImage()
            if self.facingSide == RIGHT:
                self.image = self.imageShapeRight
            else:
                self.image = self.imageShapeLeft

    def shootBullet(self):
        if self.facingSide == RIGHT:
            bullet = Bullet(self.rect.x + self.rect.width +1, self.rect.centery, self.facingSide)
        else:
            bullet = Bullet(self.rect.x -1, self.rect.centery, self.facingSide)
        self.mapData.camera.add(bullet)
        self.mapData.allSprites.add(bullet)
        self.mapData.friendlyBullet.add(bullet)

    def createBarricade(self):
        if TAG_MARIE == 1:
            print('You created a barricade.')
        mousePos = pygame.mouse.get_pos()

        diffx = mousePos[0] + self.mapData.cameraPlayer.view_rect.x - self.rect.centerx
        diffy = mousePos[1] + self.mapData.cameraPlayer.view_rect.y - self.rect.centery

        barricadePosx = BARRICADE_DISTANCE * (diffx) / self.vectorNorm(diffx, diffy) + self.rect.centerx
        barricadePosy = BARRICADE_DISTANCE * (diffy) / self.vectorNorm(diffx, diffy) + self.rect.centery

        barricade = Barricade(barricadePosx,barricadePosy)

        occupied = pygame.sprite.spritecollideany(barricade, self.mapData.allSprites)

        if occupied is None:
            self.mapData.camera.add(barricade)
            self.mapData.allSprites.add(barricade)
            self.mapData.obstacleGroup.add(barricade)

        else:
            print('cannot put down')
            barricade.destroy()

    def onCollision(self, collidedWith, sideOfCollision,objectSize=0):
        if collidedWith == SOLID:
            if sideOfCollision == RIGHT:
                #On colle le player sur le mur à droite
                self.speedx = 0
                self.collisionMask.rect.right += self.mapData.tmxData.tilewidth - (self.collisionMask.rect.right % self.mapData.tmxData.tilewidth) - 1
            if sideOfCollision == LEFT:
                self.speedx = 0
                self.collisionMask.rect.left -= (self.collisionMask.rect.left % self.mapData.tmxData.tilewidth)  # On colle le player sur le mur de gauche
            if sideOfCollision == DOWN:
                self.speedy = 0
            if sideOfCollision == UP:
                # Coller le player sur le plafond
                while self.mapData.tmxData.get_tile_gid((self.collisionMask.rect.left + 1) / self.mapData.tmxData.tilewidth,
                                               (self.collisionMask.rect.top) / self.mapData.tmxData.tileheight,
                                               COLLISION_LAYER) != SOLID and self.mapData.tmxData.get_tile_gid(
                                                self.collisionMask.rect.right / self.mapData.tmxData.tilewidth,
                                                (self.collisionMask.rect.top) / self.mapData.tmxData.tileheight, COLLISION_LAYER) != SOLID:
                    self.collisionMask.rect.bottom -= 1
                self.collisionMask.rect.bottom += 1  # Redescendre de 1 pour sortir du plafond
                self.speedy = 0

        if collidedWith == SPIKE:
            self.dead()

        if collidedWith == OBSTACLE:
            if sideOfCollision == RIGHT:
                if TAG_MARIE == 1:
                    print(objectSize)
                #On colle le player à gauche de l'obstacle
                self.speedx = 0
                self.rect.right += -2


            if sideOfCollision == LEFT:
                self.speedx = 0
                self.rect.left += 2
            if sideOfCollision == DOWN:
                self.speedy = 0
                self.rect.bottom += -2

            if sideOfCollision == UP:
                self.speedy = 0
                self.rect.top += 2

    def nextItem(self):
        self.currentItem += 1
        if self.currentItem >= len(self.inventory.itemList):
            self.currentItem = 0

    def hurt(self):
        if not self.isInvincible:
            self.invincibleOnHit()
            self.visualFlash()

    def notify(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.updateSpeedRight()
                self.rightPressed = True
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.updateSpeedLeft()
                self.leftPressed = True
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                self.updateSpeedUp()
                self.upPressed = True
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.updateSpeedDown()
                self.downPressed = True
            elif event.key == pygame.K_SPACE:
                self.nextItem()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.rightPressed = False
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.leftPressed = False
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                self.upPressed = False
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.downPressed = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            self.inventory.itemList[self.currentItem].useItem()
            if TAG_MARIE == 1 :
                print("You pressed the left mouse button") # event.pos


    def updatePressedKeys(self):
        if self.rightPressed:
            self.updateSpeedRight()
        if self.leftPressed:
            self.updateSpeedLeft()
        if self.upPressed:
            self.updateSpeedUp()
        if self.downPressed:
            self.updateSpeedDown()
