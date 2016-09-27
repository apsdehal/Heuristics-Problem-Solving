import os
from node import Node

class InputParser:
	def __init__(self, args):

		inputFile = "./given_info.txt"

		if args[1] != None:
			inputFile = args[1]

		if not os.path.exists(inputFile):
			print "Path you specified doesn't exist"
			os.exit()


		with open(inputFile, 'r') as data:
			nNodes = 0
			nDays = 0

			nodes = []

			flag = 0

			for line in data:
				if "site day" in line:
					flag = 1
					continue
				if "site avenue" in line:
					flag = 0
					continue


				line = line.strip().split(" ")
				if len(line) == 1 and line[0] == "":
					continue


				if flag == 0:
					nodes.append(Node(int(line[1]), int(line[2]), int(line[3]), float(line[4])))
					nNodes = nNodes + 1
				else:
					nodes[int(line[0]) - 1].hours.append([int(line[2]), int(line[3])])
					nDays = nDays + 1

			self.nodes = nodes
			self.nDays = nDays / nNodes
			self.nNodes = nNodes

	def getInfo(self):
		return {
			"nodes": self.nodes,
			"nNodes": self.nNodes,
			"nDays": self.nDays
		}
