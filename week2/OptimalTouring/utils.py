def RouteInitPhase(info):
	paths = [[] for _ in range(info['nDays'])]
	clusters = info['clusters']
	nodes = info['nodes']

	i = 0
	for cluster in clusters:
		maximum = 0
		currentMaximumRatio = (nodes[maximum].profit * nodes[maximum].profit) / (nodes[maximum].hours[i][0] + (nodes[maximum].visit / 3))

		for j in range(0, len(cluster)):
			currentNode = nodes[cluster[j]]
			if (currentNode.profit * currentNode.profit) / (currentNode.hours[i][0] + (currentNode.visit / 3)) > currentMaximumRatio:
				maximum = cluster[j]
				currentMaximumRatio = (nodes[maximum].profit * nodes[maximum].profit) / (nodes[maximum].hours[i][0] + (nodes[maximum].visit / 3))

		info['inserted'][maximum] = i
		paths[i].append(maximum)
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
		for i in range(length-1,0):
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
