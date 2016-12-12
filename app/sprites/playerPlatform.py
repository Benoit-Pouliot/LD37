import pygame
import os
import math

from app.settings import *
from app.sprites.barricade import Barricade
from app.sprites.bullet import PlayerBullet
from app.sprites.collisionMask import CollisionMask
from app.sprites.inventory import Inventory
from app.sprites.target import Target
from app.sprites.grenade import Grenade
from app.tools.cooldown import Cooldown
from app.tools.imageBox import *
from app.sprites.mine import Mine
from app.sprites.GUI.lifeBar import LifeBar


class PlayerPlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, gameData, max_health=10):
        super().__init__()

        self.name = "player"

        self.imageBase = rectSurface((PLAYER_DIMX, PLAYER_DIMY), BLUE, 3)
        self.imageBase.set_colorkey(COLORKEY)

        self.imageShapeLeft = None
        self.imageShapeRight = None

        self.setShapeImage()
        self.image = self.imageShapeRight

        self.imageTransparent = rectSurface((PLAYER_DIMX, PLAYER_DIMY), WHITE, 3)
        self.imageTransparent.set_colorkey(COLORKEY)

        self.rect = self.image.get_rect()  # Position centrée du player
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

        self.speedx = 0
        self.speedy = 0
        self.maxSpeedx = 3
        self.maxSpeedy = 3
        self.accx = 2
        self.accy = 2

        self.isPhysicsApplied = True
        self.isCollisionApplied = True
        self.facingSide = RIGHT
        self.friendly = True

        self.maxHealth = max_health
        self.lifeBar = LifeBar(max_health)

        self.hurtSound = pygame.mixer.Sound(os.path.join('music_pcm', 'Hit_Hurt.wav'))
        self.hurtSound.set_volume(.25)

        self.soundShootGun = pygame.mixer.Sound(os.path.join('music_pcm', 'Laser_Shoot.wav'))
        self.soundShootGun.set_volume(.25)
        self.soundShootGrenade = pygame.mixer.Sound(os.path.join('music_pcm', 'Grenade_Shoot.wav'))
        self.soundShootGrenade.set_volume(.25)
        self.soundBarricade = pygame.mixer.Sound(os.path.join('music_pcm', 'Hit_Hurt.wav'))
        self.soundBarricade.set_volume(.25)
        self.soundPlaceMine = pygame.mixer.Sound(os.path.join('music_pcm', 'placeMine.wav'))
        self.soundPlaceMine.set_volume(.15)

        self.life = 1
        self.lifeMax = 1
        self.lifeMaxCap = 5
        self.isInvincible = False
        self.invincibleFrameCounter = [0, 0]  # Timer, flashes nb
        self.invincibleTimer = 20  # Must be even number
        self.invincibleNbFlashes = 5

        self.rightPressed = False
        self.leftPressed = False
        self.upPressed = False
        self.downPressed = False
        self.leftShiftPressed = False
        self.spacePressed = False
        self.leftMousePressed = False
        self.rightMousePressed = False

        self.mapData = gameData.mapData
        self.mapData.player = self
        self.gameData = gameData

        self.target = Target(0, 0)
        self.mapData.camera.add(self.target)

        self.grenadeCooldown = Cooldown(self.gameData.upgrade['grenadeCooldown'][1])
        self.mineCooldown = Cooldown(self.gameData.upgrade['mineCooldown'][1])
        self.gunCooldown = Cooldown(self.gameData.upgrade['gunCooldown'][1])
        self.barricadeCooldown = Cooldown(self.gameData.upgrade['barricadeCooldown'][1])

        self.isAlive = True

        self.barricadeMaxHeath = 10
        self.barricadeCharges = 2
        self.barricadeChargesMax = 2

        self.currentItem = 0

        if TAG_BP == 2:
            self.spriteRED = None

        self.inventory = Inventory()

        if self.gameData.upgrade['gun'][1]>0:
            self.inventory.addItem('gun', self.shootBullet)
        if self.gameData.upgrade['grenade'][1]>0:
            self.inventory.addItem('grenade', self.shootGrenade)
        if self.gameData.upgrade['mine'][1]>0:
            self.inventory.addItem('mine', self.shootMine)

        # Link your own sounds here
        # self.soundSpring = pygame.mixer.Sound(os.path.join('music_pcm', 'LvlUpFail.wav'))
        # self.soundBullet = pygame.mixer.Sound(os.path.join('music_pcm', 'Gun.wav'))
        # self.soundGetHit = pygame.mixer.Sound(os.path.join('music_pcm', 'brokenGlass.wav'))
        # self.soundSpring.set_volume(1)
        # self.soundBullet.set_volume(.3)
        # self.soundGetHit.set_volume(.3)

        self.collisionMask = CollisionMask(self.rect.x + 3, self.rect.y, self.rect.width-6, self.rect.height)

    def setShapeImage(self):
        self.imageShapeLeft = pygame.transform.flip(self.imageBase, True, False)
        self.imageShapeRight = self.imageBase

    def update(self):
        self.capSpeed()

        self.x += self.speedx
        self.y += self.speedy
        self.rect.x = self.x
        self.rect.y = self.y


        if TAG_BP == 2:
            if self.spriteRED is not None:
                self.spriteRED.kill()
            self.spriteRED = pygame.sprite.Sprite()
            self.spriteRED.image = pygame.Surface((300,300), pygame.SRCALPHA, 32)
            pygame.draw.circle(self.spriteRED.image, RED, [150, 150], 150,5)
            self.spriteRED.rect = self.spriteRED.image.get_rect()
            self.spriteRED.rect.x = self.rect.centerx-150
            self.spriteRED.rect.y = self.rect.centery-150
            self.mapData.camera.add(self.spriteRED)
            self.mapData.allSprites.add(self.spriteRED)
            self.spriteRED.isPhysicsApplied = False
            self.spriteRED.isCollisionApplied = False


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
        self.updateCooldowns()

    def capSpeed(self):
        if self.speedx > 0 and self.speedx > self.maxSpeedx:
            self.speedx = self.maxSpeedx
        if self.speedx < 0 and self.speedx < -self.maxSpeedx:
            self.speedx = -self.maxSpeedx
        if self.speedy > 0 and self.speedy > self.maxSpeedy:
            self.speedy = self.maxSpeedy
        if self.speedy < 0 and self.speedy < -self.maxSpeedy:
            self.speedy = -self.maxSpeedy

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

    def updateCooldowns(self):
        self.grenadeCooldown.update()
        self.mineCooldown.update()
        self.gunCooldown.update()
        self.barricadeCooldown.update()

        if self.barricadeCharges < self.barricadeChargesMax and self.barricadeCooldown.isZero:
            self.barricadeCharges += 1
            if self.barricadeCharges < self.barricadeChargesMax:
                self.barricadeCooldown.start()


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

        # self.image = self.rot_center(self.imageBase, -angleRad/math.pi*180)
        self.image = pygame.transform.rotate(self.imageBase, -angleRad/math.pi*180)

    def vectorNorm(self,x,y):
        return math.sqrt(x**2+y**2+EPS)

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
        # Can break collision ATM
        if self.speedx == 0:
            self.speedx = self.maxSpeedx

        self.speedx = (-self.speedx/abs(self.speedx)) * self.maxSpeedx
        self.speedy = (-self.speedy/abs(self.speedx)) * self.maxSpeedx

    def stop(self):
        self.speedx = 0
        self.speedy = 0

    def invincibleOnHit(self):
        self.isInvincible = True
        if TAG_ANIKA == 1:
            print('invincibility activated')
        self.invincibleFrameCounter[0] = 1

    def invincibleUpdate(self):
        if self.invincibleFrameCounter[0] > 0 and self.invincibleFrameCounter[1] < self.invincibleNbFlashes:
            self.invincibleFrameCounter[0] += 1
            if self.invincibleFrameCounter[0]== self.invincibleTimer:
                self.invincibleFrameCounter[0] = 1
                self.invincibleFrameCounter[1] +=1

        elif self.invincibleFrameCounter[1] == self.invincibleNbFlashes:
            self.isInvincible = False
            if TAG_ANIKA == 1:
                print('player is no more invincible')
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
            self.imageBase = self.imageTransparent
            self.image = self.imageTransparent
        elif self.invincibleFrameCounter[0] == 15:
            self.imageBase = rectSurface((PLAYER_DIMX, PLAYER_DIMY), BLUE, 3)
            self.imageBase.set_colorkey(COLORKEY)
            self.setShapeImage()

    def shootBullet(self):
        if self.gunCooldown.isZero:
            self.soundShootGun.play()
            speedx, speedy = self.power2speed(10)

            bullet = PlayerBullet(self.rect.centerx, self.rect.centery, speedx, speedy, self.gameData)
            self.mapData.camera.add(bullet)
            self.mapData.allSprites.add(bullet)
            self.mapData.friendlyBullet.add(bullet)

            self.gunCooldown.start()

    def shootGrenade(self):
        if self.gameData.upgrade['grenade'][1] > 0:
            if self.grenadeCooldown.isZero:
                self.soundShootGrenade.play()
                speedx, speedy = self.power2speed(8)

                grenade = Grenade(self.rect.centerx, self.rect.centery, speedx, speedy, self.gameData)

                self.mapData.camera.add(grenade)
                self.mapData.allSprites.add(grenade)
                self.mapData.friendlyBullet.add(grenade)

                self.grenadeCooldown.start()

    def shootMine(self):
        if self.gameData.upgrade['mine'][1] > 0:
            if self.mineCooldown.isZero:
                self.soundPlaceMine.play()
                mine = Mine(self.rect.centerx, self.rect.centery, self.gameData)

                self.mapData.camera.add(mine)
                self.mapData.allSprites.add(mine)
                self.mapData.mineGroup.add(mine)

                self.mineCooldown.start()


    def power2speed(self, rawPowerValue):

        speedx = self.target.powerx*rawPowerValue
        speedy = self.target.powery*rawPowerValue
        return speedx, speedy

    def createBarricade(self):
        #self.stop()
        if self.gameData.upgrade['barricade'][1] > 0 and self.barricadeCharges > 0:

            mousePos = pygame.mouse.get_pos()

            diffx = mousePos[0] + self.mapData.cameraPlayer.view_rect.x - self.rect.centerx
            diffy = mousePos[1] + self.mapData.cameraPlayer.view_rect.y - self.rect.centery

            barricadePosx = BARRICADE_DISTANCE * (diffx) / self.vectorNorm(diffx, diffy) + self.rect.centerx
            barricadePosy = BARRICADE_DISTANCE * (diffy) / self.vectorNorm(diffx, diffy) + self.rect.centery

            barricade = Barricade(barricadePosx, barricadePosy, self.gameData)

            occupied = pygame.sprite.spritecollideany(barricade, self.mapData.enemyGroup)
            if occupied is None:
                occupied = pygame.sprite.spritecollideany(barricade, self.mapData.obstacleGroup)

            if occupied is None:
                self.soundBarricade.play()
                self.mapData.camera.add(barricade)
                self.mapData.allSprites.add(barricade)
                self.mapData.obstacleGroup.add(barricade)

                self.mapData.allSprites.add(barricade.lifeBar)
                self.mapData.camera.add(barricade.lifeBar, layer=CAMERA_HUD_LAYER)

                self.barricadeCharges -= 1

                if self.barricadeCooldown.isZero:
                    self.barricadeCooldown.start()

            else:
                barricade.destroy()

    def onCollision(self, collidedWith, sideOfCollision,limit=0):
        if collidedWith == SOLID or collidedWith == ENTRANCEWALL:
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

        if collidedWith == OBSTACLE:
            if sideOfCollision == RIGHT:
                #On colle le player à gauche de l'obstacle
                self.speedx = 0
                self.rect.right = limit
            if sideOfCollision == LEFT:
                self.speedx = 0
                self.rect.left = limit
            if sideOfCollision == DOWN:
                self.speedy = 0
                self.rect.bottom = limit

            if sideOfCollision == UP:
                self.speedy = 0
                self.rect.top = limit

    def nextItem(self):
        self.currentItem += 1
        if self.currentItem >= len(self.inventory.itemList):
            self.currentItem = 0

    def isHit(self, damage=1):
        # Could be different depending on which enemy...
        self.hurt(damage)

    def hurt(self, damage):

        if not self.isInvincible:

            self.lifeBar.healthCurrent -= damage
            self.hurtSound.play()

            if TAG_ANIKA == 1:
                print('player health :', self.lifeBar.healthCurrent)

            self.checkIfIsAlive()

            self.invincibleOnHit()
            if TAG_ANIKA == 1:
                print('player is now invincible')
            self.visualFlash()

    def checkIfIsAlive(self):
        if self.lifeBar.healthCurrent <= 0:
            self.destroy()

    def destroy(self):
        if TAG_ANIKA == 1:
            print('player is dead')
        self.dead()

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
                #self.nextItem()
                self.shootGrenade()
                self.spacePressed = True
            elif event.key == pygame.K_LSHIFT:
                self.shootMine()
                self.leftShiftPressed = True


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.rightPressed = False
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.leftPressed = False
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                self.upPressed = False
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.downPressed = False
            elif event.key == pygame.K_LSHIFT:
                self.leftShiftPressed = False
            elif event.key == pygame.K_SPACE:
                self.spacePressed = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == MOUSE_LEFT:
                self.leftMousePressed = True
            elif event.button == MOUSE_RIGHT:
                self.rightMousePressed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == MOUSE_LEFT:
                self.leftMousePressed = False
            elif event.button == MOUSE_RIGHT:
                self.rightMousePressed = False

    def updatePressedKeys(self):
        if self.rightPressed:
            self.updateSpeedRight()
        if self.leftPressed:
            self.updateSpeedLeft()
        if self.upPressed:
            self.updateSpeedUp()
        if self.downPressed:
            self.updateSpeedDown()
        if self.leftMousePressed:
            self.inventory.itemList[0].useItem()
        if self.rightMousePressed:
            self.createBarricade()
        if self.leftShiftPressed:
            self.shootMine()
        if self.spacePressed:
            self.shootGrenade()

    # Suppose to work, but dont
    # Need to understand why the camera is OK, with a simple rotation?
    # http://pygame.org/wiki/RotateCenter?parent=
    def rot_center(self, image, angle):
        rot_image = pygame.transform.rotate(image, angle)
        self.rect = rot_image.get_rect(center=self.rect.center)
        return rot_image
