import os
import pygame

from app.sprites.enemy.enemy import Enemy
from app.scene.platformScreen.collisionPlayerPlatform import *
from app.tools.animation import Animation

class Bullet(Enemy):
    def __init__(self, x, y, speedx, speedy, friendly=True):
        super().__init__(x, y)

        self.name = "bullet"

        self.image = pygame.image.load(os.path.join('img', 'Bullet.png'))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y

        # if direction == RIGHT:
        #     self.speedx = 10
        #     self.image = self.imageBulletRight[0]
        #     self.imageBulletList = self.imageBulletRight
        #     self.rect.x = x
        # elif direction == LEFT:
        #     self.speedx = -10
        #     self.image = self.imageBulletLeft[0]
        #     self.imageBulletList = self.imageBulletLeft
        #     self.rect.x = x - self.rect.width
        self.speedx = speedx
        self.speedy = speedy

        self.animation = None
        self.attackDMG = 1

        self.friendly = friendly
        self.isCollisionApplied = True

    def update(self):

        self.x += self.speedx
        self.y += self.speedy

        self.rect.x = self.x
        self.rect.y = self.y

        if self.animation is not None :
           next(self.animation)
        self.updateCollisionMask()

    def updateCollisionMask(self):
        self.collisionMask.rect.x = self.rect.x
        self.collisionMask.rect.y = self.rect.y


    # For animation testing by Marie. timer is the number of time between frame.
    def stand_animation(self,frames,timer):
        while True:
            for frame in frames:
                self.image = frame
                for i in range(timer):
                    yield None

    def onCollision(self, collidedWith, sideOfCollision,limit=0):
        if collidedWith == SOLID:
            self.detonate()

        if collidedWith == OBSTACLE:
            pass

    def hitEnemy(self):
        self.detonate()

    def detonate(self):
        self.kill()

class PlayerBullet(Bullet):
    def __init__(self, x, y, speedx, speedy, gameData, friendly=True):
        super().__init__(x, y, speedx, speedy)

        self.attackDMG = gameData.upgrade['gun'][1]


# class BeerBullet(Bullet):
#     def __init__(self, x, y, direction=RIGHT, friendly=True):
#         super().__init__(x, y, os.path.join('img', 'biere1.png'))
#
#         self.name = "bullet"
#
#         image1 = pygame.image.load(os.path.join('img', 'biere1.png'))
#         image2 = pygame.image.load(os.path.join('img', 'biere2.png'))
#         image3 = pygame.image.load(os.path.join('img', 'biere3.png'))
#         image4 = pygame.image.load(os.path.join('img', 'biere4.png'))
#         self.frames = [image1,image2,image3,image4]
#         self.image = self.frames[0]
#
#         self.animation = self.stand_animation(self.frames,6)
#
#         self.direction = direction
#
#         self.rect = self.image.get_rect()
#         self.rect.y = y - self.rect.height / 2
#
#         if direction == RIGHT:
#             self.speedx = 10
#             self.rect.x = x
#         elif direction == LEFT:
#             self.speedx = -10
#             self.rect.x = x - self.rect.width
#         self.speedy = 0
#
#         self.friendly = friendly


class Shuriken(Bullet):
    def __init__(self, x, y, bullet_speedx, bullet_speedy, gameData, friendly=False):
        super().__init__(x,y,0,0)

        self.name = "bullet"

        self.shurikenFrames = [pygame.image.load(os.path.join('img', 'shuriken.png'))]
        self.image = self.shurikenFrames[0]
        for k in range(1, 5):
            self.shurikenFrames.append(pygame.transform.rotate(self.shurikenFrames[k-1], k*360/6))
        self.animation = Animation(self, self.shurikenFrames, 5)

        self.x = x
        self.y = y - self.rect.height / 2

        self.speedx = bullet_speedx
        self.speedy = bullet_speedy

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.friendly = friendly

        self.lifetime_counter = 0

    def update(self):
        self.animation.update(self)
        self.lifetime_counter += 1

        if self.lifetime_counter < 120:
            self.x += self.speedx
            self.y += self.speedy
            self.rect.x = self.x
            self.rect.y = self.y
            self.updateCollisionMask()
        else:
            self.kill()
