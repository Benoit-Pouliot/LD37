__author__ = 'Bobsleigh'

import math

#-angleRad/math.pi*180
class SteeringAI:
    def __init__(self, mapData, userRect, userSpeedx, userSpeedy):
        self.mapData = mapData
        self.steeringAmount = 10
        self.rect = userRect
        self.userSpeedx = userSpeedx
        self.userSpeedy = userSpeedy

    def getAction(self):
        angleSpeed = math.atan2(self.mapData.player.speedy, self.mapData.player.speedx)
        angleToTarget = math.atan2(self.mapData.player.rect.y - self.rect.y, self.mapData.player.rect.x - self.rect.x)

        desiredSpdX = (self.mapData.player.rect.x - self.rect.x)/self.vectorNorm(self.mapData.player.rect.x - self.rect.x, self.mapData.player.rect.y - self.rect.y) * self.mapData.player.maxSpeedx
        desiredSpdY = (self.mapData.player.rect.y - self.rect.y)/self.vectorNorm(self.mapData.player.rect.x - self.rect.x, self.mapData.player.rect.y - self.rect.y) * self.mapData.player.maxSpeedy

        steeringX = desiredSpdX - self.userSpeedx
        steeringY = desiredSpdY - self.userSpeedy

        return steeringX, steeringY


    def vectorNorm(self,x,y):
        result = math.sqrt(x**2+y**2)
        if result == 0:
            return 1

        return result

    def truncate(self, value, max):
        if value > max:
            value = max