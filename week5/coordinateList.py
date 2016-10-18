import math

myCoordinateList = []

def getCoordinateList():
	global myCoordinateList
	if(len(myCoordinateList)!=0):
		return myCoordinateList
	xPrev = -1
	for y in range(0,67):
		x = math.ceil(math.sqrt(4356 - pow(y,2)))
		x = int(x)
		if(x!=xPrev):
			myCoordinateList.append((x,y))
		xPrev = x;
	for pair in reversed(myCoordinateList):
		x = pair[0]* -1
		y = pair[1]
		if(x!=0):
			myCoordinateList.append((x,y))
	
	for pair in myCoordinateList[:]:
		x = pair[0]
		y = pair[1] * -1
		if(y!=0):
			myCoordinateList.append((x,y))

	return myCoordinateList

m = getCoordinateList()
for a in m:
	print(a)