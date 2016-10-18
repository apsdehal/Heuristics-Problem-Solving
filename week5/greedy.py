from grid import Grid
from coordinate import Coordinate
from stone import Stone
import math
import coordinateList

class Greedy:
    def __init__(self, stride, nStones):
        self.JUMP = 8 if nStones < 8 else (nStones + 2)
        self.stride = stride;
        self.grid = Grid(stride, self.JUMP)
        self.coordList = coordinateList.getCoordinateList()

    def getAllTiles(self):
        locs = []
        for i in range(0, self.grid.WIDTH, self.stride):
            for j in range(0, self.grid.HEIGHT, self.stride):
                locs.append(Coordinate(i, j))

        return locs

    def getStoneTiles(self, stones):
        locs = [];

        for k in range(0, 2):
            for stone in stones[k]:
                locs.append(self.getTile(stone.x, stone.y))

        return locs

    def getTile(self, x, y):
        return Coordinate(int(math.floor(x / self.stride) * self.stride), int(math.floor(y / self.stride) * self.stride))

    def getOpponentStones(self, stones):
        return stones[1]

    def getOpponentLastStone(self, stones):
        return stones[1][-1]

    def move(self, stones):
        num = 0
        i = 0
        j = 0

        if (len(stones[0]) == 0 and len(stones[1]) == 0):
            return self.grid.center()

        # Get last stone of opponent
        opponentLastStone = stones[1][-1]

        if opponentLastStone.x + 66 < self.grid.WIDTH:
            finalCoord = Coordinate(opponentLastStone.x + 66, opponentLastStone.y)
        else:
            finalCoord = Coordinate(opponentLastStone.x - 66, opponentLastStone.y)


        for i in range(0, len(self.coordList), self.JUMP):
            coord = self.coordList[i]

            x = opponentLastStone.x + coord.x
            y = opponentLastStone.y + coord.y

            if x < 0 or y < 0 or x > self.grid.WIDTH or y > self.grid.HEIGHT:
                continue

            currStone = Stone(x, y)
            flag = 0

            if not opponentLastStone.getFeasible(currStone):
                continue

            for l in range(0, 2):
                for stone in stones[l]:
                    if not stone.getFeasible(currStone):
                        flag = 1
                        break
                if flag == 1:
                    break

            if flag == 1:
                continue


            stones[0].append(currStone)

            self.grid.setColor(stones)

            ret = self.grid.getColorDist()

            stones[0].pop()

            if (ret[0] > num):
                num = ret[0]
                finalCoord = Coordinate(currStone.x, currStone.y)

        return finalCoord

    def updatePull(self, stones, player):
        self.grid.updatePull(stones[player][-1], player)
