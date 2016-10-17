import math
import socket
import sys

MAX_POINTS = 1000
MAX_STONES_POSSIBLE = 15
OPPONENT = -1 
PLAYER = 1
MIN_STONE_DIST = 66
pull = [[0] * MAX_POINTS for item in range(0, MAX_POINTS)]
maxStones = 0

noOfMoves = 0
lastMoveOfOpponet_x = 0
lastMoveOfOpponet_y = 0
myMoves = 0
opponentMoves = 0
myStonePositions = []
opponentStonePositions = []

HOST = 'localhost'    
PORT = 9000        
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def initPull():
	for i in range(0,MAX_POINTS):
		for j in range(0,MAX_POINTS):
			pull[i][j] = 0

def updateOpponentMove(x, y):
	opponentStonePositions.append((x,y))
	opponentMoves += 1
	updatePull(x,y,OPPONENT)

def updatePull(x, y, who):
	if(who==OPPONENT):
		for i in range(0,MAX_POINTS):
			for j in range(0,MAX_POINTS):
				xDist = pow(x-i,2)
				yDist = pow(y-j,2)
				dist = xDist + yDist
				if(dist!=0):
					pull[i][j] = pull[i][j] - 1.0/dist

def makeMove():
	maxScore = 0
	score = 0
	x=0
	y=0
	move = "";
	for i in range(0,MAX_POINTS):
		for j in range(0,MAX_POINTS):
			if(pull[i][j] < 0):
				if(feasibleMove(i,j)):
					score = calcScoreByEvaluatingMove(i,j)
					if(score > maxScore):
						maxScore = score
						x = i
						y = j
	#update information about my moves
	myStonePositions.append((x,y))
	myMoves =+ 1 
	return str(x) + " " + str(y)

def calcScore():
	myScore = 0
	opponentScore = 0
	for i in range(0,MAX_POINTS):
		for j in range(0,MAX_POINTS):
			if(pull[i][j] > 0):
				myScore += 1
			elif(pull[i][j] < 0):
				opponentScore += 1
	return (myScore,opponentScore)

def calcScoreByEvaluatingMove(x,y):
	score = 0
	xDist = 0
	yDist = 0
	dist = 0
	for i in range(0,MAX_POINTS):
		for j in range(0,MAX_POINTS):
			if(pull[i][j] > 0):
				score += 1
			else:
				xDist = pow(x-i,2)
				yDist = pow(y-j,2)
				dist = xDist + yDist
				if(dist!=0 and (pull[i][j] + 1.0/dist) > 0):
					score += 1
	return score

def feasibleMove(x,y):
	x_stone=0
	y_stone=0
	for x_stone,y_stone in opponentStonePositions:
		if(dist(x,y,x_stone,y_stone) < MIN_STONE_DIST):
			return False
	return True

def dist(x1, y1, x2, y2):
	return  math.sqrt(pow(x1-x2,2) + pow(y1-y2,2))

# main code
# maxStones == number of stones for the game
maxStones = int(sys.argv[1])
s.connect((HOST, PORT))

while 1:
    serverResponse = s.recv(1024)
    data = serverResponse.split()

    # Check if the game has ended
    if int(data[0]) == 1:
        break
	
	numberOfMoves = int(data[1]) -1
	if(numberOfMoves > 0):
		lastMoveOfOpponet_x = int(data[2 + noOfMoves*3])
		lastMoveOfOpponet_y = int(data[2 + noOfMoves*3 + 1])
		updateOpponentMove(lastMoveOfOpponet_x,lastMoveOfOpponet_y)

    #algorithm to make move
    myMove = makeMove();

    s.sendall(myMove)

s.close()