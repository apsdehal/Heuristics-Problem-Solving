import sys
def getParent(reds,blues):
	taken = set()
	pairs = []
	for red in reds:
		minDist = sys.maxint
		partner = None
		for blue in blues:
			blue_str = " ".join(str(x) for x in blue)
			if not blue_str in taken:
				if dist(red, blue) < minDist:
					minDist = dist(red,blue)
					partner = blue
					partner_str = blue_str
		pairs.append([red,partner])
		taken.add(partner_str)
	return pairs

def getPairs(reds,blues):
	return getParent(reds,blues)

def dist(red, blue):
	return abs(red[0] - blue[0]) + abs(red[1]-blue[1])
