import sys
import kmeans
from inputParser import InputParser

if __name__ == "__main__":
	parsedInfo = InputParser(sys.argv)
	info = parsedInfo.getInfo()
	kmeans.getClusters(info)

