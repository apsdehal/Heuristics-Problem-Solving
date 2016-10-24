class Coordinate:
    def __init__(self, x, y, vx = None, vy = None):
        self.x = int(x)
        self.y = int(y)
        self.vx = int(vx)
        self.vy = int(vy)
        self.direction = [self.vx, self.vy]

    def equals(self, coord):
        return self.x == coord.x and self.y == coord.y
