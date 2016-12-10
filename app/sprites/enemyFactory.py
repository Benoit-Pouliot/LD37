from app.sprites.enemy.enemyGenerator import EnemyGenerator

class EnemyFactory:
    def __init__(self):
        self.dictEnemies = {'enemyGenerator': EnemyGenerator}

    def create(self, tmxEnemy, mapData):

        enemyName = tmxEnemy.name
        if enemyName in self.dictEnemies:
            enemy = self.dictEnemies[enemyName](tmxEnemy.x, tmxEnemy.y)

            for nameProp, prop in tmxEnemy.properties.items():
                if nameProp in enemy.dictProperties:
                    enemy.dictProperties[nameProp](prop)

            enemy.setMapData(mapData)
            return enemy
        return None
