import sys
sys.path.insert(0, './jeopardy_helpers')
import kmeans
import graphGenerator
from inputParser import InputParser
import utils
import nodeInserter
import datetime
from random import randint


if __name__ == "__main__":
	start = datetime.datetime.now()
	parsedInfo = InputParser(sys.argv)
	info = parsedInfo.getInfo()
	info = graphGenerator.graphGen(info)

	mainInfo = info
	bestPath = None
	bestValue = 0

	while True:
		info = kmeans.getClusters(info)
		info = utils.associateInsertedMap(info)
		info = utils.RouteInitPhase(info)

		info['clusterParameter'] = [1, 1.1, 1.2, 1.3][randint(0, 3)]
		for i in range(0, 10):
			info, shouldGoAhead = nodeInserter.insertNodesInPaths(info)
			if not shouldGoAhead:
				break

		info = utils.calculateReachAndWait(info)

		isValid, num = utils.validatePath(info)

		if not isValid:
			continue

		currVal = utils.valueGenerated(info)

		if currVal > bestValue:
			bestValue = currVal
			bestPath = info['paths']

		info = mainInfo

		t = datetime.datetime.now() - start
		if t.seconds > 80:
			break

	utils.printPaths(bestPath)
