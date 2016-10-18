import math
class Stone:
    MIN_DIST = 66 * 66
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def getFeasible(self, stone):
        dist = (stone.x - self.x) * (stone.x - self.x) + (stone.y - self.y) * (stone.y - self.y)
        if dist < self.MIN_DIST:
            return False
        else:
            return True

    def getD(self, x, y):
        return math.sqrt((self.x - x) * (self.x - x) + (self.y - y) * (self.y - y))
