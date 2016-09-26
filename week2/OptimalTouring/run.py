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

	utils.RouteInitPhase(info)
