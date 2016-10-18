import math

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def setX(self, x):
        self.x = x
    def setY(self, y):
        self.y = y

    def getD(self, loc):
        return math.sqrt((self.x - loc.x) * (self.x - loc.x) + (self.y - loc.y) * (self.y - loc.y))

    def move(self, x, y):
        return Location(self.x + x, self.y + y)
