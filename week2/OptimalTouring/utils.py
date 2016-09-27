def RouteInitPhase(info):
	paths = [[] for _ in range(info['nDays'])]
	clusters = info['clusters']
	nodes = info['nodes']

	i = 0
	for cluster in clusters:
		maximum = 0
		currentMaximumRatio = (nodes[maximum].profit * nodes[maximum].profit) / (nodes[maximum].hours[i][0] + nodes[maximum].visit)

		for j in range(0, len(cluster)):
			currentNode = nodes[cluster[j]]
			if (currentNode.profit * currentNode.profit) / (currentNode.hours[i][0] + currentNode.visit) > currentMaximumRatio:
				maximum = cluster[j]
				currentMaximumRatio = (nodes[maximum].profit * nodes[maximum].profit) / (nodes[maximum].hours[i][0] + nodes[maximum].visit)

		info['inserted'][maximum] = i
		paths[i].append(maximum)
		info['nodes'][maximum].path = i
		i += 1

	info['paths'] = paths

	return info


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
				maxShift = nextNode.maxShift + node.wait - node.visit - info['costMatrix'][path[i]][path[i+1]]
				maxshiftBasedOnCloseTime = node.hours[day][1] - node.visit - node.reach
				node.maxShift = min(maxShift,maxshiftBasedOnCloseTime)
			info['nodes'][path[i]] = node
			print "node:",path[i] , " maxshift:", node.maxShift
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
			currentNode.wait = currentNode.hours[i][0] - startTime if currentNode.hours[i][0] > startTime else 0

			if currentNode.wait > 0:
				startTime = currentNode.hours[i][0] + currentNode.visit
			else:
				startTime += currentNode.visit
			info['nodes'][node] = currentNode
		i += 1


def insertNode(info):
	pathShifts = [[] for _ in range(info['nDays'])]

	for node in info['nodes']:
		for path in info['paths']:
			for it in range(len(path - 1)):
				continue
