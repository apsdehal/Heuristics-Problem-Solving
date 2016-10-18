import math

def getCoordinateList():
	myCoordinateList = []
	xPrev = -1
	for y in range(0,67):
		x = math.ceil(math.sqrt(4356 - pow(y,2)))
		x = int(x)
		if(x!=xPrev):
			myCoordinateList.append((x,y))
		xPrev = x;
	return myCoordinateList
