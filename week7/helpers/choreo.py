from util import getPairs
from util import dist

class Choreo:
    def __init__(self, io):
        pairs = getPairs(io.red,io.blue)
        self.paths_red = []
        self.paths_blue = []
        for red,blue in pairs:
            path_red = []
            path_blue = []
            getPath(red,blue,path_red,path_blue)
            paths_red.append(path_red)
            paths_blue.append(path_blue)

    def move():
        dataToSend = ""
        for pathRed in self.paths_red:
            if(len(pathRed)>1):
                dataToSend = dataToSend + " " + pathRed[0][0] + " " + pathRed[0][1]
                dataToSend = dataToSend + " " + pathRed[1][0] + " " + pathRed[1][1]
                del pathRed[0]
        for pathBlue in self.paths_blue:
            if(len(pathBlue)>1):
                dataToSend = dataToSend + " " + pathBlue[0][0] + " " + pathBlue[0][1]
                dataToSend = dataToSend + " " + pathBlue[1][0] + " " + pathBlue[1][1]
                del pathBlue[0]
        return dataToSend

    def getPath(red,blue,pathRed,pathBlue):
        pathRed.append([red[0],red[1]])
        pathBlue.append([blue[0],blue[1]])
        if(dist(red,blue)==1):
            return True
        if(red[0]>blue[0]):
            x = 1
        elif(red[0]==blue[0]):
            x = 0
        else:
            x = -1
        redNext = [red[0]-x,red[1]]
        blueNext = [blue[0]+x,blue[1]]
        if x!=0 and isNotStarLoc(redNext,blueNext) and getPath(redNext,blueNext,pathRed,pathBlue):
            return True
        if(red[1]>blue[1]):
            y = 1
        elif(red[1]==blue[1]):
            y = 0
        else:
            y = -1
        redNext = [red[0],red[1]-y]
        blueNext = [blue[0],blue[1]+y]
        if y!=0 and isNotStarLoc(redNext,blueNext) and getPath(redNext,blueNext,pathRed,pathBlue):
            return True
        redNext = [red[0]-x,red[1]]
        blueNext = [blue[0],blue[1]+y]
        if x!=0 and y!=0 and isNotStarLoc(redNext,blueNext) and getPath(redNext,blueNext,pathRed,pathBlue):
            return True
        redNext = [red[0],red[1]-y]
        blueNext = [blue[0]+x,blue[1]]
        if x!=0 and y!=0 and isNotStarLoc(redNext,blueNext) and getPath(redNext,blueNext,pathRed,pathBlue):
            return True
        pathRed.pop()
        pathBlue.pop()
        return False

    def initStars(starData,board):
        self.starData = starData
        self.board = board
        for star in starData:
            self.board[star[0]][star[1]] = '*'

    def isNotStarLoc(loc1, loc2):
        if(self.board[loc1[0]][loc1[1]]=='*' or self.board[loc2[0]][loc2[1]]=='*' ):
            return False
        return True
