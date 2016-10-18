from grid import Grid
from coordinate import Coordinate
from stone import Stone
import math

class Greedy:
    def __init__(self, stride):
        self.stride = stride;
        self.grid = Grid(stride)

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
        coord = self.getTile(opponentLastStone.x, opponentLastStone.y)

        finalI = coord.x
        finalJ = coord.y
        for i in range(coord.x, coord.x + self.stride):
            for j in range(coord.y, coord.y + self.stride):
                currStone = Stone(i, j)
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
                    finalI = i
                    finalJ = j


        return Coordinate(finalI, finalJ)
