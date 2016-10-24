from board import Board

class Hunter:
    def __init__(self, info):
        self.maxWalls = info['maxWalls']
        self.wallPlacementDelay = info['wallPlacementDelay']
        self.board = Board(info['boardSizeX'], info['boardSizeY'])
        self.wallPlacementDelay = info['wallPlacementDelay']

    def move(self, info):
        self.walls = info['walls']
        self.hunterCoord = info['hunter'];
        self.preyCoord = info['prey']

        if self.preyInFront():
            return self.moveFront(info)
        else:
            return self.moveBack(info)

    def longDist(self):
        return max(abs(self.preyCoord.x - self.hunterCoord.x), abs(self.preyCoord.y - self.hunterCoord.y))

    def shortDist(self):
        return min(abs(self.preyCoord.x - self.hunterCoord.x), abs(self.preyCoord.y - self.hunterCoord.y))

    def isOccupied(self, coord):
        if coord.x < 0 or coord.x >= self.board.xSize or coord.y < 0 or coord.y >= self.board.ySize:
            return True

        for wall in self.walls:
            if (wall.occupies(coord)):
                return True

        return False

    def newVerticalWall(self):
        greater = self.hunterCoord
        lesser = self.hunterCoord

        while not self.isOccupied(greater):
            if greater.equals(self.hunterCoord) or greater.equals(self.preyCoord):
                return False

            greater.y += 1

        while not self.isOccupied(lesser):
            if lesser.equals(self.hunterCoord) or lesser.equals(self.preyCoord):
                return False

            lesser.y += 1

        return Wall(1, self.hunterCoord.x, lesser.y, greater.y)

    def newVerticalWall(self):
        greater = self.hunterCoord
        lesser = self.hunterCoord

        while not self.isOccupied(greater):
            if greater.equals(self.hunterCoord) or greater.equals(self.preyCoord):
                return False

            greater.x += 1

        while not self.isOccupied(lesser):
            if lesser.equals(self.hunterCoord) or lesser.equals(self.preyCoord):
                return False

            lesser.x += 1

        return Wall(0, self.hunterCoord.y, lesser.x, greater.x)

    def wallInBetween(self):
        ret = 0

        for wall in self.walls:
            if wall.type == wall.HORIZONTAL:

                ret = ret or self.hunterCoord.y < wall.coord < self.preyCoord.y \
                or self.preyCoord.y < wall.coord < self.hunterCoord.y
            elif wall.type == wall.VERTICAL:

                ret = ret or self.hunterCoord.x < wall.coord < self.preyCoord.x \
                or self.preyCoord.x < wall.coord < self.hunterCoord.x

        return ret

    def removeAndBuildWall(self):
