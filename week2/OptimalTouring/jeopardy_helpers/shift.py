class Shift:
	def __init__(self, prev, path, val, index, profit):
		self.prev = prev
		self.path = path
		self.val = val
		self.index = index
		self.ratio = (profit * profit) / val
