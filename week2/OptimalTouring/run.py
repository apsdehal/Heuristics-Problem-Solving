import sys
import kmeans
import graphGenerator
from inputParser import InputParser
import utils

if __name__ == "__main__":
	parsedInfo = InputParser(sys.argv)
	info = parsedInfo.getInfo()
	info = kmeans.getClusters(info)
	info = graphGenerator.graphGen(info)
	info = utils.associateInsertedMap(info)
	info = utils.RouteInitPhase(info)
	info = utils.calculateReachAndWait(info)
	info = utils.calcMaxShift(info)
	pathShifts = utils.generatePathShifts(info)

	info = utils.insertNode(info, pathShifts)

	print info['paths']

