from app.sprites.enemy.enemyWalk import EnemyWalk
from app.sprites.enemy.enemyShooter import EnemyShooter
from app.sprites.enemy.enemySprint import EnemySprint
from app.settings import *

# List data of all enemies spawning in a level.
#
# self.listData is a list
# (time, listEnemiesValues, nbEnemies, type)
# - time              : The time when the enemies are spawning (in FRAME)
# - listEnemiesValues : The type of enemies we want to spawn
#                       If several type, we take it randomly each spawn
# - nbEnemies         : Number of enemies spawning
# - plustime          : if positive, loop with time = time + plustime
#
# It is important to use only addData and reqData to change the list
#


class EnemyGenListData():
    def __init__(self, mapData):

        self.listData = []
        self.mapData = mapData

        # For now, the game is slow at 120
        self.limitNumberEnemy = 80

        if TAG_MARIE == 1:
            self.limitNumberEnemy = 3

        # The link between numeration and the enemy
        self.dictListEnemiesValues = {1: EnemyWalk,
                                      2: EnemyShooter,
                                      3: EnemySprint}

    def addData(self, time, listEnemiesValues, nbEnemies=1, plustime=0):
        if plustime < 0:
            raise ValueError('You cant create a type of EnemyGenListData where plustime < 0')
        if nbEnemies >= 1:
            index = len(self.listData)
            for k in range(len(self.listData)):
                if self.listData[k][0] > time:
                    index = k
                    break
            self.listData.insert(index, (time, listEnemiesValues, nbEnemies, plustime) )
