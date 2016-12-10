from app.sprites.enemy.enemy import Enemy
from app.sprites.enemy.enemyWalk import EnemyWalk
from app.sprites.enemy.enemyShooter import EnemyShooter


class EnemyGenerator(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.name = "enemyGenerator"

        self.imageIter = 0 # counter
        self.imageWait = 100  # time between enemy spawn

    def spawnEnemy(self, typeEnemy):

        # we place then a little randomly around [x,y] TODO
        enemy = typeEnemy(self.rect.x, self.rect.y, self.mapData)
        enemy.setMapData(self.mapData)

        self.mapData.camera.add(enemy)
        self.mapData.allSprites.add(enemy)
        self.mapData.enemyBullet.add(enemy)
