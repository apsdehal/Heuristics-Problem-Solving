import socket
import time
import sys
from spoiler import Spoiler
from choreo import Choreo

class IO:
    def __init__(self, host = "localhost", port, boardSize):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, int(port)))
        self.boardSize = boardSize

    def parseInput(self, filename, player):
        red = []
        blue = []
        fh = open(filename)
        file_contents = fh.readlines()

        adding_red = True

        for line in file_contents:
            fields = []
            line = line.rstrip('\r\n')

            if line == "Red dancer positions (start at 0)":
                continue

            if line == "Blue dancer positions (start at 0)":
                adding_red = False
                continue
            if line == "    ":
                continue

            fields = line.split(' ')

            if adding_red:
                red.append([int(fields[0]), int(fields[1])])
            else:
                blue.append([int(fields[0]), int(fields[1])])

        self.red = red
        self.blue = blue
        self.setupBoard(self.boardSize, red, blue)

        if player == 'choreographer':
            self.playerName = "choreo"
            self.player = Choreo(self)
        else:
            self.playerName = "spoiler"
            self.player = Spoiler(self)

    def setupBoard(self, red, blue):
        board = [['.' for i in range(size)] for j in range(size)]
        for r in red:
            board[r[0]][r[1]] = 'R'
        for b in blue:
            board[b[0]][b[1]] = 'B'
        self.board = board

    def begin():
        data = ""
        flag = 0
        while 1:
            data += s.recv(1024)

            if "$" in data:
                break

            if "#" in data and flag == 0:
                starData = self.getStarConfiguration(data)
                self.player.initStars(starData,self.board)
                flag = 1

            if "^" in data and flag == 0:
                self.sendOutput(self.player.move())

            if "#" in data and flag == 1:
                self.sendOutput(self.player.move(self.red,self.blue))
                data = ""

        self.s.close()

    def sendOutput(self, move):
        self.s.sendall('{}'.format(moves))

    def getStarConfiguration(self, data):
        data = data.split('#')[0].strip()

        data = data.split(' ')

        stars = []

        for i in range(0, len(data), 2):
            stars.append((int(data[i]), int(data[i + 1])))

        self.stars = stars

        return stars
