from grid import Grid
from coordinate import Coordinate
from stone import Stone
from multiprocessing.dummy import Pool as ThreadPool
import math
import coordinateList
import itertools
import copy

class Greedy:
    def __init__(self, stride):
        self.stride = stride;
        self.grid = Grid(stride)
        self.JUMP = 8
        self.coordList = coordinateList.getCoordinateList()[0::self.JUMP]

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
        self.opponentLastStone = stones[1][-1]
        self.stones = stones

        if self.opponentLastStone.x + 66 < self.grid.WIDTH:
            finalCoord = Coordinate(self.opponentLastStone.x + 66, self.opponentLastStone.y)
        else:
            finalCoord = Coordinate(self.opponentLastStone.x - 66, self.opponentLastStone.y)

        pool = ThreadPool(4)
        rets = pool.map(self.tryStone, self.coordList)
        pool.close()
        pool.join()

        for x in rets:
            if (x == 0):
                continue
            if (x[0][0] > num):
                num = x[0][0]
                finalCoord = Coordinate(x[1].x, x[1].y)

        return finalCoord

    def tryStone(self, coord):
        x = self.opponentLastStone.x + coord.x
        y = self.opponentLastStone.y + coord.y

        if x < 0 or y < 0 or x > self.grid.WIDTH or y > self.grid.HEIGHT:
            return 0

        currStone = Stone(x, y)
        flag = 0

        if not self.opponentLastStone.getFeasible(currStone):
            return 0

        for l in range(0, 2):
            for stone in self.stones[l]:
                if not stone.getFeasible(currStone):
                    flag = 1
                    break
            if flag == 1:
                break

        if flag == 1:
            return 0

        copyStones = copy.deepcopy(self.stones)
        copyStones[0].append(currStone)

        self.grid.setColor(copyStones)

        ret = self.grid.getColorDist()

        return (ret, currStone)

    def updatePull(self, stones, player):
        self.grid.updatePull(stones[player][-1], player)
