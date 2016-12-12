from app.settings import *
from app.tools.functionTools import *
from app.tools.circle import Circle
import pygame
import copy

class CollisionPlayerPlatform:
    def __init__(self, player, map):
        # self.soundControl = soundPlayerController
        self.tileWidth = map.tmxData.tilewidth
        self.tileHeight = map.tmxData.tileheight
        self.mapHeight = map.tmxData.height * self.tileHeight
        self.mapWidth = map.tmxData.width * self.tileWidth
        self.player = player
        self.map = map

    def collisionAllSprites(self, player, mapData, gameData):
        for sprite in mapData.allSprites:
            if sprite.isPhysicsApplied == True or sprite.isCollisionApplied == True:
                if seekAtt(sprite, "type") == "enemy":
                    sprite.applyAI()

                self.rightCollision(sprite, mapData)
                self.leftCollision(sprite, mapData)
                self.downCollision(sprite, mapData)
                self.upCollision(sprite, mapData)

                self.collisionWithObstacle(sprite, mapData.obstacleGroup)
                self.collisionWithMine(sprite, mapData.mineGroup)
        self.collisionWithEnemy(player, mapData.enemyGroup)
        self.pickUpItem(player, mapData.itemGroup, gameData)




    def rightCollision(self,sprite, map):

        # mapHeight = map.tmxData.height * tileHeight
        i=0

        if sprite.collisionMask.rect.right + sprite.speedx > 0:
            if sprite.speedx >= self.tileWidth: #Si on va plus vite qu'une tile/seconde
                while sprite.collisionMask.rect.right+i*self.tileWidth < sprite.collisionMask.rect.right + sprite.speedx:
                    if sprite.collisionMask.rect.right+i*self.tileWidth >= self.mapWidth:
                        j=0
                        while map.tmxData.get_tile_gid((self.mapWidth - 1 - j*self.tileWidth)/self.tileWidth, sprite.collisionMask.rect.top/self.tileHeight, COLLISION_LAYER) == SOLID and map.tmxData.get_tile_gid((self.mapWidth - 1- j*self.tileWidth)/self.tileWidth, (sprite.collisionMask.rect.bottom)/self.tileHeight, COLLISION_LAYER) == SOLID:
                            j += 1
                        sprite.onCollision(SOLID, RIGHT)
                        return

                    upRightTileGid = map.tmxData.get_tile_gid((sprite.collisionMask.rect.right + i*self.tileWidth)/self.tileWidth, sprite.collisionMask.rect.top/self.tileHeight, COLLISION_LAYER)
                    downRightTileGid = map.tmxData.get_tile_gid((sprite.collisionMask.rect.right + i*self.tileWidth)/self.tileWidth, (sprite.collisionMask.rect.bottom-1)/self.tileHeight, COLLISION_LAYER)

                    if (upRightTileGid  == SOLID or downRightTileGid  == SOLID) and sprite.speedx > 0 and sprite.facingSide == RIGHT:
                        while map.tmxData.get_tile_gid((sprite.collisionMask.rect.right + 1)/self.tileWidth, sprite.collisionMask.rect.top/self.tileHeight, COLLISION_LAYER) != SOLID and map.tmxData.get_tile_gid((sprite.collisionMask.rect.right + 1)/self.tileWidth, (sprite.collisionMask.rect.bottom-1)/self.tileHeight, COLLISION_LAYER) != SOLID:
                            sprite.collisionMask.rect.right += 1
                            sprite.onCollision(SOLID, RIGHT)
                    i += 1

            else:
                upRightTileGid = self.map.tmxData.get_tile_gid((sprite.collisionMask.rect.right + sprite.speedx)/self.tileWidth, (sprite.collisionMask.rect.top + 1)/self.tileHeight, COLLISION_LAYER)
                downRightTileGid = self.map.tmxData.get_tile_gid((sprite.collisionMask.rect.right + sprite.speedx)/self.tileWidth, (sprite.collisionMask.rect.bottom-1)/self.tileHeight, COLLISION_LAYER)

                if (upRightTileGid  == SOLID or downRightTileGid == SOLID) and sprite.speedx > 0:
                    sprite.onCollision(SOLID, RIGHT)
                elif upRightTileGid  == ENTRANCEWALL or downRightTileGid == ENTRANCEWALL:
                    sprite.onCollision(ENTRANCEWALL, RIGHT)
                elif upRightTileGid  == SPRING or downRightTileGid == SPRING:
                    sprite.onCollision(SPRING, RIGHT)

    def getUpRightTileGid(self):
        return self.map.tmxData.get_tile_gid((self.player.collisionMask.rect.right + self.player.speedx)/self.tileWidth, self.player.collisionMask.rect.top/self.tileHeight, COLLISION_LAYER)
    def getDownRightTileGid(self):
        return self.map.tmxData.get_tile_gid((self.player.collisionMask.rect.right + self.player.speedx)/self.tileWidth, (self.player.collisionMask.rect.bottom-1)/self.tileHeight, COLLISION_LAYER)
    def getLowMidRightTileGid(self):
        return self.map.tmxData.get_tile_gid((self.player.collisionMask.rect.right + self.player.speedx)/self.tileWidth, (self.player.collisionMask.rect.centery-10-1)/self.tileHeight, COLLISION_LAYER)
    def getHighMidRightTileGid(self):
        return self.map.tmxData.get_tile_gid((self.player.collisionMask.rect.right + self.player.speedx)/self.tileWidth, (self.player.collisionMask.rect.centery+10-1)/self.tileHeight, COLLISION_LAYER)
    # def getRightTilesList(self): à terminer si besoin (décomposer le nb de pts de vérification sur le sprite selon sa taille, à place de 4 fixes)
    #     tileList = []
    #     pointNumber = self.tileHeight
    #     tileList.append(self.map.tmxData.get_tile_gid((self.player.collisionMask.rect.right + self.player.speedx)/self.tileWidth, (self.player.collisionMask.rect.centery+10-1)/self.tileHeight, COLLISION_LAYER))

    def leftCollision(self,sprite, map):
        tileWidth = map.tmxData.tilewidth
        tileHeight = map.tmxData.tileheight
        # mapWidth = map.tmxData.width * tileWidth
        # mapHeight = map.tmxData.height * tileHeight
        i = 0

        if -sprite.speedx >= tileWidth:
            while sprite.collisionMask.rect.x-i*tileWidth > sprite.collisionMask.rect.x + sprite.speedx:
                if sprite.collisionMask.rect.x-i*tileWidth <= 0:
                    j=0
                    while map.tmxData.get_tile_gid((0 + j*tileWidth)/tileWidth, sprite.collisionMask.rect.top/tileHeight, COLLISION_LAYER) == SOLID and map.tmxData.get_tile_gid((0 + j*tileWidth)/tileWidth, (sprite.collisionMask.rect.bottom-1)/tileHeight, COLLISION_LAYER) == SOLID:
                        j += 1
                        sprite.onCollision(SOLID, LEFT)
                    return

                upLeftTileGid = map.tmxData.get_tile_gid((sprite.collisionMask.rect.left - i*tileWidth)/tileWidth, sprite.collisionMask.rect.top/tileHeight, COLLISION_LAYER)
                downLeftTileGid = map.tmxData.get_tile_gid((sprite.collisionMask.rect.left - i*tileWidth)/tileWidth, (sprite.collisionMask.rect.bottom-1)/tileHeight, COLLISION_LAYER)

                if (upLeftTileGid  == SOLID or downLeftTileGid  == SOLID) and sprite.facingSide == LEFT:
                    while map.tmxData.get_tile_gid((sprite.collisionMask.rect.left)/tileWidth, sprite.collisionMask.rect.top/tileHeight, COLLISION_LAYER) != SOLID and map.tmxData.get_tile_gid((sprite.collisionMask.rect.left)/tileWidth, (sprite.collisionMask.rect.bottom-1)/tileHeight, COLLISION_LAYER) != SOLID:
                        sprite.collisionMask.rect.left -= 1
                    sprite.onCollision(SOLID, LEFT)
                i += 1

        else:
            upLeftTileGid = map.tmxData.get_tile_gid((sprite.collisionMask.rect.left + sprite.speedx)/tileWidth, sprite.collisionMask.rect.top/tileHeight, COLLISION_LAYER)
            downLeftTileGid = map.tmxData.get_tile_gid((sprite.collisionMask.rect.left + sprite.speedx)/tileWidth, (sprite.collisionMask.rect.bottom-1)/tileHeight, COLLISION_LAYER)


            if (upLeftTileGid  == SOLID or downLeftTileGid  == SOLID) and sprite.speedx < 0:
                #while map.tmxData.get_tile_gid((player.collisionMask.rect.left)/tileWidth, player.collisionMask.rect.top/tileHeight, COLLISION_LAYER) != SOLID and map.tmxData.get_tile_gid((player.collisionMask.rect.left)/tileWidth, (player.collisionMask.rect.bottom-1)/tileHeight, COLLISION_LAYER) != SOLID:
                     #player.collisionMask.rect.left -= 1
                sprite.onCollision(SOLID, LEFT)
            elif upLeftTileGid  == ENTRANCEWALL or downLeftTileGid  == ENTRANCEWALL:
                sprite.onCollision(ENTRANCEWALL, LEFT)
            elif (upLeftTileGid  == SPRING or downLeftTileGid  == SPRING) and sprite.speedx < 0:
                sprite.onCollision(SPRING, LEFT)


    def downCollision(self,sprite, map):
        tileWidth = map.tmxData.tilewidth
        tileHeight = map.tmxData.tileheight
        # mapWidth = map.tmxData.width * tileWidth
        # mapHeight = map.tmxData.height * tileHeight

        downLeftTileGid = map.tmxData.get_tile_gid((sprite.rect.left+1)/tileWidth, (sprite.rect.bottom + sprite.speedy)/tileHeight, COLLISION_LAYER)
        downRightTileGid = map.tmxData.get_tile_gid((sprite.rect.right-1)/tileWidth, (sprite.rect.bottom + sprite.speedy)/tileHeight, COLLISION_LAYER)
        downMidTileGID = map.tmxData.get_tile_gid((sprite.rect.centerx)/tileWidth, (sprite.rect.bottom + sprite.speedy)/tileHeight, COLLISION_LAYER)

        if downLeftTileGid == SOLID or downRightTileGid == SOLID or downMidTileGID == SOLID:
            sprite.onCollision(SOLID, DOWN)
        elif downLeftTileGid == ENTRANCEWALL or downRightTileGid == ENTRANCEWALL  or downMidTileGID == ENTRANCEWALL:
            sprite.onCollision(ENTRANCEWALL, DOWN)
        elif downLeftTileGid == SPRING or downRightTileGid == SPRING  or downMidTileGID == SPRING:
            sprite.onCollision(SPRING, DOWN)
        else:
            sprite.onCollision(NONE, DOWN)

    def upCollision(self,sprite, map):
        tileWidth = map.tmxData.tilewidth
        tileHeight = map.tmxData.tileheight

        upLeftTileGid = map.tmxData.get_tile_gid((sprite.rect.left+1)/tileWidth, (sprite.rect.top + sprite.speedy)/tileHeight, COLLISION_LAYER)
        upRightTileGid = map.tmxData.get_tile_gid((sprite.rect.right - 1)/tileWidth, (sprite.rect.top + sprite.speedy)/tileHeight, COLLISION_LAYER)
        upMidTileGid = map.tmxData.get_tile_gid(sprite.rect.centerx/tileWidth, (sprite.rect.top + sprite.speedy)/tileHeight, COLLISION_LAYER)

        if upLeftTileGid == SOLID or upRightTileGid == SOLID or upMidTileGid == SOLID:
            sprite.onCollision(SOLID, UP)

        elif upLeftTileGid == ENTRANCEWALL or upRightTileGid == ENTRANCEWALL:
            sprite.onCollision(ENTRANCEWALL, UP)
        elif upLeftTileGid == LADDER or upRightTileGid == LADDER or upMidTileGid == LADDER:
            sprite.onCollision(LADDER, UP)
        else:
            sprite.onCollision(NONE, UP)

    def collisionWithEnemy(self, player, enemyGroup):
        collisionList = pygame.sprite.spritecollide(player, enemyGroup, False)
        for enemy in collisionList:
            player.hurt(1)
            # self.soundControl.hurt()
            pass

    def collisionWithObstacle(self, sprite, obsctacleGroup):
        sideOfCollision = None
        #Test for horizontal move
        posx = copy.deepcopy(sprite.rect.x)
        posy = copy.deepcopy(sprite.rect.y)

        sprite.rect.x += sprite.speedx
        sprite.rect.y += sprite.speedy

        collisionList = pygame.sprite.spritecollide(sprite, obsctacleGroup, False)
        for obstacle in collisionList:

            if sprite.speedx > 0:
                limit = obstacle.rect.left
                sideOfCollision = RIGHT
            elif sprite.speedx < 0:
                limit = obstacle.rect.right
                sideOfCollision = LEFT
            if sideOfCollision == LEFT or sideOfCollision == RIGHT:
                sprite.onCollision(OBSTACLE, sideOfCollision, limit)

            if sprite.speedy > 0:
                limit = obstacle.rect.top
                sideOfCollision = DOWN
            elif sprite.speedy < 0:
                limit = obstacle.rect.bottom
                sideOfCollision = UP
            if sideOfCollision == UP or sideOfCollision == DOWN:
                sprite.onCollision(OBSTACLE, sideOfCollision, limit)

            if sideOfCollision is not None and sprite.speedx == 0 and sprite.speedy == 0 and sprite.friendly is False:
                # An obstacle? We hit with an attack!
                sprite.attackOnCollision()

        #Test for vertical move
        # sprite.rect.y += sprite.speedy
        # collisionList = pygame.sprite.spritecollide(sprite, obsctacleGroup, False)
        # for obstacle in collisionList:
        #     if sprite.speedx > 0:
        #         limit = obstacle.rect.left
        #         sideOfCollision = RIGHT
        #     elif sprite.speedx < 0:
        #         limit = obstacle.rect.right
        #         sideOfCollision = LEFT
        #
        #     if sideOfCollision == LEFT or sideOfCollision == RIGHT:
        #         sprite.onCollision(OBSTACLE, sideOfCollision, limit)
        #         if sprite.friendly == False:
        #             obstacle.isHit(sprite.attack)
        #
        #     if sprite.speedy > 0:
        #         limit = obstacle.rect.top
        #         sideOfCollision = DOWN
        #     elif sprite.speedy < 0:
        #         limit = obstacle.rect.bottom
        #         sideOfCollision = UP
        #
        #     if sideOfCollision == UP or sideOfCollision == DOWN:
        #         sprite.onCollision(OBSTACLE, sideOfCollision, limit)
        #
        #     if sideOfCollision is not None:
        #         if sprite.friendly == False:
        #             obstacle.isHit(sprite.attack)

        #Reset Sprite.... this IS hardcoded...
        sprite.rect.x = posx
        sprite.rect.y = posy


    def collisionWithMine(self, sprite, mineGroup):
        collisionList = pygame.sprite.spritecollide(sprite, mineGroup, False)

        for mine in collisionList:
            mine.detonate()


    def pickUpItem(self, player, itemGroup, gameMemory):
        collisionList = pygame.sprite.spritecollide(player, itemGroup, False)
        for item in collisionList:
            gameMemory.registerItemPickedUp(item)
            item.kill()

