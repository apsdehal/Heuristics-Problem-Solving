import math

def graphGen(info):
	nNodes = info['nNodes']
	costMatrix = [[(abs(info['nodes'][x].x - info['nodes'][y].x)
				 + abs(info['nodes'][x].y - info['nodes'][y].y))
	 				 for x in range(nNodes)]
	 				 for y in range(nNodes)]

	info['costMatrix'] = costMatrix

	return info
