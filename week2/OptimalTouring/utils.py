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
