import socket
import sys
from greedy import Greedy
from stone import Stone

class Voronoi:

	HOST = 'localhost'
	PORT = 9000
	STRIDE = 60
	NUMBER_OF_PLAYERS = 2

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def __init__(self, stones, nPlayers, port):
		self.PORT = port
		self.NUMBER_OF_PLAYERS = nPlayers
		self.s.connect((self.HOST, self.PORT))
		self.maxStones = stones
		self.greedy = Greedy(self.STRIDE, self.maxStones)
		self.stones = []
		self.stones.append([])
		self.stones.append([])

	def start(self):
		while 1:
			serverResponse = self.s.recv(1024)
			data = serverResponse.split()

			# Check if the game has ended
			if int(data[0]) == 1:
				break

			self.noOfMoves = int(data[1]) - 1
			if(self.noOfMoves >= 0):
				self.lastMoveOfOpponent_x = int(data[2 + self.noOfMoves * 3])
				self.lastMoveOfOpponent_y = int(data[2 + self.noOfMoves * 3 + 1])
				self.stones[1].append(Stone(self.lastMoveOfOpponent_x, self.lastMoveOfOpponent_y))
				self.greedy.updatePull(self.stones, 1)

			nextMove = self.greedy.move(self.stones)

			self.stones[0].append(Stone(nextMove.x, nextMove.y))
			self.greedy.updatePull(self.stones, 0)

			self.s.sendall(str(nextMove.x) + " " + str(nextMove.y))

		self.s.close()


if __name__ == "__main__":
	maxStones = int(sys.argv[1])
	numberOfPlayers = int(sys.argv[2])
	port = int(sys.argv[3])
	voronoi = Voronoi(maxStones,numberOfPlayers,port)
	voronoi.start()
