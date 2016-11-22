import sys
import math
import heapq
from munkres import Munkres
from collections import deque

def getParent(reds,blues):
	taken = set()
	pairs = []
	for red in reds:
		minDist = sys.maxint
		partner = None
		for blue in blues:
			blue_str = " ".join(str(x) for x in blue)
			if not blue_str in taken:
				distance = dist(red, blue)
				if distance < minDist:
					minDist = distance
					partner = blue
					partner_str = blue_str
		pairs.append([red,partner])
		taken.add(partner_str)
	return pairs

def getParentPQ(reds, blues):
	reds = io.red
	blues = io.blue
	takenRed = set()
	takenBlue = set()
	pairs = []

	pq = []
	for i in range(0, len(blues)):
		for j in range(0, len(reds)):
			heapq.heappush(pq, (dist(blues[i], reds[j]), i, j))

	while len(pq) != 0:
		curr = heapq.heappop(pq)

		if not curr[1] in takenBlue and not curr[2] in takenRed:
			pairs.append([reds[curr[2]], blues[curr[1]]])
			takenRed.add(curr[2])
			takenBlue.add(curr[1])

	print pairs

	return pairs

def getParentMunkres(io):
	board = io.board
	tupleBoard = io.tupleBoard
	m = Munkres()
	costMatrix = generateCostMatrix(board, tupleBoard, len(io.red))
	indices = m.compute(costMatrix)
	pairs = []

	for index in indices:
		pairs.append([io.red[index[0]], io.blue[index[1]]])

	print pairs

	return pairs


def generateCostMatrix(board, tupleBoard, lenDancers):
	sz = len(board[0])
	costMatrix = [[0 for x in range(0, lenDancers)] for y in range(0, lenDancers)]

	for i in range(0, sz):
		for j in range(0, sz):
			if board[i][j] == 'R':
				startBFS((i, j), board, costMatrix, tupleBoard)

	return costMatrix


def startBFS(pair, board, costMatrix, tupleBoard):
	q = deque()
	sz = len(board[0])
	visited = [[0 for i in range(sz)] for j in range(sz)]

	source = tupleBoard[pair[0]][pair[1]][0]

	q.append((pair, 0))

	while len(q):
		curr = q.popleft()
		s = curr[0]

		if s[0] - 1 >= 0 and not visited[s[0] - 1][s[1]]:
			currChar = board[s[0] - 1][s[1]]
			visited[s[0] - 1][s[1]] = 1

			if currChar == 'B':
				# Found a B set to cost matrix
				d = tupleBoard[s[0] - 1][s[1]][0]
				costMatrix[source][d] = curr[1] + 1
			elif currChar == '.':
				# Safe to walk
				q.append(((s[0] - 1, s[1]), curr[1] + 1))

		if s[0] + 1 < sz and not visited[s[0] + 1][s[1]]:
			currChar = board[s[0] + 1][s[1]]
			visited[s[0] + 1][s[1]] = 1

			if currChar == 'B':
				# Found a B set to cost matrix
				d = tupleBoard[s[0] + 1][s[1]][0]
				costMatrix[source][d] = curr[1] + 1
			elif currChar == '.':
				# Safe to walk
				q.append(((s[0] + 1, s[1]), curr[1] + 1))

		if s[1] - 1 >= 0 and not visited[s[0]][s[1] - 1]:
			currChar = board[s[0]][s[1] - 1]
			visited[s[0]][s[1] - 1] = 1

			if currChar == 'B':
				# Found a B set to cost matrix
				d = tupleBoard[s[0]][s[1] - 1][0]
				costMatrix[source][d] = curr[1] + 1
			elif currChar == '.':
				# Safe to walk
				q.append(((s[0], s[1] - 1), curr[1] + 1))

		if s[1] + 1 < sz and not visited[s[0]][s[1] + 1]:
			currChar = board[s[0]][s[1] + 1]
			visited[s[0]][s[1] + 1] = 1

			if currChar == 'B':
				# Found a B set to cost matrix
				d = tupleBoard[s[0]][s[1] + 1][0]
				costMatrix[source][d] = curr[1] + 1
			elif currChar == '.':
				# Safe to walk
				q.append(((s[0], s[1] + 1), curr[1] + 1))



def getPairs(io):
	myPairs = getParentMunkres(io)
	return myPairs


def dist(red, blue):
	return abs(red[0] - blue[0]) + abs(red[1]-blue[1])

def centroid(points):
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    _len = len(points)
    centroid_x = math.floor(sum(x_coords)/_len)
    centroid_y = math.floor(sum(y_coords)/_len)
    return [centroid_x, centroid_y]

def getMaxDist(pairs):
	index = 0
	maxDistance = 0
	maxDistanceIndex = -1
	for red, blue in pairs:
		distance = dist(red,blue)
		index += 1
		if(distance >maxDistance):
			maxDistance = distance
			maxDistanceIndex = index
	return maxDistance , maxDistanceIndex
def evolve(pairs):
	temp = 0
