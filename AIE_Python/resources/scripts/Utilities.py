import operator
import math

class Vector(list):

	def __add__(self, other):
		return self.__class__(map(operator.add, self, other))

	def __iadd__(self, other):
		return self.__class__(map(operator.iadd, self, other))

	def __sub__(self, other):
		return self.__class__(map(operator.sub, self, other))

	def __isub__(self, other):
		return self.__class__(map(operator.isub, self, other))

	def __mul__(self, other):
		return self.__class__([x * other for x in self])

	def __rmul__(self, other):
		return self.__class__([other * x for x in self])

	def __imul__(self, other):
		return self.__class__([x * other for x in self])

	def __div__(self, other):
		return self.__class__([x / other for x in self])

	def __idiv__(self, other):
		return self.__class__([x / other for x in self])

	def getMagnitude(self):
		total = 0.0
		for x in self:
			total += x * x
		return math.sqrt(total)

	def normalize(self):
		s = self.getMagnitude()
		for x in range(len(self)):
			self[x] /= s

	def truncate(self, maximum):
		for x in range(len(self)):
			if self[x] > maximum:
				self[x] = maximum

		#i = maximum