def collisionBulletEnemy(bullet, map):
    collisionList = pygame.sprite.spritecollide(bullet, map.enemyGroup, False)
    for enemy in collisionList:
        enemy.isHit(bullet.attackDMG)
        bullet.hitEnemy()
        break  #so that only 1 enemy is hit by a bullet

def collisionGrenadeEnemy(grenade, map):
    collisionList = pygame.sprite.spritecollide(grenade, map.enemyGroup, False)
    for enemy in collisionList:
        grenade.detonate()

def collisionAttackPlayer(map, player):
    collisionList = pygame.sprite.spritecollide(player, map.attackGroup, False)
    for attack in collisionList:
        player.hurt(1)
        attack.kill()

def collisionBarricadePlayer(map, barricade):
    collisionList = pygame.sprite.spritecollide(barricade, map.attackGroup, False)
    for attack in collisionList:
        barricade.isHit(attack.attackDMG)
        attack.kill()

def collisionBulletPlayer(map, player):
    collisionList = pygame.sprite.spritecollide(player, map.enemyBullet, False)
    for bullet in collisionList:
        player.hurt(1)
        bullet.kill()

def printTile(tile):
    if tile == SOLID:
        print('SOLID')
    elif tile == ENTRANCEWALL:
        print('ENTRANCEWALL')
    elif tile == SPRING:
        print('SPRING')
    else:
        print(tile)

