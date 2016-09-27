class Node:
	def __init__(self, x, y, visit, profit):
		self.x = x
		self.y = y
		self.visit = visit
		self.profit = profit
		self.hours = []
		self.reach = -1
		self.wait = -1
		self.maxShift = -1

