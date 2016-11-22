import socket
import time
import sys
from spoiler import Spoiler
from choreo import Choreo

class IO:
    def __init__(self, host, port, boardSize):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, int(port)))
        self.boardSize = boardSize

    def parseInput(self, filename, nStars, player):
        self.nStars = nStars
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

    def setupBoard(self, size, red, blue):
        board = [['.' for i in range(size)] for j in range(size)]
        tupleBoard = [[0 for i in range(size)] for j in range(size)]

        for i in range(0, len(red)):
            r = red[i]
            board[r[0]][r[1]] = 'R'
            tupleBoard[r[0]][r[1]] = (i, 'R')

        for i in range(0, len(blue)):
            b = blue[i]
            board[b[0]][b[1]] = 'B'
            tupleBoard[b[0]][b[1]] = (i, 'B')

        self.board = board
        self.tupleBoard = tupleBoard

    def begin(self):
        data = ""
        flag = 0
        while 1:
            data += self.s.recv(1024)

            if "$" in data:
                break

            if "#" in data and flag == 0:
                starData = self.getStarConfiguration(data)
                flag = 1

            if "^" in data and flag == 0:
                self.sendOutput(self.player.move())

            if "#" in data and flag == 1:
                self.sendOutput(self.player.move())
                data = ""

        self.s.close()

    def sendOutput(self, moves):
        print moves
        self.s.sendall('{}'.format(moves))

    def getStarConfiguration(self, data):
        data = data.split('#')[0].strip()

        data = data.split(' ')

        stars = []

        for i in range(0, len(data), 2):
            stars.append((int(data[i]), int(data[i + 1])))
            self.board[int(data[i])][int(data[i + 1])] = 'S'

        self.stars = stars

        return stars
