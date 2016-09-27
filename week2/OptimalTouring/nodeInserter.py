import utils

def insertNodesInPaths(info):
	info = utils.calculateReachAndWait(info)
	info = utils.calcMaxShift(info)
	pathShifts = utils.generatePathShifts(info)
	info, shouldGoAhead = utils.insertNode(info, pathShifts)
	return info, shouldGoAhead

