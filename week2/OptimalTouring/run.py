import sys
from inputParser import InputParser

if __name__ == "__main__":
	parsedInfo = InputParser(sys.argv)
	print parsedInfo.getInfo()
