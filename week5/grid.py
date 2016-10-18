from coordinate import Coordinate
class Grid:
    WIDTH = 1000
    HEIGHT = 1000
    def __init__(self, stride = 50, stones = None):
        self.stride = stride
        self.board = [[0 for i in range(0, self.WIDTH)] for j in range(0, self.HEIGHT)]
        if stones != None:
            self.setColor(stones)

    def center(self):
        return Coordinate(self.WIDTH / 2, self.HEIGHT / 2)

    def setColor(self, stones):
        if len(stones) == 1:
            setColorSingle(0, 0, self.WIDTH, self.HEIGHT)
        else:
            for i in range(0, self.WIDTH, self.stride):
                for j in range(0, self.HEIGHT, self.stride):
                    locs = self.getMark(i, j)
                    colors = []
                    for loc in locs:
                        c = self.getCurrentColor(loc, stones)
                        colors.append(c)

                    if len(color) == 2:
                        self.setPatchColor(i, j, self.stride, self.stride, stones)
                    else:
                        self.setPatchColorSingle(i, j, self.stride, self.stride, colors[0])
    def getColor(self, i, j):
        return self.board[i][j]

    def colorDist(self):
        ret = {}

        for i in range(0, self.WIDTH):
            for j in range(0, self.HEIGHT):
                k = self.board[i][j]

                if ret[k] == None:
                    ret[k] = 0

                ret[k] = ret[k] + 1
        return ret

    def getCurrentColor(self, loc, stones):
        pull = 0.0
        c = 0

        for i in range(0, 2):
            sum = 0.0
            for stone in stones[i]:
                sum += 1.0 / loc.getDS(stone)
                if pull < sum:
                    pull = sum
                    c = i
        return c

    def getMark(i, j):
        locs = [];

        locs.append(Coordinate(i, j))

        if i + stride - 1 < self.WIDTH:
            locs.append(Coordinate(i + stride - 1, j))

        if j + stride - 1 < self.HEIGHT:
            locs.append(Coordinate(i, j + stride - 1));

        if i + stride - 1 < self.WIDTH && j + stride - 1 < self.HEIGHT:
            locs.append(Coordinate(i+ stride - 1, j + stride - 1))

        if i + stride / 2 < self.WIDTH && j + stride / 2 < self.HEIGHT:
            locs.append(Coordinate(i + stride / 2, j + stride / 2))

    def setPatchColorSingle(self, i, j, width, height, c):
        p = i
        q = j

        while p < i + width and p < self.WIDTH:
            while q < j + height and q < self.HEIGHT:
                self.board[p][q] = c
                q = q + 1
            p = p + 1

    def setPatchColor(self, i, j, width, height, stones):
        p = i
        q = j

        while p < i + width and p < self.WIDTH:
            while q < j + height and q < self.HEIGHT:
                loc = Coordinate(p, q)
                c = self.getCurrentColor(loc, stones)
                self.board[p][q] = c
                q = q + 1
            p = p + 1
