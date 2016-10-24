from board import Board
from wall import Wall

class Hunter:
    def __init__(self, info):
        self.maxWalls = info['maxWalls']
        self.wallPlacementDelay = info['wallPlacementDelay']
        self.board = Board(info['boardSizeX'], info['boardSizeY'])

    def move(self, info):
        self.walls = info['walls']
        self.hunterCoord = info['hunter'];
        self.preyCoord = info['prey']

        if self.preyInFront():
            return self.moveFront(info)
        else:
            return self.moveBack(info)

    def preyInFront(self):
        h2p =  self.preyCoord.x - self.hunterCoord.x, self.preyCoord.y - self.hunterCoord.y

        return h2p[0] * self.hunterCoord.vx > 0 and h2p[1] * self.hunterCoord.vy > 0

    def moveFront(self, info):
        if self.wallInBetween():
            resp = self.removeAndBuildWall()
        else:
            resp = self.goodTimeForWall()
            resp = {'wallAdd': resp}

        if len(self.walls) >= self.maxWalls:
            resp['wallDelete'] = self.removeWalls()

        resp['gameNum'] = info['gameNum']
        resp['tickNum'] = info['tickNum']

        return resp

    def moveBack(self, info):
        resp = self.goodTimeForWall()
        resp = {'wallAdd': resp}

        if len(self.walls) >= self.maxWalls:
            resp['wallDelete'] = self.removeWalls()

        resp['gameNum'] = info['gameNum']
        resp['tickNum'] = info['tickNum']

        return resp


    def removeWalls(self):
        currArea = self.preyArea(self.walls)

        resp = []

        for i in xrange(len(self.walls)):
            area = self.preyArea(self.walls[:i] + self.walls[i + 1: ])
            if area == currArea:
                resp.append(i)

        return resp

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

    def newHorizontalWall(self):
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

        w = None
        for i in xrange(len(self.walls)):
            wall = self.walls[i]
            if wall.type == wall.HORIZONTAL:

                if self.hunterCoord.y < wall.coord < self.preyCoord.y \
                or self.preyCoord.y < wall.coord < self.hunterCoord.y:
                    w = i
                    break

            elif wall.type == wall.VERTICAL:

                if self.hunterCoord.x < wall.coord < self.preyCoord.x \
                or self.preyCoord.x < wall.coord < self.hunterCoord.x:
                    w = i
                    break


        if self.walls[w].type == 0 and abs(self.walls[w].coord - self.hunterCoord.y) > 2:
            return None

        elif self.walls[w].type == 1 and abs(self.walls[w].coord - self.hunterCoord.x) > 2:
            return None

        ret = {}
        ret['wallDelete'] = [w]

        del self.walls[w]

        verArea = self.preyArea(self.walls[:] + [self.newVerticalWall()])
        horArea = self.preyArea(self.walls[:] + [self.newHorizontalWall()])

        ret['wallAdd'] = 2 if verArea < horArea else 1

        return ret

    def goodTimeForWall(self):
        if self.haveCooldown():
            return False

        currArea = self.preyArea(self.walls)
        verArea = self.preyArea(self.walls[:] + [self.newVerticalWall()])
        horArea = self.preyArea(self.walls[:] + [self.newHorizontalWall()])

        minArea = min(verArea, horArea)

        if minArea > currArea:
            return 0
        else if minArea == verArea:
            return 2
        else:
            return 1


    def preyArea(self, walls):
        left, right, top, down = 0, self.board.xSize - 1, self.board.ySize - 1, 0
        for wall in walls:
            if wall.type == wall.HORIZONTAL:
                dist = wall.coord - self.preyCoord.y

                met = wall.start <= self.preyCoord.x <= wall.end

                if met:
                    if dist < 0 and abs(dist) < abs(down - self.preyCoord.y):
                        down = wall.coord
                    elif dist > 0 and dist <  abs(top - self.preyCoord.y):
                        top = wall.coord
            elif wall.type == wall.VERTICAL:
                dist = wall.coord - self.preyCoord.x

                met = wall.start <= self.preyCoord.y <= wall.end

                if met:
                    if dist < 0 and abs(dist) < abs(left - self.preyCoord.x):
                        left = wall.coord
                    elif dist > 0 and dist < abs(right - self.preyCoord.x):
                        right = wall.coord

        return abs(top - down) * abs(left - right)
