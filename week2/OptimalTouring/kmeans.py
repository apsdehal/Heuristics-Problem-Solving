from sklearn import cluster
import numpy as np

def getClusters(info):
	data = []
	for i in info['nodes']:
		data.append([i.x, i.y])
	data = np.array(data)

	kmeans = cluster.KMeans(n_clusters = info['nDays'], init = 'k-means++', n_init=20, max_iter=500)
	clusters = kmeans.fit_predict(data)

	finalClusters = [[] for _ in range(info['nDays'])]

	print len(clusters)
	for i in range(0, len(clusters)):
		currCluster = clusters[i]
		info['nodes'][i].cluster = currCluster
		print currCluster
		finalClusters[currCluster].append(i)

	print finalClusters
