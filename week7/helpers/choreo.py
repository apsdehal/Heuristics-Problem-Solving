from util import getPairs
from util import dist
from collections import deque

class Choreo:
    def __init__(self, io):
        self.board = io.board
        self.pairs = getPairs(io.red,io.blue)
        self.boardSize = io.boardSize

    def move(self):
        toBeRemoved = []
        output = ""
        for i in range(len(self.pairs)):
            curr = self.pairs[i]
            red = curr[0]
            blue = curr[1]

            if self.getDist(red, blue) == 1:
                toBeRemoved.append(i)
                continue
            else:
                path = self.BFS(red, blue)

                redString = str(red[0]) + " " + str(red[1]) + " "
                blueString = str(blue[0]) + " " + str(blue[1]) + " "

                moveOnlyOne = False

                if path[0][0]== path[1][0] and path[0][1] == path[1][1] :
                    moveOnlyOne = True

                self.board[red[0]][red[1]] = '.'

                if not moveOnlyOne:
                    self.board[blue[0]][blue[1]] = '.'

                red = path[0]
                blue = path[1]

                redString = str(red[0]) + " " + str(red[1]) + " "
                blueString = str(blue[0]) + " " + str(blue[1]) + " "

                red[0] = int(red[0])
                red[1] = int(red[1])

                blue[0] = int(blue[0])
                blue[1] = int(blue[1])

                self.board[red[0]][red[1]] = 'R'
                if not moveOnlyOne:
                    self.board[blue[0]][blue[1]] = 'B'

                self.pairs[i][0] = red
                if not moveOnlyOne:
                    self.pairs[i][1] = blue

                output += redString
                if not moveOnlyOne:
                    output += blueString

        newPairs = []

        for i in range(len(self.pairs)):
            if i not in toBeRemoved:
                newPairs.append(self.pairs[i])

        self.pairs = newPairs

        return output.strip()

    def BFS(self, red, blue):
        q = deque()
        visited = [[0 for i in range(self.boardSize)] for j in range(self.boardSize)]
        parent = {}
        q.append(red)

        redCoordString = self.getCoordinateString(red)
        blueCoordString = self.getCoordinateString(blue)
        
        parent[redCoordString] = None

        while len(q):

            curr = q.popleft()
            currCoordinateString = self.getCoordinateString(curr)

            if currCoordinateString == blueCoordString:
                break

            if curr[0] - 1 >= 0 and not visited[curr[0] - 1][curr[1]]:
                if blue[0] == curr[0] - 1 and blue[1] == curr[1]:
                    parent[blueCoordString] = currCoordinateString
                    break

                currBoardChar = self.board[curr[0] - 1][curr[1]]


                if currBoardChar == '.':
                    next = [curr[0] - 1, curr[1]]
                    visited[curr[0] - 1][curr[1]] = 1
                    parent[self.getCoordinateString(next)] = currCoordinateString
                    q.append(next)

            if curr[0] + 1 < self.boardSize and not visited[curr[0] + 1][curr[1]]:
                if blue[0] == curr[0] + 1 and blue[1] == curr[1]:
                    parent[blueCoordString] = currCoordinateString
                    break

                currBoardChar = self.board[curr[0] + 1][curr[1]]


                if currBoardChar == '.':
                    next = [curr[0] + 1, curr[1]]
                    visited[curr[0] + 1][curr[1]] = 1
                    parent[self.getCoordinateString(next)] = currCoordinateString
                    q.append(next)

            if curr[1] - 1 >= 0 and not visited[curr[0]][curr[1] - 1]:
                if blue[0] == curr[0] and blue[1] == curr[1] - 1:
                    parent[blueCoordString] = currCoordinateString
                    break

                currBoardChar = self.board[curr[0]][curr[1] - 1]


                if currBoardChar == '.':
                    next = [curr[0], curr[1] - 1]
                    visited[curr[0]][curr[1] - 1] = 1
                    parent[self.getCoordinateString(next)] = currCoordinateString
                    q.append(next)

            if curr[1] + 1 < self.boardSize and not visited[curr[0]][curr[1] + 1]:
                if blue[0] == curr[0] and blue[1] == curr[1] + 1:
                    parent[blueCoordString] = currCoordinateString
                    break

                currBoardChar = self.board[curr[0]][curr[1] + 1]


                if currBoardChar == '.':
                    next = [curr[0], curr[1] + 1]
                    visited[curr[0]][curr[1] + 1] = 1
                    parent[self.getCoordinateString(next)] = currCoordinateString
                    q.append(next)

        finalPath = []
        currStr = blueCoordString

        while parent[currStr] != redCoordString:
            currStr = parent[currStr]

        finalPath.append(currStr.split(" "))
        finalPath.append(parent[blueCoordString].split(" "))

        return finalPath


    def getCoordinateString(self, c):
        return str(c[0]) + " " + str(c[1])

    def getDist(self, c1, c2):
        return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])

    def isNotStarLoc(self, loc1, loc2):
        if(self.board[loc1[0]][loc1[1]]=='S' or self.board[loc2[0]][loc2[1]]=='S' ):
            return False
        return True
