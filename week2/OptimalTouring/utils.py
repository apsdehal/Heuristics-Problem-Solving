import math
import shift

def RouteInitPhase(info):
	paths = [[] for _ in range(info['nDays'])]
	clusters = info['clusters']
	nodes = info['nodes']

	i = 0
	for cluster in clusters:
		maximum = 0
		currentMaximumRatio = (nodes[maximum].profit * nodes[maximum].profit) / \
		(nodes[maximum].hours[i][0] + nodes[maximum].visit)

		for j in range(0, len(cluster)):
			currentNode = nodes[cluster[j]]
			if (currentNode.profit * currentNode.profit) / (currentNode.hours[i][0] + \
				currentNode.visit) > currentMaximumRatio:
				maximum = cluster[j]
				currentMaximumRatio = (nodes[maximum].profit * nodes[maximum].profit) / \
				(nodes[maximum].hours[i][0] + nodes[maximum].visit)

		info['inserted'][maximum] = i
		paths[i].append(maximum)
		info['nodes'][maximum].path = i
		i += 1

	info['paths'] = paths

	return info

def printNodes(info):
	for node in info['nodes']:
		print node.x, node.y, node.visit, node.profit, node.hours, node.index

def associateInsertedMap(info):
	info['inserted'] = [-1 for _ in range(info['nNodes'])]
	return info

def calcMaxShift(info):
	paths = info['paths']
	day = 0;
	for path in paths:
		length = len(path)
		for i in range(length-1,-1, -1):
			node = info['nodes'][path[i]]
			if(i==length-1):	#node is last node in path
				node.maxShift = node.hours[day][1]-node.visit-node.reach
			else:
				nextNode = info['nodes'][path[i+1]]
				maxShift = nextNode.maxShift + node.wait - node.visit - \
				info['costMatrix'][path[i]][path[i+1]]
				maxshiftBasedOnCloseTime = node.hours[day][1] - node.visit - node.reach
				node.maxShift = min(maxShift,maxshiftBasedOnCloseTime)
			info['nodes'][path[i]] = node
			print "node:",path[i] , " maxshift:", node.maxShift, " reach time:", node.reach, " duration", node.visit, " closing time", node.hours[day][1]
		day = day + 1;
	return info

def calculateReachAndWait(info):
	paths = info['paths']

	i = 0
	for path in paths:
		startTime = 0
		for node in path:
			currentNode = info['nodes'][node]

			currentNode.reach = startTime
			currentNode.wait = currentNode.hours[i][0] - startTime \
			if currentNode.hours[i][0] > startTime else 0

			if currentNode.wait > 0:
				startTime = currentNode.hours[i][0] + currentNode.visit
			else:
				startTime += currentNode.visit
			info['nodes'][node] = currentNode
		i += 1


def generatePathShifts(info):
	pathShifts = [[] for _ in range(info['nDays'])]

	"""If a node p is inserted in a route t between i and j, let shiftp = travelip +
	waitp + visitp + travelpj - travelij denote the time cost added to the overall route time
	due to the insertion of p. The node p can be inserted in a route t between i and j
	if and only if startit + visiti + travelip + visitp <= closept and at the same time
	shiftp <= waitj + maxShiftj."""

	for node in info['nodes']:
		if info['inserted'][node.index]:
			continue

		globalMinShift = shift.Shift(math.inf, math.inf, math.inf, 0)

		i = 0
		for path in info['paths']:
			localMinShift = shift.Shift(math.inf, math.inf, math.inf, 0)

			clusterParameter = 1

			# We prefer that same cluster nodes are added preferably
			if node.cluster == i:
				clusterParameter = 1.3

			for it in range(-1, len(path)):
				if it == -1:
					zeroNode = info['nodes'][path[0]]

					# Calculate shift by using wait time of first node, visit time, distance between node and second node
					shiftVal = 0 + node.hours[i][0] + node.visit \
					+ info['costMatrix'][node.index][zeroNode.index]

					shiftVal /= clusterParameter

					# First condition that shift must be less than wait + maxShift of second node
					if shiftVal > zeroNode.wait + zeroNode.maxShift:
						continue

					# Second condition if start time of the first node + visit time + travel time to second node
					# must be less than closing hours - visit time of second node
					if node.hours[i][0] + node.visit + zeroNode.visit \
					+ info['costMatrix'][node.index][zeroNode.index] > zeroNode.hours[i][1]:
						continue

					if shiftVal < localMinShift.val:
						localMinShift = shift.Shift(it, i, shiftVal, node.index, node.profit)
						continue

				else if it == len(path) - 1:
					finalNode = info['nodes'][path[it]]
					waitp = node.hours[i][0] - (finalNode.reach + finalNode.visit) \
					if (finalNode.reach + finalNode.visit) < node.hours[i][0] else 0

					if node.hours[i][1] > 24 * 60 - 1:
						continue

					shiftVal = info['costMatrix'][finalNode.index][node.index] \
					+ waitp + node.visit

					shiftVal /= clusterParameter

					if finalNode.reach + finalNode.visit \
					+ info['costMatrix'][finalNode.index][node.index] + node.visit \
					> node.hours[i][1]:
						continue

					if shiftVal < localMinShift.val:
						localMinShift = shift.Shift(it, i, shiftVal, node.index, node.profit)

				else:
					prevNode = info['nodes'][path[it-1]]
					nextNode = info['nodes'][path[it+1]]
					waitp = node.hours[i][0] - (prevNode.reach + prevNode.visit) \
					if (prevNode.reach + prevNode.visit) < node.hours[i][0] else 0

					shiftVal = info['costMatrix'][prevNode.index][node.index] + waitp + \
					node.visit + info['costMatrix'][node.index][nextNode.index] - \
					info['costMatrix'][prevNode.index][nextNode.index]

					shiftVal /= clusterParameter

					if shiftVal > nextNode.wait + nextNode.maxShift:
						continue

					if prevNode.reach + prevNode.visit + info['costMatrix'][prevNode.index][node.index] \
					+ node.visit > node.hours[i][1]:
						continue

					if shiftVal < localMinShift.val:
						localMinShift = shift.Shift(it, i, shiftVal, node.index, node.profit)

			if globalMinShift.val > localMinShift.val:
				globalMinShift = localMinShift
			i += 1

		pathShifts[globalMinShift.path].append(globalMinShift)


	return pathShifts
