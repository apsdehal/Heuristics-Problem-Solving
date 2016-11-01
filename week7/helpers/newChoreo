from util import getPairs
from util import dist

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

                redString = str[red[0]] + " " + str[red[1]] + " "
                blueString = str[blue[0]] + " " + str[blue[1]] + " "

                self.board[red[0]][red[1]] = '.'
                self.board[blue[0]][blue[1]] = '.'
                
                red = path[1]
                blue = path[len(path) - 2]
                
                redString = str[red[0]] + " " + str[red[1]] + " "
                blueString = str[blue[0]] + " " + str[blue[1]] + " "
            
                self.board[red[0]][red[1]] = 'R'
                self.board[blue[0]][blue[1]] = 'B'

                self.pairs[i][0] = red 
                self.pairs[i][1] = blue

                output += redString + blueString

        newPairs = []

        for i in range(len(self.pairs)):
            if i not in toBeRemoved:
                newPairs.append(self.pairs[i])

        self.pairs = newPairs

        return output.strip()

    def BFS(self, red, blue):
        q = []
        visited = [[0 for i in range(self.boardSize)] for j in range(self.boardSize)]

        q.append(red)

        while len(q):
            curr = q.popleft()

            if curr[0] - 1 

    def getDist(self, c1, c2):
        return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])

    def isNotStarLoc(self, loc1, loc2):
        if(self.board[loc1[0]][loc1[1]]=='S' or self.board[loc2[0]][loc2[1]]=='S' ):
            return False
        return True
