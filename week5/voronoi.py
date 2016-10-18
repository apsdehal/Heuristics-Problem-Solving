import socket
import sys
from greedy import Greedy

class Voronoi:

	HOST = 'localhost'
	PORT = 9000
	STRIDE = 40

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def __init__(self, stones):
		self.s.connect((self.HOST, self.PORT))
		self.maxStones = stones
		self.greedy = Greedy(self.STRIDE)

	def start(self):
		while 1:
			serverResponse = self.s.recv(1024)
			data = serverResponse.split()
			print data

			# Check if the game has ended
			if int(data[0]) == 1:
				break

			self.noOfMoves = int(data[1]) - 1
			if(self.noOfMoves >= 0):
				self.lastMoveOfOpponent_x = int(data[2 + self.noOfMoves * 3])
				self.lastMoveOfOpponent_y = int(data[2 + self.noOfMoves * 3 + 1])


			self.s.sendall(myMove)

		self.s.close()


if __name__ == "__main__":
	maxStones = int(sys.argv[1])
	voronoi = Voronoi(maxStones)
	voronoi.start()
