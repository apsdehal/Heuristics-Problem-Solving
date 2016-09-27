import sys
import kmeans
import graphGenerator
from inputParser import InputParser
import utils
import nodeInserter

if __name__ == "__main__":
	parsedInfo = InputParser(sys.argv)
	info = parsedInfo.getInfo()
	info = kmeans.getClusters(info)
	info = graphGenerator.graphGen(info)
	info = utils.associateInsertedMap(info)
	info = utils.RouteInitPhase(info)

	for i in range(0, 10):
		info, shouldGoAhead = nodeInserter.insertNodesInPaths(info)
		if not shouldGoAhead:
			break

	info = utils.calculateReachAndWait(info)
	utils.printNodes(info)
	print info['paths']
	print utils.validatePath(info)
