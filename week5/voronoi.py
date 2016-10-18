import math
import socket
import sys
from itertools import product
import scipy.spatial.distance


class Voronoi:

	MAX_POINTS = 1000
	MAX_STONES_POSSIBLE = 15
	OPPONENT = -1
	PLAYER = 1
	MIN_STONE_DIST = 66
	pull = [[0] * MAX_POINTS for item in range(0, MAX_POINTS)]
	visited = [[0] * MAX_POINTS for item in range(0, MAX_POINTS)]
	maxStones = 0

	noOfMoves = 0
	lastMoveOfOpponent_x = 0
	lastMoveOfOpponent_y = 0
	myMoves = 0
	opponentMoves = 0
	myStonePositions = []
	opponentStonePositions = []

	HOST = 'localhost'
	PORT = 9000

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def __init__(self, stones):
		self.s.connect((self.HOST, self.PORT))
		self.maxStones = stones
		self.initPull()

	def start(self):
		while 1:
			serverResponse = self.s.recv(1024)
			data = serverResponse.split()
			print data

			# Check if the game has ended
			if int(data[0]) == 1:
				break

			self.noOfMoves = int(data[1]) -1
			if(self.noOfMoves >= 0):
				self.lastMoveOfOpponent_x = int(data[2 + self.noOfMoves * 3])
				self.lastMoveOfOpponent_y = int(data[2 + self.noOfMoves * 3 + 1])
				print self.lastMoveOfOpponent_x, self.lastMoveOfOpponent_y
				self.updateOpponentMove(self.lastMoveOfOpponent_x, self.lastMoveOfOpponent_y)

			#algorithm to make move
			myMove = self.makeMove();

			self.s.sendall(myMove)

		self.s.close()


	def initPull(self):
		for i in range(0, self.MAX_POINTS):
			for j in range(0, self.MAX_POINTS):
				self.pull[i][j] = 0

	def updateOpponentMove(self, x, y):
		self.opponentStonePositions.append((x, y))
		self.opponentMoves += 1
		self.visited[x][y] = 1
		self.updatePull(x, y, self.OPPONENT)

	def updatePull(self, x, y, who):
		if (who == self.OPPONENT):
			for i in range(0, self.MAX_POINTS):
				for j in range(0, self.MAX_POINTS):
					xDist = (x - i) ** 2
					yDist = (y - j) ** 2
					dist = xDist + yDist
					if(dist != 0):
						if dist <= 66 * 66:
							self.visited[i][j] = 1
						self.pull[i][j] = self.pull[i][j] - 1.0 / dist

		else:
			for i in range(0, self.MAX_POINTS):
				for j in range(0, self.MAX_POINTS):
					xDist = (x - i) ** 2
					yDist = (y - j) ** 2
					dist = xDist + yDist
					if(dist != 0):
						if dist <= 66 * 66:
							self.visited[i][j] = 1
						self.pull[i][j] = self.pull[i][j] + 1.0 / dist


	def makeMove(self):
		maxScore = 0
		score = 0
		x=0
		y=0
		move = "";
		for i in range(0, self.MAX_POINTS):
			for j in range(0, self.MAX_POINTS):
				if (not self.visited[i][j]):
					if(self.pull[i][j] < 0):
						if(self.feasibleMove(i, j)):
							score = self.calcScoreByEvaluatingMove(i, j)
							if(score > maxScore):
								maxScore = score
								x = i
								y = j
		#update information about my moves
		self.myStonePositions.append((x,y))
		self.myMoves = self.myMoves + 1
		self.updatePull(x, y, self.PLAYER)
		return str(x) + " " + str(y)

	def calcScore(self):
		myScore = 0
		opponentScore = 0
		for i in range(0, self.MAX_POINTS):
			for j in range(0, self.MAX_POINTS):
				if(self.pull[i][j] > 0):
					myScore += 1
				elif(self.pull[i][j] < 0):
					opponentScore += 1
		return (myScore, opponentScore)

	def calcScoreByEvaluatingMove(self, x, y):
		score = 0
		xDist = 0
		yDist = 0
		dist = 0
		for i in range(0, self.MAX_POINTS):
			for j in range(0, self.MAX_POINTS):
				if(self.pull[i][j] > 0):
					score += 1
				else:
					xDist = (x - i) ** 2
					yDist = (y - j) ** 2
					dist = xDist + yDist
					if(dist != 0 and (self.pull[i][j] + 1.0 / dist) > 0):
						score += 1
		return score

	def feasibleMove(self, x,y):
		x_stone=0
		y_stone=0
		for x_stone, y_stone in self.opponentStonePositions:
			if(self.dist(x, y, x_stone, y_stone) < self.MIN_STONE_DIST):
				return False
		for x_stone, y_stone in self.myStonePositions:
			if(self.dist(x, y, x_stone, y_stone) < self.MIN_STONE_DIST):
				return False
		return True

	def dist(self, x1, y1, x2, y2):
		return  ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

# main code
# maxStones == number of stones for the game
maxStones = int(sys.argv[1])
voronoi = Voronoi(maxStones)
voronoi.start()
