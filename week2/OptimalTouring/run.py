import sys
import kmeans
import graphGenerator
from inputParser import InputParser
import utils
import nodeInserter
import time

if __name__ == "__main__":
	start = time.clock()
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
		for i in range(0, 10):
			info, shouldGoAhead = nodeInserter.insertNodesInPaths(info)
			if not shouldGoAhead:
				break

		info = utils.calculateReachAndWait(info)

		isValid, num = utils.validatePath(info)

		if not isValid:
			print info['paths'][num]
			for x in info['paths'][num]:
				currNode = info['nodes'][x]
				print currNode.index, currNode.visit, currNode.profit, currNode.hours[num], currNode.reach, currNode.wait, currNode.path
			print info['inserted']
			break

		currVal = utils.valueGenerated(info)

		if currVal > bestValue:
			bestValue = currVal
			bestPath = info['paths']
			print bestPath
			print bestValue

		info = mainInfo

		if time.clock() - start > 95:
			print time.clock() - start
			break
