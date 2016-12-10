from app.sprites.enemy.enemy import Enemy
from app.sprites.enemy.enemyWalk import EnemyWalk

class EnemyGenerator(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.name = "enemyGenerator"

        self.imageIter = 0
        self.imageWait = 120

    def update(self):
        super().update()

        self.imageIter += 1
        if self.imageIter > self.imageWait:

            enemy = EnemyWalk(self.rect.x, self.rect.y)
            enemy.setMapData(self.mapData)

            self.mapData.camera.add(enemy)
            self.mapData.allSprites.add(enemy)
            self.mapData.enemyBullet.add(enemy)

            self.imageIter = 0