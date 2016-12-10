from app.sprites.enemy.enemy import Enemy
from app.sprites.enemy.enemyWalk import EnemyWalk
from app.sprites.enemy.enemyShooter import EnemyShooter


class EnemyGenerator(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.name = "enemyGenerator"

        self.imageIter = 1000000000000  # counter
        self.imageWait = 1000000000000  # time between enemy spawn

    def update(self):
        super().update()

        self.imageIter += 1

        # if the time limit "imageWait" is reached, spawn an enemy
        if self.imageIter > self.imageWait:

            # enemy = EnemyWalk(self.rect.x, self.rect.y)  # position of enemy spawn
            enemy = EnemyWalk(600, 500, self.mapData)

            self.mapData.camera.add(enemy)
            self.mapData.allSprites.add(enemy)
            self.mapData.enemyBullet.add(enemy)

            self.imageIter = 0
