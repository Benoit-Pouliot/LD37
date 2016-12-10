import random

class EnemySupervisor():
    def __init__(self, mapData):

        self.mapData = mapData
        self.listEnemyGenerator = []


    def addEnemyGenerator(self, enemyGen):
        self.listEnemyGenerator.append(enemyGen)

    def updateSupervisor(self):


        for listData in self.mapData.enemyGenListData.listData:
            if listData[0] < self.mapData.internalMapTime:
                for k in range(listData[2]):

                    randEnemyGen = random.randint(0,len(self.listEnemyGenerator)-1)
                    randTypeIDEnemy = random.choice(listData[1])
                    self.listEnemyGenerator[randEnemyGen].spawnEnemy(self.mapData.enemyGenListData.dictListEnemiesValues[randTypeIDEnemy])

                if listData[3] > 0:
                    self.mapData.enemyGenListData.addData(listData[0]+listData[3],listData[1],listData[2],listData[3])
                self.mapData.enemyGenListData.listData.pop(0)
