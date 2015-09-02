
class Colorcodes:
	OFF = -1
	GREEN = 0
	ORANGE = 1
	RED = 2

class MatrixVisualization:
	def getWidth(self):
		raise NotImplementedError()
	def getHeight(self):
		raise NotImplementedError()
	def setPx(self, x, y, color):
		raise NotImplementedError()
	def clear(self):
		raise NotImplementedError()
	def write(self):
		raise NotImplementedError()

class MatrixData:
	def getPx(self,x,y):
		raise NotImplementedError()
	def setWidth(self):
		raise NotImplementedError()
	def setHeight(self):
		raise NotImplementedError()
