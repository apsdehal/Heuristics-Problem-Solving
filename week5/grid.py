from coordinate import Coordinate
class Grid:
    WIDTH = 1000
    HEIGHT = 1000
    STRIDE = 10
    def __init__(self, stride = 50, jump = 10, stones = None):
        self.stride = stride
        self.STRIDE = 10 if jump < 10 else jump - 1
        self.board = [[-1 for i in range(0, self.WIDTH)] for j in range(0, self.HEIGHT)]
        self.pull = [[0 for i in range(0, self.WIDTH)] for j in range(0, self.HEIGHT)]
        self.visited = [[0 for i in range(0, self.WIDTH)] for j in range(0, self.HEIGHT)]

        if stones != None:
            self.setColor(stones)

    def center(self):
        return Coordinate(self.WIDTH / 2, self.HEIGHT / 2)

    def setColor(self, stones):
        if len(stones[0]) == 1 and len(stones[1]) == 0:
            self.setPatchColorSingle(0, 0, self.WIDTH, self.HEIGHT, 0)
        else:
            for i in range(0, self.WIDTH, self.STRIDE):
                for j in range(0, self.HEIGHT, self.STRIDE):
                    currCoord = Coordinate(i, j)
                    self.board[i][j] = self.getCurrentColor(currCoord, stones[0][-1])
                    curr = self.board[i][j]
                    for k in range(1, 9):
                        for l in range(1, 9):
                            self.board[i + k][j + l] = curr


    def getColor(self, i, j):
        return self.board[i][j]

    def getColorDist(self):
        ret = [0, 1]

        for i in range(0, self.WIDTH):
            for j in range(0, self.HEIGHT):
                k = self.board[i][j]
                ret[k] = ret[k] + 1
        return ret

    def getCurrentColor(self, coord, stone):
        if self.pull[coord.x][coord.y] > 0:
            return 0

        if coord.x == stone.x and coord.y == stone.y:
            return 0 if self.pull[coord.x][coord.y] > 0 else 1

        sum = self.pull[coord.x][coord.y] + 1.0 / coord.getD(stone)

        return 0 if sum > 0 else 1

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

    def updatePull(self, stone, player):
        self.visited[stone.x][stone.y] = 1
        if player == 0:
            for i in range(1, self.WIDTH):
                for j in range(1, self.HEIGHT):
                    if i == stone.x and j == stone.y:
                        continue
                    self.pull[i][j] += 1.0 / stone.getD(i, j)
        else:
            for i in range(1, self.WIDTH):
                for j in range(1, self.HEIGHT):
                    if i == stone.x and j == stone.y:
                        continue
                    self.pull[i][j] -= 1.0 / stone.getD(i, j)

    def isVisited(self, coord):
        return self.visited[coord.x][coord.y]
