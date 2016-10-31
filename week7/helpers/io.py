import socket
import time
import sys

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

        self.setupBoard(self.boardSize, red, blue)

    def setupBoard(self, red, blue):
    	board = [['.' for i in range(size)] for j in range(size)]
    	for r in red:
    		board[r[0]][r[1]] = 'R'
    	for b in blue:
    		board[b[0]][b[1]] = 'B'
        self.board = board




parse_input(sys.argv[1])
setup_board(int(sys.argv[3]))

counter = 0

data = ""
while 1:
	data = s.recv(1024)
	if "$" in data:
		break

	moves = str(counter)
	moves += " 2 " + str(counter+1) + " 2"
	counter += 1
#	for r in red:
#		moves += str(r[0]) + " " + str(r[1]) + " " + str(r[0]+1) + " " + str(r[1]) + " "
#	for b in blue:
#		moves += str(b[0]) + " " + str(b[1]) + " " + str(b[0]) + " " + str(b[1]) + " "

	s.sendall('{}'.format(moves))
s.close()