def collisionExplosionEnemy(explosion, mapData):
    circle = Circle((explosion.collisionMask.rect.centerx, explosion.collisionMask.rect.centery),explosion.collisionMask.rect.width/2)

    for enemy in mapData.enemyGroup:
        if collisionCircleRect(circle, enemy.rect):
            enemy.isHit(explosion.attackDMG)

    for barricade in mapData.obstacleGroup:
        if collisionCircleRect(circle, barricade.rect):
            barricade.isHit(explosion.attackDMG)

    if collisionCircleRect(circle, mapData.player.rect):
        mapData.player.isHit(explosion.attackDMG)


def collisionCircleRect(circle, rect):
    circleDistancex = abs(circle.x - rect.centerx)
    circleDistancey = abs(circle.y - rect.centery)

    if (circleDistancex > (rect.width/2 + circle.r)):
        return False
    if (circleDistancey > (rect.height/2 + circle.r)):
        return False

    if (circleDistancex <= (rect.width/2)):
        return True
    if (circleDistancey <= (rect.height/2)):
        return True

    cornerDistance_sq = (circleDistancex - rect.width/2)**2 + (circleDistancey - rect.height/2)**2

    return (cornerDistance_sq <= (circle.r**2))

def printTopTile(tile):
    if tile == SOLID:
        print("SOLID")
    elif tile == ENTRANCEWALL:
        print("ENTRANCEWALL")
    elif tile == SPRING:
        print("SPRING")
    elif tile == LADDER:
        print("LADDER")

def printJumpState(state):
    if state == GROUNDED:
        print("GROUNDED")
    elif state == JUMP:
        print("JUMP")
    elif state == CLIMBING:
        print("CLIMBING")

