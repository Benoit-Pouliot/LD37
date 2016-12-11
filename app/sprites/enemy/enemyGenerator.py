from app.sprites.enemy.enemy import Enemy
from app.settings import *
import random

class EnemyGenerator(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.name = "enemyGenerator"

        self.factorRamdom = 50

    def spawnEnemy(self, typeEnemy):

        randX = (random.random()*2-1)*self.factorRamdom
        randY = (random.random()*2-1)*self.factorRamdom
        enemy = typeEnemy(self.rect.x+randX, self.rect.y+randY, self.mapData)
        enemy.setMapData(self.mapData)

        self.mapData.camera.add(enemy)
        self.mapData.allSprites.add(enemy)
        self.mapData.enemyGroup.add(enemy)
