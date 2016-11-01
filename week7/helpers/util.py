import sys
import math
import heapq

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

	return pairs

def getPairs(reds,blues):
	myPairs = getParentPQ(reds,blues)
	maxDistance, maxDistanceIndex = getMaxDist(myPairs)
	evolve(myPairs)
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
