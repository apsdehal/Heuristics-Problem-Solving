class Coordinate:
    def __init__(self, x, y, vx = None, vy = None):
        self.x = int(x)
        self.y = int(y)

        self.vy = vy if vy == None else int(vy)
        self.vx = vx if vx == None else int(vx)

        self.direction = [self.vx, self.vy]

    def equals(self, coord):
        return self.x == coord.x and self.y == coord.y
