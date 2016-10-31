def getParent(reds,blues):
	taken = set()
	pairs = {}
	for red in reds:
		minDist = sys.maxint
		partner = None
		for blue in blues:
			if not blue in taken:
				if dist(red, blue) < minDist:
					minDist = dist(red,blue)
					partner = blue
		pairs[red] = blue
	return pairs

def getPairs(red,blues):
	return getParent(reds,blues)

def dist(red, blue):
	return abs(red[0] - blue[0]) + abs(red[1]-blue[1])
