import sys
import math
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

def getPairs(reds,blues):
	return getParent(reds,blues)

def dist(red, blue):
	return abs(red[0] - blue[0]) + abs(red[1]-blue[1])

def centroid(points):
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    _len = len(points)
    centroid_x = math.floor(sum(x_coords)/_len)
    centroid_y = math.floor(sum(y_coords)/_len)
    return [centroid_x, centroid_y]
