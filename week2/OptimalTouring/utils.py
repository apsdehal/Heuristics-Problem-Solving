def RouteInitPhase(info):
	paths = [[] for _ in range(info['nDays'])]
	clusters = info['clusters']
	nodes = info['nodes']

	i = 0
	for cluster in clusters:
		maximum = 0
		for j in range(0, len(cluster)):
			if nodes[cluster[j]].profit > nodes[maximum].profit:
				maximum = cluster[j]
		paths[i].append(maximum)
		i += 1

	info['paths'] = paths

	return info
