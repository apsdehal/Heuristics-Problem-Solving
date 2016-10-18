from coordinate import Coordinate
class Grid:
    WIDTH = 1000
    HEIGHT = 1000
    def __init__(self, stride = 50, stones = None):
        self.stride = stride
        self.board = [[-1 for i in range(0, self.WIDTH)] for j in range(0, self.HEIGHT)]
        if stones != None:
            self.setColor(stones)

    def center(self):
        return Coordinate(self.WIDTH / 2, self.HEIGHT / 2)

    def setColor(self, stones):
        if len(stones[0]) == 1 and len(stones[1]) == 0:
            self.setPatchColorSingle(0, 0, self.WIDTH, self.HEIGHT, 0)
        else:
            for i in range(0, self.WIDTH, self.stride):
                for j in range(0, self.HEIGHT, self.stride):
                    coords = self.getMark(i, j)
                    colors = []
                    for coord in coords:
                        c = self.getCurrentColor(coord, stones)
                        colors.append(c)

                    if len(colors) == 2:
                        self.setPatchColor(i, j, self.stride, self.stride, stones)
                    else:
                        self.setPatchColorSingle(i, j, self.stride, self.stride, colors[0])
    def getColor(self, i, j):
        return self.board[i][j]

    def getColorDist(self):
        ret = [0, 1]

        for i in range(0, self.WIDTH):
            for j in range(0, self.HEIGHT):
                k = self.board[i][j]
                ret[k] = ret[k] + 1
        return ret

    def getCurrentColor(self, coord, stones):
        pull = 0.0
        c = 0

        for i in range(0, 2):
            sum = 0.0
            for stone in stones[i]:
                if coord.x == stone.x and coord.y == stone.y:
                    continue

                sum += 1.0 / coord.getD(stone)
                if pull < sum:
                    pull = sum
                    c = i
        return c

    def getMark(self, i, j):
        coords = [];

        coords.append(Coordinate(i, j))

        if i + self.stride - 1 < self.WIDTH:
            coords.append(Coordinate(i + self.stride - 1, j))

        if j + self.stride - 1 < self.HEIGHT:
            coords.append(Coordinate(i, j + self.stride - 1));

        if i + self.stride - 1 < self.WIDTH and j + self.stride - 1 < self.HEIGHT:
            coords.append(Coordinate(i+ self.stride - 1, j + self.stride - 1))

        if i + self.stride / 2 < self.WIDTH and j + self.stride / 2 < self.HEIGHT:
            coords.append(Coordinate(i + self.stride / 2, j + self.stride / 2))

        return coords

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
                coord = Coordinate(p, q)
                c = self.getCurrentColor(coord, stones)
                self.board[p][q] = c
                q = q + 1
            p = p + 1
