import math
from coordinate import Coordinate
myCoordinateList = []

def getCoordinateList():
	global myCoordinateList
	if(len(myCoordinateList)!=0):
		return myCoordinateList
	xPrev = -1
	for y in range(0,67):
		x = math.ceil(math.sqrt(4356 - y ** 2))
		x = int(x)
		if(x != xPrev):
			myCoordinateList.append(Coordinate(x, y))
		xPrev = x;
	for pair in reversed(myCoordinateList):
		x = pair.x * -1
		y = pair.y
		if(x!=0):
			myCoordinateList.append(Coordinate(x,y))

	for pair in myCoordinateList[:]:
		x = pair.x
		y = pair.y * -1
		if(y!=0):
			myCoordinateList.append(Coordinate(x,y))

	return myCoordinateList

m = getCoordinateList()
